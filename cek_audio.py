import sounddevice as sd

def cetak_daftar_audio():
    print("=========================================================================")
    print("                  DAFTAR PERANGKAT AUDIO DI LAPTOP KAMU                  ")
    print("=========================================================================")
    print("Index | Nama Perangkat | Host API | (Max Input Ch, Max Output Ch)")
    print("-------------------------------------------------------------------------")
    
    # sd.query_devices() mengembalikan list/dictionary seluruh device audio
    devices = sd.query_devices()
    
    for index, device in enumerate(devices):
        # Ambil informasi penting dari setiap device
        nama = device['name']
        host_api = sd.query_hostapis(device['hostapi'])['name']
        input_ch = device['max_input_channels']
        output_ch = device['max_output_channels']
        
        # Beri tanda khusus jika device tersebut diatur sebagai default oleh Windows
        tanda = "⭐️" if index == sd.default.device[0] or index == sd.default.device[1] else "  "
        
        print(f"{tanda} {index:<2} | {nama[:40]:<40} | {host_api:<12} | ({input_ch} in, {output_ch} out)")

    print("=========================================================================")
    print("💡 Catatan untuk Proyek TA kamu:")
    print("   - Gunakan Index yang memiliki nilai 'in' > 0 (misal: Stereo Mix atau Microphone).")
    print("   - JANGAN gunakan Index yang memiliki nilai '0 in', karena itu murni Speaker (Output).")

if __name__ == "__main__":
    cetak_daftar_audio()