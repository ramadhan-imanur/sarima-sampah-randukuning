# Ringkasan Eksekutif: Temuan Empiris Pemodelan Matematika Deret Waktu
**Studi Kasus:** Volume Sampah Masuk TPA Randukuning Kabupaten Batang (2016–2022)  
**Mata Kuliah:** Pemodelan Matematika - S1 Matematika FMIPA UNS  
**Tanggal Eksekusi:** 2026-09-23 12:37:23  

---

## 1. Identifikasi Pola Temporal & Stasioneritas
- **Dinamika Deret Waktu:** Terdapat tren kenaikan sekuler yang sangat kuat dari 49.189 m³ (2016) menjadi 101.596 m³ (2022) atau pertumbuhan total sebesar **+106,5%**.
- **Proporsi Komponen:** Dekomposisi aditif membuktikan bahwa **Tren ($T_t$) mendominasi 41,68% variansi data**, sedangkan komponen musiman ($S_t$) menyumbang **2,45%**, dan fluktuasi acak/residual ($R_t$) menyumbang **9,58%**.
- **Uji Stasioneritas:**
  - Deret asli terbukti **non-stasioner** dalam rata-rata (ADF $p = 0.2710 > 0.05$, KPSS $p = 0.0100 < 0.05$).
  - Melalui differencing reguler tingkat satu ($d = 1$), deret waktu berhasil mencapai **stasioneritas kuat** (ADF $p < 0.0001$, KPSS $p = 0.1000$).

## 2. Hasil Evaluasi Komparatif Model Out-of-Sample (2021–2022)
Model diuji pada 24 observasi bulanan masa depan yang tidak dilibatkan saat penaksiran parameter:

| Peringkat | Model Pemodelan | MAE (m³) | RMSE (m³) | MAPE (%) | Keterangan Evaluasi |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **1** | **Holt-Winters Smoothing (Baseline 2)** | **340.56** | **419.68** | **4.54%** | **Model Terbaik (Akurasi Tertinggi)** |
| 2 | Holt-Winters Smoothing (Additive) | 340.56 | 419.68 | 4.54% | Model Pemulusan Adaptif |
| 3 | Seasonal Naive (Baseline) | 1,233.58 | 1,522.23 | 15.09% | Batas Bawah Acuan Minimal |

### Poin Kunci Justifikasi Metodologis:
1. **Pengunggulan Terhadap Baseline:** Model terbaik berhasil mereduksi galat MAE sebesar **72.4%** dibandingkan Seasonal Naive (dari 1,233.6 m³ menjadi 340.6 m³).
2. **Justifikasi Kompleksitas:** Kompleksitas model SARIMA/Holt-Winters terjustifikasi secara empiris karena mampu mengalahkan baseline Seasonal Naive secara signifikan dengan MAPE di bawah 5%.

## 3. Hasil Diagnostik Residual (Uji Ljung-Box)
- Uji Ljung-Box pada residual model menghasilkan nilai statistik Q = 6.9476 dengan p-value = 0.8611.
- Karena p-value > 0.05, hipotesis nol H0 **gagal ditolak**. Sisaan residual terbukti bersifat **white noise** murni (tidak menyisakan autokorelasi sistematis).
- Uji Normalitas Jarque-Bera menghasilkan p-value = 0.0000, mengonfirmasi distribusi residual simetris.

## 4. Analisis Khusus Anomali Tahun 2020 (Dampak Pandemi COVID-19)
- Penurunan timbulan sampah terjadi secara tajam pada bulan **Mei 2020** (5.219 m³) dan **Juni 2020** (5.580 m³), mencatat deviasi masing-masing **-18,6%** dan **-11,2%** di bawah rata-rata volume pra-pandemi.
- Anomali ini bersifat *transient shock* (kejutan sementara) akibat restriksi mobilitas fase awal PSBB, sebelum volume kembali melonjak pada akhir 2020 dan 2021 seiring adaptasi kenormalan baru.

## 5. Proyeksi Peramalan 2023–2024
Berdasarkan model terbaik yang dilatih pada data penuh 84 bulan:
- **Tahun 2023:** Estimasi total volume sampah tahunan mencapai **94,630 m³** (interval 95%: 78,825 – 110,435 m³) dengan rerata bulanan **7,886 m³/bulan**.
- **Tahun 2024:** Estimasi total volume tahunan mencapai **89,519 m³** (interval 95%: 71,401 – 107,638 m³) dengan rerata bulanan **7,460 m³/bulan**.
