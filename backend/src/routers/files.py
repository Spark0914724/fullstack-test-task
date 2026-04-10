from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.db import async_session_maker, STORAGE_DIR
from src.schemas import FileItem, FileUpdate, PaginatedResponse
from src.services import files as files_service
from src.tasks import scan_file_for_threats

router = APIRouter(prefix="/files", tags=["files"])


async def get_session():
    async with async_session_maker() as session:
        yield session


@router.get("", response_model=PaginatedResponse[FileItem])
async def list_files(page: int = 1, page_size: int = 20, session: AsyncSession = Depends(get_session)):
    items, total = await files_service.list_files(session, page, page_size)
    return PaginatedResponse(items=items, total=total, page=page, page_size=page_size)


@router.post("", response_model=FileItem, status_code=201)
async def create_file(
    title: str = Form(...),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
):
    file_item = await files_service.create_file(session, title, file)
    scan_file_for_threats.delay(file_item.id)
    return file_item


@router.get("/{file_id}", response_model=FileItem)
async def get_file(file_id: str, session: AsyncSession = Depends(get_session)):
    return await files_service.get_file(session, file_id)


@router.patch("/{file_id}", response_model=FileItem)
async def update_file(file_id: str, payload: FileUpdate, session: AsyncSession = Depends(get_session)):
    return await files_service.update_file(session, file_id, payload.title)


@router.get("/{file_id}/download")
async def download_file(file_id: str, session: AsyncSession = Depends(get_session)):
    file_item = await files_service.get_file(session, file_id)
    stored_path = STORAGE_DIR / file_item.stored_name
    if not stored_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stored file not found")
    return FileResponse(path=stored_path, media_type=file_item.mime_type, filename=file_item.original_name)


@router.delete("/{file_id}", status_code=204)
async def delete_file(file_id: str, session: AsyncSession = Depends(get_session)):
    await files_service.delete_file(session, file_id)
