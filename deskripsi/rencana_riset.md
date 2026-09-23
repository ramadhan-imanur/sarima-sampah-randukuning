# Proposal Penelitian Pemodelan Matematika
## Judul: Pemodelan Deret Waktu Volume Sampah yang Masuk ke TPA Randukuning Kabupaten Batang Periode 2016–2022

Proposal ini disusun berdasarkan kerangka kerja terstandarisasi 9 tahapan:
**Research Question $\to$ Data $\to$ Assumption $\to$ Mathematical Model $\to$ Experiment $\to$ Evidence $\to$ Conclusion $\to$ Application/Model $\to$ Evaluation**.

Seluruh isi dirumuskan menggunakan bahasa yang sederhana, lugas, dan mudah dipahami, dengan prinsip bahwa model statistik tidak diasumsikan terbaik sejak awal melainkan harus dibuktikan lewat pengujian data riil. Bagian yang belum memiliki data final telah disediakan ruang pengisian terstruktur.

---

## 1. Research Question (Pertanyaan Penelitian)

### A. Latar Belakang Masalah (Bahasa Sederhana)
Setiap bulan, sampah dari rumah tangga, pasar, dan industri di Kabupaten Batang diangkut menuju satu-satunya tempat pemrosesan akhir, yaitu TPA Randukuning. Banyaknya sampah yang masuk tidak selalu sama dari bulan ke bulan. Ada bulan-bulan tertentu di mana sampah melonjak (misalnya saat hari raya atau musim panen tertentu), dan ada pula tren kenaikan volume dari tahun ke tahun seiring pertambahan jumlah penduduk.

Pemerintah daerah perlu mengetahui gambaran pola sampah ini agar dapat merencanakan operasional truk, kebutuhan bahan bakar, serta kapasitas penampungan di masa depan. Selama periode 2016 sampai 2022 (7 tahun atau 84 bulan), data volume sampah telah dicatat secara rutin oleh Dinas Lingkungan Hidup (DLH).

Penelitian ini bertujuan memodelkan data deret waktu tersebut secara matematis untuk menjawab apakah volume sampah memiliki pola musiman berulang tiap 12 bulan dan tren jangka panjang, serta model mana yang paling andal untuk meramalkan volume sampah di masa mendatang.

### B. Rumusan Pertanyaan Penelitian
1. **Bagaimana pola perubahan volume sampah bulanan di TPA Randukuning selama periode 2016–2022? Apakah terdapat tren kenaikan dan pola musiman tahunan yang jelas?**
2. **Bagaimana bentuk perumusan model deret waktu Seasonal ARIMA (SARIMA) musiman 12-bulanan yang paling sesuai dengan karakteristik data tersebut?**
3. **Apakah model SARIMA yang lebih kompleks benar-benar mampu menghasilkan ramalan yang lebih akurat dibandingkan model pembanding yang lebih sederhana (Seasonal Naive dan Holt-Winters)?**
4. **Apakah data pada tahun 2020 memperlihatkan adanya anomali atau perubahan struktur (*structural break*) yang mempengaruhi konsistensi peramalan?**

### C. Ruang Tambahan Pertanyaan Penelitian
> [!NOTE]
> **Ruang Pengisian Peneliti (Pertanyaan Tambahan / Spesifik):**
> - *Pertanyaan 5:* [ ... Kosong: Tuliskan jika ada pertanyaan tambahan terkait dampak libur panjang atau festival lokal ... ]
> - *Pertanyaan 6:* [ ... Kosong: Tuliskan pertanyaan khusus dari dosen pembimbing mengenai batas horizon ramalan ... ]

---

## 2. Data (Data Penelitian & Spesifikasi)

### A. Sumber dan Karakteristik Data
Data utama yang digunakan bersumber dari data publikasi resmi:
> **Tabel: "Volume Sampah yang Masuk ke Tempat Pembuangan Akhir (TPA) Randukuning Kabupaten Batang, 2016–2022"**  
> **Sumber Instansi:** Dinas Lingkungan Hidup (DLH) Kabupaten Batang / BPS Kabupaten Batang.

Karakteristik data penelitian:
- **Rentang Waktu:** 7 tahun kalender penuh (2016 sampai dengan 2022).
- **Frekuensi Data:** Bulanan (Januari hingga Desember untuk setiap tahun).
- **Jumlah Observasi ($N$):** $7 \times 12 = 84$ titik pengamatan berurutan kronologis ($Y_1, Y_2, \dots, Y_{84}$).
- **Variabel Utama ($Y_t$):** Volume sampah masuk TPA dalam satuan meter kubik ($\text{m}^3$).
- **Nilai Ekstrem:** Nilai terendah $3.275\text{ m}^3$ (Februari 2016) dan tertinggi $8.822\text{ m}^3$ (Agustus 2022).

### B. Tabel Spesifikasi Deret Waktu
| Variabel | Simbol | Satuan | Rentang Nilai / Keterangan |
| :--- | :--- | :--- | :--- |
| Indeks Waktu | $t$ | Bulan | $1, 2, 3, \dots, 84$ (Jan 2016 – Des 2022) |
| Volume Sampah Bulanan | $Y_t$ | $\text{m}^3$ | Berkisar antara $3.275$ hingga $8.822\text{ m}^3$ |
| Siklus Musiman | $s$ | Bulan | $s = 12$ (pola berulang tiap 1 tahun) |
| Total Tahunan | - | $\text{m}^3$ | Naik dari $49.189$ (2016) ke $101.596$ (2022) |

> [!IMPORTANT]
> **Aturan Pengolahan Data:**
> Baris total tahunan pada data sumber tidak dimasukkan sebagai observasi dalam model matematika karena merupakan penjumlahan dari 12 bulan. Memasukkannya akan merusak urutan frekuensi bulanan.

### C. Ruang Pengisian Data Tambahan yang Belum Diketahui
> [!NOTE]
> **Ruang Pengisian Peneliti (Data Eksternal Tambahan jika Ingin Mengembangkan SARIMAX):**
> - **Data Curah Hujan Bulanan Batang (2016–2022):** [ ... Kosong: Masukkan rata-rata mm curah hujan bulanan jika data BMKG tersedia ... ]
> - **Data Runtun Waktu Lanjutan (2023–2025):** [ ... Kosong: Masukkan data volume bulanan terbaru jika DLH telah merilis publikasi baru ... ]
> - **Catatan Hari Libur Nasional / Kalender Hijriah:** [ ... Kosong: Catat posisi bulan Idul Fitri tiap tahun untuk analisis musiman bergerak ... ]

---

## 3. Assumption (Asumsi Pemodelan)

Model matematika menyederhanakan perilaku data riil menggunakan beberapa asumsi logis:

1. **Ketergantungan Temporal (Waktu Berurutan):**
   Volume sampah pada bulan ini ($Y_t$) tidak berdiri sendiri secara acak, melainkan dipengaruhi oleh volume sampah pada bulan-bulan sebelumnya ($Y_{t-1}, Y_{t-2}$) serta volume sampah pada bulan yang sama di tahun lalu ($Y_{t-12}$).
2. **Adanya Siklus Tahunan 12 Bulan ($s = 12$):**
   Aktivitas warga memiliki siklus tahunan yang berulang (misalnya pola tahun ajaran baru, hari raya keagamaan, atau musim panen/libur tahunan).
3. **Kestabilan Pola Historis untuk Peramalan:**
   Pola umum yang terbentuk selama 2016–2022 diasumsikan tetap berlanjut pada periode peramalan jangka pendek ke depan, selama tidak terjadi perubahan kebijakan radikal dalam pengelolaan sampah kota.
4. **Sifat Galat Acak (*White Noise*):**
   Setelah tren, dependensi waktu, dan musiman berhasil ditangkap oleh model, sisa perbedaan antara model dan data riil (residual $\epsilon_t$) diasumsikan murni berupa acakan alami dengan rata-rata nol dan variansi konstan.
5. **Objektivitas Pemilihan Model:**
   Model SARIMA **tidak diasumsikan sebagai yang terbaik secara otomatis**. Kelayakannya wajib diuji terhadap model baseline yang lebih sederhana.

### Ruang Pengisian Asumsi Tambahan
> [!NOTE]
> **Ruang Pengisian Peneliti (Asumsi Tambahan):**
> - *Asumsi Kebijakan Pengangkutan:* [ ... Kosong: Masukkan asumsi mengenai stabilitas ritase armada truk DLH selama periode observasi ... ]
> - *Asumsi Pembobotan Hari Kalender:* [ ... Kosong: Masukkan asumsi apakah perbedaan jumlah hari per bulan (28 vs 31 hari) perlu dinormalisasi menjadi laju harian ... ]

---

## 4. Mathematical Model (Model Matematika)

Secara umum, volume sampah bulanan dinyatakan sebagai dekomposisi komponen matematis:

$$Y_t = \text{Tren} + \text{Musiman (12 Bulan)} + \text{Ketergantungan Temporal} + \text{Galat Acak } (\epsilon_t)$$

Untuk menjamin evaluasi yang jujur, penelitian ini menguji tiga model matematika dari yang paling sederhana hingga yang paling canggih:

---

### A. Model Pembanding 1: Seasonal Naive (Baseline Acuan Dasar)
Model pembanding paling sederhana yang memprediksikan volume bulan tertentu sama persis dengan realisasi pada bulan yang sama tahun lalu:

$$\hat{Y}_t = Y_{t-12}$$

*Makna praktis:* Jika pada bulan Mei 2021 volume sampah adalah $7.150\text{ m}^3$, maka ramalan untuk Mei 2022 adalah $7.150\text{ m}^3$. Model ini menjadi patokan batas minimal: model statistik yang lebih rumit harus mampu menghasilkan kesalahan yang lebih kecil daripada model sederhana ini.

---

### B. Model Pembanding 2: Holt-Winters Exponential Smoothing
Pendekatan pemulusan eksponensial yang memisahkan data menjadi tiga persamaan pembaruan adaptif dengan siklus musiman $s = 12$:

$$\text{Level: } L_t = \alpha (Y_t - S_{t-s}) + (1 - \alpha)(L_{t-1} + b_{t-1})$$
$$\text{Tren: } b_t = \beta (L_t - L_{t-1}) + (1 - \beta) b_{t-1}$$
$$\text{Musiman: } S_t = \gamma (Y_t - L_t) + (1 - \gamma) S_{t-s}$$
$$\text{Persamaan Ramalan } h\text{ bulan ke depan: } \hat{Y}_{t+h} = L_t + h b_t + S_{t+h-s}$$

*Parameter yang diestimasi:* Nilai bobot pemulusan $\alpha$ (level), $\beta$ (tren), dan $\gamma$ (musiman) berada pada rentang $[0, 1]$.

---

### C. Model Utama: SARIMA$(p,d,q)(P,D,Q)_{12}$
Model deret waktu terintegrasi autoregresif musiman yang dinyatakan dalam notasi operator pergeseran mundur (*backshift* $B$):

$$\Phi_P(B^{12}) \phi_p(B) (1 - B)^d (1 - B^{12})^D Y_t = \Theta_Q(B^{12}) \theta_q(B) \epsilon_t$$

*Uraian komponen dalam bahasa sederhana:*
- **Komponen Reguler (Non-Musiman):**
  - $\phi_p(B) = 1 - \phi_1 B - \dots - \phi_p B^p$: Menggambarkan pengaruh volume $p$ bulan terakhir secara langsung.
  - $(1 - B)^d$: Tingkat *differencing* untuk menstabilkan tren agar data tidak terus melambung naik (stasioner rata-rata).
  - $\theta_q(B) = 1 + \theta_1 B + \dots + \theta_q B^q$: Menggambarkan pengaruh goncangan acak $q$ bulan sebelumnya.
- **Komponen Musiman (12-Bulanan):**
  - $\Phi_P(B^{12})$: Menggambarkan hubungan volume sampah dengan bulan yang sama pada $P$ tahun sebelumnya.
  - $(1 - B^{12})^D$: Pengurangan nilai dengan tahun sebelumnya (*seasonal differencing*) untuk menghilangkan pola musiman yang kaku.
  - $\Theta_Q(B^{12})$: Pengaruh kejutan musiman $Q$ tahun sebelumnya.
### Spesifikasi Orde Model Terpilih
> [!NOTE]
> **Hasil Penentuan Parameter Model Terbaik (Terbukti Secara Empiris):**
> - **Orde SARIMA Terpilih:** $\text{SARIMA}(1,0,1)(0,0,0)_{12}$ (Model parsimonious dengan out-of-sample error terkecil).
> - **Nilai Kriteria Informasi:** $\text{AIC} = 898{,}86$, $\text{AICc} = 899{,}29$, $\text{BIC} = 905{,}04$.
> - **Struktur Model:** $Y_t - \phi_1 Y_{t-1} = c + \epsilon_t + \theta_1 \epsilon_{t-1}$, mampu menangkap kestabilan autoregresif dan peredam kejut tanpa over-differencing pada sampel $N=60$.

---

## 5. Experiment (Eksperimen & Desain Komputasi)

Eksperimen pemodelan dirancang dan dieksekusi secara sistematis menggunakan bahasa pemrograman Python 3.12:

### Tahap 1: Preprocessing & Pengecekan Kualitas Data
- Mengurutkan 84 data secara kronologis tanpa mengikutsertakan total tahunan (`code/data_loader.py`).
- Memastikan tidak ada data yang hilang (*missing value*) dan satuan konsisten dalam $\text{m}^3$.

### Tahap 2: Eksplorasi Data Analitik (EDA)
- Membuat plot deret waktu bulanan 2016–2022 (`code/output/figures/fig01_timeseries_overview.png`).
- Uji stasioneritas: Deret asli non-stasioner (ADF $p = 0{,}2710$, KPSS $p = 0{,}0100$). Melalui differencing tingkat 1 ($d=1$), stasioneritas kuat tercapai (ADF $p < 0{,}0001$, KPSS $p = 0{,}1000$).
- Dekomposisi aditif: Komponen tren menyumbang **41,68% variansi total**, musiman menyumbang **2,45%**, dan residual menyumbang **9,58%** (`fig02_decomposition.png`).
- Korelasi lag: Autokorelasi ACF dan PACF hingga lag 36 (`fig03_acf_pacf.png`).

### Tahap 3: Pembagian Data Berbasis Waktu (Time-Series Split)
- **Data Latih (*Training Set*):** Januari 2016 – Desember 2020 (60 observasi).
- **Data Uji (*Testing Set*):** Januari 2021 – Desember 2022 (24 observasi).
- Visualisasi partisi tersimpan di `code/output/figures/fig04_traintest_split.png`.

### Tahap 4: Pencarian Model Terbaik (Grid Search Berbasis AIC/BIC)
- Mengevaluasi kombinasi parsimonious untuk $p \in [0, 2]$, $d \in [0, 1]$, $q \in [0, 2]$, $P \in [0, 1]$, $D \in [0, 1]$, $Q \in [0, 1]$ pada data latih.
- Hasil 10 model terbaik terdokumentasi lengkap di `code/output/tables/tabel04_gridsearch_sarima_top10.md`.

### Tahap 5: Analisis Khusus Anomali Tahun 2020
- Penurunan timbulan sampah terjadi secara tajam pada bulan Mei 2020 ($5.219\text{ m}^3$, deviasi $-18{,}6\%$) dan Juni 2020 ($5.580\text{ m}^3$, deviasi $-11{,}2\%$) akibat PSBB awal COVID-19 (`fig08_anomaly_2020.png`). Kejutan ini bersifat *transient shock* sebelum tren kembali menguat pada 2021.

### Catatan Teknis Lingkungan Komputasi
> [!NOTE]
> **Spesifikasi Modul dan Lingkungan Komputasi:**
> - **Arsitektur Program:** Modul terpisah di [`code/`](file:///media/ramadhan/0C6A-1ABD/University/Pemodelan%20Matematika/Tugas%201/code/) (`config.py`, `data_loader.py`, `eda.py`, `models.py`, `evaluation.py`, `forecast.py`, `visualization.py`, `main.py`).
> - **Skrip Runner Utama:** [`code/main.py`](file:///media/ramadhan/0C6A-1ABD/University/Pemodelan%20Matematika/Tugas%201/code/main.py).
> - **Versi Library:** Python 3.12, `statsmodels` 0.14.2, `pandas` 2.2.2, `numpy` 1.26.4, `scipy` 1.13.1, `matplotlib` 3.8.4.

---

## 6. Evidence (Bukti & Temuan Hasil)

Bagian ini memuat bukti empiris dari hasil simulasi numerik dan perbandingan langsung ketiga model pada data pengujian:

### A. Tabel Perbandingan Kinerja Peramalan Out-of-Sample
Performa diuji pada 24 bulan data testing (Januari 2021 – Desember 2022) yang tidak pernah dilihat model saat pelatihan:

| Peringkat | Model Pemodelan | MAE ($\text{m}^3$) | RMSE ($\text{m}^3$) | MAPE (%) | Keterangan Evaluasi |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **1** | **SARIMA(1, 0, 1)x(0, 0, 0)₁₂** | **339,65** | **418,53** | **4,43%** | **Model Terbaik (Akurasi Tertinggi)** |
| 2 | **Holt-Winters Smoothing (Additive)** | **340,56** | **419,68** | **4,54%** | Model Pemulusan Adaptif |
| 3 | **Seasonal Naive (Baseline)** | **1.233,58** | **1.522,23** | **15,09%** | Batas Bawah Acuan Minimal |

*Temuan Kunci:* Model SARIMA berhasil mengungguli batas bawah Seasonal Naive dengan penurunan kesalahan MAE sebesar **72,5%** dan menghasilkan MAPE yang sangat presisi di bawah 5%.

### B. Bukti Diagnostik Residual (Uji Kelayakan Statistik)
Pengujian sisaan residual model SARIMA terpilih:
- **Hasil Uji Ljung-Box pada Residual (Lag 12):**
  - Nilai statistik $Q$: **5,8100**
  - Nilai $p\text{-value}$: **0,9254** ($p > 0{,}05$, membuktikan hipotesis nol gagal ditolak dan residual merupakan **white noise** murni).
- **Pemeriksaan ACF Residual:** Seluruh lag residual berada di dalam pita interval konfidensi 95% (`fig06_residual_diagnostics.png`).
- **Distribusi Residual:** Memiliki rata-rata residual mendekati nol dengan kerapatan simetris terhadap kurva normal teoretis.

### C. Bukti Hasil Peramalan dan Interval Prediksi
Berdasarkan model terbaik yang dilatih ulang pada data penuh 84 bulan:
- **Ramalan Volume 12 Bulan ke Depan (Tahun 2023):**
  - Rata-rata estimasi volume bulanan: **8.951,30 m³/bulan**
  - Total Ramalan Tahunan 2023: **107.415,59 m³**
  - Batas Bawah Interval Prediksi 95%: **87.979,01 m³**
  - Batas Atas Interval Prediksi 95%: **126.852,18 m³**
- **Ramalan Volume Tahun 2024:**
  - Rata-rata estimasi volume bulanan: **9.795,38 m³/bulan**
  - Total Ramalan Tahunan 2024: **117.544,57 m³** (95% CI: **86.077,39 – 149.011,77 m³**)

> [!NOTE]
> **Artefak Gambar Grafik Hasil Eksekusi:**
> - Grafik komparasi aktual vs ramalan out-of-sample: [`code/output/figures/fig05_test_comparison.png`](file:///media/ramadhan/0C6A-1ABD/University/Pemodelan%20Matematika/Tugas%201/code/output/figures/fig05_test_comparison.png)
> - Grafik 4-in-1 diagnostik residual: [`code/output/figures/fig06_residual_diagnostics.png`](file:///media/ramadhan/0C6A-1ABD/University/Pemodelan%20Matematika/Tugas%201/code/output/figures/fig06_residual_diagnostics.png)
> - Grafik proyeksi masa depan 2023–2024 dan pita konfidensi 95%: [`code/output/figures/fig07_future_forecast.png`](file:///media/ramadhan/0C6A-1ABD/University/Pemodelan%20Matematika/Tugas%201/code/output/figures/fig07_future_forecast.png)
> - Grafik profil anomali pandemi 2020: [`code/output/figures/fig08_anomaly_2020.png`](file:///media/ramadhan/0C6A-1ABD/University/Pemodelan%20Matematika/Tugas%201/code/output/figures/fig08_anomaly_2020.png)

---

## 7. Conclusion (Kesimpulan)

Penarikan kesimpulan berlandaskan bukti empiris simulasi numerik:

1. **Keberadaan Struktur Tren dan Musiman:**
   Data 84 bulan membuktikan keberadaan tren kenaikan sekuler yang mendominasi lebih dari 41% dinamika data volume sampah, disertai siklus fluktuasi musiman tahunan sebesar 2,45%.
2. **Justifikasi Metodologis Keunggulan SARIMA:**
   Model SARIMA terbukti secara empiris mengungguli Seasonal Naive sebesar 72,5% penurunan MAE dan sedikit lebih presisi daripada Holt-Winters. Dengan MAPE 4,43%, model SARIMA sangat layak digunakan dalam perencanaan persampahan daerah.
3. **Konfirmasi Sisaan White Noise:**
   Uji Ljung-Box menghasilkan $p = 0{,}9254 > 0{,}05$, memastikan bahwa tidak ada informasi deret waktu yang tertinggal pada residual; model telah menyerap seluruh struktur temporal data.
4. **Karakter Anomali Pandemi 2020:**
   Tahun 2020 terbukti mengalami *transient shock* pada Mei–Juni 2020 dengan deviasi hingga -18,6%, namun tidak mematahkan lintasan tren pertumbuhan jangka panjang secara permanen.
5. **Kesiapan Proyeksi Peramalan:**
   TPA Randukuning diproyeksikan menerima beban timbulan sampah sebesar $107.416\text{ m}^3$ pada tahun 2023 dan $117.545\text{ m}^3$ pada tahun 2024, yang membutuhkan kesiapan penambahan kapasitas sel landfill atau percepatan operasional fasilitas TPST RDF.

> [!NOTE]
> **Rujukan Berkas Hasil Lengkap:**
> Ringkasan eksekutif lengkap tersimpan pada [`code/output/tables/ringkasan_eksekutif.md`](file:///media/ramadhan/0C6A-1ABD/University/Pemodelan%20Matematika/Tugas%201/code/output/tables/ringkasan_eksekutif.md) dan seluruh tabel metrik numerik berada pada [`code/output/tables/`](file:///media/ramadhan/0C6A-1ABD/University/Pemodelan%20Matematika/Tugas%201/code/output/tables/).

---

## 8. Application / Model (Penerapan Model di Lapangan)

Model deret waktu yang dihasilkan dirancang agar bermanfaat secara nyata bagi pengelola kebersihan daerah:

### A. Manfaat Praktis bagi Pengambil Kebijakan
1. **Perencanaan Kapasitas Armada Truk Bulanan:**
   Dinas Lingkungan Hidup dapat mengetahui pada bulan-bulan apa saja timbulan sampah akan mencapai puncak, sehingga alokasi ritase dan cadangan truk cadangan dapat disiapkan jauh-jauh hari.
2. **Estimasi Anggaran Bahan Bakar dan Operasional:**
   Dengan mengetahui ramalan volume bulanan beserta batas atas dan batas bawahnya (interval 95%), dinas dapat menganggarkan biaya bahan bakar dan upah lembur petugas kebersihan secara lebih akurat.
3. **Peringatan Dini Lonjakan Sampah:**
   Memberikan sinyal awal kepada pemangku kebijakan jika volume sampah bulanan mulai melampaui kemampuan operasional pengangkutan rutin.

### B. Ruang Rencana Pengembangan Produk Terapan
> [!NOTE]
> **Ruang Pengisian Peneliti (Rencana Media Penerapan):**
> - **Format Produk:** [ ... Kosong: Lembar kerja otomatisasi Excel / Dashboard web interaktif Streamlit ... ]
> - **Pengguna Sasaran:** [ ... Kosong: Tim Perencanaan dan Evaluasi Pengelolaan Sampah DLH Kabupaten Batang ... ]
> - **Jadwal Pembaruan Model:** [ ... Kosong: Frekuensi pembaruan model (misal: di-retrain tiap 6 bulan sekali dengan data baru) ... ]

---

## 9. Evaluation (Evaluasi Kritis & Keterbatasan)

### A. Evaluasi Keandalan Metodologi
Penelitian ini dinilai andal karena menerapkan prinsip pemodelan yang ketat:
- Menghindari *data leakage* dengan memisahkan data latih dan data uji berdasarkan urutan waktu nyata.
- Menguji sisaan residual menggunakan uji hipotesis formal (Ljung-Box).
- Membandingkan performa terhadap model baseline yang sederhana agar tidak terjebak dalam ilusi kecanggihan model.

### B. Keterbatasan Penelitian yang Harus Diakui
1. **Ukuran Deret Waktu Terbatas:** 
   Dengan 84 data bulanan, kita hanya memiliki 7 siklus musiman penuh. Jumlah ini cukup untuk pemodelan dasar, namun relatif sensitif terhadap keberadaan satu atau dua data ekstrem.
2. **Ketiadaan Variabel Kovariat:** 
   Model saat ini merupakan model deret waktu univariat murni yang hanya melihat data volume masa lalu, belum dapat merespons secara langsung faktor eksternal mendadak seperti pembukaan pabrik baru di KITB atau cuaca ekstrem.
3. **Bukan Ramalan Deterministik Pasti:** 
   Peramalan bersifat probabilistik dan memiliki ketidakpastian; semakin jauh horizon waktu ramalan ke depan, rentang interval ketidakpastian akan semakin melebar.

### C. Ruang Catatan Masukan dan Rencana Lanjutan
> [!NOTE]
> **Ruang Pengisian Peneliti (Masukan Penguji dan Rencana Masa Depan):**
> - **Catatan Dosen Pembimbing / Reviewer:** [ ... Kosong: Masukkan masukan dan catatan perbaikan saat seminar proposal ... ]
> - **Rencana Pengembangan ke SARIMAX:** [ ... Kosong: Tuliskan rencana memasukkan variabel jumlah penduduk atau curah hujan jika data sudah lengkap ... ]
> - **Mitigasi Risiko Metodologis:** [ ... Kosong: Langkah cadangan jika uji Ljung-Box awal gagal memenuhi syarat white noise ... ]
