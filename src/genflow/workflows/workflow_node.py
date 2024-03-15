from genflow.metadata.types import OutputSlot
from genflow.workflows.genflow_node import GenflowNode, type_metadata
from genflow.workflows.property import Property
from genflow.workflows.read_graph import read_graph
from genflow.api.models.graph import Graph as APIGraph
import json
from genflow.workflows.run_workflow import run_workflow
from genflow.workflows.run_job_request import RunJobRequest
from genflow.common.environment import Environment
from genflow.workflows.processing_context import ProcessingContext
from genflow.workflows.genflow_node import InputNode, OutputNode
from genflow.workflows.graph import Graph
from typing import Any, Type

from genflow.workflows.types import WorkflowUpdate


def properties_from_input_nodes(nodes: list[GenflowNode]):
    return [
        Property(
            name=node.name,
            title=node.name,
            default=node.value,  # type: ignore
            min=node.min if hasattr(node, "min") else None,  # type: ignore
            max=node.max if hasattr(node, "max") else None,  # type: ignore
            type=type_metadata(node.return_type()),  # type: ignore
        )
        for node in nodes
        if isinstance(node, InputNode)
    ]


class WorkflowNode(GenflowNode):
    inputs: dict[str, Any] | None = None

    def __init__(self, **kwargs):
        id = kwargs.pop("id", "")
        ui_properties = kwargs.pop("ui_properties", {})
        super().__init__(id=id, ui_properties=ui_properties)
        self.inputs = kwargs

    @classmethod
    def get_workflow_file(cls) -> str:
        return ""

    @classmethod
    def read_workflow(cls) -> dict:
        workflow_file = cls.get_workflow_file()
        if workflow_file == "":
            return {}
        if not hasattr(cls, "workflow_json"):
            with open(workflow_file, "r") as f:
                cls.workflow_json = json.load(f)
        return cls.workflow_json

    @classmethod
    def properties(cls):
        graph = cls.load_graph()
        return properties_from_input_nodes(graph.nodes)

    @classmethod
    def load_workflow(cls):
        return read_graph(cls.read_workflow())

    @classmethod
    def load_graph(cls):
        edges, nodes = cls.load_workflow()
        return Graph.from_dict(
            {
                "nodes": [node.model_dump() for node in nodes],
                "edges": [edge.model_dump() for edge in edges],
            }
        )

    @classmethod
    def outputs(cls):
        graph = cls.load_graph()
        return [
            OutputSlot(type=type_metadata(output.return_type()), name=output.name)  # type: ignore
            for output in graph.outputs()
        ]

    def get_api_graph(self) -> APIGraph:
        edges, nodes = self.load_workflow()
        return APIGraph(edges=edges, nodes=nodes)

    async def process(self, context: ProcessingContext):
        capabilities = ["db"]

        if Environment.get_comfy_folder():
            capabilities.append("comfy")

        req = RunJobRequest(
            user_id=context.user_id,
            auth_token=context.auth_token,
            graph=self.get_api_graph(),
            params=self.inputs or {},
        )
        output = {}
        for msg_json in run_workflow(req, capabilities):
            msg = json.loads(msg_json)
            if msg["type"] == "error":
                raise Exception(msg["error"])
            if msg["type"] == "workflow_update":
                output = msg["result"]

        return output
