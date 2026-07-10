from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from database import get_db
from models import HighlightLog

router = APIRouter(prefix="/logs", tags=["Highlight Logs"])

@router.get("")
async def get_logs(limit: int = 50, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(HighlightLog)
        .order_by(HighlightLog.timestamp.desc())
        .limit(limit)
    )
    logs = result.scalars().all()
    return logs

@router.delete("/clear")
async def clear_all_logs(db: AsyncSession = Depends(get_db)):
    await db.execute(delete(HighlightLog))
    await db.commit()
    return {"success": True}

@router.delete("/{log_id}")
async def delete_log(log_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(HighlightLog).where(HighlightLog.id == log_id))
    log = result.scalar_one_or_none()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    await db.delete(log)
    await db.commit()
    return {"success": True}