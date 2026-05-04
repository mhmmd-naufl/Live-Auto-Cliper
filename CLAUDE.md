# CLAUDE.md — Project Brief: Sistem Pemotongan Highlight Siaran Langsung

## Identitas Project

- **Judul**: Sistem Pemotongan Highlight Siaran Langsung Dengan Metode Fast Forward Moving Picture Experts Group Stream Copy Dan Ambang Batas Energi Audio
- **Mahasiswa**: Muhammad Naufal Aulia (NIM. 362258302068)
- **Institusi**: Politeknik Negeri Banyuwangi — Prodi Sarjana Terapan Teknologi Rekayasa Perangkat Lunak
- **Mitra Industri**: CV. Alzen Metro Data, Banyuwangi
- **Status**: Tahap awal implementasi (proposal sudah disetujui, Maret 2026)

---

## Ringkasan Sistem

Sistem web yang mengotomasi pembuatan video highlight dari siaran langsung olahraga. Cara kerjanya:

1. Terhubung ke OBS Studio via OBS-WebSocket
2. Memantau energi audio secara real-time menggunakan metode RMS → dikonversi ke dBFS
3. Jika audio melampaui threshold DAN bertahan minimal N detik (Time-Persistence Thresholding) → trigger valid
4. Mengirim perintah `SaveReplayBuffer` ke OBS Studio
5. Memotong video hasil Replay Buffer menggunakan FFmpeg Stream Copy (tanpa re-encoding)
6. Menyimpan file highlight ke direktori tujuan + update log

---

## Tech Stack

### Backend
- **Bahasa**: Python
- **Framework**: FastAPI (async, high-performance)
- **WebSocket Client**: `obsws-python` atau library OBS-WebSocket kompatibel
- **Audio Processing**: Kalkulasi RMS → dBFS (formula: `20 * log10(magnitude)`)
- **Video Processing**: FFmpeg CLI via `subprocess` (stream copy, `-c copy`)
- **Database**: SQLite (via SQLAlchemy atau aiosqlite)

### Frontend
- **Framework**: React.js (Vite atau Create React App)
- **Real-time**: WebSocket ke backend FastAPI
- **Visualisasi**: Grafik audio dBFS real-time (bar chart)
- **Styling**: Tailwind CSS (atau CSS biasa)

### Tools & Integrasi Eksternal
- **OBS Studio** (versi 28+) — sumber audio & eksekutor Replay Buffer
- **OBS-WebSocket** — protokol komunikasi dua arah dengan OBS
- **FFmpeg** — pemotongan video dengan stream copy

---

## Arsitektur Sistem (Gambaran Umum)

```
OBS Studio
  │
  │ (OBS-WebSocket: audio RMS data)
  ▼
FastAPI Backend
  ├── Audio Monitor (RMS → dBFS → threshold check)
  ├── Time-Persistence Filter (min. duration validation)
  ├── Trigger Engine (SaveReplayBuffer command ke OBS)
  ├── Offset Calculator (Unix Timestamp based)
  ├── FFmpeg Runner (stream copy, -ss offset)
  ├── REST API (konfigurasi, log)
  └── WebSocket Server (push data ke frontend)
        │
        ▼
   React Dashboard
      ├── Grafik audio real-time (dBFS)
      ├── Panel konfigurasi (threshold, durasi, folder)
      ├── Status koneksi OBS
      └── Highlights Log (timestamp, filename, status)
```

---

## Database Schema

### Tabel: `configurations`
| Kolom | Tipe | Keterangan |
|---|---|---|
| id | Integer (PK) | ID unik konfigurasi |
| obs_host | VARCHAR(255) | IP/hostname OBS |
| obs_port | Integer | Port WebSocket OBS |
| obs_password | VARCHAR(255) | Password OBS WebSocket |
| threshold_db | Float | Ambang batas dBFS (misal: -20.0) |
| file_path | Text | Direktori penyimpanan highlight |
| updated_at | Timestamp | Waktu update terakhir |
| persistence_duration | Float | Durasi minimum lonjakan audio (detik) |

### Tabel: `highlight_logs`
| Kolom | Tipe | Keterangan |
|---|---|---|
| id | Integer (PK) | ID unik log |
| config_id | Integer (FK) | Relasi ke configurations |
| timestamp | Timestamp | Waktu deteksi momen |
| duration | Float | Durasi video hasil (detik) |
| trigger_value | Float | Nilai dBFS saat trigger |
| filename | VARCHAR(255) | Nama file output |
| status | VARCHAR(50) | SUCCESS / FAILED |
| error_message | Text | Pesan error jika gagal |

**Relasi**: `configurations` 1 → N `highlight_logs`

---

## Algoritma Inti

### 1. RMS → dBFS Conversion
```python
import math
def magnitude_to_dbfs(magnitude: float) -> float:
    if magnitude <= 0:
        return -60.0  # floor value
    return 20 * math.log10(magnitude)
```

### 2. Time-Persistence Thresholding
- Catat `T_Start` (Unix timestamp) saat dBFS pertama kali melampaui threshold
- Jika dBFS turun di bawah threshold sebelum durasi minimum → reset timer
- Jika dBFS bertahan ≥ `persistence_duration` detik → trigger valid

### 3. Offset Calculation
```
Offset = Durasi_Replay_Buffer - (T_Save - T_Start)
```
- `T_Save`: timestamp saat `SaveReplayBuffer` dikirim
- `T_Start`: timestamp saat lonjakan audio pertama terdeteksi
- Offset digunakan sebagai parameter `-ss` pada FFmpeg

### 4. FFmpeg Stream Copy
```bash
ffmpeg -ss {offset} -i {input_file} -c copy {output_file}
```

---

## Struktur Folder Rencana

```
project-root/
├── backend/
│   ├── main.py                  # Entry point FastAPI
│   ├── config.py                # Settings & env vars
│   ├── database.py              # SQLAlchemy setup
│   ├── models.py                # DB models (configurations, highlight_logs)
│   ├── routers/
│   │   ├── config.py            # Endpoint konfigurasi sistem
│   │   └── logs.py              # Endpoint highlight logs
│   ├── services/
│   │   ├── obs_client.py        # Koneksi & komunikasi OBS-WebSocket
│   │   ├── audio_monitor.py     # RMS listener, dBFS converter
│   │   ├── trigger_engine.py    # Time-persistence thresholding logic
│   │   ├── offset_calculator.py # Algoritma perhitungan offset
│   │   └── ffmpeg_runner.py     # FFmpeg stream copy executor
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── AudioChart.jsx       # Grafik dBFS real-time
│   │   │   ├── ConnectionPanel.jsx  # Form koneksi OBS WebSocket
│   │   │   ├── ActionCenter.jsx     # Konfigurasi threshold & folder
│   │   │   └── HighlightsLog.jsx    # Tabel log aktivitas
│   │   └── hooks/
│   │       └── useWebSocket.js      # Custom hook WebSocket ke backend
│   └── package.json
│
└── CLAUDE.md                    # File ini
```

---

## Iterasi Pengembangan (Iterative Incremental)

| Iterasi | Fokus | Fitur Utama |
|---|---|---|
| **Iterasi 1** | Integrasi & Konektivitas | Koneksi OBS-WebSocket, receive audio data, status dashboard |
| **Iterasi 2** | Analisis Audio & Trigger | RMS → dBFS, Time-Persistence Thresholding, SaveReplayBuffer |
| **Iterasi 3** | Manajemen Parameter & Output | Konfigurasi via dashboard, offset calculation, FFmpeg runner |
| **Iterasi 4** | Dashboard & Laporan | Grafik real-time, highlights log, UI final |

---

---

## Pengujian

- **Metode**: Black Box Testing
- **Evaluasi**: Confusion Matrix (TP, FP, TN, FN)
- **Metrik**: Accuracy, Precision, Recall, F1-Score
- **Ground truth**: Catatan manual observer terhadap sampel video livestreaming

### Test Case Utama:
- Koneksi OBS-WebSocket (berhasil, gagal OBS mati, password salah, auto-reconnect)
- Pemantauan sinyal audio (hening, normal, keras melebihi threshold)
- Eksekusi pemotongan video (Replay Buffer aktif/tidak, format file, stream copy)
- Konfigurasi via dashboard (threshold baru, durasi buffer, input tidak valid)

---

## Konvensi Coding

### Python (Backend)
- Style: **PEP 8**
- Async: gunakan `async/await` untuk semua I/O (WebSocket, DB, subprocess)
- Naming: `snake_case` untuk variabel dan fungsi
- Type hints: wajib pada semua fungsi

### JavaScript/React (Frontend)
- Style: **ES6+**
- Komponen: functional component + hooks
- Naming: `camelCase` untuk variabel, `PascalCase` untuk komponen

---

## Status Revisi Proposal (Belum Selesai)

Proposal masih dalam proses revisi. Berikut daftar poin revisi dari dosen yang perlu diselesaikan secara bertahap. Claude harus aware terhadap poin-poin ini saat membantu revisi dokumen.

### Konten & Substansi
- [ ] Perjelas permasalahan yang dialami mitra (CV. Alzen Metro Data) — lebih spesifik dan terstruktur
- [ ] Cek abstrak — eliminasi kalimat yang terindikasi bersumber dari AI
- [ ] Perjelas tujuan TA — lebih konkret dan terukur
- [ ] Tambahkan gambaran sistem yang berjalan (proses manual saat ini) vs sistem yang diusulkan
- [ ] Gambaran umum sistem yang akan dibangun belum jelas — perjelas di Bab I atau Bab III

### Teknis Penulisan
- [ ] Hapus kata ambigu: *atas, bawah, sebelumnya, setelahnya, tersebut* — ganti dengan rujukan eksplisit ke nomor gambar/tabel/bab
- [ ] Cek semua kata asing — pastikan ditulis *italic* (contoh: *livestreaming*, *clipping*, *threshold*, *replay buffer*, dll.)
- [ ] Hapus kata ganti orang "penulis" — ganti dengan kalimat pasif atau subjek sistem
- [ ] Rapikan penulisan semua tabel (format, alignment, konsistensi kolom)

### Struktur & Kelengkapan
- [ ] Rumus 2.1–2.6 & 3.1 — tambahkan contoh implementasi ke konteks topik permasalahan nyata (bukan hanya rumus abstrak)
- [ ] Setiap gambar & tabel harus memiliki kalimat penjelasan yang merujuk ke nomor gambar/tabel secara eksplisit
- [ ] Cek relevansi database (tabel `configurations` & `highlight_logs`) dengan use case yang ada

---

## Catatan Penting

- Sistem ini **real-time sensitive** — latency antara deteksi dan trigger harus seminimal mungkin
- FFmpeg **harus stream copy** (`-c copy`), bukan re-encode — ini constraint utama untuk performa
- Koneksi OBS-WebSocket harus punya **mekanisme auto-reconnect**
- Nilai dBFS dari OBS dikirim sebagai **magnitude linear (0–1)**, bukan dBFS langsung — perlu konversi
- File Replay Buffer OBS ada di folder sementara OBS, harus segera dipindahkan setelah `SaveReplayBuffer`
- Deployment lokal via **loopback (127.0.0.1)** — tidak perlu HTTPS atau autentikasi kompleks untuk MVP
- Proposal masih **belum final** (sedang revisi) — beberapa detail teknis mungkin berubah
