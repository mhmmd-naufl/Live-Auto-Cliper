# Checklist Revisi Proposal Tugas Akhir
## Sistem Pemotongan Highlight Siaran Langsung
**Muhammad Naufal Aulia — NIM. 362258302068**
**Dibuat berdasarkan sesi bimbingan: Mei 2026**

> Centang `[x]` setiap item yang sudah selesai direvisi.
> Laporkan progress ke dosen pembimbing secara berkala.

---

## 🔴 KRITIS — Wajib selesai sebelum proposal disetujui

### K-1: Hapus semua kata "penulis"
Ditemukan di lokasi berikut — ganti semua menjadi kalimat pasif atau bersubjek sistem/penelitian:

- [x] Bab III, Initial Planning: *"penulis melakukan wawancara..."* → *"Wawancara dilakukan dengan pihak CV. Alzen Metro Data..."*
- [x] Bab III, Initial Planning: *"penulis memperoleh informasi..."*
- [x] Bab III, Initial Planning: *"penulis merancang sistem..."*
- [x] Bab III, Studi Literatur: *"penulis mencari referensi..."*
- [x] Bab III, Studi Literatur: *"penulis juga melakukan koordinasi..."*
- [x] Bab III, Requirement: *"penulis merumuskan kebutuhan..."*
- [x] Bab III, Analysis dan Design: *"penulis menentukan berbagai aktivitas..."*
- [x] Bab III, Analysis dan Design: *"penulis menganalisis peran-peran..."*
- [x] Bab III, Implementation: *"penulis mulai menerapkan hasil..."*
- [x] Bab III, Testing: *"penulis melakukan observasi..."*

---

### K-2: Tulis ulang Abstrak
- [ ] Identifikasi dan hapus semua kalimat yang terindikasi ditulis oleh AI (terlalu mekanis dan paralel strukturnya)
- [ ] Tulis ulang dengan gaya bahasa akademik yang lebih organik — mulai dari masalah nyata di CV. Alzen, baru ke solusi, metode, dan hasil yang diharapkan
- [x] Pastikan abstrak tidak lebih dari 250 kata setelah revisi

---

### K-3: Tambahkan gambaran sistem lama vs sistem baru
- [x] Tambahkan sub-bagian atau tabel perbandingan di Bab I atau Bab III yang mendeskripsikan:
  - Alur proses manual yang saat ini berjalan di CV. Alzen Metro Data
  - Identifikasi titik-titik masalah pada proses manual tersebut
  - Bagaimana sistem yang diusulkan menjawab setiap masalah tersebut
- [x] Bisa berupa tabel perbandingan (Sebelum vs Sesudah) atau flowchart sistem lama vs sistem baru

---

### K-4: Perbaiki Tujuan Penelitian agar terukur
Tujuan saat ini masih abstrak. Setiap tujuan harus mengandung kriteria keberhasilan yang bisa diukur.

- [x] Tujuan 1 — tambahkan kriteria metrik minimal (contoh: *"...dengan nilai F1-Score minimal [X]%..."*)
- [x] Tujuan 2 — tambahkan kriteria konkret keberhasilan integrasi OBS-WebSocket
- [x] Tujuan 3 — tambahkan kriteria presisi pemotongan video yang diharapkan
- [x] Pastikan setelah direvisi, setiap tujuan bisa langsung diverifikasi saat pengujian di Bab IV

---

### K-5: Sinkronkan Rumusan Masalah dengan Tujuan Penelitian
- [x] Petakan setiap rumusan masalah ke tujuan penelitian yang menjawabnya secara 1:1
- [x] Pastikan Rumusan Masalah ke-3 dan Tujuan ke-3 memiliki cakupan yang simetris (keduanya menyebut offset calculation DAN FFmpeg Stream Copy)

---

## 🟠 SUBSTANSI & KONTEN

### S-1: Perkuat permasalahan mitra di Latar Belakang
- [ ] Tambahkan minimal 2–3 data atau fakta kuantitatif hasil wawancara/observasi langsung dengan CV. Alzen Metro Data
- [ ] Contoh yang perlu dicari: berapa kali siaran per minggu, berapa operator yang dibutuhkan, seberapa sering momen terlewat

---

### S-2: Tambahkan contoh implementasi nyata untuk semua rumus

#### Rumus 2.1 — Konversi dBFS
- [ ] Tambahkan contoh numerik setelah rumus, contoh: *"Jika OBS mengirimkan nilai magnitude 0.5, maka dBFS = 20 × log10(0.5) = −6.02 dBFS..."*

#### Rumus 2.3 — Accuracy
- [ ] Tambahkan contoh angka TP, TN, FP, FN dari skenario pengujian hipotetis

#### Rumus 2.4 — Precision
- [ ] Tambahkan contoh angka konkret

#### Rumus 2.5 — Recall
- [ ] Tambahkan contoh angka konkret

#### Rumus 2.6 — F1-Score
- [ ] Tambahkan contoh angka konkret, hitung dari nilai Precision dan Recall yang sudah dicontohkan di atas (konsisten)

#### Rumus 3.1 — Offset
- [ ] Tambahkan contoh numerik dengan skenario konkret, contoh: *"Jika durasi Replay Buffer = 30 detik, T_Save = 100, T_Start = 95, maka Offset = 30 − (100 − 95) = 25 detik..."*

---

### S-3: Perbaiki semua referensi nomor gambar yang salah di Bab III
Semua referensi gambar di body text Bab III meleset satu angka dari Daftar Gambar:

- [x] *"Gambar 3.1"* di body text → seharusnya **Gambar 3.2** (Use Case Diagram)
- [x] *"Gambar 3.2"* di body text → seharusnya **Gambar 3.3** (Flowchart)
- [x] *"gambar 3.3"* di body text → seharusnya **Gambar 3.4** (Mockup)
- [x] *"Gambar 3.4"* di body text → seharusnya **Gambar 3.5** (PDM)
- [x] Setelah selesai, cross-check semua nomor gambar antara Daftar Gambar dan body text sekali lagi

---

### S-4: Perjelas relevansi database dengan use case
- [x] Tambahkan kalimat eksplisit yang menghubungkan kolom `persistence_duration` di tabel `configurations` dengan use case yang relevan
- [x] Pastikan setiap kolom di kedua tabel database bisa ditelusuri ke use case atau kebutuhan fungsional yang mana

---

### S-5: Tambahkan sub-bab 2.1.7 Time-Persistence Thresholding *(BARU)*
- [x] Tambahkan sub-bab baru di posisi **2.1.7** (setelah dBFS, sebelum FFmpeg Stream Copy)
- [x] Gunakan konten yang sudah disusun dalam sesi bimbingan ini (4 paragraf)
- [ ] Pastikan di awal **Algoritma Deteksi Ambang Batas di Bab III** ada kalimat yang merujuk ke sub-bab 2.1.7 ini

---

### S-6: Tambahkan minimal 2 penelitian terkait
- [ ] Cari dan tambahkan minimal 2 penelitian terkait agar total menjadi minimal 5
- [ ] Topik yang relevan: deteksi event audio otomatis, audio threshold pada siaran langsung, atau sistem clipping berbasis sinyal audio
- [ ] Tambahkan ke Tabel 2.1 dengan format kolom yang konsisten

---

### S-7: Perbaiki sub-bab Iterative Incremental *(sudah ada draftnya)*
- [x] Ganti isi sub-bab dengan versi revisi yang sudah disusun dalam sesi bimbingan ini
- [x] Pastikan deskripsi 7 tahapan yang panjang sudah dipangkas menjadi ringkasan 1 kalimat dengan catatan rujukan ke Bab III

---

### S-8: Perbaiki sub-bab dBFS *(sudah ada draftnya)*
- [x] Ganti paragraf kedua dengan versi revisi yang sudah disusun dalam sesi bimbingan ini
- [x] Pastikan kalimat menggantung setelah "obs-audio-controls.c" sudah dilengkapi
- [x] Pastikan kata "tersebut" yang ambigu sudah diganti dengan rujukan eksplisit

---

### S-9: Perbaiki kalimat "asumsi" di sub-bab RMS
- [x] Temukan kalimat: *"ditetapkan berdasarkan asumsi bahwa gangguan audio sesaat..."*
- [x] Ganti kata "asumsi" — gunakan referensi dari Gul et al. (2024) atau formulasikan sebagai parameter awal yang akan divalidasi saat pengujian

---

### S-10: Pangkas sub-bab FastAPI dan ReactJS
- [x] Gabungkan sub-bab 2.1.8 FastAPI dan 2.1.9 ReactJS menjadi satu sub-bab ringkas bernama **"Teknologi Pendukung"** atau **"Tools Pengembangan"** (ini jadinya saya hapus)
- [ ] Masing-masing cukup 2–3 kalimat: definisi singkat + alasan pemilihan
- [x] Hapus penjelasan teknis mendalam yang tidak berkontribusi pada metode inti penelitian

---

### S-11: Tambahkan kalimat pengantar rumus Offset di Bab III
- [x] Sebelum rumus 3.1 di Bab III, tambahkan kalimat yang menjelaskan dari mana logika rumus ini berasal
- [x] Contoh: *"Perhitungan offset didasarkan pada karakteristik teknis fitur Replay Buffer OBS Studio, di mana file yang disimpan selalu memiliki durasi statis sesuai konfigurasi..."*

---

## 🟡 TEKNIS PENULISAN

### T-1: Standarkan penulisan italic semua kata asing
Lakukan *global search* untuk kata-kata berikut dan pastikan **semua** ditulis italic tanpa pengecualian:

- [x] *livestreaming* — cek di seluruh dokumen termasuk judul sub-bab
- [x] *clipping* — cek di seluruh dokumen termasuk judul sub-bab
- [x] *real-time* — sering tidak italic di beberapa paragraf
- [x] *trigger* — beberapa kalimat tidak italic
- [x] *highlight* — cek di Daftar Isi dan body text
- [x] *replay buffer* — standarkan
- [x] *threshold* — standarkan
- [x] *stream copy* — standarkan
- [x] *backend* dan *frontend* — standarkan
- [x] *dashboard* — standarkan
- [x] *framework* dan *library* — standarkan
- [x] *encoding* / *re-encoding* — standarkan
- [x] *buffer* — standarkan
- [x] *cooldown* — standarkan

---

### T-2: Standarkan penulisan "OBS-WebSocket"
- [x] Ganti semua variasi *"OBS-Websocket"* (huruf s kecil) menjadi **"OBS-WebSocket"** (W dan S kapital)
- [x] Lakukan global search untuk memastikan tidak ada yang terlewat

---

### T-3: Standarkan penulisan "Black Box Testing"
- [x] Ganti semua variasi *"Blackbox"* (satu kata) menjadi **"Black Box"** (dua kata)
- [x] Termasuk di judul sub-bab 2.1.11 dan Daftar Isi

---

### T-4: Perbaiki typo
- [x] *"anjang"* di sub-bab Clipping → **"panjang"**
- [x] *"itensitas"* di Tabel 3.10 TC-AUD-02 → **"intensitas"**
- [x] *"Kebutuhuan"* di judul Tabel 3.2 → **"Kebutuhan"**
- [x] *"disimpen"* di Tabel 3.12 TC-CONF-01 → **"disimpan"**
- [x] *"internet,,"* di sub-bab Studi Literatur → hapus titik koma ganda
- [x] Cek dan hapus semua spasi ganda yang ada sebelum kata *"real time"*

---

### T-5: Perbaiki kalimat ganda di sub-bab OBS Studio
- [x] Temukan dua kalimat yang sama-sama diawali *"Dalam alur kerjanya..."* dalam satu paragraf
- [x] Gabungkan atau tulis ulang agar tidak ada pengulangan frasa pembuka yang identik

---

### T-6: Perbaiki format penulisan rumus
- [x] Ubah semua rumus yang saat ini diformat sebagai tabel Word menjadi format **Equation Editor** (Insert → Equation di Microsoft Word)
- [x] Pastikan nomor rumus rata kanan menggunakan tab stop, bukan spasi manual
- [x] Berlaku untuk: Rumus 2.1, 2.3, 2.4, 2.5, 2.6, dan 3.1

---

### T-7: Hapus kata ambigu "tersebut" dan kata ambigu lainnya
- [x] Lakukan global search untuk kata *"tersebut"* — ganti setiap kemunculan dengan rujukan eksplisit ke nama konsep, tabel, gambar, atau bab yang dimaksud
- [x] Lakukan hal yang sama untuk: *"di atas"*, *"di bawah"*, *"sebelumnya"*, *"setelahnya"*

---

## 🔵 STRUKTUR & KORELASI JUDUL c

### ST-1: Konfirmasi judul ke pembimbing
- [x] Diskusikan dengan pembimbing apakah frasa *"Fast Forward Moving Picture Experts Group"* di judul sudah tepat secara akademik, mengingat yang menjadi metode adalah *Stream Copy*, bukan keseluruhan FFmpeg sebagai framework
- [x] Catat hasil diskusi dan sesuaikan judul jika diperlukan

---

### ST-2: Tambahkan kalimat penghubung Bab II → Bab III untuk algoritma
- [ ] Di awal penjelasan **Algoritma Deteksi Ambang Batas** di Bab III, tambahkan kalimat yang merujuk ke sub-bab 2.1.7: *"...sebagaimana diuraikan pada sub-bab 2.1.7..."*
- [ ] Di awal penjelasan **Algoritma Perhitungan Offset** di Bab III, tambahkan kalimat pengantar yang menjelaskan logika rumus berasal dari karakteristik Replay Buffer OBS

---

## 📊 Ringkasan Progress Revisi

| Kategori | Total Item | Selesai | Status |
|----------|-----------|---------|--------|
| 🔴 Kritis (K) | 5 | 0 | 🔴 Belum |
| 🟠 Substansi (S) | 11 | 0 | 🔴 Belum |
| 🟡 Teknis Penulisan (T) | 7 | 0 | 🔴 Belum |
| 🔵 Struktur (ST) | 2 | 0 | 🔴 Belum |
| **Total** | **25** | **0** | |

> Update tabel ini secara berkala setelah menyelesaikan setiap kategori.
> 🔴 Belum dimulai | 🟡 Sedang dikerjakan | 🟢 Selesai

---

## 📌 Urutan Pengerjaan yang Disarankan

### Hari 1–2 (Darurat, kerjakan dulu)
1. K-1 — Hapus semua kata "penulis"
2. S-3 — Perbaiki referensi nomor gambar yang salah
3. T-4 — Perbaiki semua typo

### Hari 3–4 (Substansi besar)
4. K-2 — Tulis ulang abstrak
5. K-3 — Tambahkan gambaran sistem lama vs baru
6. K-4 — Perbaiki tujuan penelitian agar terukur

### Hari 5–6 (Bab II)
7. S-5 — Tambahkan sub-bab 2.1.7 Time-Persistence Thresholding *(draft sudah ada)*
8. S-7 — Terapkan revisi sub-bab Iterative Incremental *(draft sudah ada)*
9. S-8 — Terapkan revisi sub-bab dBFS *(draft sudah ada)*
10. S-10 — Pangkas FastAPI dan ReactJS
11. S-6 — Tambahkan 2 penelitian terkait

### Hari 7 (Finishing)
12. T-1 — Standarkan italic semua kata asing
13. T-2 — Standarkan OBS-WebSocket
14. T-3 — Standarkan Black Box Testing
15. T-6 — Perbaiki format rumus ke Equation Editor
16. T-7 — Hapus kata "tersebut" yang ambigu
17. K-5, S-1, S-2, S-4, S-9, S-11, ST-1, ST-2 — selesaikan sisa item

---

*File ini dibuat berdasarkan sesi bimbingan Mei 2026.*
*Update progress dengan mengisi centang `[x]` pada setiap item yang sudah selesai.*
