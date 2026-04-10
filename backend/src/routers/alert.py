from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import async_session_maker
from src.deps import get_session
from src.schemas import AlertItem, PaginatedResponse
from src.services import alert as alert_service

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=PaginatedResponse[AlertItem])
async def list_alerts(page: int = 1, page_size: int = 20, session: AsyncSession = Depends(get_session)):
    items, total = await alert_service.list_alerts(session, page, page_size)
    return PaginatedResponse(items=items, total=total, page=page, page_size=page_size)
