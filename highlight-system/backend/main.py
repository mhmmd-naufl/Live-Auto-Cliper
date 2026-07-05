from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import init_db
from services.obs_client import obs_client
from services.audio_monitor import audio_monitor
from services.trigger_engine import trigger_engine
from routers import config as config_router
from routers import logs as logs_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("✅ Database tersambung")
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
    allow_credentials=True,
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


# --- OBS ---
@app.post("/obs/connect")
async def connect_obs(host: str = "127.0.0.1", port: int = 4455, password: str = "Test123"):
    return await obs_client.connect(host=host, port=port, password=password)


@app.post("/obs/disconnect")
async def disconnect_obs():
    return await obs_client.disconnect()


@app.get("/obs/status")
async def obs_status():
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
    return {
        "connected": audio_monitor.connected,
        "current_dbfs": round(audio_monitor.current_dbfs, 2),
        "threshold_db": audio_monitor.threshold_db,
        "persistence_duration": audio_monitor.persistence_duration,
    }