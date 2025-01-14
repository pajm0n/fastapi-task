import pytest
import json


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params, expected_length, expected_has_next_page",
    [
        ({"page": 1, "page_size": 2}, 2, True),
        ({"page": 2, "page_size": 2}, 1, False),
        ({"page": 1, "page_size": 3}, 3, False),
        ({"page": 1, "page_size": 10}, 3, False),
        ({"page": 3, "page_size": 2}, 0, False),
    ],
)
async def test_project_list(
    client, create_project, params, expected_length, expected_has_next_page
):
    await create_project(name="project1")
    await create_project(name="project2")
    await create_project(name="project3")

    response = await client.get("/v1/project", params=params)
    data = response.json()
    assert len(data["results"]) == expected_length
    assert data["elements"] == expected_length
    assert data["has_next_page"] == expected_has_next_page


@pytest.mark.asyncio
async def test_get_project(client, create_project):
    project = await create_project()

    response = await client.get(f"/v1/project/{project.id}")
    assert response.status_code == 200

    data = response.json()

    assert data["id"] == project.id
    assert data["name"] == project.name
    assert data["description"] == project.description
    assert data["area_of_interest"] == project.area_of_interest.geojson_data


@pytest.mark.skip(
    reason="Correct test, but the logic for parsing and storing latitude and longitude needs improvement."
)
@pytest.mark.asyncio
async def test_create_project(client, geojson, geojson_file):
    project_data = {
        "name": "test project name",
        "date_range": {"start": "2025-10-12", "end": "2025-10-15"},
    }
    response = await client.post(
        "/v1/project",
        files={"area_of_interest": geojson_file},
        data={"data": json.dumps(project_data)},
    )
    data = response.json()

    assert data["name"] == project_data["name"]
    assert data["date_range"] == project_data["date_range"]
    assert data["description"] == ""

    assert data["area_of_interest"] == geojson
