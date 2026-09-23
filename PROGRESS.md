# Status Progres: Tugas 1 (Pemodelan Matematika Timbulan Sampah TPA Randukuning Batang)

Dokumen ini adalah **Progress Tracker Lokal Tugas 1** pada repositori mata kuliah Pemodelan Matematika `/media/ramadhan/0C6A-1ABD/University/Pemodelan Matematika/Tugas 1/`.

---

## 1. Status Terkini
- **Fase**: **KESEPAKATAN METODOLOGIS BARU (SARIMA & DERET WAKTU), PEMBARUAN DESKRIPSI & PROPOSAL 9-TAHAP, SERTA GRAPHIFY REFRESH SELESAI**
- **Fokus Aktif**: Mempersiapkan skrip pemodelan deret waktu Python (EDA, pembagian data berbasis waktu, baseline Seasonal Naive & Holt-Winters, grid-search SARIMA, dan uji Ljung-Box).
- **Status Akhir Komponen**:
  1. **Dokumen Kesepakatan Dasar (`.raw/catatan1.md`)**: **TERINTEGRASI PENUH** (Menetapkan model utama SARIMA$(p,d,q)(P,D,Q)_{12}$, pembanding Seasonal Naive dan Holt-Winters, validasi out-of-sample time-based split, diagnostik residual white noise, dan analisis objektif anomali 2020).
  2. **Dokumen Deskripsi Tugas (`deskripsi/deskripsi_tugas.md`)**: **TERBARUKAN & TERSTRUKTUR** (Menyajikan latar belakang deret waktu 84 bulan DLH, formulasi SARIMA dan baseline, prosedur estimasi/validasi/diagnostik, keterbatasan, dan keselarasan dengan RPS UNS).
  3. **Dokumen Proposal Riset (`deskripsi/proposal_riset.md`)**: **TERBARUKAN DENGAN FORMAT 9-TAHAP** (Research question -> data -> assumption -> mathematical model -> experiment -> evidence -> conclusion -> application/model -> evaluation; ditulis dengan bahasa sederhana dan menyediakan ruang pengisian bertanda `[ ... Kosong: ... ]`).
  4. **Basis Data Knowledge Graph Lokal (`.neuron/graph.json` & `GRAPH_REPORT.md`)**: **TER-GRAPHIFY REFRESH** (Bertambah dari 33 nodes/41 edges menjadi **41 nodes, 55 edges, dan 7 klaster komunitas tematik**).
  5. **Dataset Runtun Waktu Volume Sampah (84 observasi bulanan 2016–2022)**: **LENGKAP & SIAP PAKAI** (`.raw/` dan `data/`).
  6. **Dataset Pendukung (Demografi 15 Kecamatan & PDRB 2021–2025)**: **LENGKAP SEBAGAI REFERENSI** (`data/`).
  7. **Koleksi 9 Literatur Acuan Ilmiah Terstandarisasi**: **LENGKAP** (`referensi/pdf/`).

---

## 2. Peta Berkas Kunci (File Registry)
- `deskripsi/` -> Panduan dan formulasi teknis tugas:
  - [`deskripsi_tugas.md`](file:///media/ramadhan/0C6A-1ABD/University/Pemodelan%20Matematika/Tugas%201/deskripsi/deskripsi_tugas.md) -> Deskripsi tugas resmi pemodelan deret waktu SARIMA vs baseline (Seasonal Naive & Holt-Winters), validasi berbasis waktu, metrik MAE/RMSE/MAPE, diagnostik Ljung-Box, dan keterbatasan.
  - [`proposal_riset.md`](file:///media/ramadhan/0C6A-1ABD/University/Pemodelan%20Matematika/Tugas%201/deskripsi/proposal_riset.md) -> Proposal riset lengkap 9 tahapan dengan bahasa sederhana, lugas, dan memiliki ruang pengisian terstruktur untuk data lanjutan.
- `.raw/` -> Berkas dataset mentah & naskah riset acuan:
  - [`catatan1.md`](file:///media/ramadhan/0C6A-1ABD/University/Pemodelan%20Matematika/Tugas%201/.raw/catatan1.md) -> Dokumen kesepakatan baru (*core instruction*) pemodelan deret waktu volume sampah TPA Randukuning.
  - `volume_sampah_tpa_randukuning_2016_2022.csv` -> Data runtun waktu bulanan volume sampah masuk TPA (84 bulan).
  - `volume_sampah_harian_terangkut_2010_2023.csv` -> Data historis timbulan vs sampah terangkut tahunan BPS.
  - [`draf_artikel_pemodelan_logistik_v1.md`](file:///media/ramadhan/0C6A-1ABD/University/Pemodelan%20Matematika/Tugas%201/.raw/draf_artikel_pemodelan_logistik_v1.md) -> Manuskrip alternatif model diferensial logistik Verhulst bulanan.
  - [`draf_artikel_sistem_dinamik_dua_tingkat_v2.md`](file:///media/ramadhan/0C6A-1ABD/University/Pemodelan%20Matematika/Tugas%201/.raw/draf_artikel_sistem_dinamik_dua_tingkat_v2.md) -> Manuskrip alternatif sistem dinamik dua-tingkat aliran-stok diferensial.
- `data/` -> Berkas dataset olahan terstruktur:
  - `sampah_dan_penduduk_2016_2022.csv` -> Integrasi tahunan volume sampah, populasi, laju timbulan per kapita, dan akumulasi.
  - `deret_waktu_penduduk_2016_2026.csv` -> Deret waktu populasi resmi BPS (SP2020 & PDRB 2021–2025).
  - `penduduk_kecamatan_panel_2016_2026.csv` -> Data panel terstruktur 15 kecamatan x 7 periode observasi.
  - `indikator_makroekonomi_2021_2025.csv` -> Indikator PDRB ADHB, ADHK, PK-RT, dan PDRB per kapita riil/nominal.
- `.final/` -> Ruang penulisan naskah laporan hasil akhir:
  - Direservasi untuk naskah manuskrip laporan pemodelan matematika (`laporan_akhir.md` / `laporan_akhir.tex`).
- `.neuron/` -> Basis data relasi pengetahuan lokal Tugas 1:
  - [`graph.json`](file:///media/ramadhan/0C6A-1ABD/University/Pemodelan%20Matematika/Tugas%201/.neuron/graph.json) -> Subgraf lokal Tugas 1 (41 nodes, 55 edges, 7 komunitas).
  - [`GRAPH_REPORT.md`](file:///media/ramadhan/0C6A-1ABD/University/Pemodelan%20Matematika/Tugas%201/.neuron/GRAPH_REPORT.md) -> Laporan aksesibel graf Tugas 1.
- `referensi/pdf/` -> Koleksi 9 literatur rujukan ilmiah (format: `NamaBelakang (Tahun) - Judul`).
- `tools/` -> Skrip komputasi dan otomasi:
  - [`proses_data_sampah_demografi.py`](file:///media/ramadhan/0C6A-1ABD/University/Pemodelan%20Matematika/Tugas%201/tools/proses_data_sampah_demografi.py) -> Otomasi konsolidasi data dan korelasi statistik.
  - [`generate_graph_report.py`](file:///media/ramadhan/0C6A-1ABD/University/Pemodelan%20Matematika/Tugas%201/tools/generate_graph_report.py) -> Generator laporan terstruktur untuk Knowledge Graph Tugas 1.
- `arsip/` -> Ruang arsip draf versi lama dan berkas backup.

---

## 3. Ringkasan Kerangka Pemodelan Tersepakati (SARIMA & Baselines)
Sesuai dengan kesepakatan pada `.raw/catatan1.md`:

1. **Variabel Target**:
   - Volume bulanan sampah masuk TPA Randukuning ($Y_t$ dalam $\text{m}^3$), $t = 1, \dots, 84$ (Januari 2016 – Desember 2022).
   - Catatan: Baris total tahunan tidak dicampurkan ke dalam observasi bulanan.

2. **Hierarki Model**:
   - **Baseline 1 (Seasonal Naive)**: $\hat{Y}_t = Y_{t-12}$
   - **Baseline 2 (Holt-Winters Smoothing)**: Level + Tren + Musiman tahunan ($s=12$)
   - **Model Utama (SARIMA)**: $\Phi_P(B^{12}) \phi_p(B) (1 - B)^d (1 - B^{12})^D Y_t = \Theta_Q(B^{12}) \theta_q(B) \epsilon_t$

3. **Prinsip Validasi & Evaluasi**:
   - Time-based Split: Data latih (2016–2020: 60 observasi) vs Data uji (2021–2022: 24 observasi) / Rolling window.
   - Metrik: MAE, RMSE, MAPE pada data uji out-of-sample.
   - Diagnostik: Uji Ljung-Box untuk memastikan residual berupa *white noise* ($p > 0{,}05$).
   - Perlakuan 2020: Diperiksa sebagai potensi *structural break* (intervensi pandemi) secara empiris.

---

## 4. Roadmap Pengerjaan Tugas 1
- [x] Restrukturisasi direktori Tugas 1 sesuai pola profesional modul universitas.
- [x] Standardisasi seluruh penamaan berkas rujukan ilmiah (`NamaBelakang (Tahun) - Judul`).
- [x] Unpivoting dan standardisasi data deret waktu volume sampah bulanan (84 observasi).
- [x] Pembersihan data sosio-demografi 15 kecamatan (2016–2026) dan agregat makroekonomi PDRB.
- [x] Integrasi dokumen kesepakatan baru `.raw/catatan1.md` sebagai *core instruction*.
- [x] Reformulasi dokumen `deskripsi/deskripsi_tugas.md` sesuai metodologi deret waktu SARIMA & baselines.
- [x] Reformulasi dokumen `deskripsi/proposal_riset.md` mengikuti struktur 9-tahap penelitian dengan bahasa sederhana dan ruang pengisian terstruktur.
- [x] Pembaruan Knowledge Graph (Graphify) lokal menghasilkan 41 nodes, 55 edges, dan 7 komunitas tematik pada `.neuron/graph.json` dan `.neuron/GRAPH_REPORT.md`.
- [x] Implementasi skrip Python pemodelan deret waktu lengkap pada `code/` (EDA, Holt-Winters, grid-search SARIMA, uji Ljung-Box, evaluasi MAE/RMSE/MAPE, 8 visualisasi ilmiah, dan ekspor tabel tabular).
- [ ] Penyusunan naskah laporan tugas akhir / makalah pemodelan matematika pada `.final/`.

---

## 5. Log Riwayat Sesi (Changelog Tugas 1)
- **[2026-09-15 20:03]**: Merapikan CSV volume sampah bulanan menjadi deret waktu 2 kolom standar ISO (84 baris).
- **[2026-09-15 21:03]**: Pembuatan Knowledge Graph Graphify lokal dan pelaporan `GRAPH_REPORT.md`.
- **[2026-09-15 21:48]**: Mendekomposisi berkas draf riset awal menjadi naskah artikel logistik V1 dan sistem dinamik dua-tingkat V2.
- **[2026-09-15 22:44]**: Mengintegrasikan subgraf Tugas 1 ke dalam Pusat Neuron Utama Repositori.
- **[2026-09-16 10:28]**: Menyusun draf awal proposal riset 9 tahapan (Research question -> data -> assumption -> mathematical model -> experiment -> evidence -> conclusion -> application/model -> evaluation) dengan bahasa sederhana dan ruang kosong terstruktur.
- **[2026-09-16 10:31]**: Menerima kesepakatan metodologis baru dari `.raw/catatan1.md` (fokus pemodelan deret waktu SARIMA musiman $s=12$ vs baseline Seasonal Naive & Holt-Winters, evaluasi out-of-sample, dan diagnostik residual Ljung-Box).
- **[2026-09-16 10:32]**: Memperbarui `deskripsi/deskripsi_tugas.md` secara komprehensif mengikuti kesepakatan baru dari `catatan1.md`.
- **[2026-09-16 10:32]**: Memperbarui `deskripsi/proposal_riset.md` dengan menyelaraskan isi ke paradigma deret waktu SARIMA dan baseline komparatif dalam format 9-tahap.
- **[2026-09-16 10:33]**: Menjalankan Graphify lokal: menambahkan simpul baru Komunitas 6 (`catatan_riset_kesepakatan_baru`, `model_sarima_musiman_12`, `baseline_seasonal_naive`, `baseline_holt_winters`, `skema_validasi_time_split`, `uji_diagnostik_residual_ljung_box`, `analisis_anomali_covid_2020`, `proposal_riset_9_tahap`) menghasilkan **41 nodes, 55 edges, 7 komunitas** pada `graph.json` dan memperbarui `GRAPH_REPORT.md`.
- **[2026-09-23 11:35]**: Mengimplementasikan arsitektur kode program Python modular di `code/` (`config.py`, `data_loader.py`, `eda.py`, `models.py`, `evaluation.py`, `forecast.py`, `visualization.py`, `main.py`). Mengeksekusi pipeline komputasi end-to-end: pembuktian empiris SARIMA(1,0,1)(0,0,0)₁₂ mengungguli Seasonal Naive sebesar 72,5% (MAE 339,65 m³ vs 1.233,58 m³), lolos uji residual white noise Ljung-Box ($p = 0,9254$), generasi 8 visualisasi ilmiah 300 DPI di `code/output/figures/`, ekspor 9 tabel tabular di `code/output/tables/`, serta integrasi bukti numerik ke `deskripsi/rencana_riset.md`.
- **[2026-09-23 12:35]**: Merestrukturisasi direktori `code/` ke standar profesional Data Science (arsitektur `src/`, `notebooks/`, `tests/`, `output/`). Mengimplementasikan paket modular `src/__init__.py`, membuat CLI orchestrator `run_pipeline.py`, menyusun berkas dependensi `requirements.txt`, membuat dokumentasi `README.md`, menyusun 13 pengujian otomatis `tests/test_pipeline.py` (100% lulus pada Pytest), serta membuat Jupyter Notebook laporan evaluasi komprehensif 32 cell terintegrasi di `code/notebooks/01_laporan_evaluasi_pemodelan.ipynb` dengan 8 visualisasi ilmiah 300 DPI dan tabel pre-rendered.
