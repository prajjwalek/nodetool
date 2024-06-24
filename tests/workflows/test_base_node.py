import enum
import os
from typing import Optional, Union
import pytest
from nodetool.api.types.graph import Edge, Graph, Node
from nodetool.metadata.node_metadata import NodeMetadata
from nodetool.workflows.processing_context import ProcessingContext
from nodetool.workflows.property import Property
from nodetool.metadata.types import TypeMetadata
from nodetool.workflows.processing_context import ProcessingContext

from nodetool.workflows.base_node import (
    NODE_BY_TYPE,
    NODES_BY_CLASSNAME,
    BaseNode,
    GroupNode,
    add_node_type,
    get_node_class,
    get_node_class_by_name,
    requires_capabilities,
    requires_capabilities_from_request,
    type_metadata,
)
from nodetool.metadata.types import OutputSlot
from nodetool.workflows.run_job_request import RunJobRequest


current_dir = os.path.dirname(os.path.realpath(__file__))
test_file = os.path.join(current_dir, "test.jpg")


class DummyClass(BaseNode):
    prop: int = 123

    def process(self, context: ProcessingContext) -> int:
        return self.prop


class StringNode(BaseNode):
    value: str = "test"

    def process(self, context: ProcessingContext) -> str:
        return self.value


def test_node_creation():
    node = BaseNode(id="")
    assert node._id == ""


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
    node = StringNode(_id="")
    assert node.outputs() == [OutputSlot(type=TypeMetadata(type="str"), name="output")]


def test_node_set_node_properties():
    node = DummyClass()
    node.set_node_properties({"prop": 789})
    assert node.prop == 789


def test_node_set_node_properties_fail():
    node = DummyClass()
    with pytest.raises(ValueError):
        node.set_node_properties({"prop": "test"})


def test_node_set_node_properties_skip_errors():
    node = DummyClass()
    node.set_node_properties({"prop": "test"}, skip_errors=True)
    assert node.prop == 123


def test_node_properties_dict():
    node = DummyClass()
    assert "prop" in node.properties_dict()


def test_node_properties():
    node = DummyClass()
    assert any(prop.name == "prop" for prop in node.properties())


def test_node_node_properties():
    node = DummyClass(prop=123)
    assert node.node_properties() == {"prop": 123}


@pytest.mark.asyncio
async def test_node_convert_output_value(context: ProcessingContext):
    node = DummyClass()
    output = 123
    assert await node.convert_output(context, output) == {"output": 123}


def test_type_metadata_basic_types():
    assert type_metadata(int) == TypeMetadata(type="int")
    assert type_metadata(str) == TypeMetadata(type="str")
    assert type_metadata(float) == TypeMetadata(type="float")
    assert type_metadata(bool) == TypeMetadata(type="bool")


def test_type_metadata_list():
    assert type_metadata(list[int]) == TypeMetadata(
        type="list", type_args=[TypeMetadata(type="int")]
    )


def test_type_metadata_dict():
    assert type_metadata(dict[str, int]) == TypeMetadata(
        type="dict", type_args=[TypeMetadata(type="str"), TypeMetadata(type="int")]
    )


def test_type_metadata_union():
    assert type_metadata(int | str) == TypeMetadata(
        type="union", type_args=[TypeMetadata(type="int"), TypeMetadata(type="str")]
    )


def test_type_metadata_optional():
    assert type_metadata(Optional[int]) == TypeMetadata(type="int", optional=True)


def test_type_metadata_enum():
    class TestEnum(enum.Enum):
        A = "a"
        B = "b"

    metadata = type_metadata(TestEnum)
    assert metadata.type == "enum"
    assert metadata.type_name == "TestEnum"
    assert metadata.values is not None
    assert set(metadata.values) == {"a", "b"}


def test_type_metadata_nested():
    assert type_metadata(list[dict[str, Union[int, str]]]) == TypeMetadata(
        type="list",
        type_args=[
            TypeMetadata(
                type="dict",
                type_args=[
                    TypeMetadata(type="str"),
                    TypeMetadata(
                        type="union",
                        type_args=[TypeMetadata(type="int"), TypeMetadata(type="str")],
                    ),
                ],
            )
        ],
    )


def test_type_metadata_unknown_type():
    class CustomClass:
        pass

    with pytest.raises(ValueError, match="Unknown type"):
        type_metadata(CustomClass)


def test_add_node_type_and_classname():
    class TestNode(BaseNode):
        pass

    add_node_type(TestNode)
    assert TestNode.get_node_type() in NODE_BY_TYPE
    assert "TestNode" in NODES_BY_CLASSNAME
    assert TestNode in NODES_BY_CLASSNAME["TestNode"]


def test_get_node_class_and_by_name():
    class TestNode(BaseNode):
        pass

    add_node_type(TestNode)
    assert get_node_class(TestNode.get_node_type()) == TestNode
    assert TestNode in get_node_class_by_name("TestNode")


def test_base_node_from_dict():
    node_dict = {
        "type": DummyClass.get_node_type(),
        "id": "test_id",
        "parent_id": "parent_id",
        "ui_properties": {"x": 100, "y": 200},
        "data": {"prop": 456},
    }
    node = DummyClass.from_dict(node_dict)
    assert isinstance(node, DummyClass)
    assert node.id == "test_id"
    assert node.parent_id == "parent_id"
    assert node._ui_properties == {"x": 100, "y": 200}
    assert node.prop == 456


def test_base_node_get_json_schema():
    schema = DummyClass.get_json_schema()
    assert "type" in schema
    assert schema["type"] == "object"
    assert "properties" in schema
    assert "prop" in schema["properties"]


@pytest.mark.asyncio
async def test_group_node():
    group = GroupNode(_id="group1")
    node1 = DummyClass(prop=1)
    node2 = DummyClass(prop=2)
    edge = Edge(
        source="node1", sourceHandle="output", target="node2", targetHandle="prop"
    )

    group.append_node(node1)
    group.append_node(node2)
    group.append_edge(edge)
    group.assign_property("test_prop", "test_value")

    assert len(group._nodes) == 2
    assert len(group._edges) == 1
    assert group._properties["test_prop"] == "test_value"

    # Test process_subgraph method (you might need to implement a mock runner)
    context = ProcessingContext(user_id="test_user", auth_token="test_token")
    await group.process_subgraph(context, None)


def test_requires_capabilities():
    class CapabilityNode(BaseNode):
        _requires_capabilities = ["test_capability"]

    nodes = [CapabilityNode(), DummyClass()]
    assert requires_capabilities(nodes) == ["test_capability"]


def test_requires_capabilities_from_request():
    class CapabilityNode(BaseNode):
        _requires_capabilities = ["test_capability"]

    req = RunJobRequest(
        graph=Graph(
            edges=[],
            nodes=[
                Node(id="1", type=CapabilityNode.get_node_type()),
                Node(id="2", type=DummyClass.get_node_type()),
            ],
        )
    )
    assert requires_capabilities_from_request(req) == ["test_capability"]
