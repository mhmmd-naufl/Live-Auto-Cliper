import subprocess
import os
import glob
import time
import json
from datetime import datetime
from config import REPLAY_BUFFER_PATH, OUTPUT_PATH, REPLAY_BUFFER_DURATION
from services.offset_calculator import calculate_cut_point


def get_latest_replay_file() -> str | None:
    """Ambil file replay buffer paling baru dari folder OBS."""
    pattern = os.path.join(REPLAY_BUFFER_PATH, "*.mkv")
    files = glob.glob(pattern)
    if not files:
        return None
    latest = max(files, key=os.path.getmtime)
    size_mb = os.path.getsize(latest) / 1024 / 1024
    print(f"📁 Latest replay file: {latest} (size: {size_mb:.1f} MB)")
    return latest


def get_video_duration(video_path: str) -> float | None:
    """Cek durasi aktual file video pakai ffprobe."""
    try:
        cmd = [
            "ffprobe", "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return float(data.get("format", {}).get("duration", 0))
    except Exception as e:
        print(f"⚠️ ffprobe error: {e}")
    return None


def run_ffmpeg_cut(t_start: float, t_save: float) -> dict:
    try:
        # Tunggu OBS selesai menulis file
        print("⏳ Menunggu Replay Buffer selesai ditulis...")
        time.sleep(3.5)

        input_file = get_latest_replay_file()
        if not input_file:
            return {"success": False, "error_message": "No replay file found"}

        # Cek durasi aktual file buffer
        actual_buffer_duration = get_video_duration(input_file)
        if not actual_buffer_duration:
            print("⚠️ Tidak bisa cek durasi file, pakai REPLAY_BUFFER_DURATION dari config")
            actual_buffer_duration = REPLAY_BUFFER_DURATION

        print(f"📏 Durasi aktual file buffer: {actual_buffer_duration:.2f}s")

        # Hitung titik potong berdasarkan durasi aktual (bukan asumsi dari .env)
        cut_info = calculate_cut_point(t_start, t_save, actual_buffer_duration)
        cut_start = cut_info["cut_start"]
        offset = cut_info["offset"]

        print(f"📐 Posisi momen (offset): {offset}s | Titik potong: {cut_start}s "
              f"| T_Start={t_start:.2f} | T_Save={t_save:.2f}")

        # Siapkan output file
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"highlight_{timestamp_str}.mp4"
        output_file = os.path.join(OUTPUT_PATH, output_filename)
        os.makedirs(OUTPUT_PATH, exist_ok=True)

        # FFmpeg: potong dari cut_start sampai akhir file (tanpa -t)
        # Tidak pakai -t karena kita mau ambil sampai ujung file yang tersedia
        cmd = [
            "ffmpeg",
            "-ss", str(cut_start),
            "-i", input_file,
            "-c", "copy",
            "-avoid_negative_ts", "make_zero",
            "-y",
            output_file
        ]

        print(f"🎬 Running FFmpeg: {' '.join(cmd)}")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=90
        )

        if result.returncode != 0:
            print(f"❌ FFmpeg Error:\n{result.stderr[-500:]}")
            return {
                "success": False,
                "filename": output_filename,
                "error_message": result.stderr[-300:]
            }

        # Cek durasi hasil
        actual_duration = get_video_duration(output_file)
        print(f"✅ Highlight saved: {output_filename} "
              f"| Durasi: {actual_duration:.2f}s "
              f"| Momen ada di detik ~{cut_info['pre_roll']}s dari awal klip")

        return {
            "success": True,
            "filename": output_filename,
            "duration": actual_duration or 0,
            "offset": offset,
            "cut_start": cut_start,
            "error_message": ""
        }

    except Exception as e:
        print(f"❌ Exception in FFmpeg: {e}")
        return {"success": False, "error_message": str(e)}