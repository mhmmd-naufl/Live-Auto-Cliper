import logging
logger = logging.getLogger(__name__)
import asyncio
import time
from sqlalchemy import select
from services.obs_client import obs_client
from services.ffmpeg_runner import run_ffmpeg_cut
from database import AsyncSessionLocal
from models import HighlightLog, Configuration
import config


async def save_log(trigger_value: float, result: dict) -> int | None:
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
            await session.refresh(log)
            logger.info(f"📝 Log disimpan: {log.filename} | status={log.status}")

            # Push log baru ke frontend via WebSocket
            try:
                from services.ws_manager import broadcast_log
                await broadcast_log({
                    "id": log.id,
                    "timestamp": log.timestamp,
                    "duration": log.duration,
                    "trigger_value": log.trigger_value,
                    "filename": log.filename,
                    "status": log.status,
                    "error_message": log.error_message,
                })
            except Exception as ws_err:
                logger.warning(f"⚠️ Gagal broadcast log: {ws_err}")

            return log.id
    except Exception as e:
        logger.warning(f"⚠️ Gagal simpan log: {e}")
        return None


class TriggerEngine:
    def __init__(self):
        self.is_processing = False
        self.last_trigger_dbfs = -60.0

    async def on_audio_trigger(self, t_start: float):
        if self.is_processing:
            logger.info("⏸️  Trigger diabaikan — proses sebelumnya masih berjalan")
            return

        self.is_processing = True

        try:
            t_save = time.time()
            logger.info(f"🎯 Trigger diterima | T_Start={t_start:.2f} | T_Save={t_save:.2f}")

            # Langkah 1: Cek Replay Buffer aktif
            rb_status = await obs_client.get_replay_buffer_status()
            if not rb_status.get("active", False):
                logger.warning("⚠️  Replay Buffer tidak aktif — trigger dibatalkan")
                await save_log(
                    trigger_value=self.last_trigger_dbfs,
                    result={"success": False, "error_message": "Replay Buffer tidak aktif"}
                )
                return

            # Langkah 2: Kirim SaveReplayBuffer ke OBS
            save_result = await obs_client.save_replay_buffer()
            if not save_result.get("success", False):
                logger.error(f"❌ Gagal menyimpan Replay Buffer: {save_result.get('message')}")
                await save_log(
                    trigger_value=self.last_trigger_dbfs,
                    result={"success": False, "error_message": save_result.get("message")}
                )
                return

            logger.info("💾 SaveReplayBuffer berhasil — mengambil path & menjalankan FFmpeg...")

            # --- TAMBAHAN: Ambil file_path terbaru dari Database ---
            target_path = config.OUTPUT_PATH  # fallback jika DB kosong
            try:
                async with AsyncSessionLocal() as session:
                    res = await session.execute(select(Configuration).order_by(Configuration.id.desc()))
                    latest_config = res.scalar_one_or_none()
                    if latest_config and latest_config.file_path:
                        target_path = latest_config.file_path
                        logger.info(f"🗄️ Path penyimpanan dari Database: {target_path}")
            except Exception as db_err:
                logger.warning(f"⚠️ Gagal mengambil path dari DB, pakai fallback: {db_err}")

            # Langkah 3: Jalankan FFmpeg di thread terpisah (kirim target_path sebagai argumen ke-3)
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                run_ffmpeg_cut,
                t_start,
                t_save,
                target_path
            )

            # Langkah 4: Simpan log
            await save_log(
                trigger_value=self.last_trigger_dbfs,
                result=result
            )

            if result.get("success"):
                logger.info(f"✅ Highlight selesai: {result.get('filename')} "
                      f"| Durasi: {result.get('duration')}s")
            else:
                logger.error(f"❌ FFmpeg gagal: {result.get('error_message')}")

        except Exception as e:
            logger.error(f"❌ Exception di TriggerEngine: {e}")
            await save_log(
                trigger_value=self.last_trigger_dbfs,
                result={"success": False, "error_message": str(e)}
            )

        finally:
            self.is_processing = False


trigger_engine = TriggerEngine()