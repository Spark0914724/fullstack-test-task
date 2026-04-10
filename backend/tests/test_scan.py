import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

from src.models import StoredFile


def make_file(extension: str, size: int = 1024, mime_type: str = "application/octet-stream") -> StoredFile:
    return StoredFile(
        id="test-id",
        title="Test",
        original_name=f"file{extension}",
        stored_name=f"test-id{extension}",
        mime_type=mime_type,
        size=size,
        processing_status="uploaded",
    )


@pytest.mark.asyncio
async def test_scan_suspicious_extension():
    from src.tasks import _scan_file_for_threats

    file_item = make_file(".exe")
    mock_session = AsyncMock()
    mock_session.get = AsyncMock(return_value=file_item)
    mock_session.commit = AsyncMock()
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)

    with patch("src.tasks.async_session_maker", return_value=mock_session), \
         patch("src.tasks.extract_file_metadata") as mock_task:
        mock_task.delay = MagicMock()
        await _scan_file_for_threats("test-id")

    assert file_item.scan_status == "suspicious"
    assert "suspicious extension .exe" in file_item.scan_details
    assert file_item.requires_attention is True


@pytest.mark.asyncio
async def test_scan_clean_file():
    from src.tasks import _scan_file_for_threats

    file_item = make_file(".txt", mime_type="text/plain")
    mock_session = AsyncMock()
    mock_session.get = AsyncMock(return_value=file_item)
    mock_session.commit = AsyncMock()
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)

    with patch("src.tasks.async_session_maker", return_value=mock_session), \
         patch("src.tasks.extract_file_metadata") as mock_task:
        mock_task.delay = MagicMock()
        await _scan_file_for_threats("test-id")

    assert file_item.scan_status == "clean"
    assert file_item.requires_attention is False


@pytest.mark.asyncio
async def test_scan_large_file():
    from src.tasks import _scan_file_for_threats

    file_item = make_file(".txt", size=11 * 1024 * 1024)
    mock_session = AsyncMock()
    mock_session.get = AsyncMock(return_value=file_item)
    mock_session.commit = AsyncMock()
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)

    with patch("src.tasks.async_session_maker", return_value=mock_session), \
         patch("src.tasks.extract_file_metadata") as mock_task:
        mock_task.delay = MagicMock()
        await _scan_file_for_threats("test-id")

    assert file_item.scan_status == "suspicious"
    assert "larger than 10 MB" in file_item.scan_details


@pytest.mark.asyncio
async def test_scan_pdf_mime_mismatch():
    from src.tasks import _scan_file_for_threats

    file_item = make_file(".pdf", mime_type="text/plain")
    mock_session = AsyncMock()
    mock_session.get = AsyncMock(return_value=file_item)
    mock_session.commit = AsyncMock()
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)

    with patch("src.tasks.async_session_maker", return_value=mock_session), \
         patch("src.tasks.extract_file_metadata") as mock_task:
        mock_task.delay = MagicMock()
        await _scan_file_for_threats("test-id")

    assert file_item.scan_status == "suspicious"
    assert "pdf extension does not match mime type" in file_item.scan_details
