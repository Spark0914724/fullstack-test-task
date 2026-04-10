from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Alert


async def get_all(session: AsyncSession, page: int, page_size: int) -> tuple[list[Alert], int]:
    total = await session.scalar(select(func.count()).select_from(Alert))
    result = await session.execute(
        select(Alert)
        .order_by(Alert.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    return list(result.scalars().all()), total or 0


async def create(session: AsyncSession, file_id: str, level: str, message: str) -> Alert:
    alert = Alert(file_id=file_id, level=level, message=message)
    session.add(alert)
    await session.commit()
    await session.refresh(alert)
    return alert
