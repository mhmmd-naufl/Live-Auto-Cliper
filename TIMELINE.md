# TIMELINE & TARGET — Tugas Akhir

## Sistem Pemotongan Highlight Siaran Langsung

**Muhammad Naufal Aulia — NIM. 362258302068**

---

## ⚠️ Situasi Saat Ini

| Item                   | Status           |
| ---------------------- | ---------------- |
| Bulan sekarang         | Mei 2026         |
| Estimasi sidang/semhas | Juni – Juli 2026 |
| Waktu tersisa          | ± 7–8 minggu     |
| Progress coding        | Belum ada        |
| Progress laporan TA    | Belum ada        |
| Hari aktif per minggu  | 5–6 hari         |

> **Kesimpulan:** Waktu sangat mepet. Tidak ada ruang untuk jeda panjang.
> Setiap minggu HARUS ada output nyata yang bisa ditunjukkan.

---

## 🎯 Strategi Utama

1. **Coding dan revisi proposal berjalan paralel** — jangan tunggu proposal selesai dulu baru coding. Revisi dikerjakan di celah waktu (pagi/malam), coding jadi fokus utama.
2. **Laporan TA dicicil mulai minggu ke-6** — Bab I dan II bisa ditulis sekarang karena isinya teoritis, tidak bergantung hasil coding.
3. **Minggu 1 adalah paling kritis** — kalau persiapan environment dan koordinasi mitra terlambat, semua jadwal berikutnya ikut mundur.
4. **Setiap akhir iterasi coding wajib evaluasi** sebelum lanjut ke iterasi berikutnya.

---

## 📅 Jadwal 8 Minggu

### Minggu 1 — Mei Minggu ke-2

**Tema: Administrasi + Persiapan Environment** 🔴 KRITIS

**Target output:** Semua tools terinstall dan terhubung, struktur folder project siap.

- [x] Install OBS Studio versi 28+
- [x] Aktifkan OBS-WebSocket di OBS (Tools → WebSocket Server Settings)
- [x] Test koneksi OBS-WebSocket secara manual (via browser atau Postman)
- [x] Aktifkan & test Replay Buffer OBS — coba simpan manual
- [x] Install FFmpeg & daftarkan ke environment variables sistem
- [x] Test FFmpeg stream copy manual di terminal: `ffmpeg -ss 5 -i input.mp4 -c copy output.mp4`
- [x] Install Python 3.10+, Node.js 18+, Git
- [x] Buat repository Git (GitHub/GitLab) untuk project
- [x] Setup Python virtual environment: `python -m venv venv`
- [x] Install dependency awal: `pip install fastapi uvicorn obsws-python aiosqlite sqlalchemy python-dotenv`
- [x] Init project React: `npm create vite@latest frontend -- --template react`
- [x] Buat struktur folder project sesuai CLAUDE.md
- [x] Buat file `.env` dan `.gitignore`
- [ ] Koordinasi mitra CV. Alzen Metro Data:
  - [ ] Konfirmasi format video (codec, resolusi, container)
  - [ ] Konfirmasi durasi Replay Buffer yang biasa dipakai
  - [ ] Minta sampel rekaman video siaran olahraga

---

### Minggu 2 — Mei Minggu ke-3

**Tema: Persiapan Data + Cicil Revisi Proposal** 🟡 PARALEL

**Target output:** Data uji siap dianotasi, revisi teknis penulisan proposal selesai.

- [ ] Amati nilai dBFS dari video sampel mitra — catat rentang normal vs momen penting
- [ ] Tentukan nilai threshold awal berdasarkan observasi (bukan asumsi)
- [ ] Buat template tabel anotasi ground truth (format: timestamp_start, timestamp_end, label)
- [ ] Mulai anotasi manual minimal 1 video sampel
- [ ] Pelajari dokumentasi OBS-WebSocket (obsproject.github.io/obs-websocket)
- [ ] Pahami format data `inputLevelsMul` yang dikirim OBS
- [ ] Coba library `obsws-python` — jalankan contoh sederhana
- [ ] **Revisi proposal (teknis penulisan):**
  - [ ] Hapus semua kata "penulis" → ganti kalimat pasif
  - [ ] Hapus kata ambigu: _tersebut, atas, bawah, sebelumnya, setelahnya_
  - [ ] Pastikan semua kata asing ditulis _italic_
  - [ ] Rapikan format semua tabel di proposal

---

### Minggu 3 — Mei Minggu ke-4

**Tema: Coding Iterasi 1 — Konektivitas Sistem** 🔴 KRITIS

**Target output:** Frontend dan backend bisa terhubung ke OBS Studio secara live.

- [ ] Buat koneksi OBS-WebSocket dari Python menggunakan `obsws-python`
- [ ] Implementasi auto-reconnect jika koneksi terputus
- [ ] Subscribe ke event audio dari OBS, print data mentah ke terminal
- [ ] Buat endpoint FastAPI:
  - [ ] `POST /connect` — inisiasi koneksi ke OBS
  - [ ] `POST /disconnect` — putus koneksi
  - [ ] `GET /status` — cek status koneksi
- [ ] Buat WebSocket endpoint FastAPI untuk push status real-time ke frontend
- [ ] Buat komponen React `ConnectionPanel` — form input IP, port, password OBS
- [ ] Tampilkan indikator status koneksi di dashboard (Connected / Disconnected)
- [ ] Test end-to-end: klik Connect di dashboard → backend → OBS terhubung
- [ ] ✅ **Evaluasi Iterasi 1 sebelum lanjut**
- [ ] **Revisi proposal (konten):**
  - [ ] Perjelas permasalahan mitra di Bab I — lebih spesifik dan terstruktur
  - [ ] Tambahkan gambaran sistem berjalan (manual) vs sistem diusulkan

---

### Minggu 4 — Juni Minggu ke-1

**Tema: Coding Iterasi 2 — Analisis Audio & Trigger** 🔴 KRITIS

**Target output:** Sistem bisa mendeteksi lonjakan audio dan memicu SaveReplayBuffer ke OBS.

- [ ] Implementasi konversi magnitude → dBFS: `20 * log10(magnitude)`
- [ ] Implementasi pembacaan RMS real-time dari stream OBS-WebSocket
- [ ] Implementasi Time-Persistence Thresholding:
  - [ ] Catat `T_Start` (Unix timestamp) saat dBFS pertama melampaui threshold
  - [ ] Reset timer jika dBFS turun sebelum durasi minimum terpenuhi
  - [ ] Trigger valid jika dBFS bertahan ≥ `persistence_duration` detik
- [ ] Implementasi pengiriman perintah `SaveReplayBuffer` ke OBS via WebSocket
- [ ] Implementasi mekanisme cooldown setelah trigger (hindari trigger beruntun)
- [ ] Push data dBFS real-time ke frontend via WebSocket
- [ ] Buat komponen React `AudioChart` — grafik bar dBFS real-time
- [ ] Tampilkan garis merah threshold horizontal pada grafik
- [ ] Test trigger nyata: suara keras ≥ 2 detik → OBS simpan Replay Buffer
- [ ] ✅ **Evaluasi Iterasi 2 sebelum lanjut**
- [ ] **Revisi proposal:**
  - [ ] Tambahkan contoh implementasi rumus 2.1 (RMS) dan 2.2 (dBFS) ke konteks nyata

---

### Minggu 5 — Juni Minggu ke-2

**Tema: Coding Iterasi 3 — Parameter & Output** 🔴 KRITIS

**Target output:** File video highlight tersimpan presisi di folder tujuan, log tercatat di database.

- [ ] Setup database SQLite dengan SQLAlchemy
- [ ] Buat model `configurations` dan `highlight_logs`
- [ ] Implementasi CRUD endpoint untuk konfigurasi:
  - [ ] `POST /config` — simpan konfigurasi
  - [ ] `GET /config` — ambil konfigurasi aktif
- [ ] Implementasi algoritma perhitungan offset:
      `Offset = Durasi_Replay_Buffer - (T_Save - T_Start)`
- [ ] Implementasi FFmpeg stream copy via subprocess Python:
      `ffmpeg -ss {offset} -i {input} -c copy {output}`
- [ ] Implementasi pemindahan file dari folder temp OBS ke direktori tujuan
- [ ] Implementasi pencatatan setiap kejadian ke tabel `highlight_logs`
- [ ] Buat komponen React `ActionCenter` — form threshold, durasi, folder path
- [ ] Test output: file MP4 tersimpan di direktori tujuan dengan durasi presisi
- [ ] Validasi kualitas video output identik dengan sumber (lossless)
- [ ] ✅ **Evaluasi Iterasi 3 sebelum lanjut**
- [ ] **Revisi proposal:**
  - [ ] Tambahkan contoh implementasi rumus 3.1 (offset) ke konteks nyata
  - [ ] Cek relevansi database dengan use case

---

### Minggu 6 — Juni Minggu ke-3

**Tema: Coding Iterasi 4 — Dashboard Final + Cicil Laporan** 🟡 PARALEL

**Target output:** Dashboard final berjalan, Bab I dan II laporan TA selesai draft pertama.

**Coding:**

- [ ] Buat endpoint `GET /logs` — ambil semua highlight logs
- [ ] Buat komponen React `HighlightsLog` — tabel riwayat aktivitas
- [ ] Tampilkan: timestamp, filename, trigger value, status, durasi di log
- [ ] Tambahkan session timer di header dashboard
- [ ] Tambahkan statistik ringkas: total highlight hari ini, rata-rata dBFS trigger
- [ ] Tambahkan toast notifikasi saat highlight berhasil disimpan
- [ ] Polish UI — loading states, error states, konsistensi tampilan
- [ ] Test end-to-end lengkap: OBS → deteksi → trigger → file tersimpan → log update
- [ ] ✅ **Evaluasi Iterasi 4 — sistem dinyatakan siap uji**

**Laporan TA (cicil):**

- [ ] Draft Bab I — Pendahuluan (latar belakang, rumusan masalah, tujuan, manfaat, batasan)
- [ ] Draft Bab II — Tinjauan Pustaka (dasar teori + penelitian terkait)

---

### Minggu 7 — Juni Minggu ke-4

**Tema: Pengujian Black Box + Confusion Matrix** 🔴 KRITIS

**Target output:** Semua test case selesai, nilai Accuracy/Precision/Recall/F1-Score terdokumentasi.

**Black Box Testing:**

- [ ] TC-CON-01: Koneksi berhasil dengan kredensial benar
- [ ] TC-CON-02: Koneksi gagal karena OBS tidak aktif
- [ ] TC-CON-03: Koneksi gagal karena password salah
- [ ] TC-CON-04: Auto-reconnect setelah OBS di-restart
- [ ] TC-AUD-01: Pembacaan dBFS saat kondisi hening
- [ ] TC-AUD-02: Pembacaan dBFS saat suara normal
- [ ] TC-AUD-03: Pembacaan dBFS saat suara keras melebihi threshold
- [ ] TC-AUD-04: Visualisasi grafik audio berjalan real-time
- [ ] TC-VID-01: Replay Buffer aktif saat trigger dikirim
- [ ] TC-VID-02: Replay Buffer tidak aktif saat trigger dikirim
- [ ] TC-VID-03: File tersimpan dalam format yang benar
- [ ] TC-VID-04: FFmpeg stream copy tanpa re-encoding
- [ ] TC-CONF-01: Perubahan threshold berhasil disimpan
- [ ] TC-CONF-02: Perubahan durasi Replay Buffer berhasil disimpan
- [ ] TC-CONF-03: Input nilai threshold tidak valid ditolak sistem

**Confusion Matrix:**

- [ ] Jalankan sistem pada semua video uji yang sudah dianotasi
- [ ] Catat hasil: TP, FP, TN, FN per video
- [ ] Hitung Accuracy: `(TP + TN) / (TP + TN + FP + FN)`
- [ ] Hitung Precision: `TP / (TP + FP)`
- [ ] Hitung Recall: `TP / (TP + FN)`
- [ ] Hitung F1-Score: `2 * (Precision * Recall) / (Precision + Recall)`
- [ ] Analisis hasil — sesuaikan threshold jika perlu dan uji ulang
- [ ] Dokumentasikan semua hasil pengujian dalam tabel

**Laporan TA (cicil):**

- [ ] Draft Bab III — Metode Penelitian (sesuaikan dengan implementasi aktual)

---

### Minggu 8 — Juli Minggu ke-1

**Tema: Penulisan Laporan Final + Finalisasi + Persiapan Sidang** 🔴 KRITIS

**Target output:** Laporan TA final siap submit, siap sidang.

**Laporan TA:**

- [ ] Draft Bab IV — Hasil & Pembahasan (screenshot, tabel pengujian, analisis)
- [ ] Draft Bab V — Penutup (kesimpulan menjawab rumusan masalah, saran)
- [ ] Lengkapi Daftar Pustaka — format konsisten
- [ ] Siapkan lampiran: dokumentasi pengujian, surat keterangan mitra
- [ ] Review laporan dengan dosen pembimbing
- [ ] Revisi sesuai catatan dosen pembimbing
- [ ] Laporan TA final ditandatangani semua pihak

**Finalisasi Kode:**

- [ ] Hapus semua `print()` debug yang tidak perlu
- [ ] Tambahkan error handling di semua titik kritis
- [ ] Pastikan tidak ada credential hardcoded (semua pakai `.env`)
- [ ] Push kode final ke repository dengan commit history rapi
- [ ] Buat `README.md` berisi panduan instalasi dan penggunaan sistem

**Persiapan Sidang:**

- [ ] Buat slide presentasi sidang (ringkas, fokus demo)
- [ ] Latihan demo sistem minimal 2 kali
- [ ] Test deployment di komputer mitra (bukan komputer dev)
- [ ] Siapkan jawaban pertanyaan umum:
  - Mengapa menggunakan RMS dan bukan metode lain?
  - Mengapa FFmpeg stream copy dan bukan re-encoding?
  - Mengapa FastAPI dan bukan framework lain?
  - Apa keterbatasan sistem ini?
- [] Backup laporan & kode di minimal 2 tempat (cloud + lokal)

---

## 📊 Ringkasan Progress per Minggu

| Minggu | Periode | Tema                                         | Status             |
| ------ | ------- | -------------------------------------------- | ------------------ |
| 1      | Mei W2  | Administrasi + Persiapan Environment         | 🟢 Selesai         |
| 2      | Mei W3  | Persiapan Data + Cicil Revisi Proposal       | 🔴 Belum           |
| 3      | Mei W4  | Coding Iterasi 1 — Konektivitas              | 🟡 Sedang berjalan |
| 4      | Jun W1  | Coding Iterasi 2 — Audio & Trigger           | 🟡 Sedang berjalan |
| 5      | Jun W2  | Coding Iterasi 3 — Parameter & Output        | 🔴 Belum           |
| 6      | Jun W3  | Coding Iterasi 4 — Dashboard + Cicil Laporan | 🔴 Belum           |
| 7      | Jun W4  | Pengujian Black Box + Confusion Matrix       | 🔴 Belum           |
| 8      | Jul W1  | Laporan Final + Finalisasi + Sidang          | 🔴 Belum           |

> Update kolom Status secara berkala:
> 🔴 Belum dimulai &nbsp;|&nbsp; 🟡 Sedang berjalan &nbsp;|&nbsp; 🟢 Selesai

---

## 🚨 Risiko & Mitigasi

| Risiko                             | Kemungkinan | Mitigasi                                                    |
| ---------------------------------- | ----------- | ----------------------------------------------------------- |
| Video sampel dari mitra terlambat  | Tinggi      | Minta di minggu 1, jangan tunggu minggu 2                   |
| OBS-WebSocket sulit diintegrasikan | Sedang      | Alokasikan 2 hari ekstra di minggu 3                        |
| Hasil Confusion Matrix buruk       | Sedang      | Kalibrasi threshold di minggu 2, jangan tunggu pengujian    |
| Revisi laporan dari dosen banyak   | Tinggi      | Submit draft awal ke pembimbing di minggu 6, bukan minggu 8 |
| Bug kritis muncul saat demo        | Sedang      | Latihan demo minimal 2x sebelum sidang                      |

---

_File ini bagian dari project TA — update setiap ada progress._
_Terakhir diperbarui: Mei 2026_
