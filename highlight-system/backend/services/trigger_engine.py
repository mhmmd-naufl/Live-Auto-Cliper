import asyncio
import time
from services.obs_client import obs_client
from services.ffmpeg_runner import run_ffmpeg_cut
from database import AsyncSessionLocal
from models import HighlightLog


async def save_log(trigger_value: float, result: dict):
    """Simpan hasil trigger ke tabel highlight_logs."""
    try:
        async with AsyncSessionLocal() as session:
            log = HighlightLog(
                trigger_value=trigger_value,
                duration=result.get("duration") or 0.0,
                filename=result.get("filename") or "",
                status="SUCCESS" if result.get("success") else "FAILED",
                error_message=result.get("error_message") or "",
            )
            session.add(log)
            await session.commit()
            print(f"📝 Log disimpan: {log.filename} | status={log.status}")
    except Exception as e:
        print(f"⚠️ Gagal simpan log: {e}")


class TriggerEngine:
    def __init__(self):
        self.is_processing = False
        self.last_trigger_dbfs = -60.0

    async def on_audio_trigger(self, t_start: float):
        """
        Dipanggil AudioMonitor saat trigger valid dan audio
        sudah turun kembali di bawah threshold (T_End).
        """
        if self.is_processing:
            print("⏸️  Trigger diabaikan — proses sebelumnya masih berjalan")
            return

        self.is_processing = True

        try:
            t_save = time.time()
            print(f"🎯 Trigger diterima | T_Start={t_start:.2f} | T_Save={t_save:.2f}")

            # Langkah 1: Cek Replay Buffer aktif
            rb_status = await obs_client.get_replay_buffer_status()
            if not rb_status.get("active", False):
                print("⚠️  Replay Buffer tidak aktif — trigger dibatalkan")
                await save_log(
                    trigger_value=self.last_trigger_dbfs,
                    result={"success": False, "error_message": "Replay Buffer tidak aktif"}
                )
                return

            # Langkah 2: Kirim SaveReplayBuffer ke OBS
            save_result = await obs_client.save_replay_buffer()
            if not save_result.get("success", False):
                print(f"❌ Gagal menyimpan Replay Buffer: {save_result.get('message')}")
                await save_log(
                    trigger_value=self.last_trigger_dbfs,
                    result={"success": False, "error_message": save_result.get("message")}
                )
                return

            print("💾 SaveReplayBuffer berhasil — menjalankan FFmpeg...")

            # Langkah 3: Jalankan FFmpeg di thread terpisah
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                run_ffmpeg_cut,
                t_start,
                t_save
            )

            # Langkah 4: Simpan log
            await save_log(
                trigger_value=self.last_trigger_dbfs,
                result=result
            )

            if result.get("success"):
                print(f"✅ Highlight selesai: {result.get('filename')} "
                      f"| Durasi: {result.get('duration')}s")
            else:
                print(f"❌ FFmpeg gagal: {result.get('error_message')}")

        except Exception as e:
            print(f"❌ Exception di TriggerEngine: {e}")
            await save_log(
                trigger_value=self.last_trigger_dbfs,
                result={"success": False, "error_message": str(e)}
            )

        finally:
            self.is_processing = False


trigger_engine = TriggerEngine()