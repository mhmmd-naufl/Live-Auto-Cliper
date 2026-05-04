import asyncio
import math
import time
import numpy as np
import sounddevice as sd
from config import AUDIO_DEVICE_ID, THRESHOLD_DB, PERSISTENCE_DURATION

class AudioMonitor:
    def __init__(self):
        self.connected = False
        self.current_dbfs = -60.0
        self.threshold_db = THRESHOLD_DB
        self.persistence_duration = PERSISTENCE_DURATION

        self.t_start = None
        self.is_above_threshold = False
        self.trigger_active = False
        self.cooldown_until = 0.0

        self.on_trigger = None
        self._listeners = []
        self._stream = None
        self._loop = None

        self._dbfs_buffer = []
        self._buffer_size = 20

    def magnitude_to_dbfs(self, magnitude: float) -> float:
        if magnitude <= 0:
            return -60.0
        return max(-60.0, 20 * math.log10(magnitude))

    def _check_threshold(self, dbfs: float):
        now = time.time()

        if now < self.cooldown_until:
            return

        # print(f"current threshold : {dbfs:.1f} dBFS")

        if dbfs >= self.threshold_db:
            if not self.is_above_threshold:
                self.t_start = now
                self.is_above_threshold = True
                print(f"🔊 Above threshold: {dbfs:.1f} dBFS")
            elif not self.trigger_active:
                duration = now - self.t_start
                if duration >= self.persistence_duration:
                    self.trigger_active = True
                    print(f"✅ Trigger valid! Duration: {duration:.2f}s")
                    if self.on_trigger and self._loop:
                        asyncio.run_coroutine_threadsafe(
                            self.on_trigger(self.t_start), self._loop
                        )
        else:
            if self.is_above_threshold:
                print(f"🔇 Below threshold: {dbfs:.1f} dBFS — reset")
            self.is_above_threshold = False
            self.trigger_active = False
            self.t_start = None

    def _audio_callback(self, indata, frames, time_info, status):
        if status:
            print(f"⚠️ Audio status: {status}")

        rms = np.sqrt(np.mean(indata ** 2))
        dbfs = self.magnitude_to_dbfs(float(rms))

        self._dbfs_buffer.append(dbfs)
        if len(self._dbfs_buffer) > self._buffer_size:
            self._dbfs_buffer.pop(0)

        avg_dbfs = sum(self._dbfs_buffer) / len(self._dbfs_buffer)
        self.current_dbfs = avg_dbfs
        self._check_threshold(avg_dbfs)

    def set_cooldown(self, seconds: float = 5.0):        
        self.cooldown_until = time.time() + seconds
        print(f"⏳ Cooldown aktif selama {seconds} detik")

    def add_listener(self, callback):
        self._listeners.append(callback)

    def remove_listener(self, callback):
        self._listeners = [l for l in self._listeners if l != callback]

    async def start(self, device_id: int = AUDIO_DEVICE_ID):
        try:
            await self.stop()
            self._loop = asyncio.get_event_loop()

            device_info = sd.query_devices(device_id)
            samplerate = int(device_info['default_samplerate'])
            channels = min(device_info['max_input_channels'], 2)

            self._stream = sd.InputStream(
                device=device_id,
                channels=channels,
                samplerate=samplerate,
                callback=self._audio_callback,
            )
            self._stream.start()
            self.connected = True
            print(f"🎙️ Audio monitor started — device: {device_info['name']}")

        except Exception as e:
            print(f"❌ Audio monitor failed: {e}")
            self.connected = False

    async def stop(self):
        try:
            if self._stream:
                self._stream.stop()
                self._stream.close()
                self._stream = None
            self.connected = False
            print("🛑 Audio monitor stopped")
        except Exception as e:
            print(f"❌ Error stopping: {e}")

audio_monitor = AudioMonitor()