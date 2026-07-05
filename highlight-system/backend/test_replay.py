import time
import obsws_python as obs

HOST = "127.0.0.1"
PORT = 4455
PASSWORD = "Test123"

client = obs.ReqClient(host=HOST, port=PORT, password=PASSWORD)

# Step 1: Cek status Replay Buffer
status = client.get_replay_buffer_status()
print(f"Replay Buffer aktif: {status.output_active}")

if not status.output_active:
    print("❌ Replay Buffer belum aktif — aktifkan dulu di OBS")
    client.disconnect()
    exit()

# Step 2: Tunggu 10 detik biar buffer terisi dulu
print("⏳ Menunggu 10 detik agar buffer terisi...")
time.sleep(10)

# Step 3: Simpan Replay Buffer
print("💾 Menyimpan Replay Buffer...")
client.save_replay_buffer()
print("✅ Perintah SaveReplayBuffer dikirim")

# Step 4: Tunggu OBS selesai nulis file
time.sleep(4)
print("✅ Selesai — cek folder Replay Buffer kamu")

client.disconnect()