# Deskripsi Tugas 1: Pemodelan Deret Waktu Volume Sampah Masuk TPA Randukuning Kabupaten Batang Periode 2016–2022

Dokumen ini memuat spesifikasi teknis dan metodologis untuk Tugas 1 (Team-Based Project) pada mata kuliah Pemodelan Matematika, Program Studi S1 Matematika FMIPA Universitas Sebelas Maret (UNS). Dokumen ini mengacu pada Rencana Pembelajaran Semester (RPS) resmi serta kesepakatan penelitian terstandarisasi.

---

## 1. Latar Belakang dan Deskripsi Masalah

Volume sampah yang masuk ke Tempat Pemrosesan Akhir (TPA) Randukuning Kabupaten Batang berubah secara dinamis dari waktu ke waktu. Perubahan volume tersebut dipengaruhi oleh dinamika aktivitas antropogenik warga, pertumbuhan populasi, kondisi sosial ekonomi wilayah pesisir, serta siklus musiman tahunan.

Data pencatatan resmi mencatat volume sampah bulanan yang masuk ke TPA Randukuning selama rentang 7 tahun (2016–2022). Dengan 12 bulan observasi per tahun, diperoleh total deret waktu:

$$N = 7 \times 12 = 84 \text{ observasi bulanan}$$

Volume tahunan memperlihatkan kenaikan signifikan: $49.189\text{ m}^3$ (2016), $71.950\text{ m}^3$ (2017), $76.513\text{ m}^3$ (2018), $81.632\text{ m}^3$ (2019), $79.692\text{ m}^3$ (2020), $86.664\text{ m}^3$ (2021), hingga mencapai $101.596\text{ m}^3$ (2022). Pada tahun 2020, terjadi anomali perlambatan laju timbulan yang bertepatan dengan masa pembatasan mobilitas sosial pandemi COVID-19.

Permasalahan utama yang dikaji adalah bagaimana membangun model matematis deret waktu yang mampu merepresentasikan pola temporal, tren, dan musiman volume sampah tersebut, serta menghasilkan peramalan (*forecasting*) masa depan yang dapat dipertanggungjawabkan secara metodologis.

Tugas ini menjawab empat pertanyaan penelitian utama:
1. Bagaimana karakteristik pola temporal, tren jangka panjang, dan pola musiman tahunan dari volume sampah yang masuk ke TPA Randukuning?
2. Bagaimana memformulasikan model Seasonal Autoregressive Integrated Moving Average (SARIMA) musiman 12-bulanan pada deret waktu tersebut?
3. Bagaimana kinerja peramalan model SARIMA jika dibandingkan secara empiris dengan model pembanding sederhana (Seasonal Naive dan Holt-Winters)?
4. Apakah data volume sampah pada tahun 2020 memperlihatkan adanya perubahan struktur (*structural break*) yang mempengaruhi kestabilan peramalan?

---

## 2. Sumber dan Spesifikasi Data

Data primer penelitian bersumber dari data publikasi resmi:
> **Tabel: "Volume Sampah yang Masuk ke Tempat Pembuangan Akhir (TPA) Randukuning Kabupaten Batang, 2016–2022"**  
> **Instansi Sumber:** Dinas Lingkungan Hidup (DLH) Kabupaten Batang / Badan Pusat Statistik (BPS) Kabupaten Batang.

### Struktur Data Penelitian
| Variabel | Keterangan Teknis |
| :--- | :--- |
| Rentang Waktu | 2016 – 2022 (7 tahun kalender) |
| Frekuensi Pengamatan | Bulanan (Januari sampai Desember) |
| Indeks Waktu ($t$) | $t = 1, 2, \dots, 84$ |
| Variabel Target ($Y_t$) | Volume sampah masuk TPA pada bulan ke-$t$ dalam satuan meter kubik ($\text{m}^3$) |
| Jumlah Observasi ($N$) | 84 observasi runtut kronologis |
| Nilai Minimum Ekstrem | $3.275\text{ m}^3$ (Februari 2016) |
| Nilai Maksimum Ekstrem | $8.822\text{ m}^3$ (Agustus 2022) |

```
Deret Waktu: Y_1, Y_2, Y_3, ..., Y_84 (Januari 2016 s.d. Desember 2022)
```

> [!IMPORTANT]
> **Kaidah Preprocessing Data:**
> Baris "Jumlah / Total" tahunan pada tabel sumber data tidak diperlakukan sebagai observasi tambahan dalam model deret waktu karena merupakan hasil agregasi dari 12 bulan. Mencampurkan baris tahunan ke dalam deret bulanan akan merusak frekuensi data dan menghasilkan bias pemodelan.

---

## 3. Formulasi Model Matematika

Secara konseptual, volume sampah pada waktu $t$ dirumuskan sebagai kombinasi fungsi komponen temporal:

$$Y_t = f(Y_{t-1}, Y_{t-2}, \dots, Y_{t-k}, t, \text{seasonality}) + \epsilon_t$$

Untuk menghindari bias pemilihan model (*model selection bias*), penelitian ini menetapkan tiga tingkatan model secara hierarkis:

$$\text{Seasonal Naive (Baseline)} \longrightarrow \text{Holt-Winters (Smoothing)} \longrightarrow \text{SARIMA (Stokastik Utama)}$$

### A. Model Pembanding 1: Seasonal Naive (Baseline Sederhana)
Sebagai dasar pembanding awal (*benchmark*), model ini memprediksikan volume bulan tertentu sama dengan nilai realisasi pada bulan yang sama di tahun sebelumnya:

$$\hat{Y}_t = Y_{t-12}$$

Model ini sangat sederhana tanpa estimasi parameter bebas, namun berfungsi sebagai batas bawah kelayakan: jika model SARIMA yang kompleks tidak mampu mengalahkan akurasi Seasonal Naive, maka kompleksitas SARIMA tidak terjustifikasi secara metodologis.

### B. Model Pembanding 2: Holt-Winters Exponential Smoothing
Pendekatan pemulusan eksponensial musiman menangani tiga komponen sekaligus: taraf (*level* $L_t$), tren linear ($b_t$), dan musiman aditif/multiplikatif ($S_t$) dengan siklus $s = 12$:

$$\hat{Y}_{t+h} = L_t + h b_t + S_{t+h-m(k+1)}$$

Model ini merepresentasikan kelas pemodelan deterministik adaptif yang populer dalam perencanaan rantai pasok dan persampahan kota.

### C. Model Utama: SARIMA$(p,d,q)(P,D,Q)_{12}$
Model utama yang dikembangkan adalah *Seasonal Autoregressive Integrated Moving Average* dengan periode musiman tahunan $s = 12$:

$$\Phi_P(B^s) \phi_p(B) (1 - B)^d (1 - B^s)^D Y_t = \Theta_Q(B^s) \theta_q(B) \epsilon_t$$

Keterangan operator dan parameter:
- $B$: Operator pergeseran mundur (*backshift operator*), di mana $B^k Y_t = Y_{t-k}$.
- $p, d, q$: Orde autoregressive, differencing, dan moving average non-musiman.
- $P, D, Q$: Orde autoregressive, differencing, dan moving average musiman tahunan.
- $s = 12$: Periode musiman bulanan dalam 1 tahun.
- $\epsilon_t$: Galat acak (*white noise*) dengan $\mathbb{E}[\epsilon_t] = 0$ dan variansi $\sigma^2$.

> [!NOTE]
> **Prinsip Metodologis Utama:**
> Model SARIMA **tidak diasumsikan sebagai model terbaik sejak awal**. Superioritas performa SARIMA harus dibuktikan secara empiris melalui pengujian pada data testing yang tidak digunakan saat pelatihan.

---

## 4. Prosedur Estimasi, Validasi, dan Diagnostik

Pipeline penelitian dijalankan melalui tahapan berurutan:

```
Data Mentah (84 Bulan)
         │
         ▼
[Tahap 1: Preprocessing & Validasi Format ISO]
         │
         ▼
[Tahap 2: Eksplorasi Data & Plot Deret Waktu (ACF/PACF, Tren, Musiman)]
         │
         ▼
[Tahap 3: Pembagian Data Berbasis Waktu (Time-Series Split / Rolling Window)]
         │
         ├── Data Latih (2016–2020: 60 Observasi)
         └── Data Uji (2021–2022: 24 Observasi)
         │
         ▼
[Tahap 4: Estimasi Parameter Baseline & Grid Search SARIMA (Kriteria AIC/BIC)]
         │
         ▼
[Tahap 5: Diagnostik Residual (Uji White Noise & Uji Ljung-Box)]
         │
         ▼
[Tahap 6: Evaluasi Akurasi Out-of-Sample (MAE, RMSE, MAPE)]
         │
         ▼
[Tahap 7: Peramalan Masa Depan & Interval Prediksi 95%]
```

### A. Pembagian Data Berbasis Waktu (Bukan Random Split)
Karena data memiliki ketergantungan urutan waktu, pembagian data **tidak boleh dilakukan secara acak**. Skema validasi menggunakan:
- **Data Pelatihan (*Training Set*):** Januari 2016 – Desember 2020 (60 observasi awal) untuk fitting parameter.
- **Data Pengujian (*Testing Set*):** Januari 2021 – Desember 2022 (24 observasi akhir) untuk menguji keandalan peramalan.
- Skema alternatif yang disarankan adalah *rolling/expanding window validation* untuk mengevaluasi konsistensi model pada beberapa horizon peramalan.

### B. Metrik Evaluasi Kebaikan Model
Evaluasi out-of-sample diukur menggunakan tiga metrik statistik:
1. **Mean Absolute Error (MAE):**
   $$\text{MAE} = \frac{1}{n} \sum_{t=1}^n |Y_t - \hat{Y}_t| \quad (\text{satuan m}^3)$$
2. **Root Mean Squared Error (RMSE):**
   $$\text{RMSE} = \sqrt{\frac{1}{n} \sum_{t=1}^n (Y_t - \hat{Y}_t)^2} \quad (\text{memberi penalti galat ekstrem})$$
3. **Mean Absolute Percentage Error (MAPE):**
   $$\text{MAPE} = \frac{100\%}{n} \sum_{t=1}^n \left| \frac{Y_t - \hat{Y}_t}{Y_t} \right| \quad (\text{persentase galat relatif})$$

### C. Diagnostik Residual (Uji Ljung-Box)
Model yang memadai harus menghasilkan sisaan (*residual*) $e_t = Y_t - \hat{Y}_t$ yang bersifat *white noise* (tidak menyisakan korelasi yang belum tertangkap). Pengujian dilakukan dengan uji Ljung-Box:
- $H_0$: Tidak terdapat autokorelasi pada residual (residual bersifat *white noise*).
- $H_1$: Terdapat autokorelasi pada residual.
Model dinyatakan lolos uji diagnostik jika nilai $p\text{-value} > 0{,}05$.

### D. Perlakuan Khusus Terhadap Anomali Tahun 2020
Tahun 2020 diperlakukan secara objektif sebagai periode yang berpotensi mengalami perubahan struktur (*structural change / intervention*). Penelitian **tidak membuat klaim kausal terburu-buru** bahwa penurunan volume disebabkan oleh pandemi semata tanpa uji empiris. Jika terbukti terjadi structural break, hal ini dilaporkan sebagai temuan analisis dan keterbatasan model, atau dikembangkan menjadi model intervensi jika didukung data tambahan.

---

## 5. Keterbatasan Penelitian

Penelitian ini secara jujur mengakui beberapa keterbatasan:
1. **Ukuran Sampel Terbatas:** Total 84 observasi bulanan hanya mencakup 7 siklus musiman tahunan, sehingga pemilihan parameter SARIMA harus dijaga tetap sederhana guna mencegah *overfitting*.
2. **Ketiadaan Variabel Kovariat Eksternal:** Model berfokus murni pada deret waktu univariat volume sampah historis karena ketiadaan data kovariat (curah hujan, armada aktif harian) dengan resolusi bulanan yang kompatibel.
3. **Sensitivitas Terhadap Perubahan Struktur:** Kualitas peramalan bergantung pada asumsi kestabilan pola historis; perubahan drastis pada kebijakan persampahan daerah di masa depan dapat menggeser lintasan volume nyata dari hasil ramalan.

---

## 6. Keselarasan dengan RPS Pemodelan Matematika UNS

Tugas ini memenuhi capaian pembelajaran mata kuliah Pemodelan Matematika FMIPA UNS:
- **Sub-CPMK 1 sampai 4:** Identifikasi variabel keadaan, perumusan asumsi, dan pemilihan kelas model matematika yang sesuai dengan sifat data lapangan.
- **Sub-CPMK 5 sampai 8:** Implementasi komputasi numerik menggunakan Python (`statsmodels`, `pmdarima`, `scipy`, `pandas`) untuk estimasi parameter dan diagnostik.
- **Sub-CPMK 9 sampai 12:** Analisis validasi model pada data riil lingkungan daerah (studi kasus persampahan TPA Randukuning Batang).
- **Sub-CPMK 13 sampai 16:** Penyusunan laporan ilmiah berbasis proyek tim dengan kaidah penalaran matematika yang jujur, objektif, dan berbasis bukti empiris.
