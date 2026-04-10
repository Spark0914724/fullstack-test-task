import io
import pytest
from unittest.mock import patch, MagicMock


@pytest.mark.asyncio
async def test_list_files_empty(client):
    response = await client.get("/files")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_upload_and_list_file(client):
    with patch("src.routers.files.scan_file_for_threats") as mock_task:
        mock_task.delay = MagicMock()
        response = await client.post(
            "/files",
            data={"title": "Test File"},
            files={"file": ("test.txt", io.BytesIO(b"hello world"), "text/plain")},
        )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test File"
    assert data["original_name"] == "test.txt"
    assert data["processing_status"] == "uploaded"

    list_response = await client.get("/files")
    assert list_response.json()["total"] == 1


@pytest.mark.asyncio
async def test_get_file_not_found(client):
    response = await client.get("/files/nonexistent-id")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_alerts_empty(client):
    response = await client.get("/alerts")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_pagination(client):
    with patch("src.routers.files.scan_file_for_threats") as mock_task:
        mock_task.delay = MagicMock()
        for i in range(5):
            await client.post(
                "/files",
                data={"title": f"File {i}"},
                files={"file": (f"file{i}.txt", io.BytesIO(b"data"), "text/plain")},
            )

    response = await client.get("/files?page=1&page_size=2")
    data = response.json()
    assert len(data["items"]) == 2
    assert data["total"] == 5
    assert data["page"] == 1
    assert data["page_size"] == 2
