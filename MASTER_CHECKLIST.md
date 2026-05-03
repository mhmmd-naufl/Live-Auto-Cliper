# Master Checklist — Tugas Akhir
## Sistem Pemotongan Highlight Siaran Langsung
**Muhammad Naufal Aulia — NIM. 362258302068**
**Politeknik Negeri Banyuwangi — 2026**

> Gunakan file ini sebagai panduan penyelesaian project dari awal hingga sidang.
> Centang `[x]` setiap item yang sudah selesai.

---

## 📋 FASE 0 — Administrasi & Dokumen Awal

### Proposal
- [ ] Proposal disetujui dosen pembimbing secara resmi
- [ ] Lembar pengesahan sudah ditandatangani semua pihak
- [ ] Proposal versi final tersimpan rapi (PDF + DOCX)
- [x] CLAUDE.md sudah dibuat dan diperbarui sesuai perkembangan project

### Revisi Proposal (dari dosen)
#### Konten & Substansi
- [ ] Perjelas permasalahan mitra CV. Alzen Metro Data — lebih spesifik dan terstruktur
- [ ] Cek abstrak — eliminasi kalimat yang terindikasi bersumber dari AI
- [ ] Perjelas tujuan TA — lebih konkret dan terukur
- [ ] Tambahkan gambaran sistem yang berjalan (proses manual) vs sistem yang diusulkan
- [ ] Perjelas gambaran umum sistem yang akan dibangun di Bab I atau Bab III

#### Teknis Penulisan
- [ ] Hapus kata ambigu: *atas, bawah, sebelumnya, setelahnya, tersebut*
- [ ] Cek semua kata asing — pastikan ditulis *italic*
- [ ] Hapus kata ganti "penulis" — ganti kalimat pasif atau subjek sistem
- [ ] Rapikan format semua tabel (alignment, konsistensi kolom)

#### Struktur & Kelengkapan
- [ ] Rumus 2.1–2.6 & 3.1 — tambahkan contoh implementasi ke konteks nyata
- [ ] Setiap gambar & tabel memiliki kalimat penjelasan yang merujuk ke nomornya
- [ ] Cek relevansi database dengan use case yang ada

---

## 🛠️ FASE 1 — Persiapan Sebelum Coding

### Lingkungan & Tools
- [x] Install OBS Studio versi 28+
- [x] Aktifkan OBS-WebSocket di OBS Studio (Tools → WebSocket Server Settings)
- [x] Test koneksi OBS-WebSocket secara manual (via browser WebSocket tool)
- [x] Aktifkan & konfigurasi Replay Buffer di OBS — test simpan manual
- [x] Install FFmpeg & daftarkan ke system environment variables
- [ ] Test FFmpeg stream copy manual: `ffmpeg -ss [offset] -i input.mp4 -c copy output.mp4`
- [x] Install Python 3.10+ 
- [x] Install Node.js 18+ dan npm
- [x] Install Git & buat repository project (GitHub/GitLab)
- [x] Setup Python virtual environment: `python -m venv venv`
- [x] Install dependency awal backend: `fastapi uvicorn obsws-python aiosqlite sqlalchemy`
- [x] Install dependency awal frontend: `npm create vite@latest` (React + JS)
- [x] Setup struktur folder project sesuai CLAUDE.md
- [x] Buat file `.env` untuk menyimpan konfigurasi sensitif (host, port, password OBS)
- [x] Buat file `.gitignore` (exclude `venv/`, `.env`, `node_modules/`, file video)

### Koordinasi Mitra (CV. Alzen Metro Data)
- [ ] Konfirmasi format video output yang dipakai (MP4/MKV, codec, resolusi)
- [ ] Konfirmasi durasi Replay Buffer yang biasa digunakan
- [ ] Konfirmasi direktori/folder penyimpanan file highlight yang diinginkan
- [ ] Dapatkan akses ke setup OBS Studio mitra untuk observasi langsung
- [ ] Dapatkan sampel rekaman video siaran olahraga untuk data uji

### Data & Kalibrasi
- [ ] Observasi nilai dBFS siaran olahraga: catat rentang normal vs momen penting
- [ ] Tentukan nilai threshold awal berdasarkan observasi (bukan hanya asumsi)
- [ ] Tentukan durasi minimum persistence awal (default proposal: 2 detik)
- [ ] Buat template tabel anotasi manual (ground truth) untuk pengujian
- [ ] Lakukan anotasi manual pada minimal 1 video sampel (catat timestamp momen penting)

### Pemahaman Teknis (Belajar Mandiri)
- [ ] Pahami struktur pesan OBS-WebSocket (baca dokumentasi resmi obsproject.com)
- [ ] Pahami format data `inputLevelsMul` dari OBS-WebSocket
- [ ] Pahami cara kerja Replay Buffer OBS secara teknis
- [ ] Coba library `obsws-python` — baca dokumentasi dan contoh penggunaan
- [ ] Pahami parameter `-ss`, `-c copy`, `-t` pada FFmpeg

---

## 💻 FASE 2 — Coding (per Iterasi)

### Iterasi 1 — Integrasi & Konektivitas Sistem
- [x] Buat koneksi OBS-WebSocket dari Python menggunakan `obsws-python`
- [ ] Implementasi auto-reconnect jika koneksi terputus
- [ ] Subscribe ke event audio dari OBS
- [ ] Terima & print data audio mentah dari OBS ke terminal
- [x] Buat endpoint FastAPI: `GET /status` — status koneksi OBS
- [x] Buat endpoint FastAPI: `POST /connect` — inisiasi koneksi ke OBS
- [x] Buat endpoint FastAPI: `POST /disconnect` — putus koneksi
- [x] Buat WebSocket endpoint FastAPI untuk push status ke frontend
- [ ] Buat komponen React: `ConnectionPanel` — form input IP, port, password
- [ ] Buat komponen React: status indikator koneksi (Connected / Disconnected)
- [ ] Test end-to-end: frontend → backend → OBS terhubung
- [ ] **Review & evaluasi Iterasi 1 sebelum lanjut**

### Iterasi 2 — Analisis Audio & Logika Trigger
- [x] Implementasi konversi magnitude → dBFS: `20 * log10(magnitude)`
- [x] Implementasi pembacaan RMS real-time dari stream audio (via sounddevice)
- [x] Implementasi Time-Persistence Thresholding:
- [x] Catat `T_Start` saat dBFS pertama melampaui threshold
- [x] Reset timer jika dBFS turun sebelum durasi minimum
- [x] Trigger valid jika dBFS bertahan ≥ `persistence_duration` detik
- [ ] Implementasi pengiriman perintah `SaveReplayBuffer` ke OBS via WebSocket
- [x] Implementasi mekanisme cooldown setelah trigger (hindari trigger beruntun)
- [ ] Push data dBFS real-time ke frontend via WebSocket
- [ ] Buat komponen React: `AudioChart` — grafik bar dBFS real-time
- [ ] Tampilkan garis threshold horizontal pada grafik
- [ ] Test trigger: suara keras ≥ 2 detik → OBS menyimpan Replay Buffer
- [ ] **Review & evaluasi Iterasi 2 sebelum lanjut**

### Iterasi 3 — Manajemen Parameter & Optimalisasi Output
- [ ] Setup database SQLite dengan SQLAlchemy (tabel `configurations` & `highlight_logs`)
- [ ] Implementasi CRUD endpoint untuk tabel `configurations`
- [ ] Implementasi algoritma perhitungan offset:
  `Offset = Durasi_Replay_Buffer - (T_Save - T_Start)`
- [ ] Implementasi FFmpeg stream copy via subprocess:
  `ffmpeg -ss {offset} -i {input} -c copy {output}`
- [ ] Implementasi pemindahan file dari folder temp OBS ke direktori tujuan
- [ ] Implementasi pencatatan log ke tabel `highlight_logs`
- [ ] Buat endpoint FastAPI: `POST /config` — simpan konfigurasi
- [ ] Buat endpoint FastAPI: `GET /config` — ambil konfigurasi aktif
- [ ] Buat komponen React: `ActionCenter` — form threshold, durasi, folder path
- [ ] Test output: file MP4 tersimpan di direktori tujuan dengan durasi yang presisi
- [ ] Validasi kualitas video output identik dengan sumber (lossless)
- [ ] **Review & evaluasi Iterasi 3 sebelum lanjut**

### Iterasi 4 — Dashboard & Laporan
- [ ] Buat endpoint FastAPI: `GET /logs` — ambil semua highlight logs
- [ ] Buat komponen React: `HighlightsLog` — tabel riwayat aktivitas
- [ ] Tampilkan timestamp, filename, trigger value, status, durasi di log
- [ ] Implementasi filter/sort pada tabel log
- [ ] Tampilkan session timer di header dashboard
- [ ] Tampilkan statistik ringkas: total highlight hari ini, rata-rata dBFS trigger
- [ ] Polish UI: responsif, dark/light mode (opsional), loading states
- [ ] Tambahkan notifikasi/toast saat highlight berhasil disimpan
- [ ] Test end-to-end lengkap: OBS → deteksi → trigger → file tersimpan → log update
- [ ] **Review & evaluasi Iterasi 4 sebelum lanjut**

---

## 🧪 FASE 3 — Pengujian

### Persiapan Pengujian
- [ ] Finalisasi tabel ground truth (anotasi manual semua video uji)
- [ ] Tentukan jumlah skenario uji per kategori
- [ ] Siapkan environment pengujian (komputer siaran + OBS aktif)
- [ ] Dokumentasikan spesifikasi hardware & software yang digunakan saat uji

### Black Box Testing
#### Koneksi OBS-WebSocket
- [ ] TC-CON-01: Koneksi berhasil dengan kredensial benar
- [ ] TC-CON-02: Koneksi gagal karena OBS tidak aktif
- [ ] TC-CON-03: Koneksi gagal karena password salah
- [ ] TC-CON-04: Auto-reconnect setelah OBS di-restart

#### Pemantauan Sinyal Audio
- [ ] TC-AUD-01: Pembacaan dBFS saat kondisi hening
- [ ] TC-AUD-02: Pembacaan dBFS saat suara normal
- [ ] TC-AUD-03: Pembacaan dBFS saat suara keras melebihi threshold
- [ ] TC-AUD-04: Visualisasi grafik audio berjalan real-time

#### Eksekusi Pemotongan Video
- [ ] TC-VID-01: Replay Buffer aktif saat trigger dikirim
- [ ] TC-VID-02: Replay Buffer tidak aktif saat trigger dikirim
- [ ] TC-VID-03: File tersimpan dalam format yang benar
- [ ] TC-VID-04: FFmpeg stream copy tanpa re-encoding

#### Konfigurasi via Dashboard
- [ ] TC-CONF-01: Perubahan threshold berhasil disimpan
- [ ] TC-CONF-02: Perubahan durasi Replay Buffer berhasil disimpan
- [ ] TC-CONF-03: Input nilai threshold tidak valid ditolak sistem

### Evaluasi Confusion Matrix
- [ ] Jalankan sistem pada semua video uji
- [ ] Catat hasil deteksi: TP, FP, TN, FN per video
- [ ] Hitung Accuracy: `(TP + TN) / (TP + TN + FP + FN)`
- [ ] Hitung Precision: `TP / (TP + FP)`
- [ ] Hitung Recall: `TP / (TP + FN)`
- [ ] Hitung F1-Score: `2 * (Precision * Recall) / (Precision + Recall)`
- [ ] Analisis hasil — apakah memenuhi ekspektasi? Lakukan penyesuaian threshold jika perlu
- [ ] Dokumentasikan semua hasil pengujian dalam tabel

---

## 📝 FASE 4 — Penulisan Laporan TA

### Bab I — Pendahuluan
- [ ] Latar belakang — selesai & direvisi sesuai catatan dosen
- [ ] Rumusan masalah — jelas dan terukur
- [ ] Tujuan penelitian — spesifik dan konkret
- [ ] Manfaat penelitian — lengkap (mitra, peneliti, keilmuan)
- [ ] Batasan masalah — jelas dan realistis

### Bab II — Tinjauan Pustaka
- [ ] Semua dasar teori relevan sudah ditulis
- [ ] Setiap rumus (2.1–2.6) ada contoh implementasi ke konteks sistem
- [ ] Penelitian terkait minimal 5 referensi (sudah ada 3 di proposal)
- [ ] Semua sitasi menggunakan format yang konsisten
- [ ] Tidak ada kalimat yang terindikasi dari AI

### Bab III — Metode Penelitian
- [ ] Tempat & jadwal penelitian — sesuai realita
- [ ] Metode Iterative Incremental — dijelaskan per iterasi
- [ ] Use Case Diagram — final dan relevan dengan database
- [ ] Flowchart — sesuai implementasi akhir
- [ ] Mockup — sesuai tampilan dashboard final
- [ ] PDM database — relevan dan konsisten dengan use case
- [ ] Algoritma deteksi ambang batas — ada contoh nyata
- [ ] Algoritma perhitungan offset — ada contoh nyata dengan angka

### Bab IV — Hasil & Pembahasan
- [ ] Hasil implementasi setiap iterasi — screenshot & penjelasan
- [ ] Hasil pengujian Black Box Testing — tabel lengkap
- [ ] Hasil Confusion Matrix — tabel + nilai metrik
- [ ] Analisis & pembahasan hasil — dihubungkan ke tujuan penelitian
- [ ] Screenshot dashboard final

### Bab V — Penutup
- [ ] Kesimpulan — menjawab semua rumusan masalah
- [ ] Saran — untuk pengembangan sistem ke depan

### Daftar Pustaka & Lampiran
- [ ] Semua referensi tercantum lengkap dan konsisten formatnya
- [ ] Lampiran: kode program inti (opsional sesuai panduan kampus)
- [ ] Lampiran: dokumentasi pengujian
- [ ] Lampiran: surat keterangan dari mitra

---

## 🚀 FASE 5 — Deployment & Finalisasi

### Deployment
- [ ] Test deployment lokal di komputer mitra (bukan komputer dev)
- [ ] Pastikan sistem berjalan stabil selama minimal 1 sesi siaran penuh
- [ ] Dokumentasikan langkah instalasi sistem (README.md)
- [ ] Buat panduan penggunaan singkat untuk operator mitra

### Finalisasi Kode
- [ ] Hapus semua `print()` debug yang tidak perlu
- [ ] Tambahkan error handling pada semua titik kritis
- [ ] Tambahkan logging ke file (bukan hanya konsol)
- [ ] Pastikan tidak ada credential hardcoded di kode (pakai `.env`)
- [ ] Kode sudah di-push ke repository dengan commit history yang rapi

### Persiapan Sidang
- [ ] Draft laporan TA sudah di-review dosen pembimbing
- [ ] Revisi laporan dari dosen pembimbing selesai
- [ ] Laporan TA final sudah disetujui dan ditandatangani
- [ ] Slide presentasi sidang dibuat (ringkas, fokus demo sistem)
- [ ] Demo sistem sudah dilatih minimal 2 kali
- [ ] Siapkan jawaban untuk pertanyaan umum: mengapa RMS? mengapa FFmpeg stream copy? kenapa FastAPI?
- [ ] Backup laporan & kode di minimal 2 tempat (cloud + lokal)

---

## 📊 Ringkasan Progress

| Fase | Keterangan | Status |
|------|-----------|--------|
| Fase 0 | Administrasi & Dokumen | 🟡 Sedang berjalan |
| Fase 1 | Persiapan Sebelum Coding | 🟡 Sedang berjalan |
| Fase 2 | Coding (4 Iterasi) | 🟡 Sedang berjalan |
| Fase 3 | Pengujian | 🔴 Belum |
| Fase 4 | Penulisan Laporan | 🔴 Belum |
| Fase 5 | Deployment & Sidang | 🔴 Belum |

> Update tabel ini secara berkala:
> 🔴 Belum dimulai | 🟡 Sedang berjalan | 🟢 Selesai

---
> Terakhir diperbarui: Mei 2026 — Sesi hari ini berhasil:
> backend FastAPI jalan, koneksi OBS berhasil, audio monitor via sounddevice aktif, deteksi dBFS real-time berjalan ✅