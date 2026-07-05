import subprocess
import os

OUTPUT = r"D:\Kuliah\TA\Pre-TA\Project\test_video_long.mp4"

# Memastikan folder direktori tujuan sudah ada
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

# Skema Pengujian Naufal (detik):
# 0-30   : hitam, hening
# 30-31  : kuning, suara sesaat (tidak boleh trigger)
# 31-60  : hitam, hening
# 60-65  : hijau, suara keras > 1 detik (TRIGGER 1)
# 65-120 : hitam, hening
# 120-121: kuning, suara sesaat (tidak boleh trigger)
# 121-150: hitam, hening
# 150-156: hijau, suara keras > 1 detik (TRIGGER 2)
# 156-300: hitam, hening

# Taktik yang benar: Satukan pembuatan warna dan audio generator di dalam -filter_complex
filter_complex_cmd = (
    # --- GENERATOR VIDEO ---
    "color=c=black:size=1280x720:rate=30:duration=30[v1];"
    "color=c=yellow:size=1280x720:rate=30:duration=1[v2];"
    "color=c=black:size=1280x720:rate=30:duration=29[v3];"
    "color=c=green:size=1280x720:rate=30:duration=5[v4];"
    "color=c=black:size=1280x720:rate=30:duration=55[v5];"
    "color=c=yellow:size=1280x720:rate=30:duration=1[v6];"
    "color=c=black:size=1280x720:rate=30:duration=29[v7];"
    "color=c=green:size=1280x720:rate=30:duration=6[v8];"
    "color=c=black:size=1280x720:rate=30:duration=144[v9];"
    
    # --- GENERATOR AUDIO (Hening disimulasikan dengan volume=0) ---
    "sine=frequency=440:duration=30,volume=0[a1];"
    "sine=frequency=1000:duration=1,volume=1[a2];"
    "sine=frequency=440:duration=29,volume=0[a3];"
    "sine=frequency=1000:duration=5,volume=1[a4];"
    "sine=frequency=440:duration=55,volume=0[a5];"
    "sine=frequency=1000:duration=1,volume=1[a6];"
    "sine=frequency=440:duration=29,volume=0[a7];"
    "sine=frequency=1000:duration=6,volume=1[a8];"
    "sine=frequency=440:duration=144,volume=0[a9];"
    
    # --- PROSES CONCATENATE (PENGGABUNGAN) ---
    "[v1][v2][v3][v4][v5][v6][v7][v8][v9]concat=n=9:v=1:a=0[v];"
    "[a1][a2][a3][a4][a5][a6][a7][a8][a9]concat=n=9:v=0:a=1[a]"
)

cmd = [
    "ffmpeg", "-y",
    "-filter_complex", filter_complex_cmd,
    "-map", "[v]",
    "-map", "[a]",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p", # Memastikan format pixel standar agar bisa diputar di semua media player Windows
    "-c:a", "aac",
    "-b:a", "192k",
    OUTPUT
]

print("🎬 Generating 5-minute test video based on your schema...")
print("⏳ Silakan tunggu beberapa detik, proses render sedang berjalan...")

# Menggunakan stdout=subprocess.PIPE dan stderr=subprocess.PIPE agar pembacaan log error lebih bersih
result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

if result.returncode == 0:
    print(f"\n✅ Done! File sukses dibuat di:\n👉 {OUTPUT}")
else:
    print(f"\n❌ Error Terjadi:\n{result.stderr}")