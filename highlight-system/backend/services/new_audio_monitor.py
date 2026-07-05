import asyncio
import math
import time
from config import THRESHOLD_DB, PERSISTENCE_DURATION
from services.obs_client import obs_client

class AudioMonitor:
    def __init__(self):
        self.connected = False
        self.current_dbfs = -60.0
        self.threshold_db = THRESHOLD_DB
        self.persistence_duration = PERSISTENCE_DURATION
        self.cooldown_seconds = 10.0

        self.t_start = None
        self.last_trigger_time = 0.0
        self.on_trigger = None
        self._loop = None

        self._dbfs_buffer = []
        self._buffer_size = 12

        self.total_samples = 0
        self.peak_dbfs = -60.0
        self.trigger_count = 0

    def magnitude_to_dbfs(self, magnitude: float) -> float:
        if magnitude <= 0:
            return -60.0
        return max(-60.0, 20 * math.log10(magnitude))

    async def _handle_input_volume_meters(self, data):
        try:
            inputs = data.get('inputs', [])
            if not inputs:
                return

            for inp in inputs:
                input_name = inp.get('inputName', '')
                if 'Desktop Audio' in input_name or 'Audio' in input_name:
                    levels = inp.get('inputLevelsMul', [0.0])
                    if levels:
                        magnitude = max(levels)
                        dbfs = self.magnitude_to_dbfs(magnitude)
                        self._process_dbfs(dbfs, input_name)
                        return
        except Exception as e:
            print(f"Error processing volume meters: {e}")

    def _process_dbfs(self, dbfs: float, input_name: str = "Desktop Audio"):
        now = time.time()
        self.total_samples += 1
        if dbfs > self.peak_dbfs:
            self.peak_dbfs = dbfs

        self._dbfs_buffer.append(dbfs)
        if len(self._dbfs_buffer) > self._buffer_size:
            self._dbfs_buffer.pop(0)

        avg_dbfs = sum(self._dbfs_buffer) / len(self._dbfs_buffer)
        self.current_dbfs = avg_dbfs

        if self.total_samples % 30 == 0:
            print(f"[{time.strftime('%H:%M:%S')}] Avg: {avg_dbfs:6.2f} dBFS | Peak: {self.peak_dbfs:6.2f}")

        if now < self.last_trigger_time + self.cooldown_seconds:
            return

        print("current dBFS : {dbfs:.1}")

        if avg_dbfs >= self.threshold_db:
            if self.t_start is None:
                self.t_start = now
                print(f"🔊 POTENSI SORAK | {avg_dbfs:.2f} dBFS")

            elapsed = now - self.t_start
            if elapsed >= self.persistence_duration:
                self.trigger_count += 1
                print(f"✅ TRIGGER #{self.trigger_count} | dBFS: {avg_dbfs:.2f} | Durasi: {elapsed:.2f}s")
                
                if self.on_trigger:
                    asyncio.run_coroutine_threadsafe(
                        self.on_trigger(self.t_start), self._loop
                    )
                
                self.last_trigger_time = now
                self.t_start = None
        else:
            if self.t_start is not None:
                print(f"🔄 Reset | Hanya {now - self.t_start:.2f}s")
                self.t_start = None

    async def start(self):
        try:
            await self.stop()
            self._loop = asyncio.get_event_loop()

            # Perbaikan pengecekan koneksi (lebih aman)
            if not hasattr(obs_client, 'client') or obs_client.client is None:
                print("❌ OBS Client belum terhubung atau belum diinisialisasi.")
                print("   Silakan connect dulu melalui /obs/connect")
                return False

            # Coba cek status koneksi dengan cara yang lebih aman
            try:
                status = obs_client.get_status()
                if not status.get('connected', False):
                    print("❌ OBS belum terkoneksi. Status:", status)
                    return False
            except:
                print("⚠️ Tidak bisa cek status OBS, mencoba lanjut...")

            # Register event
            obs_client.client.register_event_callback(
                "InputVolumeMeters", self._handle_input_volume_meters
            )

            self.connected = True
            print("="*75)
            print("🎙️ AUDIO MONITOR - OPTIMASI SIARAN BOLA v3 AKTIF")
            print(f"Threshold     : {self.threshold_db} dBFS")
            print(f"Persistence   : {self.persistence_duration} detik")
            print(f"Cooldown      : {self.cooldown_seconds} detik")
            print("="*75)
            return True

        except Exception as e:
            print(f"❌ Gagal start Audio Monitor: {e}")
            return False

    async def stop(self):
        self.connected = False
        print("🛑 Audio Monitor dihentikan")

audio_monitor = AudioMonitor()