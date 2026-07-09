import asyncio
from functools import partial
import obsws_python as obs
from config import OBS_HOST, OBS_PORT, OBS_PASSWORD


class OBSClient:
    def __init__(self):
        self.client = None
        self.connected = False
        self.host = OBS_HOST
        self.port = OBS_PORT
        self.password = OBS_PASSWORD
        self._reconnect_task = None
        self._reconnect_interval = 5
        self._explicit_disconnect = False

    async def _create_client_sync(self, host, port, password):
        loop = asyncio.get_event_loop()
        fn = partial(obs.ReqClient, host=host, port=port, password=password, timeout=5)
        return await loop.run_in_executor(None, fn)

    async def _attempt_connect(self):
        try:
            self.client = await self._create_client_sync(self.host, self.port, self.password)
            self.connected = True
            print(f"✅ Connected to OBS at {self.host}:{self.port}")
            return True
        except Exception as e:
            self.connected = False
            print(f"❌ Failed to connect to OBS: {e}")
            return False

    async def connect(self, host: str = OBS_HOST, port: int = OBS_PORT, password: str = OBS_PASSWORD, enable_reconnect: bool = True) -> dict:
        self.host = host
        self.port = port
        self.password = password
        self._explicit_disconnect = False

        ok = await self._attempt_connect()
        if enable_reconnect and self._reconnect_task is None:
            self._start_reconnect_loop()

        if ok:
            return {"success": True, "message": f"Connected to OBS at {host}:{port}"}
        else:
            if enable_reconnect:
                return {"success": False, "message": f"Failed to connect to OBS at {host}:{port} — will retry"}
            return {"success": False, "message": f"Failed to connect to OBS at {host}:{port}"}

    def _start_reconnect_loop(self):
        if self._reconnect_task is None or self._reconnect_task.done():
            loop = asyncio.get_event_loop()
            self._reconnect_task = loop.create_task(self._reconnect_loop())

    def _stop_reconnect_loop(self):
        if self._reconnect_task and not self._reconnect_task.done():
            self._reconnect_task.cancel()
        self._reconnect_task = None

    async def _reconnect_loop(self):
        try:
            while not self._explicit_disconnect:
                if not self.connected:
                    print("🔁 OBS reconnect attempt...")
                    await self._attempt_connect()
                await asyncio.sleep(self._reconnect_interval)
        except asyncio.CancelledError:
            return

    async def disconnect(self, allow_reconnect: bool = False) -> dict:
        try:
            if not allow_reconnect:
                self._explicit_disconnect = True
                self._stop_reconnect_loop()

            if self.client:
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, getattr(self.client, "disconnect"))
                self.client = None

            self.connected = False
            print("🔌 Disconnected from OBS")
            return {"success": True, "message": "Disconnected from OBS"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def get_status(self) -> dict:
        return {
            "connected": self.connected,
            "host": self.host,
            "port": self.port,
            "auto_reconnect": (self._reconnect_task is not None and not self._reconnect_task.done()),
        }

    async def _call_client(self, method_name: str, *args, **kwargs):
        if not self.client:
            return {"success": False, "message": "OBS not connected"}
        try:
            loop = asyncio.get_event_loop()
            fn = partial(getattr(self.client, method_name), *args, **kwargs)
            res = await loop.run_in_executor(None, fn)
            return {"success": True, "result": res}
        except Exception as e:
            print(f"⚠️ OBS client call failed: {e}")
            self.connected = False
            if not self._explicit_disconnect:
                self._start_reconnect_loop()
            return {"success": False, "message": str(e)}

    async def save_replay_buffer(self) -> dict:
        res = await self._call_client("save_replay_buffer")
        if not res.get("success"):
            return {"success": False, "message": res.get("message")}
        print("💾 Replay Buffer saved!")
        return {"success": True, "message": "Replay Buffer saved"}

    async def get_replay_buffer_status(self) -> dict:
        res = await self._call_client("get_replay_buffer_status")
        if not res.get("success"):
            return {"active": False, "error": res.get("message")}
        status = res.get("result")
        try:
            active = bool(getattr(status, "output_active", False))
        except Exception:
            active = bool(status.get("output_active", False)) if isinstance(status, dict) else False
        return {"active": active}


obs_client = OBSClient()
