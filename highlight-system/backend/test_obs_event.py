import obsws_python as obs
import time
import math

host = "127.0.0.1"
port = 4455
password = "Test123"

def convert_to_dbfs(magnitudo):
    if magnitudo <= 0.00001:
        return -100.0
    return 20 * math.log10(magnitudo)

def handle_event(data):
    # OBS WebSocket v5 mengirim nama event sebagai data.name
    # dan datanya di dalam data.attrs (tergantung versi library)
    # Mari kita cek apakah ini event volume meter
    if getattr(data, "name", None) == "InputVolumeMeters" or type(data).__name__ == "InputVolumeMeters":
        # Mengambil data inputs, sesuaikan dengan struktur objek obsws_python
        inputs = getattr(data, "inputs", []) if hasattr(data, "inputs") else data.get_inputs()
        
        for input_data in inputs:
            # Di obsws_python, data event sering kali berbentuk dictionary atau objek dengan atribut
            if isinstance(input_data, dict):
                input_name = input_data.get("inputName")
                levels_mul = input_data.get("inputLevelsMul", [0.0])
            else:
                input_name = getattr(input_data, "inputName", "Unknown")
                levels_mul = getattr(input_data, "inputLevelsMul", [0.0])
            
            if levels_mul:
                magnitudo_rata_rata = sum(levels_mul) / len(levels_mul)
                dbfs = convert_to_dbfs(magnitudo_rata_rata)
                print(f"🎤 Input: {input_name} | Vol: {dbfs:.2f} dBFS")

print("Menghubungkan ReqClient...")
req_client = obs.ReqClient(host=host, port=port, password=password)

print("Menghubungkan EventClient...")
event_client = obs.EventClient(host=host, port=port, password=password)
event_client.callback.register(handle_event)

print("\n--- Mengaktifkan fitur InputVolumeMeters ---")
# MENGGUNAKAN .send() UNTUK OBS WEBSOCKET v5
# Perintah resminya adalah 'ToggleInputVolumeMeters'
req_client.send(obs.requests.ToggleInputVolumeMeters(request_data={"data": True}))

print("Mendengarkan data audio selama 10 detik...\n")
time.sleep(10)

print("\nMematikan fitur InputVolumeMeters dan memutuskan koneksi...")
# Matikan kembali fitur saat selesai
req_client.send(obs.requests.ToggleInputVolumeMeters(request_data={"data": False}))

event_client.disconnect()
req_client.disconnect()
print("Selesai!")