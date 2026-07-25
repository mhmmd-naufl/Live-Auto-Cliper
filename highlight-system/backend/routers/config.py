from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models import Configuration
from pydantic import BaseModel
from datetime import datetime, timezone
import sounddevice as sd
import os

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

    if data.threshold_db > 0 or data.threshold_db < -60:
        raise HTTPException(status_code=400, detail="Threshold must be between -60 and 0 dBFS")
    
    if data.persistence_duration <= 0:
        raise HTTPException(status_code=400, detail="Persistence duration must be greater than 0")
    
    if data.file_path and not os.path.exists(data.file_path):
        raise HTTPException(status_code=400, detail=f"Directory does not exist: {data.file_path}")

    config.obs_host = data.obs_host
    config.obs_port = data.obs_port
    config.obs_password = data.obs_password
    config.threshold_db = data.threshold_db
    config.file_path = data.file_path
    config.persistence_duration = data.persistence_duration
    config.updated_at = datetime.now(timezone.utc)
    
    import config as global_config
    global_config.OUTPUT_PATH = data.file_path
    
    print(f"📁 Path penyimpanan telah diupdate di: {data.file_path}")

    await db.commit()
    await db.refresh(config)
    return config

@router.get("/input-devices")
async def get_input_devices():
    try:
        devices = sd.query_devices()
        
        input_devices = []
        default_device_name = sd.query_devices(kind='input')['name']
        
        for i, dev in enumerate(devices):
            if dev['max_input_channels'] > 0:
                input_devices.append({
                    "index": i,
                    "name": dev['name'],
                    "channels": dev['max_input_channels'],
                    "sample_rate": dev.get('default_samplerate'),
                    "is_default": dev['name'] == default_device_name
                })
        
        return {
            "status": "success",
            "devices": input_devices,
            "default_device": default_device_name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal membaca perangkat audio: {str(e)}")