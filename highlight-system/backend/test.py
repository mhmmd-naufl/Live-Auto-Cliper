import sounddevice as sd
import numpy as np

def callback(indata, frames, time, status):
    rms = np.sqrt(np.mean(indata**2))
    print(f"RMS: {rms:.3f}")

with sd.InputStream(device=15, channels=2, samplerate=44100, callback=callback):
    print("Merekam 5 detik... putar audio sekarang")
    sd.sleep(5000)