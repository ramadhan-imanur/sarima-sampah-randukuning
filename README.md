# Pemodelan Matematika Deret Waktu: Dinamika & Proyeksi Timbulan Sampah TPA Randukuning Batang (2016–2022)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests: Pytest](https://img.shields.io/badge/tests-pytest-green.svg)](https://docs.pytest.org/)

Repositori ini memuat implementasi komputasi dan analisis ekonometrika deret waktu (*time series forecasting*) terstandarisasi untuk pemodelan volume sampah bulanan yang masuk ke **Tempat Pemrosesan Akhir (TPA) Randukuning, Kabupaten Batang, Jawa Tengah** periode **2016–2022** (84 observasi bulanan).

> **Konteks Akademis:**  
> Program Studi S1 Matematika, Fakultas Matematika dan Ilmu Pengetahuan Alam (FMIPA)  
> **Universitas Sebelas Maret (UNS)**, Surakarta.  
> Mata Kuliah: *Pemodelan Matematika*.

---

## 1. Latar Belakang & Pertanyaan Riset

Volume sampah yang masuk ke TPA Randukuning melonjak secara drastis dari **49.189 m³** (2016) hingga mencapai **101.596 m³** (2022), atau tumbuh sebesar **+106,5%**. Lonjakan ini dipicu oleh pertumbuhan demografi pesisir dan akselerasi kegiatan ekonomi di Kabupaten Batang. Selain tren sekuler yang kuat, data menunjukkan adanya fluktuasi musiman tahunan dan kejutan eksternal (*transient shock*) berupa penurunan volume pada Mei–Juni 2020 akibat pembatasan sosial pandemi COVID-19.

Penelitian ini menjawab 4 pertanyaan utama:
1. Bagaimana karakteristik pola temporal, tren jangka panjang, dan musiman tahunan data volume sampah TPA Randukuning?
2. Bagaimana memformulasikan model *Seasonal Autoregressive Integrated Moving Average* (SARIMA) dan model pembanding (*benchmarks*) secara matematis?
3. Apakah model stokastik kompleks (SARIMA/Holt-Winters) secara empiris mampu mengungguli model acuan batas bawah (*Seasonal Naive*) pada data uji *out-of-sample*?
4. Bagaimana sifat anomali timbulan pada periode pandemi 2020 dan bagaimana proyeksi timbulan sampah untuk tahun 2023–2024?

---

## 2. Hierarki Model & Metodologi

Untuk menghindari *model selection bias*, model dievaluasi secara berjenjang dengan partisi waktu yang ketat (*Time-Based Split*: **60 bulan latih (2016–2020)** vs **24 bulan uji (2021–2022)**) tanpa kebocoran data (*no data leakage*):

$$\text{Seasonal Naive (Baseline 1)} \longrightarrow \text{Holt-Winters Smoothing (Baseline 2)} \longrightarrow \text{SARIMA}(p,d,q)(P,D,Q)_{12}$$

1. **Seasonal Naive (Baseline 1)**: $\hat{Y}_{t+h} = Y_{t+h-12}$
2. **Holt-Winters Exponential Smoothing (Baseline 2)**: Menangani taraf ($L_t$), tren linear ($b_t$), dan musiman aditif ($S_t$, $s=12$).
3. **SARIMA$(p,d,q)(P,D,Q)_{12}$**: Formulasi stokastik non-stasioner musiman dengan operator differencing $(1-B)^d (1-B^{12})^D$.

---

## 3. Hasil Temuan Empiris

### A. Evaluasi Kinerja Out-of-Sample (24 Bulan Data Uji: 2021–2022)

| Peringkat | Model | MAE (m³) | RMSE (m³) | MAPE (%) | Justifikasi Metodologis |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **1** | **Holt-Winters (Additive)** | **340.56** | **419.68** | **4.54%** | **Model Terbaik (Akurasi Sangat Tinggi, MAPE < 5%)** |
| 2 | Seasonal Naive (Baseline) | 1,233.58 | 1,522.23 | 15.09% | Batas Bawah Acuan Minimal |

> **Poin Kunci:** Model pemulusan adaptif Holt-Winters berhasil mereduksi galat MAE hingga **72,4%** dibanding Seasonal Naive, membuktikan bahwa kompleksitas pemodelan matematis sangat terjustifikasi secara empiris.

### B. Diagnostik Residual
- **Uji Ljung-Box:** $Q = 6.9476$ ($p = 0.8611 > 0.05$). Hipotesis nol $H_0$ gagal ditolak, membuktikan sisaan residual merupakan proses ***white noise* murni** (tidak mengandung autokorelasi sistematis tersisa).

### C. Proyeksi Peramalan Masa Depan
- **Tahun 2023:** Estimasi akumulasi tahunan **94.630 m³** (95% CI: 78.825 – 110.435 m³), rerata **7.886 m³/bulan**.
- **Tahun 2024:** Estimasi akumulasi tahunan **89.519 m³** (95% CI: 71.401 – 107.638 m³), rerata **7.460 m³/bulan**.

---

## 4. Struktur Repositori

```text
.
├── code/                              # Seluruh arsitektur kode dan artefak eksekusi
│   ├── README.md                      # Dokumentasi teknis rinci modul code/
│   ├── requirements.txt               # Daftar pustaka Python yang dibutuhkan
│   ├── main.py                        # Entrypoint eksekusi langsung
│   ├── run_pipeline.py                # CLI orchestrator runner lengkap
│   ├── notebooks/                     # Jupyter Notebook evaluasi interaktif
│   │   └── 01_laporan_evaluasi_pemodelan.ipynb
│   ├── src/                           # Modul package Python modular
│   │   ├── config.py                  # Konfigurasi path, hyperparameter, & style plot
│   │   ├── data_loader.py             # Validasi integritas & time-based split
│   │   ├── eda.py                     # Analisis deskriptif, uji ADF, KPSS, & dekomposisi
│   │   ├── models.py                  # Estimator Seasonal Naive, Holt-Winters, & SARIMA
│   │   ├── evaluation.py              # Metrik MAE, RMSE, MAPE, & uji Ljung-Box
│   │   ├── forecast.py                # Engine peramalan 24 bulan & agregasi tahunan
│   │   └── visualization.py           # Pembangkit figur visualisasi 300 DPI
│   ├── tests/                         # Pengujian otomatis berbasis Pytest (13 test cases)
│   │   └── test_pipeline.py
│   └── output/                        # Artefak keluaran komputasi
│       ├── figures/                   # 8 visualisasi ilmiah 300 DPI (fig01 s.d. fig08)
│       └── tables/                    # 9 berkas tabular metrik (CSV & Markdown)
├── data/                              # Dataset publikasi resmi terstruktur
│   ├── sampah_dan_penduduk_2016_2022.csv   # Dataset 84 bulan volume sampah masuk TPA
│   ├── deret_waktu_penduduk_2016_2026.csv   # Data deret waktu demografi BPS Batang
│   ├── penduduk_kecamatan_panel_2016_2026.csv
│   ├── indikator_makroekonomi_2021_2025.csv # Data PDRB ADHB & ADHK Kabupaten Batang
│   ├── pdrb_adhb_2021_2025.csv
│   ├── pdrb_adhk_2021_2025.csv
│   ├── matriks_jumlah_penduduk_2016_2026.csv
├── .gitignore                         # Filter berkas cache, rahasia, draf, & catatan lokal
├── LICENSE                            # Lisensi terbuka MIT
└── README.md                          # Dokumentasi utama proyek ini
```

---

## 5. Panduan Instalasi & Eksekusi

### Persyaratan Sistem
- Python versi `>= 3.10`

### Langkah Instalasi
```bash
# 1. Kloning repositori
git clone https://github.com/ramadhan-imanur/sarima-sampah-randukuning.git
cd sarima-sampah-randukuning/code

# 2. Buat virtual environment (opsional namun disarankan)
python3 -m venv venv
source venv/bin/activate  # Di Windows: venv\Scripts\activate

# 3. Pasang dependensi
pip install -r requirements.txt
```

### Menjalankan Pipeline
```bash
# Menjalankan pipeline lengkap (termasuk Grid Search SARIMA):
python3 run_pipeline.py

# Atau menjalankan mode cepat (parsimonious model optimal):
python3 run_pipeline.py --quick

# Atau via entrypoint utama:
python3 main.py
```

### Menjalankan Pengujian Unit (Testing)
```bash
pytest tests/ -v
```

---

## 6. Sumber Data & Lisensi

- **Sumber Data Primer:** Dinas Lingkungan Hidup (DLH) Kabupaten Batang & Badan Pusat Statistik (BPS) Kabupaten Batang (Publikasi resmi *Kabupaten Batang Dalam Angka* & *PDRB Kabupaten Batang Menurut Pengeluaran*).
- **Lisensi Kode:** Proyek ini didistribusikan di bawah lisensi [MIT](LICENSE).
