import json
import os

import pytest
from genflow.api.models.graph import Edge
from genflow.api.models.graph import Graph
from genflow.workflows.run_job_request import RunJobRequest
from tests.conftest import make_job
from fastapi.testclient import TestClient
from genflow.models.user import User
from genflow.models.workflow import Workflow
from genflow.nodes.genflow.input import IntInputNode
from genflow.nodes.genflow.math import AddNode
from genflow.nodes.genflow.output import IntOutputNode

current_dir = os.path.dirname(os.path.realpath(__file__))
test_file = os.path.join(current_dir, "test.jpg")


def test_get(client: TestClient, headers: dict[str, str], user: User):
    job = make_job(user)
    job.save()
    response = client.get(f"/api/jobs/{job.id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["id"] == job.id
    assert data["status"] == job.status


def test_index(client: TestClient, headers: dict[str, str], user: User):
    make_job(user)
    make_job(user)
    response = client.get("/api/jobs", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data["jobs"]) == 2


def test_index_limit(client: TestClient, headers: dict[str, str], user: User):
    make_job(user)
    make_job(user)
    response = client.get("/api/jobs", params={"page_size": 1}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data["jobs"]) == 1


@pytest.mark.asyncio
async def test_run(
    client: TestClient,
    workflow: Workflow,
    user: User,
    headers: dict[str, str],
):
    int_a = {"id": "1", "type": IntInputNode.get_node_type(), "data": {"value": 10}}
    int_b = {
        "id": "2",
        "type": IntInputNode.get_node_type(),
        "data": {"value": 5},
    }
    add = {
        "id": "3",
        "type": AddNode.get_node_type(),
    }
    int_output = {
        "id": "4",
        "type": IntOutputNode.get_node_type(),
    }

    nodes = [int_a, int_b, add, int_output]

    edges = [
        Edge(id="1", source="1", target="3", sourceHandle="output", targetHandle="a"),
        Edge(id="2", source="2", target="3", sourceHandle="output", targetHandle="b"),
        Edge(
            id="3", source="3", target="4", sourceHandle="output", targetHandle="value"
        ),
    ]

    req = RunJobRequest(
        workflow_id=workflow.id,
        auth_token=str(user.auth_token),
        graph=Graph(nodes=nodes, edges=edges),
        params={},
    )

    response = client.post("/api/jobs/", json=req.model_dump(), headers=headers)
    assert response.status_code == 200

    # read response body line by line and convert to a list of dicts
    messages = [json.loads(line) for line in response.iter_lines()]

    assert len(messages) > 0

    for i in ["1", "2", "3", "4"]:
        assert any(
            m.get("node_id") == i and m.get("status") == "running" for m in messages
        )
        assert any(
            m.get("node_id") == i and m.get("status") == "completed" for m in messages
        )
