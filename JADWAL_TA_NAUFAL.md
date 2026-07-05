# Jadwal TA — Muhammad Naufal Aulia
## Sistem Pemotongan Highlight Siaran Langsung
**Dibuat: Juni 2026 | Target Sidang: Juli 2026**

> ⚠️ Jadwal ini dibuat berdasarkan kondisi nyata:
> - Proposal terlambat dari deadline tapi masih bisa dikumpulkan
> - Coding 50% selesai (backend jalan, UI belum ada)
> - Minggu 1 banyak urusan kampus
> - Waktu efektif: 6–8 jam/hari
>
> **Aturan main:**
> - Setiap hari ada TARGET HARIAN yang spesifik
> - Kalau target hari ini tidak selesai, JANGAN lanjut ke hari berikutnya sebelum diselesaikan
> - Centang `[x]` setiap item yang selesai
> - Update file ini setiap malam sebelum tidur

---

## 🔴 MINGGU 1 — Proposal + Koordinasi Kampus
**2 Juni – 8 Juni 2026**
**Tema: Bereskan proposal, konfirmasi ke dosen, hubungi mitra**

> Minggu ini banyak ke kampus. Coding tidak jadi prioritas utama minggu ini.
> Fokus: proposal selesai dikumpulkan + mitra dikonfirmasi.

### Senin, 2 Juni
**Target: Selesaikan semua revisi proposal yang tersisa**
- [x] Perbaiki "momen gol" → "momen penting" di deskripsi Precision dan Recall
- [x] Perbaiki "Presisi" → "Precision" di deskripsi F1-Score
- [x] Perbaiki "Be Berdasarkan" typo di Bab III sub-bab Requirement
- [x] Perbaiki "OBS-websocket" huruf kecil di tabel Use Case
- [x] Tambahkan contoh numerik rumus 2.1 (dBFS) — draft sudah ada
- [x] Tambahkan paragraf skenario ilustrasi + contoh numerik rumus 2.3–2.6 — draft sudah ada
- [x] Ganti kata "asumsi" di sub-bab RMS — draft sudah ada
- [ ] Tambahkan kalimat `persistence_duration` ke use case — draft sudah ada
- [ ] Update Daftar Isi — sesuaikan nomor sub-bab setelah penambahan 2.1.7
- [ ] Ganti tabel deskripsi use case dengan versi revisi
- [ ] Ganti narasi PDM dengan versi revisi
- [ ] Update use case diagram dengan versi final (Usecase_4)

### Selasa, 3 Juni
**Target: Kumpulkan proposal ke dosen pembimbing**
- [ ] Baca ulang seluruh proposal dari awal sampai akhir — 1 kali penuh
- [ ] Cek konsistensi italic kata asing satu kali lagi
- [ ] Cek semua nomor gambar dan tabel
- [ ] Print atau kirim ke dosen pembimbing
- [ ] Hubungi mitra CV. Alzen — minta jadwal pertemuan minggu ini atau minggu depan

### Rabu–Kamis, 4–5 Juni
**Target: Urusan kampus + cicil persiapan mitra**
- [ ] Konfirmasi revisi dengan dosen pembimbing (sesuai jadwal kampus)
- [ ] Siapkan bahan pertemuan mitra:
  - [ ] Daftar pertanyaan teknis (format video, durasi Replay Buffer, dll)
  - [ ] Demo terminal backend yang sudah jalan — pastikan bisa didemonstrasikan
  - [ ] Siapkan penjelasan singkat sistem dalam 2–3 kalimat non-teknis
- [ ] Kalau ada waktu sisa: mulai setup project React frontend (init Vite)

### Jumat, 6 Juni
**Target: Pertemuan mitra ATAU setup frontend**
- [ ] Kalau pertemuan mitra terjadi:
  - [ ] Konfirmasi format video OBS mitra (MP4/MKV, resolusi, codec)
  - [ ] Konfirmasi durasi Replay Buffer yang biasa dipakai
  - [ ] Catat berapa kali siaran per minggu
  - [ ] Minta izin observasi satu sesi siaran langsung
- [ ] Kalau pertemuan mitra belum bisa:
  - [ ] Setup project React + Tailwind
  - [ ] Buat komponen `ConnectionPanel` — form IP, port, password OBS

### Sabtu–Minggu, 7–8 Juni
**Target: Mulai coding UI**
- [ ] Komponen `ConnectionPanel` selesai dan bisa konek ke backend
- [ ] Komponen status koneksi (Connected / Disconnected) selesai
- [ ] Test end-to-end: klik Connect di UI → backend → OBS terhubung
- [ ] Selesaikan kalibrasi offset jika belum beres

---

## 🟠 MINGGU 2 — Coding UI + Kalibrasi
**9 Juni – 15 Juni 2026**
**Tema: UI fungsional selesai, sistem end-to-end berjalan dengan UI**

> Minggu ini fokus penuh coding. Tidak ada alasan untuk tidak coding setiap hari.

### Senin, 9 Juni
- [ ] Komponen `ActionCenter` — form threshold, durasi, folder path
- [ ] Endpoint `POST /config` dan `GET /config` di backend
- [ ] Test: perubahan threshold dari UI tersimpan ke database

### Selasa, 10 Juni
- [ ] Komponen `AudioChart` — grafik dBFS real-time (bar chart sederhana)
- [ ] WebSocket push data dBFS dari backend ke frontend
- [ ] Tampilkan garis threshold horizontal di grafik

### Rabu, 11 Juni
- [ ] Komponen `HighlightsLog` — tabel riwayat aktivitas
- [ ] Endpoint `GET /logs` di backend
- [ ] Tampilkan timestamp, filename, trigger value, status di tabel

### Kamis, 12 Juni
- [ ] Implementasi `SaveReplayBuffer` via WebSocket ke OBS
- [ ] Selesaikan kalibrasi perhitungan offset
- [ ] Test trigger nyata: suara keras → OBS simpan Replay Buffer → file terpotong

### Jumat, 13 Juni
- [ ] Implementasi FFmpeg stream copy via subprocess
- [ ] Test output: file MP4 tersimpan di direktori tujuan
- [ ] Validasi kualitas video output (lossless)

### Sabtu–Minggu, 14–15 Juni
- [ ] Polish UI — loading states, error states
- [ ] Toast notifikasi saat highlight berhasil disimpan
- [ ] Session timer di header dashboard
- [ ] Test end-to-end lengkap: OBS → deteksi → trigger → file tersimpan → log update
- [ ] ✅ Evaluasi sistem — apakah sudah siap diuji?

---

## 🟡 MINGGU 3 — Pertemuan Mitra + Pengujian
**16 Juni – 22 Juni 2026**
**Tema: Validasi sistem di kondisi nyata + Black Box Testing**

### Senin–Selasa, 16–17 Juni
- [ ] Pertemuan mitra CV. Alzen — demo sistem, kalibrasi dengan setup OBS mitra
- [ ] Catat semua feedback mitra
- [ ] Kalibrasi ulang threshold dan persistence_duration berdasarkan audio siaran nyata

### Rabu–Kamis, 18–19 Juni
**Black Box Testing:**
- [ ] TC-CON-01: Koneksi berhasil dengan kredensial benar
- [ ] TC-CON-02: Koneksi gagal karena OBS tidak aktif
- [ ] TC-CON-03: Koneksi gagal karena password salah
- [ ] TC-CON-04: Auto-reconnect setelah OBS di-restart
- [ ] TC-AUD-01: Pembacaan dBFS saat kondisi hening
- [ ] TC-AUD-02: Pembacaan dBFS saat suara normal
- [ ] TC-AUD-03: Pembacaan dBFS saat suara keras melebihi threshold
- [ ] TC-AUD-04: Visualisasi grafik audio berjalan real-time

### Jumat, 20 Juni
- [ ] TC-VID-01: Replay Buffer aktif saat trigger dikirim
- [ ] TC-VID-02: Replay Buffer tidak aktif saat trigger dikirim
- [ ] TC-VID-03: File tersimpan dalam format yang benar
- [ ] TC-VID-04: FFmpeg stream copy tanpa re-encoding
- [ ] TC-CONF-01: Perubahan threshold berhasil disimpan
- [ ] TC-CONF-02: Perubahan durasi Replay Buffer berhasil disimpan
- [ ] TC-CONF-03: Input nilai threshold tidak valid ditolak sistem

### Sabtu–Minggu, 21–22 Juni
**Confusion Matrix:**
- [ ] Siapkan video uji yang sudah dianotasi manual
- [ ] Jalankan sistem pada semua video uji
- [ ] Catat TP, FP, TN, FN per video
- [ ] Hitung Precision, Recall, F1-Score
- [ ] Analisis hasil — sesuaikan threshold jika F1-Score di bawah 80%
- [ ] Dokumentasikan semua hasil pengujian dalam tabel

---

## 🔵 MINGGU 4 — Penulisan Laporan Bab IV + V
**23 Juni – 29 Juni 2026**
**Tema: Tulis hasil pengujian dan kesimpulan**

### Senin–Selasa, 23–24 Juni
- [ ] Draft Bab IV — Hasil implementasi per iterasi (screenshot + penjelasan)
- [ ] Tabel Black Box Testing lengkap
- [ ] Tabel Confusion Matrix + nilai metrik

### Rabu, 25 Juni
- [ ] Analisis dan pembahasan hasil pengujian
- [ ] Hubungkan hasil ke tujuan penelitian
- [ ] Screenshot dashboard final

### Kamis, 26 Juni
- [ ] Draft Bab V — Kesimpulan menjawab semua rumusan masalah
- [ ] Saran pengembangan (termasuk rekomendasi deep learning untuk penelitian lanjutan)
- [ ] Lengkapi Daftar Pustaka

### Jumat, 27 Juni
- [ ] Review seluruh laporan dari Bab I sampai V
- [ ] Kirim draft laporan ke dosen pembimbing
- [ ] Siapkan lampiran: dokumentasi pengujian, surat keterangan mitra

### Sabtu–Minggu, 28–29 Juni
- [ ] Revisi berdasarkan catatan dosen pembimbing
- [ ] Finalisasi kode: hapus print() debug, tambah error handling, cek .env
- [ ] Push kode final ke repository
- [ ] Buat README.md panduan instalasi

---

## 🟢 MINGGU 5 — Finalisasi + Persiapan Sidang
**30 Juni – 6 Juli 2026**
**Tema: Laporan final + latihan sidang**

### Senin–Selasa, 30 Juni – 1 Juli
- [ ] Laporan TA final selesai semua revisi dari dosen
- [ ] Laporan ditandatangani semua pihak
- [ ] Deploy sistem di komputer mitra untuk test final

### Rabu–Kamis, 2–3 Juli
- [ ] Buat slide presentasi sidang (ringkas, fokus demo)
- [ ] Latihan demo sistem — minimal 2 kali penuh
- [ ] Siapkan jawaban pertanyaan umum:
  - Mengapa RMS dan bukan deep learning?
  - Mengapa FFmpeg stream copy?
  - Mengapa FastAPI?
  - Apa keterbatasan sistem ini?
  - Apa yang akan dikembangkan selanjutnya?

### Jumat–Minggu, 4–6 Juli
- [ ] Simulasi sidang dengan teman atau kakak tingkat
- [ ] Revisi slide jika perlu
- [ ] Backup laporan dan kode di minimal 2 tempat
- [ ] **SIAP SIDANG** 🎯

---

## 📊 Ringkasan Target per Minggu

| Minggu | Periode | Target Utama | Status |
|--------|---------|-------------|--------|
| 1 | 2–8 Juni | Proposal selesai + mitra dikonfirmasi | 🔴 Belum |
| 2 | 9–15 Juni | UI fungsional + sistem end-to-end | 🔴 Belum |
| 3 | 16–22 Juni | Pengujian selesai | 🔴 Belum |
| 4 | 23–29 Juni | Laporan Bab IV + V selesai | 🔴 Belum |
| 5 | 30 Juni–6 Juli | Finalisasi + siap sidang | 🔴 Belum |

---

## ⚠️ Aturan Darurat

**Kalau suatu hari target tidak tercapai:**
1. Jangan panik — catat apa yang belum selesai
2. Tambahkan ke hari berikutnya PAGI HARI sebelum mulai target baru
3. Kalau 2 hari berturut-turut target meleset → evaluasi, hubungi dosen pembimbing

**Kalau dosen susah ditemui:**
1. Kirim pesan/email setiap hari — jangan tunggu dibalas dulu
2. Sambil tunggu balasan, tetap lanjut coding dan laporan
3. Jangan jadikan "nunggu dosen" sebagai alasan berhenti

**Kalau mitra susah diatur jadwalnya:**
1. Tetap lanjut pengujian dengan simulasi audio sendiri
2. Koordinasi mitra bisa dilakukan paralel dengan pengujian
3. Jangan tunggu mitra untuk mulai testing

---

*Jadwal dibuat berdasarkan sesi bimbingan Juni 2026.*
*Update setiap malam. Centang yang sudah selesai.*
*Target sidang: minggu pertama Juli 2026.*
