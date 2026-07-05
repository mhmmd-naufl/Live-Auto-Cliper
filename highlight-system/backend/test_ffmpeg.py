import subprocess
import os

# Ganti ini dengan path file MKV hasil replay buffer kamu
INPUT_FILE = r"D:\Kuliah\TA\Pre-TA\Project\file-hasil\Replay 2026-06-12 16-17-13.mkv"  # sesuaikan nama filenya
OUTPUT_DIR = r"D:\Kuliah\TA\Pre-TA\Project\file-highlight"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def test_cut(offset: float, duration: float = 30.0, label: str = ""):
    output_file = os.path.join(OUTPUT_DIR, f"test_offset_{label}.mp4")
    
    cmd = [
        "ffmpeg",
        "-ss", str(offset),
        "-i", INPUT_FILE,
        "-t", str(duration),
        "-c", "copy",
        "-avoid_negative_ts", "make_zero",
        "-y",
        output_file
    ]
    
    print(f"\n🎬 Test offset={offset}s, duration={duration}s")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        size = os.path.getsize(output_file) / 1024 / 1024
        print(f"✅ Berhasil → {output_file} ({size:.1f} MB)")
    else:
        print(f"❌ Gagal:\n{result.stderr[-300:]}")

# Test beberapa nilai offset
test_cut(offset=0,  label="0s")    # dari awal
test_cut(offset=10, label="10s")   # potong 10 detik dari awal
test_cut(offset=30, label="30s")   # potong 30 detik dari awal
test_cut(offset=50, label="50s")   # dekat akhir

print("\nSelesai — buka folder output dan cek durasi setiap file")