import asyncio
import math
import time
import numpy as np
import sounddevice as sd
from config import AUDIO_DEVICE_ID, THRESHOLD_DB, PERSISTENCE_DURATION


def get_input_devices():
    try:
        devices = sd.query_devices()
    except Exception as e:
        print(f"❌ Failed to query audio devices: {e}")
        return []

    input_devices = []
    for idx, dev in enumerate(devices):
        if dev.get('max_input_channels', 0) > 0:
            input_devices.append({
                'id': idx,
                'name': dev.get('name'),
                'max_input_channels': int(dev.get('max_input_channels', 0)),
                'default_samplerate': float(dev.get('default_samplerate', 0)),
            })
    return input_devices


def print_input_devices():
    devs = get_input_devices()
    if not devs:
        print("No input audio devices found.")
        return
    print("Available input audio devices:")
    for d in devs:
        print(f"  [{d['id']}] {d['name']} - channels: {d['max_input_channels']} - rate: {d['default_samplerate']}")


class AudioMonitor:
    def __init__(self):
        self.connected = False
        self.current_dbfs = -60.0
        self.threshold_db = THRESHOLD_DB
        self.persistence_duration = PERSISTENCE_DURATION
        self.cooldown_seconds = 8.0
        self.t_start = None
        self.last_trigger_time = 0.0
        self.on_trigger = None
        self._stream = None
        self._loop = None
        self._trigger_valid = False

        # Buffer untuk smoothing
        self._dbfs_buffer = []
        self._buffer_size = 8

        # Print periodic dBFS ke terminal
        self._last_print_time = 0.0
        self._print_interval = 0.5

    def magnitude_to_dbfs(self, magnitude: float) -> float:
        if magnitude <= 0:
            return -60.0
        return max(-60.0, 20 * math.log10(magnitude))

    def _audio_callback(self, indata, frames, time_info, status):
        if status:
            print(f"⚠️ Audio status: {status}")

        # Hitung RMS dari frame audio
        rms = np.sqrt(np.mean(indata ** 2))
        dbfs = self.magnitude_to_dbfs(float(rms))

        # Smoothing (moving average)
        self._dbfs_buffer.append(dbfs)
        if len(self._dbfs_buffer) > self._buffer_size:
            self._dbfs_buffer.pop(0)

        avg_dbfs = sum(self._dbfs_buffer) / len(self._dbfs_buffer)
        self.current_dbfs = avg_dbfs

        # Cetak dBFS ke terminal setiap 0.5 detik
        now = time.time()
        if now - self._last_print_time >= self._print_interval:
            self._last_print_time = now
            print(f"📊 dBFS: {avg_dbfs:6.1f}")

        # Cek threshold (hanya dipanggil SEKALI)
        self._check_threshold(avg_dbfs)

    def _check_threshold(self, dbfs: float):
        now = time.time()

        # Cooldown check — cegah trigger terlalu sering
        if now < self.last_trigger_time + self.cooldown_seconds:
            return

        if dbfs >= self.threshold_db:
            # Audio di atas threshold — catat waktu mulai
            if self.t_start is None:
                self.t_start = now
                print(f"🔊 Potensi highlight | dBFS: {dbfs:.1f}")

            elapsed = now - self.t_start
            if elapsed >= self.persistence_duration:
                if not self._trigger_valid:
                    self._trigger_valid = True
                    print(f"✅ Trigger valid! dBFS={dbfs:.1f} | Duration={elapsed:.2f}s | Menunggu audio turun...")
        else:
            # Audio turun di bawah threshold
            if self._trigger_valid:
                # Trigger sudah valid, sekarang audio turun — eksekusi
                print(f"🔽 Audio turun (T_End) | Eksekusi SaveReplayBuffer...")
                if self.on_trigger:
                    from services.trigger_engine import trigger_engine
                    trigger_engine.last_trigger_dbfs = dbfs
                    asyncio.run_coroutine_threadsafe(
                        self.on_trigger(self.t_start), self._loop
                    )
                self.last_trigger_time = now
                self._trigger_valid = False
                self.t_start = None
            elif self.t_start is not None:
                # Audio turun sebelum persistence terpenuhi — reset
                print(f"🔄 Reset (hanya {now - self.t_start:.2f}s)")
                self.t_start = None

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
                blocksize=0,
            )
            self._stream.start()
            self.connected = True
            print(f"🎙️ Audio Monitor ACTIVE — Device: {device_info['name']}")
            print(f"Threshold: {self.threshold_db} dBFS | Persistence: {self.persistence_duration}s")

        except Exception as e:
            print(f"❌ Failed to start audio monitor: {e}")

    async def stop(self):
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None
        self.connected = False
        self._trigger_valid = False
        self.t_start = None
        print("🛑 Audio monitor stopped")


# Instance global
audio_monitor = AudioMonitor()