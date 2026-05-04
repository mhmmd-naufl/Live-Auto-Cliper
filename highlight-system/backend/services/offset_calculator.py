from dotenv import load_dotenv
import os

load_dotenv()

REPLAY_BUFFER_DURATION = float(os.getenv("REPLAY_BUFFER_DURATION", "300"))

def calculate_offset(t_start: float, t_save: float, buffer_duration: float = REPLAY_BUFFER_DURATION) -> float:
    """
    Hitung offset titik awal pemotongan video.
    
    Offset = Durasi_Replay_Buffer - (T_Save - T_Start)
    
    Contoh:
    - Replay Buffer: 300 detik
    - T_Start: detik ke-250 (lonjakan audio terdeteksi)
    - T_Save: detik ke-252 (perintah simpan dikirim)
    - Offset = 300 - (252 - 250) = 298 detik
    - Artinya momen terjadi di detik ke-298 dari file video
    """
    elapsed = t_save - t_start
    offset = buffer_duration - elapsed

    # Pastikan offset tidak negatif
    offset = max(0.0, offset)

    # Pastikan offset tidak melebihi durasi buffer
    offset = min(offset, buffer_duration)

    return round(offset, 2)