import logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("highlight.log", encoding="utf-8"),
    ],
)
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from contextlib import asynccontextmanager
from database import init_db, AsyncSessionLocal
from services.obs_client import obs_client
from services.audio_monitor import audio_monitor
from services import offset_calculator
from services.ws_manager import manager
from services.trigger_engine import trigger_engine
from routers import config as config_router
from routers import logs as logs_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    logger.info("Database tersambung")

    # Sinkronkan konfigurasi runtime (OUTPUT_PATH, threshold, persistence, pre_roll)
    # dari database agar nilai yang tersimpan tidak hilang saat restart.
    try:
        from sqlalchemy import select
        from models import Configuration
        import config as global_config
        from services import offset_calculator

        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Configuration).order_by(Configuration.id.desc())
            )
            cfg = result.scalar_one_or_none()
            if cfg:
                if cfg.file_path:
                    global_config.OUTPUT_PATH = cfg.file_path
                if cfg.threshold_db is not None:
                    audio_monitor.threshold_db = cfg.threshold_db
                if cfg.persistence_duration:
                    audio_monitor.persistence_duration = cfg.persistence_duration
                if cfg.pre_roll is not None:
                    offset_calculator.PRE_ROLL = cfg.pre_roll
                if cfg.cooldown_seconds:
                    audio_monitor.cooldown_seconds = cfg.cooldown_seconds
                logger.info("✅ Runtime config disinkronkan dari database")
    except Exception as e:
        logger.warning(f"⚠️ Gagal sinkron config dari DB: {e}")

    yield


app = FastAPI(
    title="Highlight System API",
    description="Sistem Pemotongan Highlight Siaran Langsung",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(config_router.router)
app.include_router(logs_router.router)


@app.get("/")
async def root():
    return {"message": "Highlight System API"}


@app.get("/health")
async def health():
    return {"status": "ok"}


# --- WebSocket (real-time push) ---
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            payload = {
                "connected": obs_client.connected,
                "current_dbfs": round(audio_monitor.current_dbfs, 2),
                "threshold_db": audio_monitor.threshold_db,
                "persistence_duration": audio_monitor.persistence_duration,
                "pre_roll": getattr(offset_calculator, "PRE_ROLL", 5.0),
            }
            await websocket.send_text(json.dumps({"type": "monitor", **payload}))
            await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)


# --- OBS ---
@app.post("/obs/connect")
async def connect_obs(host: str = "127.0.0.1", port: int = 4455, password: str = "Test123"):
    return await obs_client.connect(host=host, port=port, password=password)


@app.post("/obs/disconnect")
async def disconnect_obs():
    return await obs_client.disconnect()


@app.get("/obs/status")
async def obs_status():
    await obs_client.ping()
    return obs_client.get_status()


@app.get("/obs/replay-buffer/status")
async def replay_buffer_status():
    return await obs_client.get_replay_buffer_status()


# --- Audio Monitor ---
@app.post("/obs/monitor/start")
async def start_monitor():
    audio_monitor.on_trigger = trigger_engine.on_audio_trigger
    await audio_monitor.start()
    return {"success": True, "message": "Audio monitor started"}


@app.post("/obs/monitor/stop")
async def stop_monitor():
    await audio_monitor.stop()
    return {"success": True, "message": "Audio monitor stopped"}


@app.get("/obs/monitor/status")
async def monitor_status():
    from services import offset_calculator
    return {
        "connected": audio_monitor.connected,
        "current_dbfs": round(audio_monitor.current_dbfs, 2),
        "threshold_db": audio_monitor.threshold_db,
        "persistence_duration": audio_monitor.persistence_duration,
        "pre_roll": offset_calculator.PRE_ROLL,
    }

@app.post("/obs/monitor/threshold")
async def update_threshold(value: float):
    audio_monitor.threshold_db = value
    logger.info(f"Threshold diupdate: {value} dBFS")
    return {"success": True, "threshold_db": value}


@app.post("/obs/monitor/persistence")
async def update_persistence(value: float):
    if value <= 0:
        return {"success": False, "message": "Persistence harus lebih dari 0"}
    audio_monitor.persistence_duration = value
    logger.info(f"Persistence diupdate: {value}s")
    return {"success": True, "persistence_duration": value}

@app.post("/obs/monitor/preroll")
async def update_preroll(value: float):
    if value < 0:
        return {"success": False, "message": "Pre-roll tidak boleh negatif"}
    from services import offset_calculator
    offset_calculator.PRE_ROLL = value
    logger.info(f"Pre-roll diupdate: {value}s")
    return {"success": True, "pre_roll": value}
    
@app.post("/obs/monitor/filepath")
async def update_filepath(value: str):
    import config
    config.OUTPUT_PATH = value
    logger.info(f"Path penyimpanan diupdate: {value}")
    return {"success": True, "file_path": value}

# --- File Picker ---
@app.get("/file-picker")
async def open_file_picker():
    import tkinter as tk
    from tkinter import filedialog
    from concurrent.futures import ThreadPoolExecutor
    import asyncio
    
    def pick_folder():
        """Buka dialog folder picker di thread terpisah."""
        root = tk.Tk()
        root.withdraw() 
        root.attributes('-topmost', True)
        
        folder_path = filedialog.askdirectory(
            title="Pilih Folder Penyimpanan Hasil Highlight",
            initialdir="D:\\Kuliah\\TA\\Pre-TA\\Project",
        )
        root.destroy()
        return folder_path
    
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        folder_path = await loop.run_in_executor(executor, pick_folder)
    
    if not folder_path:
        return {"success": False, "message": "Folder tidak dipilih", "path": None}
    
    return {"success": True, "message": "Folder berhasil dipilih", "path": folder_path}
