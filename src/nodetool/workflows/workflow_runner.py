import asyncio
from contextlib import contextmanager
from datetime import datetime

from pydantic import BaseModel

from nodetool.api.types.job import JobUpdate, JobCancelledException
from nodetool.workflows.base_node import GroupNode
from nodetool.workflows.types import NodeProgress, NodeUpdate
from nodetool.workflows.run_job_request import RunJobRequest

from nodetool.workflows.processing_context import (
    ProcessingContext,
)
from nodetool.workflows.base_node import (
    BaseNode,
)
from nodetool.workflows.base_node import requires_capabilities_from_request
from nodetool.common.environment import Environment
from nodetool.workflows.graph import Graph, topological_sort

"""
This module contains the WorkflowRunner class, which is responsible for executing a graph of nodes in a workflow.

The WorkflowRunner class provides the following main functionalities:
1. Running a workflow graph by processing nodes in topological order.
2. Handling parallel execution of nodes at each level of the graph.
3. Managing the execution context, including input/output handling and result collection.
4. Supporting cancellation of running jobs.
5. Handling special node types like GroupNodes (e.g., loop nodes).
6. Managing capabilities required by the workflow, such as GPU support for ComfyUI nodes.

Key components:
- WorkflowRunner: The main class that orchestrates the execution of a workflow.
- run: The primary method to execute a workflow given a RunJobRequest and ProcessingContext.
- process_graph: Processes the entire graph in topological order.
- process_node: Handles the execution of individual nodes, including special cases like GroupNodes.
- torch_capabilities: A context manager to handle GPU-related setups for ComfyUI nodes.

This module is central to the execution of workflows in the nodetool system, providing a flexible
and extensible way to process complex node graphs with various node types and capabilities.
"""


log = Environment.get_logger()


class WorkflowRunner:
    """
    The WorkflowRunner is responsible for executing a graph of nodes in a topological order.
    Nodes will be executed asynchronously in parallel, and the results will be collected and returned.
    If the workflow requires gpu, it will be executed on a worker.
    """

    job_id: str
    status: str = "running"
    is_cancelled: bool = False
    current_node: str | None = None

    def __init__(self, job_id: str):
        self.job_id = job_id

    def is_running(self):
        return self.status == "running"

    def cancel(self):
        self.status = "cancelled"
        self.is_cancelled = True

    async def run(self, req: RunJobRequest, context: ProcessingContext):
        """
        Evaluates graph nodes in topological order.

        Each level of the graph is processed in parallel.

        Output nodes are collected and returned as a dictionary.
        """
        assert req.graph is not None, "Graph is required"

        graph_capabilities = requires_capabilities_from_request(req)

        graph = Graph.from_dict(
            {
                "nodes": [node.model_dump() for node in req.graph.nodes],
                "edges": [edge.model_dump() for edge in req.graph.edges],
            }
        )
        graph = graph.build_sub_graphs()

        input_nodes = {node.name: node for node in graph.inputs()}
        output_nodes = graph.outputs()

        if req.params:
            for key, value in req.params.items():
                if key not in input_nodes:
                    raise ValueError("No input node found for param: " + str(key))

                node = input_nodes[key]
                node.assign_property("value", value)

        with self.torch_capabilities(graph_capabilities, context):
            await self.process_graph(context, graph)

        if self.is_cancelled:
            print("Job cancelled")
            context.post_message(JobUpdate(job_id=self.job_id, status="cancelled"))
            self.status = "cancelled"
            return

        output = {}
        for node in output_nodes:
            output[node.name] = context.get_result(node._id, "output")

        context.post_message(
            JobUpdate(job_id=self.job_id, status="completed", result=output)
        )

        self.status = "completed"

    async def process_graph(self, context: ProcessingContext, graph: Graph):
        """
        Process the graph in a topological order, executing each node in parallel.

        Args:
            context (ProcessingContext): The processing context containing the graph, edges, and nodes.
            graph (Graph): The graph to be processed.

        Returns:
            None
        """
        context.graph = graph
        sorted_nodes = topological_sort(graph.edges, graph.nodes)

        for level in sorted_nodes:
            nodes = [graph.find_node(i) for i in level]
            await asyncio.gather(
                *[self.process_node(context, node) for node in nodes if node]
            )

    async def process_node(self, context: ProcessingContext, node: BaseNode):
        """
        Process a node in the workflow.
        Skip nodes that have already been processed.
        Checks for special types of nodes, such as loop nodes.

        Args:
            context (ProcessingContext): The processing context.
            node (Node): The node to be processed.

        Returns:
            None
        """
        if self.is_cancelled:
            return

        self.current_node = node._id

        # Skip nodes that have already been processed in a sub graph.
        if node._id in context.processed_nodes:
            return

        try:
            # If the node is a loop node, run the loop node, which will process the subgraph.
            if isinstance(node, GroupNode):
                await self.run_group_node(node, context)
            else:
                await self.process_regular_node(context, node)
        except JobCancelledException:
            self.cancel()

    async def run_group_node(self, group_node: GroupNode, context: ProcessingContext):
        """
        Find all nodes from the subgraph of the loop node and pass it to
        the loop node for processing.
        """
        # Assign the input values from edges to the node properties.
        for name, value in context.get_node_inputs(group_node._id).items():
            group_node.assign_property(name, value)

        await group_node.process_subgraph(
            context=context,
            runner=self,
        )
        context.processed_nodes.add(group_node._id)

    async def process_regular_node(self, context: ProcessingContext, node: BaseNode):
        """
        Processes a single node in the graph.

        This will get all the results from the input nodes and assign
        them to the properties of the node. Then the node is processed
        and the result is stored in the context's results dictionary.

        Once the node is processed, it is added to the completed_tasks set.
        """
        started_at = datetime.now()

        try:
            # Assign the input values from edges to the node properties.
            for name, value in context.get_node_inputs(node.id).items():
                node.assign_property(name, value)

            context.post_message(
                NodeUpdate(
                    node_id=node.id,
                    node_name=node.get_title(),
                    status="running",
                    started_at=started_at.isoformat(),
                )
            )

            result = await node.process(context)
            result = await node.convert_output(context, result)
        except Exception as e:
            context.post_message(
                NodeUpdate(
                    node_id=node.id,
                    node_name=node.get_title(),
                    status="error",
                    error=str(e)[:1000],
                    started_at=started_at.isoformat(),
                    completed_at=datetime.now().isoformat(),
                )
            )
            raise e
        else:
            res_for_update = result.copy()

            for o in node.outputs():
                # Comfy types are not sent to the client because they are not JSON serializable.
                if o.type.is_comfy_type():
                    del res_for_update[o.name]
                if isinstance(res_for_update.get(o.name), BaseModel):
                    res_for_update[o.name] = res_for_update[o.name].model_dump()

            context.post_message(
                NodeUpdate(
                    node_id=node._id,
                    node_name=node.get_title(),
                    status="completed",
                    result=res_for_update,
                    started_at=started_at.isoformat(),
                    completed_at=datetime.now().isoformat(),
                )
            )

        context.processed_nodes.add(node._id)
        context.set_result(node._id, result)

    @contextmanager
    def torch_capabilities(self, capabilities: list[str], context: ProcessingContext):
        if "comfy" in capabilities:
            if not "comfy" in context.capabilities:
                raise ValueError("Comfy nodes are not supported in this environment")

            import comfy.model_management
            import comfy.utils
            import torch

            def hook(value, total, preview_image):
                comfy.model_management.throw_exception_if_processing_interrupted()
                context.post_message(
                    NodeProgress(
                        node_id=self.current_node or "",
                        progress=value,
                        total=total,
                        # preview_image=self.encode_image(preview_image),
                    )
                )

            comfy.utils.set_progress_bar_global_hook(hook)

            # comfy.model_management.unload_all_models()
            log.info(f"VRAM: {torch.cuda.memory_allocated(0) / 1024 / 1024 / 1024}")
            with torch.inference_mode():
                comfy.model_management.cleanup_models()
                yield
                # gc.collect()
                # comfy.model_management.soft_empty_cache()
                log.info(f"VRAM: {torch.cuda.memory_allocated(0) / 1024 / 1024 / 1024}")

        else:
            yield
