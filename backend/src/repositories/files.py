import mimetypes
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import STORAGE_DIR
from src.models import StoredFile


async def get_all(session: AsyncSession, page: int, page_size: int) -> tuple[list[StoredFile], int]:
    total = await session.scalar(select(func.count()).select_from(StoredFile))
    result = await session.execute(
        select(StoredFile)
        .order_by(StoredFile.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    return list(result.scalars().all()), total or 0


async def get_by_id(session: AsyncSession, file_id: str) -> StoredFile | None:
    return await session.get(StoredFile, file_id)


async def create(session: AsyncSession, title: str, upload_file: UploadFile) -> StoredFile:
    content = await upload_file.read()
    file_id = str(uuid4())
    suffix = Path(upload_file.filename or "").suffix
    stored_name = f"{file_id}{suffix}"
    stored_path = STORAGE_DIR / stored_name
    stored_path.write_bytes(content)

    file_item = StoredFile(
        id=file_id,
        title=title,
        original_name=upload_file.filename or stored_name,
        stored_name=stored_name,
        mime_type=upload_file.content_type or mimetypes.guess_type(stored_name)[0] or "application/octet-stream",
        size=len(content),
        processing_status="uploaded",
    )
    session.add(file_item)
    await session.commit()
    await session.refresh(file_item)
    return file_item


async def update_title(session: AsyncSession, file_item: StoredFile, title: str) -> StoredFile:
    file_item.title = title
    await session.commit()
    await session.refresh(file_item)
    return file_item


async def delete(session: AsyncSession, file_item: StoredFile) -> None:
    stored_path = STORAGE_DIR / file_item.stored_name
    if stored_path.exists():
        stored_path.unlink()
    await session.delete(file_item)
    await session.commit()
