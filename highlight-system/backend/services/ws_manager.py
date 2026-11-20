import json
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active.discard(websocket)

    async def broadcast(self, message: dict):
        if not self.active:
            return
        data = json.dumps(message, default=str)
        dead = []
        for ws in list(self.active):
            try:
                await ws.send_text(data)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.active.discard(ws)


manager = ConnectionManager()


async def broadcast_monitor(payload: dict):
    await manager.broadcast({"type": "monitor", **payload})


async def broadcast_log(log: dict):
    await manager.broadcast({"type": "log", "log": log})