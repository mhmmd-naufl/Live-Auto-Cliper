import asyncio
from obswebsocket import obsws, events

async def main():
    ws = obsws("127.0.0.1", 4455, "Test123")
    
    def on_volume(message):
        print(f"🎤 Volume event: {message}")
    
    ws.register(on_volume, events.InputVolumeMeters)
    ws.connect()
    print("✅ Terhubung ke OBS")
    
    print("Mendengarkan 15 detik...")
    await asyncio.sleep(15)
    
    ws.disconnect()
    print("Selesai")

asyncio.run(main())