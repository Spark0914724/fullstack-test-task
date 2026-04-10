from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import StoredFile
from src.repositories import files as files_repo


async def list_files(session: AsyncSession, page: int, page_size: int) -> tuple[list[StoredFile], int]:
    return await files_repo.get_all(session, page, page_size)


async def get_file(session: AsyncSession, file_id: str) -> StoredFile:
    file_item = await files_repo.get_by_id(session, file_id)
    if not file_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return file_item


async def create_file(session: AsyncSession, title: str, upload_file: UploadFile) -> StoredFile:
    content_length = upload_file.size or 0
    if content_length == 0:
        data = await upload_file.read(1)
        await upload_file.seek(0)
        if not data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File is empty")
    return await files_repo.create(session, title, upload_file)


async def update_file(session: AsyncSession, file_id: str, title: str) -> StoredFile:
    file_item = await files_repo.get_by_id(session, file_id)
    if not file_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return await files_repo.update_title(session, file_item, title)


async def delete_file(session: AsyncSession, file_id: str) -> None:
    file_item = await files_repo.get_by_id(session, file_id)
    if not file_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    await files_repo.delete(session, file_item)
