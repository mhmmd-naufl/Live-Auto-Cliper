from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import init_db
from services.obs_client import obs_client
from services.audio_monitor import audio_monitor

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("Database Berhasil Tersambung")
    yield

app = FastAPI(
    title="Highlight System API",
    description="Sistem Pemotongan Highlight Siaran Langsung",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Highlight System API"}

@app.get("/health")
async def health():
    return {"status": "ok"}
  
@app.post("/obs/connect")
async def connect_obs(host: str = "127.0.0.1", port: int = 4455, password: str = "Test123"):
    result = await obs_client.connect(host=host, port=port, password=password)
    return result

@app.post("/obs/disconnect")
async def disconnect_obs():
    result = await obs_client.disconnect()
    return result

@app.get("/obs/status")
async def obs_status():
    return obs_client.get_status()
  
@app.get("/obs/replay-buffer/status")
async def replay_buffer_status():
    return await obs_client.get_replay_buffer_status()

@app.post("/obs/monitor/start")
async def start_monitor():
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
        "current_dbfs": audio_monitor.current_dbfs,
        "threshold_db": audio_monitor.threshold_db,
        "is_above_threshold": audio_monitor.is_above_threshold,
    }

@app.get("/obs/debug/inputs")
async def debug_inputs():
    try:
        inputs = obs_client.client.get_input_list()
        return {"inputs": inputs.inputs}
    except Exception as e:
        return {"error": str(e)}