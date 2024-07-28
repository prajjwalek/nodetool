import asyncio
from enum import Enum
import json
import time
import uuid
from typing import Any
from anthropic import BaseModel
from fastapi import WebSocket, WebSocketDisconnect
from queue import Queue
from nodetool.common.environment import Environment
from nodetool.workflows.processing_context import ProcessingContext
from nodetool.workflows.run_workflow import run_workflow
from nodetool.workflows.run_job_request import RunJobRequest
from nodetool.workflows.workflow_runner import WorkflowRunner

log = Environment.get_logger()


class CommandType(str, Enum):
    RUN_JOB = "run_job"
    CANCEL_JOB = "cancel_job"
    GET_STATUS = "get_status"


class WebSocketCommand(BaseModel):
    command: CommandType
    data: dict


class WebSocketRunner:
    """
    Runs a workflow using a WebSocket connection.

    Attributes:
        websocket (WebSocket | None): The WebSocket connection.
        context (ProcessingContext | None): The processing context for job execution.
        active_job (asyncio.Task | None): The currently active job.
        use_thread (bool): Flag indicating whether to use a separate thread for job execution.
        job_id (str | None): The ID of the current job.
        runner (WorkflowRunner | None): The workflow runner for job execution.
        pre_run_hook (Any): A hook function to be executed before running a job.
        post_run_hook (Any): A hook function to be executed after running a job.
    """

    websocket: WebSocket | None = None
    context: ProcessingContext | None = None
    active_job: asyncio.Task | None = None
    use_thread: bool = False
    job_id: str | None = None
    runner: WorkflowRunner | None = None
    pre_run_hook: Any
    post_run_hook: Any

    def __init__(
        self,
        pre_run_hook: Any = None,
        post_run_hook: Any = None,
        use_thread: bool = False,
    ):
        """
        Initializes a new instance of the WebSocketRunner class.

        Args:
            pre_run_hook (Any, optional): A hook function to be executed before running a job.
            post_run_hook (Any, optional): A hook function to be executed after running a job.
            use_thread (bool, optional): Flag indicating whether to use a separate thread for job execution.
        """
        self.pre_run_hook = pre_run_hook
        self.post_run_hook = post_run_hook
        self.use_thread = use_thread

    async def connect(self, websocket: WebSocket):
        """
        Establishes the WebSocket connection.

        Args:
            websocket (WebSocket): The WebSocket connection.
        """
        await websocket.accept()
        self.websocket = websocket

    async def disconnect(self):
        """
        Closes the WebSocket connection and cancels any active job.
        """
        if self.active_job:
            try:
                self.active_job.cancel()
            except Exception:
                pass
        if self.websocket:
            try:
                await self.websocket.close()
            except Exception:
                pass
        self.websocket = None
        self.active_job = None
        self.job_id = None

    async def run_job(
        self,
        req: RunJobRequest,
    ):
        """
        Runs a job based on the provided RunJobRequest.

        Args:
            req (RunJobRequest): The RunJobRequest containing job details.

        Raises:
            ValueError: If WebSocket is not connected.
        """
        try:
            if not self.websocket:
                raise ValueError("WebSocket is not connected")
            start_time = time.time()
            self.job_id = uuid.uuid4().hex
            self.runner = WorkflowRunner(job_id=self.job_id)
            api_client = Environment.get_nodetool_api_client(
                user_id=req.user_id,
                auth_token=req.auth_token,
                # api_url=req.api_url
            )

            self.context = ProcessingContext(
                user_id=req.user_id,
                auth_token=req.auth_token,
                workflow_id=req.workflow_id,
                api_client=api_client,
            )

            res = await self.context.api_client.post(
                "api/auth/verify", json={"token": req.auth_token}
            )
            if Environment.is_production():
                if res.json()['valid'] == False:
                    raise ValueError("Invalid auth token")

            log.info("Running job: %s", self.job_id)
            if self.pre_run_hook:
                self.pre_run_hook()

            async for msg in run_workflow(req, self.runner, self.context, use_thread=True):
                try:
                    print(msg)
                    await self.websocket.send_text(msg.model_dump_json())
                except Exception as e:
                    log.exception(e)

            if self.post_run_hook:
                self.post_run_hook()

            total_time = time.time() - start_time
            log.info(
                f"Finished job {self.job_id} - Total time: {total_time:.2f} seconds"
            )
        except Exception as e:
            log.exception(e)

        # TODO: Implement bookkeeping for credits used
        self.active_job = None
        self.job_id = None

    async def cancel_job(self):
        """
        Cancels the active job if one exists.

        Returns:
            dict: A dictionary with a message indicating the job was cancelled, or an error if no active job exists.
        """
        print("Cancelling job")
        if self.active_job:
            if self.runner:
                self.runner.cancel()
            if self.context:
                self.context.is_cancelled = True
            # self.active_job.cancel()
            self.active_job = None
            self.job_id = None
            return {"message": "Job cancelled"}
        return {"error": "No active job to cancel"}

    def get_status(self):
        """
        Gets the current status of job execution.

        Returns:
            dict: A dictionary with the status ("running" or "idle") and the job ID.
        """
        return {
            "status": "running" if self.active_job else "idle",
            "job_id": self.job_id,
        }

    async def handle_command(self, command: WebSocketCommand):
        """
        Handles incoming WebSocket commands.

        Args:
            command (WebSocketCommand): The WebSocket command to handle.

        Returns:
            dict: A dictionary with the response to the command.
        """
        if command.command == CommandType.RUN_JOB:
            if self.active_job:
                return {"error": "A job is already running"}
            req = RunJobRequest(**command.data)
            log.info(f"Starting workflow: {req.workflow_id}")
            self.active_job = asyncio.create_task(self.run_job(req))
            return {"message": "Job started"}
        elif command.command == CommandType.CANCEL_JOB:
            return await self.cancel_job()
        elif command.command == CommandType.GET_STATUS:
            return self.get_status()
        else:
            return {"error": "Unknown command"}

    async def run(self, websocket: WebSocket):
        """
        Main method to run the WorkflowRunner.

        Args:
            websocket (WebSocket): The WebSocket connection.
        """
        await self.connect(websocket)
        try:
            while True:
                assert self.websocket, "WebSocket is not connected"
                data = await self.websocket.receive_text()
                command = WebSocketCommand(**json.loads(data))
                response = await self.handle_command(command)
                await self.websocket.send_text(json.dumps(response))
        except WebSocketDisconnect:
            log.info("WebSocket disconnected")
        except Exception as e:
            log.error(f"WebSocket error: {str(e)}")
        finally:
            await self.disconnect()
