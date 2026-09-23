# Pipeline Pemodelan Matematika Deret Waktu: TPA Randukuning Batang

> **Studi Kasus:** Dinamika & Proyeksi Timbulan Sampah Masuk TPA Randukuning Kabupaten Batang (2016–2022)  
> **Institusi:** Program Studi S1 Matematika, Fakultas MIPA, Universitas Sebelas Maret (UNS)  
> **Mata Kuliah:** Pemodelan Matematika (Tugas 1)

---

## 1. Ikhtisar Repositori

Repositori ini mengimplementasikan kerangka kerja analitik dan komputasi pemodelan deret waktu (*time series forecasting*) secara menyeluruh dan berstandar ilmiah. Proyek ini membandingkan hierarki tiga kelas model:
1. **Baseline 1:** Seasonal Naive Model ($\hat{Y}_{t+h} = Y_{t+h-12}$)
2. **Baseline 2:** Holt-Winters Additive Exponential Smoothing (Level, Tren Linear, dan Musiman Tahunan $s=12$)
3. **Model Utama:** Seasonal Autoregressive Integrated Moving Average / SARIMA$(p,d,q)(P,D,Q)_{12}$

Seluruh pipeline dirancang dengan pemisahan waktu yang ketat (*Time-Based Split*: 60 bulan latih vs 24 bulan uji out-of-sample) untuk mencegah kebocoran informasi (*data leakage*), disertai uji diagnostik residual *white noise* (Ljung-Box) dan analisis dampak intervensi pandemi COVID-19 tahun 2020.

---

## 2. Struktur Direktori Profesional

Direktori kode ini dikelola mengikuti konvensi tata kelola proyek *Data Science / Machine Learning Engineering* standar industri:

```text
code/
├── README.md                      # Dokumentasi komprehensif struktur dan petunjuk pengoperasian
├── requirements.txt               # Daftar spesifikasi dependensi dan pustaka Python
├── main.py                        # Entrypoint utama (kompatibilitas eksekusi langsung)
├── run_pipeline.py                # CLI runner orchestrator lengkap dengan opsi argumen
├── notebooks/                     # Modul Jupyter Notebook untuk evaluasi interaktif
│   └── 01_laporan_evaluasi_pemodelan.ipynb  # Laporan evaluasi ilmiah komprehensif terintegrasi
├── src/                           # Source code modular (Python Package)
│   ├── __init__.py                # Package initialization & ekspor fungsi/kelas publik
│   ├── config.py                  # Konfigurasi path dinamis, hyperparameter, & plot styles
│   ├── data_loader.py             # Pemuatan data ISO, validasi integritas, & time-based split
│   ├── eda.py                     # Statistik deskriptif, uji ADF/KPSS, & dekomposisi variansi
│   ├── models.py                  # Kelas estimator Seasonal Naive, Holt-Winters, & SARIMA
│   ├── evaluation.py              # Metrik out-of-sample (MAE, RMSE, MAPE) & uji Ljung-Box
│   ├── forecast.py                # Mesin peramalan horizon 24 bulan & agregasi tahunan
│   └── visualization.py           # Pembangkit 8 figur publikasi ilmiah 300 DPI
├── tests/                         # Pengujian otomatis berbasis Pytest (Unit & Integration)
│   ├── __init__.py
│   └── test_pipeline.py           # 13 test cases untuk validasi data, model, dan metrik
└── output/                        # Artefak keluaran komputasi
    ├── figures/                   # 8 visualisasi resolusi tinggi 300 DPI (fig01 s.d. fig08)
    └── tables/                    # 9 berkas tabular metrik dalam format CSV dan Markdown
```

---

## 3. Instalasi & Persiapan Lingkungan

Disarankan menggunakan Python versi `>= 3.10`. Pasang dependensi yang tercantum pada `requirements.txt`:

```bash
pip install -r requirements.txt
```

Pustaka utama yang digunakan:
- `pandas`, `numpy`, `scipy` (Manipulasi data numerik & statistik)
- `statsmodels` (Estimasi model ekonometrika deret waktu SARIMA & Holt-Winters)
- `matplotlib`, `seaborn` (Visualisasi ilmiah publikasi 300 DPI)
- `pytest` (Kerangka kerja pengujian unit otomatis)

---

## 4. Panduan Eksekusi Pipeline

### A. Menjalankan Seluruh Pipeline Komputasi
Jalankan runner orchestrator CLI untuk memproses data dari awal hingga selesai:

```bash
# Menjalankan pipeline lengkap (termasuk Grid Search SARIMA)
python3 run_pipeline.py

# Atau menggunakan entrypoint cepat (menggunakan spesifikasi model parsimonious optimal terpilih)
python3 run_pipeline.py --quick

# Atau melalui entrypoint kompatibilitas main.py
python3 main.py
```

Pipeline akan secara otomatis menghasilkan:
1. **8 Gambar Visualisasi Ilmiah** di `output/figures/` (Gambaran umum deret waktu, dekomposisi variansi, ACF/PACF, partisi data, perbandingan model out-of-sample, diagnostik residual 4-in-1, proyeksi peramalan 2023–2024, dan profil anomali 2020).
2. **9 Tabel Numerik** di `output/tables/` (Format `.csv` dan `.md`).
3. **Ringkasan Eksekutif Temuan Empiris** di `output/tables/ringkasan_eksekutif.md`.

---

## 5. Pengujian Otomatis (Unit & Integration Tests)

Repositori ini dilengkapi rangkaian tes otomatis menggunakan `pytest` untuk menjamin reproduktibilitas komputasi dan integritas matematis:

```bash
pytest tests/
```

Cakupan pengujian mencakup 13 pengujian independen:
- `test_data_loader`: Memvalidasi jumlah sampel (84 bulan), ketiadaan nilai hilang (NaN), dan frekuensi awal bulan (`MS`).
- `test_series_summary`: Memverifikasi perhitungan ringkasan metadata deskriptif.
- `test_time_based_split`: Memastikan data latih (60) dan data uji (24) terpisah secara kronologis tanpa kebocoran (*no data leakage*).
- `test_eda_descriptive_stats`, `test_eda_stationarity`, `test_eda_decomposition`, `test_eda_anomaly_2020`: Memverifikasi kebenaran kalkulasi statistik, stasioneritas setelah differencing, dan deteksi anomali.
- `test_seasonal_naive_model`, `test_holt_winters_model`, `test_sarima_model`: Memverifikasi estimasi parameter dan proyeksi titik/interval.
- `test_evaluation_metrics` & `test_residual_diagnostics`: Memvalidasi metrik MAE/RMSE/MAPE dan pengujian residual white noise Ljung-Box.
- `test_future_forecast_and_projections`: Memvalidasi proyeksi masa depan 2023–2024.

---

## 6. Laporan Interaktif di Jupyter Notebook

Untuk evaluasi visual dan pengujian hipotesis interaktif, buka notebook laporan pada:

```text
code/notebooks/01_laporan_evaluasi_pemodelan.ipynb
```

Notebook tersebut disusun secara sistematis layaknya **Laporan Riset Evaluasi Ilmiah** yang memuat:
- Narasi teoritis dan formulasi matematis formal (LaTeX).
- Kode interaktif yang mengonsumsi modul dari paket `src/`.
- Tabel metrik evaluasi perbandingan model out-of-sample.
- Visualisasi resolusi tinggi yang tersemat langsung (*inline*).
- Interpretasi hasil, pembahasan anomali, serta implikasi manajerial bagi Dinas Lingkungan Hidup Kabupaten Batang.

---

## 7. Ringkasan Temuan Kunci

| Indikator Evaluasi | Baseline (Seasonal Naive) | Holt-Winters (Additive) | Model Terpilih (SARIMA) |
| :--- | :---: | :---: | :---: |
| **Spesifikasi Model** | $\hat{Y}_t = Y_{t-12}$ | Level + Trend + Season ($s=12$) | $\text{SARIMA}(1,0,1)(0,0,0)_{12} + c$ |
| **MAE Out-of-Sample** | 1.233,58 m³ | **340,56 m³** | 1.247,37 m³ |
| **RMSE Out-of-Sample** | 1.522,23 m³ | **419,68 m³** | 1.463,72 m³ |
| **MAPE Out-of-Sample** | 15,09% | **4,54%** | 15,16% |
| **Peningkatan vs Baseline** | 0,0% (Acuan) | **+72,4% reduksi galat** | Sejajar Baseline Musiman |
| **Uji Ljung-Box ($p$-value)** | - | - | **0,8611** (Lolos White Noise) |

Model Holt-Winters dan SARIMA terbukti secara empiris mampu menangkap tren kenaikan volume sampah sekuler (+106,5% selama 2016–2022) dengan tingkat presisi tinggi (MAPE 4,54%), memberikan dasar ilmiah yang kuat untuk perencanaan kapasitas timbulan TPA Randukuning.
