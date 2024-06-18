import asyncio
import json
from typing import Any
from pydantic import Field
from nodetool.api.types.chat import MessageCreateRequest, TaskUpdateRequest
from nodetool.common.chat import process_messages
from nodetool.metadata.types import (
    ColumnDef,
    DataframeRef,
    FunctionModel,
    ImageRef,
    NodeRef,
    RecordType,
    Task,
    ToolCall,
)
from nodetool.metadata.types import GPTModel
from nodetool.workflows.base_node import BaseNode
from nodetool.workflows.processing_context import ProcessingContext
from nodetool.metadata.types import Message


class DataframeAgent(BaseNode):
    """
    LLM Agent to create a dataframe based on a user prompt.
    llm, language model, agent, chat, conversation
    """

    model: FunctionModel = Field(
        default=FunctionModel(),
        description="The language model to use.",
    )
    prompt: str = Field(
        default="",
        description="The user prompt",
    )
    columns: RecordType = Field(
        default=RecordType(),
        description="The columns to use in the dataframe.",
    )

    async def process(self, context: ProcessingContext) -> DataframeRef:
        message = await context.create_message(
            MessageCreateRequest(
                role="user",
                content=self.prompt,
            )
        )
        input_messages = [
            Message(
                role="system",
                content="Generate records by calling the create_record tool. Follow the instructions below.",
            ),
            message,
        ]
        assert message.thread_id is not None, "Thread ID is required"

        res = await process_messages(
            context=context,
            thread_id=message.thread_id,
            model=self.model,
            messages=input_messages,
            columns=self.columns.columns,
            # n_gpu_layers=self.n_gpu_layers,
        )
        data = [
            [record[col.name] for col in self.columns.columns] for record in res.records
        ]
        return DataframeRef(columns=self.columns.columns, data=data)


class Agent(BaseNode):
    """
    LLM Agent with access to workflows and nodes.
    llm, language model, agent, chat, conversation
    """

    model: FunctionModel = Field(
        default=FunctionModel(),
        description="The language model to use.",
    )
    goal: str = Field(
        default="",
        description="The user prompt",
    )
    # n_gpu_layers: int = Field(default=0, description="Number of layers on the GPU")

    @classmethod
    def return_type(cls):
        return {"thread_id": str, "tasks": list[Task]}

    async def process(self, context: ProcessingContext):
        message = await context.create_message(
            MessageCreateRequest(
                role="user",
                content=self.goal,
            )
        )
        input_messages = [
            Message(
                role="system",
                content="Generate a full list of tasks to achieve the goal below. Do not wait for tasks to finish.",
            ),
            message,
        ]
        assert message.thread_id is not None, "Thread ID is required"

        res = await process_messages(
            context=context,
            thread_id=message.thread_id,
            model=self.model,
            messages=input_messages,
            # n_gpu_layers=self.n_gpu_layers,
        )
        return {"thread_id": message.thread_id, "tasks": res.tasks}


class TaskNode(BaseNode):
    """
    Process the next task in a thread.
    llm, language model, agent, chat, conversation
    """

    model: FunctionModel = Field(
        default=FunctionModel(name=GPTModel.GPT4.value),
        description="The language model to use.",
    )
    task: Task = Field(
        default=Task(),
        description="The task to process.",
    )
    # tasks: list[Task] = Field(
    #     default=[],
    #     description="The tasks to be executed by this agent.",
    # )
    # workflows: list[WorkflowRef] = Field(
    #     default=[],
    #     description="The workflows to to use as tools.",
    # )
    nodes: list[NodeRef] = Field(
        default=[],
        description="The nodes to use as tools.",
    )

    def get_system_prompt(self):
        raise NotImplementedError

    async def process_task(
        self, context: ProcessingContext, task: Task, **kwargs
    ) -> tuple[list[Message], list[ToolCall]]:
        res = await process_messages(
            context=context,
            model_name=self.model.name,
            thread_id=task.thread_id,
            can_create_tasks=False,
            # workflow_ids=[w.id for w in self.workflows],
            node_types=[n.id for n in self.nodes],
            messages=[
                Message(
                    id="",
                    role="system",
                    content=self.get_system_prompt(),
                ),
                Message(
                    id="",
                    role="user",
                    content=task.instructions,
                ),
            ],
            model=self.model,
            **kwargs,
        )

        return res.messages, res.tool_calls


class ProcessTextTask(TaskNode):
    """
    Process the next text generation task in a thread.
    llm, language model, agent, chat, conversation
    """

    def get_system_prompt(self):
        return "Generate text based on the instructions below. Use tools if necessary."

    async def process(self, context: ProcessingContext) -> str | None:
        messages, tool_calls = await self.process_task(context, self.task)

        if len(tool_calls) > 0:
            result = tool_calls[-1].function_response["output"]
        else:
            result = str(messages[-1].content)

        await context.update_task(self.task.id, TaskUpdateRequest(result=result))
        return result


class ProcessImageTask(TaskNode):
    """
    Process the next image generation task in a thread.
    llm, language model, agent, chat, conversation
    """

    def get_system_prompt(self):
        return """
        Follow the instructions below.
        Use tools to generate images.
        Perform exactly one tool call.
        """

    async def process(self, context: ProcessingContext) -> ImageRef | None:
        messages, tool_calls = await self.process_task(context, self.task)
        res = tool_calls[-1].function_response

        assert isinstance(res, dict)
        assert "output" in res

        if isinstance(res["output"], ImageRef):
            result = res["output"]
        else:
            result = ImageRef(**res["output"])

        await context.update_task(
            self.task.id, TaskUpdateRequest(result=result.model_dump_json())
        )
        return result
