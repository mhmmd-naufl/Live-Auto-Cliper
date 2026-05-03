import asyncio
import obsws_python as obs
from dotenv import load_dotenv
import os

load_dotenv()

OBS_HOST = os.getenv("OBS_HOST", "127.0.0.1")
OBS_PORT = int(os.getenv("OBS_PORT", "4455"))
OBS_PASSWORD = os.getenv("OBS_PASSWORD", "Test123")

class OBSClient:
    def __init__(self):
        self.client = None
        self.connected = False
        self._reconnect_task = None

    async def connect(self, host: str = OBS_HOST, port: int = OBS_PORT, password: str = OBS_PASSWORD) -> dict:
        try:
            self.client = obs.ReqClient(
                host=host,
                port=port,
                password=password,
                timeout=5
            )
            self.connected = True
            print(f"✅ Connected to OBS at {host}:{port}")
            return {"success": True, "message": f"Connected to OBS at {host}:{port}"}
        except Exception as e:
            self.connected = False
            print(f"❌ Failed to connect to OBS: {e}")
            return {"success": False, "message": str(e)}

    async def disconnect(self) -> dict:
        try:
            if self.client:
                self.client.disconnect()
            self.connected = False
            print("🔌 Disconnected from OBS")
            return {"success": True, "message": "Disconnected from OBS"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def get_status(self) -> dict:
        return {
            "connected": self.connected,
            "host": OBS_HOST,
            "port": OBS_PORT,
        }

    async def save_replay_buffer(self) -> dict:
        try:
            if not self.connected or not self.client:
                return {"success": False, "message": "OBS not connected"}
            self.client.save_replay_buffer()
            print("💾 Replay Buffer saved!")
            return {"success": True, "message": "Replay Buffer saved"}
        except Exception as e:
            print(f"❌ Failed to save replay buffer: {e}")
            return {"success": False, "message": str(e)}

    async def get_replay_buffer_status(self) -> dict:
        try:
            if not self.connected or not self.client:
                return {"active": False}
            status = self.client.get_replay_buffer_status()
            return {"active": status.output_active}
        except Exception as e:
            return {"active": False, "error": str(e)}

# Singleton instance
obs_client = OBSClient()