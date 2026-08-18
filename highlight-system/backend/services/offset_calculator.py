from dotenv import load_dotenv
import os

load_dotenv()

REPLAY_BUFFER_DURATION = float(os.getenv("REPLAY_BUFFER_DURATION", "60"))
PRE_ROLL = float(os.getenv("PRE_ROLL", "5"))  # detik sebelum momen yang ikut dikliping


def calculate_offset(t_start: float, t_save: float, buffer_duration: float = REPLAY_BUFFER_DURATION) -> float:
    elapsed = t_save - t_start
    offset = buffer_duration - elapsed

    offset = max(0.0, offset)
    offset = min(offset, buffer_duration)

    return round(offset, 2)


def calculate_cut_point(t_start: float, t_save: float, buffer_duration: float = REPLAY_BUFFER_DURATION) -> dict:
    offset = calculate_offset(t_start, t_save, buffer_duration)

    # Titik mulai potong = mundur PRE_ROLL detik dari posisi momen
    cut_start = max(0.0, offset - PRE_ROLL)

    return {
        "offset": offset,           # posisi momen penting di file (untuk referensi/log)
        "cut_start": round(cut_start, 2),  # titik mulai FFmpeg (-ss)
        "pre_roll": PRE_ROLL,
    }