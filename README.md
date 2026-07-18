# Cara Menjalankan Sistem Highlight Otomatis

## Prasyarat

Pastikan semua software berikut sudah terinstall sebelum menjalankan sistem:

- **Python 3.12+**
- **Node.js 18+**
- **OBS Studio 28+** dengan OBS-WebSocket aktif
- **FFmpeg** — bisa dipanggil dari terminal (`ffmpeg` dan `ffprobe`)

---

## Langkah 1 — Persiapan OBS Studio

1. Buka **OBS Studio**
2. Aktifkan OBS-WebSocket:
   - Klik menu **Tools → WebSocket Server Settings**
   - Centang **Enable WebSocket Server**
   - Set **Port**: `4455`
   - Set **Password** sesuai keinginan (catat passwordnya)
   - Klik **OK**
3. Aktifkan Replay Buffer:
   - Klik menu **Output → Replay Buffer** (atau di panel Controls klik **Start Replay Buffer**)
   - Pastikan durasi Replay Buffer di **Settings → Output → Replay Buffer** sesuai dengan nilai `REPLAY_BUFFER_DURATION` di file `.env`

---

## Langkah 2 — Konfigurasi File `.env`

Buka file `.env` di folder `highlight-system/backend/` dan sesuaikan nilainya:

```env
# Koneksi OBS WebSocket
OBS_HOST=127.0.0.1
OBS_PORT=4455
OBS_PASSWORD=passwordmu

# Audio — sesuaikan AUDIO_DEVICE_ID dengan Stereo Mix di perangkat kamu
AUDIO_DEVICE_ID=15
THRESHOLD_DB=-38.0
PERSISTENCE_DURATION=2.0
COOLDOWN_SECONDS=8

# Video
REPLAY_BUFFER_DURATION=60
PRE_ROLL=10
POST_ROLL=30
REPLAY_BUFFER_PATH=D:\path\ke\folder\replay-buffer
OUTPUT_PATH=D:\path\ke\folder\hasil-highlight
```

> **Cara cari AUDIO_DEVICE_ID yang benar:**
> Jalankan perintah berikut di terminal:
> ```
> python -c "import sounddevice as sd; print(sd.query_devices())"
> ```
> Cari baris yang bertuliskan **Stereo Mix**, catat nomor di depannya, masukkan ke `AUDIO_DEVICE_ID`.

---

## Langkah 3 — Menjalankan Backend

Buka terminal, masuk ke folder backend:

```bash
cd highlight-system/backend
```

Aktifkan virtual environment:

```bash
# Windows
venv\Scripts\activate
```

Jalankan server:

```bash
uvicorn main:app --reload
```

Tunggu hingga muncul:
```
✅ Database tersambung
INFO: Uvicorn running on http://127.0.0.1:8000
```

Backend siap digunakan. Dokumentasi API tersedia di `http://127.0.0.1:8000/docs`.

---

## Langkah 4 — Menjalankan Frontend

Buka terminal **baru** (jangan tutup terminal backend), masuk ke folder frontend:

```bash
cd highlight-system/frontend
```

Jalankan:

```bash
npm run dev
```

Tunggu hingga muncul:
```
Local: http://localhost:5173/
```

Buka browser dan akses `http://localhost:5173`.

---

## Langkah 5 — Menggunakan Dashboard

### Koneksi ke OBS

1. Di panel **OBS — WEBSOCKET** (kiri bawah), isi:
   - **Host / IP Address**: `127.0.0.1`
   - **Port**: `4455`
   - **Password**: sesuai yang diset di OBS
2. Klik tombol **Connect**
3. Tunggu hingga status berubah menjadi **● Terhubung ke OBS Studio**

### Konfigurasi Sistem

Di panel **Action Center** (kanan bawah), atur:

| Parameter | Keterangan |
|---|---|
| **Threshold Sensitivity** | Batas minimum dBFS untuk deteksi. Geser slider atau ketik langsung. Nilai kuning = aktif saat ini |
| **Durasi Delay (Persistence)** | Berapa lama suara harus bertahan di atas threshold sebelum trigger (detik) |
| **Durasi Pre-Roll** | Berapa detik sebelum momen highlight yang ikut masuk ke video output |
| **Folder Hasil** | Folder tujuan penyimpanan file highlight `.mp4` |

Klik **SAVE** untuk menyimpan dan menerapkan perubahan.

> **Catatan:** Persistence, pre-roll, dan folder hanya bisa diubah saat monitoring **berhenti**. Threshold bisa digeser kapan saja untuk kalibrasi real-time.

### Mulai Monitoring

1. Pastikan OBS sudah terhubung (status Connected)
2. Pastikan **Replay Buffer** sudah aktif di OBS
3. Klik tombol **START** di header dashboard
4. Sistem mulai memantau audio secara real-time — grafik RMS akan bergerak mengikuti intensitas suara

### Saat Momen Terdeteksi

Sistem akan otomatis:
1. Mendeteksi lonjakan audio yang melewati threshold selama durasi persistence
2. Menunggu audio turun kembali di bawah threshold
3. Mengirim perintah **SaveReplayBuffer** ke OBS
4. Memotong video menggunakan FFmpeg
5. Menyimpan file `.mp4` ke folder hasil
6. Mencatat log di panel **Highlights Log**

### Menghentikan Monitoring

Klik tombol **STOP** di header dashboard.

### Memutus Koneksi

Klik tombol **Disconnect** di panel OBS — WEBSOCKET.

---

## Troubleshooting

| Masalah | Solusi |
|---|---|
| `Failed to start audio monitor` | Cek `AUDIO_DEVICE_ID` di `.env`, jalankan ulang query device |
| `Replay Buffer is not active` | Aktifkan Replay Buffer di OBS terlebih dahulu |
| `FFmpeg not found` | Pastikan FFmpeg sudah diinstall dan ada di PATH sistem |
| Grafik tidak bergerak | Periksa apakah Stereo Mix aktif dan volume sistem tidak mute |
| Video highlight terlalu pendek | Naikkan `REPLAY_BUFFER_DURATION` di `.env` dan samakan dengan setting OBS |
| Koneksi OBS gagal setelah laptop sleep | Restart backend, cek ulang `AUDIO_DEVICE_ID` karena bisa berubah setelah sleep |
