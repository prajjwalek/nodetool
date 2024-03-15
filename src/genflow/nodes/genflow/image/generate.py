import os

from genflow.workflows.workflow_node import WorkflowNode


current_dir = os.path.dirname(os.path.realpath(__file__))
workflows_dir = os.path.join(current_dir, "workflows")


class StableDiffusionNode(WorkflowNode):
    @classmethod
    def get_workflow_file(cls) -> str:
        return os.path.join(workflows_dir, "stable_diffusion.json")
