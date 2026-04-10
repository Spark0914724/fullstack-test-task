from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Alert
from src.repositories import alert as alert_repo


async def list_alerts(session: AsyncSession, page: int, page_size: int) -> tuple[list[Alert], int]:
    return await alert_repo.get_all(session, page, page_size)
