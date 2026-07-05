import time
import math

# ============================================================
# CONFIG (sesuaikan dengan .env kamu)
# ============================================================
THRESHOLD_DB = -38.0
PERSISTENCE_DURATION = 1.0
REPLAY_BUFFER_DURATION = 60.0
PRE_ROLL=10

# ============================================================
# 1. TEST: RMS → dBFS Conversion
# ============================================================
print("=" * 50)
print("TEST 1: RMS → dBFS Conversion")
print("=" * 50)

def magnitude_to_dbfs(magnitude: float) -> float:
    if magnitude <= 0:
        return -60.0
    return max(-60.0, 20 * math.log10(magnitude))

test_values = [0.0, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0]
for v in test_values:
    dbfs = magnitude_to_dbfs(v)
    status = "✅ ABOVE threshold" if dbfs >= THRESHOLD_DB else "❌ below threshold"
    print(f"  RMS={v:.3f} → {dbfs:.1f} dBFS | {status}")

# ============================================================
# 2. TEST: Time-Persistence Thresholding (simulasi)
# ============================================================
print("\n" + "=" * 50)
print("TEST 2: Time-Persistence Thresholding")
print("=" * 50)

# Simulasi urutan nilai dBFS yang masuk ke sistem
# Format: (dbfs, detik_relatif)
audio_sequence = [
    (-45.0, 0.0),   # hening
    (-45.0, 0.1),
    (-30.0, 0.2),   # mulai keras
    (-28.0, 0.3),
    (-25.0, 0.4),
    (-22.0, 0.5),
    (-20.0, 0.6),
    (-19.0, 0.7),
    (-18.0, 0.8),
    (-20.0, 0.9),
    (-22.0, 1.0),
    (-21.0, 1.1),   # bertahan > 1 detik → harusnya trigger
    (-21.0, 1.2),
    (-45.0, 1.3),   # turun lagi
    (-45.0, 1.4),
]

t_start = None
triggered = False
base_time = time.time()

print(f"Threshold: {THRESHOLD_DB} dBFS | Persistence: {PERSISTENCE_DURATION}s")
print()

for dbfs, rel_time in audio_sequence:
    now = base_time + rel_time

    if dbfs >= THRESHOLD_DB:
        if t_start is None:
            t_start = now
            print(f"  t={rel_time:.1f}s | dBFS={dbfs:.1f} | 🔊 T_Start dicatat = {t_start:.3f}")

        elapsed = now - t_start
        if elapsed >= PERSISTENCE_DURATION and not triggered:
            triggered = True
            print(f"  t={rel_time:.1f}s | dBFS={dbfs:.1f} | ✅ TRIGGER VALID! elapsed={elapsed:.2f}s")
        else:
            print(f"  t={rel_time:.1f}s | dBFS={dbfs:.1f} | ⏳ elapsed={elapsed:.2f}s (menunggu {PERSISTENCE_DURATION}s)")
    else:
        if t_start is not None and not triggered:
            print(f"  t={rel_time:.1f}s | dBFS={dbfs:.1f} | 🔄 RESET (hanya {now - t_start:.2f}s)")
            t_start = None
        else:
            print(f"  t={rel_time:.1f}s | dBFS={dbfs:.1f} | 😴 hening")

# ============================================================
# 3. TEST: Unix Timestamp & Offset Calculation
# ============================================================
print("\n" + "=" * 50)
print("TEST 3: Unix Timestamp & Offset Calculation")
print("=" * 50)

def calculate_offset(t_start, t_save, buffer_duration, pre_roll=10.0):
    elapsed = t_save - t_start
    offset = buffer_duration - elapsed - pre_roll
    offset = max(0.0, offset)
    return round(offset, 2)

buffer = 60.0
pre_roll = 10.0

scenarios = [
    (1,  "Persistence 1s (cepat)"),
    (2,  "Persistence 2s"),
    (5,  "Persistence 5s"),
    (10, "Persistence 10s (lama)"),
]

print(f"Buffer={buffer}s | Pre-roll={pre_roll}s\n")
for elapsed, desc in scenarios:
    offset = calculate_offset(0, elapsed, buffer, pre_roll)
    output_duration = buffer - offset
    print(f"  {desc}:")
    print(f"    offset={offset}s → FFmpeg: -ss {offset} -t 30")
    print(f"    Video mulai dari detik ke-{offset}, sisa buffer = {output_duration}s")
    print()