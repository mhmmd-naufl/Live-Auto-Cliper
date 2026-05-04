import sounddevice as sd
import numpy as np
import time

# Cek sample rate yang benar dulu
device_info = sd.query_devices(12)
samplerate = int(device_info['default_samplerate'])
channels = min(device_info['max_input_channels'], 2)
print(f"Device: {device_info['name']}")
print(f"Sample rate: {samplerate}")
print(f"Channels: {channels}")

def cb(indata, frames, t, status):
    rms = np.sqrt(np.mean(indata**2))
    print(f'RMS: {rms:.6f}')

stream = sd.InputStream(device=12, channels=channels, samplerate=samplerate, callback=cb)
stream.start()
print("Monitoring 5 detik...")
time.sleep(5)
stream.stop()
print("Selesai")