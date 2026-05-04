import subprocess
import os
import glob
import time
from datetime import datetime
from config import REPLAY_BUFFER_PATH, OUTPUT_PATH, REPLAY_BUFFER_DURATION, POST_ROLL
from services.offset_calculator import calculate_offset

def get_latest_replay_file() -> str | None:
    """Ambil file .mkv terbaru dari folder Replay Buffer OBS."""
    pattern = os.path.join(REPLAY_BUFFER_PATH, "*.mkv")
    files = glob.glob(pattern)
    if not files:
        return None
    return max(files, key=os.path.getmtime)

def run_ffmpeg_cut(t_start: float, t_save: float) -> dict:
    try:
        # Tunggu OBS selesai nulis file
        time.sleep(2)

        input_file = get_latest_replay_file()
        if not input_file:
            return {
                "success": False,
                "filename": "",
                "duration": 0.0,
                "error_message": f"No .mkv file found in {REPLAY_BUFFER_PATH}"
            }

        # Hitung offset sesuai rumus proposal
        # Offset = Durasi_Replay_Buffer - (T_Save - T_Start)
        offset = calculate_offset(t_start, t_save)
        print(f"📐 Offset: {offset}s | T_Start={t_start:.2f} | T_Save={t_save:.2f}")

        # Nama file output
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"highlight_{timestamp_str}.mp4"
        output_file = os.path.join(OUTPUT_PATH, output_filename)

        os.makedirs(OUTPUT_PATH, exist_ok=True)

        # FFmpeg stream copy — mulai dari offset, durasi POST_ROLL detik
        cmd = [
            "ffmpeg",
            "-ss", str(offset),
            "-i", input_file,
            "-t", str(POST_ROLL),
            "-c", "copy",
            "-avoid_negative_ts", "make_zero",
            "-y",
            output_file
        ]

        print(f"🎬 Running FFmpeg...")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            print(f"❌ FFmpeg error: {result.stderr[-300:]}")
            return {
                "success": False,
                "filename": output_filename,
                "duration": 0.0,
                "error_message": result.stderr[-300:]
            }

        print(f"✅ Highlight saved: {output_filename} (offset: {offset}s, duration: {POST_ROLL}s)")

        return {
            "success": True,
            "filename": output_filename,
            "duration": POST_ROLL,
            "error_message": ""
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "filename": "",
            "duration": 0.0,
            "error_message": "FFmpeg timeout"
        }
    except Exception as e:
        return {
            "success": False,
            "filename": "",
            "duration": 0.0,
            "error_message": str(e)
        }