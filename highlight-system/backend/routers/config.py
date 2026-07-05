from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models import Configuration
from pydantic import BaseModel
from datetime import datetime, timezone

router = APIRouter(prefix="/config", tags=["Configuration"])

class ConfigUpdate(BaseModel):
    obs_host: str = "127.0.0.1"
    obs_port: int = 4455
    obs_password: str = ""
    threshold_db: float = -19.0
    file_path: str = ""
    persistence_duration: float = 2.0

@router.get("")
async def get_config(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Configuration).order_by(Configuration.id.desc()))
    config = result.scalar_one_or_none()
    if not config:
        # Buat default config jika belum ada
        config = Configuration()
        db.add(config)
        await db.commit()
        await db.refresh(config)
    return config

@router.put("")
async def update_config(data: ConfigUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Configuration).order_by(Configuration.id.desc()))
    config = result.scalar_one_or_none()
    if not config:
        config = Configuration()
        db.add(config)

    config.obs_host = data.obs_host
    config.obs_port = data.obs_port
    config.obs_password = data.obs_password
    config.threshold_db = data.threshold_db
    config.file_path = data.file_path
    config.persistence_duration = data.persistence_duration
    config.updated_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(config)
    return config