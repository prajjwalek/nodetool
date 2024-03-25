from genflow.workflows.genflow_node import GenflowNode
from genflow.workflows.processing_context import ProcessingContext


from typing import Any


class LoopNode(GenflowNode):
    """
    Loops over a list of items and processes the remaining nodes for each item.
    loop, itereate, repeat, for, each, batch
    """

    items: list[Any] = []

    async def process(self, context: ProcessingContext) -> Any:
        return None


class LoopOutputNode(GenflowNode):
    """
    Output the result of a loop.
    loop, result, return
    """

    input: Any = None

    async def process(self, context: ProcessingContext) -> Any:
        return self.input
