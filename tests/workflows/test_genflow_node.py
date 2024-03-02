import os
import pytest
from genflow.metadata.node_metadata import NodeMetadata
from genflow.workflows.processing_context import ProcessingContext
from genflow.workflows.property import Property
from genflow.metadata.types import TypeMetadata

from genflow.workflows.genflow_node import GenflowNode
from genflow.metadata.types import OutputSlot


current_dir = os.path.dirname(os.path.realpath(__file__))
test_file = os.path.join(current_dir, "test.jpg")


class DummyClass(GenflowNode):
    prop: int = 123

    def process(self, context: ProcessingContext) -> int:
        return self.prop


class StringNode(GenflowNode):
    value: str = "test"

    def process(self, context: ProcessingContext) -> str:
        return self.value


def test_node_creation():
    node = GenflowNode()
    assert node.id == ""


def test_node_metadata_method():
    node = DummyClass()
    assert isinstance(node.metadata(), NodeMetadata)


def test_node_find_property_method():
    node = DummyClass(prop=123)
    assert isinstance(node.find_property("prop"), Property)


def test_node_find_property_fail():
    node = DummyClass(prop=123)
    with pytest.raises(ValueError):
        node.find_property("non_existent_prop")


def test_node_find_output_method():
    node = DummyClass()
    assert isinstance(node.find_output("output"), OutputSlot)


def test_node_find_output_fail():
    node = DummyClass()
    with pytest.raises(ValueError):
        node.find_output("non_existent_output")


def test_node_assign_property_method():
    node = DummyClass()
    node.assign_property("prop", 456)
    assert node.prop == 456


def test_node_assign_property_fail():
    node = DummyClass()
    with pytest.raises(ValueError):
        node.assign_property("prop", "test")


def test_node_is_assignable_method():
    node = DummyClass()
    assert node.is_assignable("prop", 456) == True


def test_node_output_type():
    node = DummyClass()
    assert node.outputs() == [OutputSlot(type=TypeMetadata(type="int"), name="output")]


def test_string_node_output_type():
    node = StringNode()
    assert node.outputs() == [OutputSlot(type=TypeMetadata(type="str"), name="output")]
