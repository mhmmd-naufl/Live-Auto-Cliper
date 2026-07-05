import obsws_python as obs
import time
import math

host = "127.0.0.1"
port = 4455
password = "Test123"

# --- 1. Definisi Rumus dBFS (Sesuai Slide TA Anda) ---
def convert_to_dbfs(magnitudo):
    if magnitudo <= 0.00001:
        return -100.0  
    return 20 * math.log10(magnitudo)

# --- 2. Fungsi Pemrosesan Data Audio ---
def handle_audio_event(data):
    if getattr(data, "name", None) == "InputVolumeMeters":
        inputs = data.attrs.get("inputs", [])
        
        for input_data in inputs:
            input_name = input_data.get("inputName")
            levels_mul = input_data.get("inputLevelsMul", [0.0])
            
            if levels_mul:
                magnitudo_rata_rata = sum(levels_mul) / len(levels_mul)
                
                # Kita filter agar hanya menampilkan input yang bersuara (seperti Desktop Audio Anda)
                if magnitudo_rata_rata > 0.00001:
                    dbfs = convert_to_dbfs(magnitudo_rata_rata)
                    print(f"🎤 [AUDIO TA] Input: {input_name} | Magnitudo: {magnitudo_rata_rata:.4f} | Vol: {dbfs:.2f} dBFS")

# --- 3. Koneksi ---
print("Menghubungkan ReqClient...")
req_client = obs.ReqClient(host=host, port=port, password=password)

print("Menghubungkan EventClient...")
event_client = obs.EventClient(host=host, port=port, password=password)
event_client.callback.register(handle_audio_event)

# --- 4. Mengaktifkan Meteran Audio Menggunakan Perintah Resmi OBS v5 ---
print("\n--- Mengaktifkan Pemantauan Audio di OBS v5 ---")

# Sesuai dengan screenshot OBS Anda, perangkat aktifnya bernama 'Desktop Audio'
target_audio = "Desktop Audio"

try:
    # SetInputVolumeMeterProperties adalah perintah resmi OBS WebSocket v5 untuk mengatur interval meteran
    # Mengatur rentang interval (windowTime) akan memaksa OBS menyemburkan event 'InputVolumeMeters'
    req_client.send("SetInputVolumeMeterProperties", {
        "inputName": target_audio,
        "monitorConfig": {
            "enabled": True,
            "windowTime": 100  # Perbarui data setiap 100 milidetik
        }
    })
    print(f"✅ Berhasil mengaktifkan meteran audio untuk {target_audio}!")
except Exception as e:
    print(f"❌ Gagal mengaktifkan: {e}")

print("\nMendengarkan data selama 15 detik... (Pastikan YouTube tetap bersuara di OBS)\n")
time.sleep(15)

# --- 5. Clean up ---
print("\n--- Mematikan Pemantauan Audio ---")
try:
    req_client.send("SetInputVolumeMeterProperties", {
        "inputName": target_audio,
        "monitorConfig": {
            "enabled": False
        }
    })
except:
    pass

event_client.disconnect()
req_client.disconnect()
print("Selesai!")