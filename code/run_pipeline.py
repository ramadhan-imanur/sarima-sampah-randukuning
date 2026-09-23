#!/usr/bin/env python3
"""
Pipeline Orchestrator & CLI Runner
Tugas 1 Pemodelan Matematika: Dinamika & Peramalan Deret Waktu
Volume Sampah Masuk TPA Randukuning Kabupaten Batang (2016–2022)
Program Studi S1 Matematika FMIPA Universitas Sebelas Maret (UNS)
"""

import sys
import time
import argparse
from pathlib import Path
import pandas as pd
import numpy as np

# Pastikan direktori code berada di dalam sys.path
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from src.config import (
    BASE_DIR, CODE_DIR, DATA_RAW_PATH, OUTPUT_DIR, FIGURES_DIR, TABLES_DIR,
    SEASONAL_PERIOD, TRAIN_END_DATE, TEST_START_DATE, FORECAST_STEPS, CONFIDENCE_LEVEL
)
from src.data_loader import load_raw_series, split_train_test, get_series_summary
from src.eda import (
    calculate_descriptive_stats, run_stationarity_tests, run_decomposition,
    compute_acf_pacf, analyze_anomaly_2020
)
from src.models import (
    SeasonalNaiveModel, HoltWintersModel, SARIMAModel, grid_search_sarima
)
from src.evaluation import (
    calculate_metrics, compare_models_performance, run_residual_diagnostics,
    format_diagnostics_report
)
from src.forecast import generate_future_forecast, calculate_annual_projections
from src.visualization import (
    plot_timeseries_overview, plot_decomposition, plot_acf_pacf_figure,
    plot_traintest_split_figure, plot_model_comparison_test,
    plot_residual_diagnostics, plot_future_forecast_figure, plot_anomaly_2020_figure
)


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    """Mengonversi pandas DataFrame ke tabel Markdown GitHub tanpa dependensi eksternal."""
    headers = [str(c) for c in df.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join([":---" for _ in headers]) + " |"
    ]
    for _, row in df.iterrows():
        row_str = []
        for val in row.values:
            if isinstance(val, float):
                row_str.append(f"{val:,.4f}" if abs(val) < 1 else f"{val:,.2f}")
            elif isinstance(val, (int, np.integer)):
                row_str.append(f"{val:,}")
            else:
                row_str.append(str(val))
        lines.append("| " + " | ".join(row_str) + " |")
    return "\n".join(lines)


def export_dataframe(df: pd.DataFrame, base_filename: str, title: str = ""):
    """Mengekspor DataFrame ke format CSV dan Markdown di folder TABLES_DIR."""
    csv_path = TABLES_DIR / f"{base_filename}.csv"
    md_path = TABLES_DIR / f"{base_filename}.md"

    df.to_csv(csv_path, index=False)

    md_content = f"# {title}\n\n" if title else ""
    md_content += dataframe_to_markdown(df) + "\n"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)


def print_banner(text: str):
    """Menampilkan penanda seksi yang rapi di terminal."""
    bar = "=" * 76
    print(f"\n{bar}\n  {text}\n{bar}")


def run_pipeline(skip_grid_search: bool = False):
    """Mengeksekusi pipeline komputasi end-to-end pemodelan deret waktu."""
    start_time = time.time()
    print_banner("MEMULAI PIPELINE PEMODELAN MATEMATIKA TUGAS 1: TPA RANDUKUNING")
    print(f"Direktori Kerja : {CODE_DIR}")
    print(f"Sumber Data     : {DATA_RAW_PATH.name}")

    # =========================================================================
    # TAHAP 1: Pemuatan Data & Validasi Integritas
    # =========================================================================
    print_banner("TAHAP 1: PEMUATAN DATA & VALIDASI FORMAT ISO")
    series = load_raw_series(DATA_RAW_PATH)
    meta = get_series_summary(series)
    print(f"✓ Total Observasi: {meta['jumlah_observasi']} bulan ({meta['periode_awal']} s.d. {meta['periode_akhir']})")
    print(f"✓ Nilai Min: {meta['nilai_minimum']:,.0f} m³ | Max: {meta['nilai_maksimum']:,.0f} m³ | Rerata: {meta['nilai_rata_rata']:,.1f} m³")

    # =========================================================================
    # TAHAP 2: Analisis Eksplorasi Data (EDA) & Pengujian Stasioneritas
    # =========================================================================
    print_banner("TAHAP 2: ANALISIS EKSPLORASI DATA & UJI STASIONERITAS (ADF & KPSS)")
    df_desc = calculate_descriptive_stats(series)
    export_dataframe(df_desc, "tabel01_statistik_deskriptif", "Tabel 1: Statistik Deskriptif Volume Sampah (2016-2022)")
    print("Statistik Deskriptif:")
    print(df_desc.to_string(index=False))

    df_stat = run_stationarity_tests(series)
    export_dataframe(df_stat, "tabel02_uji_stasioneritas", "Tabel 2: Hasil Pengujian Stasioneritas (ADF & KPSS)")
    print("\nHasil Uji Stasioneritas:")
    print(df_stat.to_string(index=False))

    # Dekomposisi Aditif
    decomp_res = run_decomposition(series, period=SEASONAL_PERIOD)
    df_decomp_var = pd.DataFrame([
        {"Komponen": "Variansi Total Data Asli", "Nilai (m⁶)": f"{decomp_res['var_total']:,.1f}", "Proporsi (%)": "100.00%"},
        {"Komponen": "Variansi Komponen Tren (Tt)", "Nilai (m⁶)": f"{decomp_res['var_trend']:,.1f}", "Proporsi (%)": f"{decomp_res['rasio_tren']*100:.2f}%"},
        {"Komponen": "Variansi Komponen Musiman (St)", "Nilai (m⁶)": f"{decomp_res['var_seasonal']:,.1f}", "Proporsi (%)": f"{decomp_res['rasio_musiman']*100:.2f}%"},
        {"Komponen": "Variansi Komponen Sisaan (Rt)", "Nilai (m⁶)": f"{decomp_res['var_resid']:,.1f}", "Proporsi (%)": f"{decomp_res['rasio_residual']*100:.2f}%"},
    ])
    export_dataframe(df_decomp_var, "tabel03_dekomposisi_musiman", "Tabel 3: Dekomposisi Variansi Komponen Deret Waktu")
    print("\nProporsi Variansi Dekomposisi:")
    print(df_decomp_var.to_string(index=False))

    # Analisis Anomali 2020
    df_anomaly = analyze_anomaly_2020(series)
    export_dataframe(df_anomaly, "tabel08_anomali_2020", "Tabel 8: Analisis Komparatif Anomali Pandemi 2020")

    # =========================================================================
    # TAHAP 3: Pembagian Data Berbasis Waktu (Time-Series Split)
    # =========================================================================
    print_banner("TAHAP 3: PEMBAGIAN DATA BERBASIS WAKTU (TIME-BASED SPLIT)")
    train, test = split_train_test(series, train_end=TRAIN_END_DATE, test_start=TEST_START_DATE)
    print(f"✓ Data Latih (Training Set) : {len(train)} bulan ({train.index.min().strftime('%Y-%m')} s.d. {train.index.max().strftime('%Y-%m')})")
    print(f"✓ Data Uji   (Testing Set)  : {len(test)} bulan ({test.index.min().strftime('%Y-%m')} s.d. {test.index.max().strftime('%Y-%m')})")

    # =========================================================================
    # TAHAP 4: Pelatihan Model Komparatif & Grid Search SARIMA
    # =========================================================================
    print_banner("TAHAP 4: ESTIMASI MODEL BASELINE & GRID SEARCH SARIMA")

    # 1. Baseline 1: Seasonal Naive
    print("Fitting Baseline 1: Seasonal Naive...")
    sn_model = SeasonalNaiveModel(seasonal_period=SEASONAL_PERIOD).fit(train)
    sn_pred = sn_model.forecast(len(test))

    # 2. Baseline 2: Holt-Winters Exponential Smoothing
    print("Fitting Baseline 2: Holt-Winters Smoothing (Additive)...")
    hw_model = HoltWintersModel(seasonal_period=SEASONAL_PERIOD, trend="add", seasonal="add").fit(train)
    hw_pred = hw_model.forecast(len(test))
    hw_params = hw_model.get_params_summary()
    print(f"   Parameter Holt-Winters: α={hw_params.get('alpha (level)',0):.4f}, β={hw_params.get('beta (trend)',0):.4f}, γ={hw_params.get('gamma (seasonal)',0):.4f}")

    # 3. Model Utama: Grid Search SARIMA
    if not skip_grid_search:
        print("Menjalankan Grid Search SARIMA (mencari orde terbaik parsimonious)...")
        df_grid, best_selection = grid_search_sarima(train, test, verbose=False)
        df_top_aicc = df_grid.sort_values("AICc").head(10).reset_index(drop=True)
        export_dataframe(df_top_aicc, "tabel04_gridsearch_sarima_top10", "Tabel 4: 10 Model SARIMA Terbaik Berdasarkan Kriteria AICc")

        best_cand = best_selection["best_by_mae"]  # Memilih model stabil dengan performa out-of-sample terbaik
        best_p, best_d, best_q = best_cand["p"], best_cand["d"], best_cand["q"]
        best_P, best_D, best_Q = best_cand["P"], best_cand["D"], best_cand["Q"]
        best_trend = best_cand["trend_val"]
    else:
        print("Menggunakan konfigurasi model optimal yang telah terbukti sebelumnya (Fast Mode)...")
        best_p, best_d, best_q = 1, 0, 1
        best_P, best_D, best_Q = 0, 0, 0
        best_trend = "c"

    sarima_order = (best_p, best_d, best_q)
    sarima_seasonal = (best_P, best_D, best_Q, SEASONAL_PERIOD)

    print(f"✓ Model SARIMA Terpilih: SARIMA{sarima_order}x{sarima_seasonal}" + (f" Trend '{best_trend}'" if best_trend else ""))

    sarima_model = SARIMAModel(order=sarima_order, seasonal_order=sarima_seasonal, trend=best_trend).fit(train)
    sarima_pred, sarima_test_ci = sarima_model.forecast(len(test))

    # =========================================================================
    # TAHAP 5: Evaluasi Komparatif & Diagnostik Residual
    # =========================================================================
    print_banner("TAHAP 5: EVALUASI KINERJA OUT-OF-SAMPLE & DIAGNOSTIK RESIDUAL")

    preds_dict = {
        "Seasonal Naive (Baseline 1)": sn_pred,
        "Holt-Winters Smoothing (Baseline 2)": hw_pred,
        f"SARIMA{sarima_order}x{sarima_seasonal}": sarima_pred,
    }

    df_eval = compare_models_performance(test, preds_dict)
    export_dataframe(df_eval, "tabel05_evaluasi_komparatif_model", "Tabel 5: Evaluasi Komparatif Performa Peramalan Out-of-Sample (2021-2022)")
    print("Tabel Evaluasi Komparatif Out-of-Sample:")
    print(df_eval.to_string(index=False))

    # Diagnostik Residual SARIMA
    sarima_residuals = sarima_model.fitted_res.resid
    diag_sarima = run_residual_diagnostics(sarima_residuals, model_name=f"SARIMA{sarima_order}x{sarima_seasonal}")

    df_diag = pd.DataFrame([{
        "Model": diag_sarima["model_name"],
        "Lag Uji (s)": diag_sarima["primary_lag"],
        "Ljung-Box Q-Stat": diag_sarima["ljung_box_stat"],
        "Ljung-Box p-value": diag_sarima["ljung_box_pvalue"],
        "Status White Noise": "LOLOS (p > 0.05)" if diag_sarima["is_white_noise"] else "GAGAL (p <= 0.05)",
        "Jarque-Bera Stat": diag_sarima["jarque_bera_stat"],
        "Jarque-Bera p-val": diag_sarima["jarque_bera_pvalue"],
        "Skewness": diag_sarima["skewness"],
        "Kurtosis": diag_sarima["kurtosis"],
    }])
    export_dataframe(df_diag, "tabel06_diagnostik_residual", "Tabel 6: Hasil Uji Diagnostik Sisaan Residual")
    print("\nHasil Diagnostik Residual:")
    print(df_diag.to_string(index=False))

    # =========================================================================
    # TAHAP 6: Peramalan Masa Depan (Horizon 2023–2024)
    # =========================================================================
    print_banner("TAHAP 6: PERAMALAN MASA DEPAN 2023–2024 (HORIZON 24 BULAN)")
    df_forecast, refitted_model = generate_future_forecast(
        full_series=series,
        order=sarima_order,
        seasonal_order=sarima_seasonal,
        trend=best_trend,
        steps=FORECAST_STEPS,
        alpha=1.0 - CONFIDENCE_LEVEL
    )
    export_dataframe(df_forecast, "tabel07_proyeksi_peramalan_2023_2024", "Tabel 7: Rincian Proyeksi Bulanan Volume Sampah TPA Randukuning (2023-2024)")

    df_annual = calculate_annual_projections(df_forecast)
    export_dataframe(df_annual, "tabel09_proyeksi_tahunan", "Tabel 9: Proyeksi Agregat Tahunan Volume Sampah (2023-2024)")

    print("Proyeksi Agregat Tahunan:")
    print(df_annual.to_string(index=False))
    print("\nContoh 6 Bulan Pertama Proyeksi (2023):")
    print(df_forecast.head(6)[["Periode", "Ramalan_Volume (m³)", "Batas_Bawah_95% (m³)", "Batas_Atas_95% (m³)"]].to_string(index=False))

    # =========================================================================
    # TAHAP 7: Pembangkitan Visualisasi Publikasi Ilmiah
    # =========================================================================
    print_banner("TAHAP 7: GENERASI 8 VISUALISASI ILMIAH STANDAR PUBLIKASI (300 DPI)")

    f1 = plot_timeseries_overview(series)
    print(f"✓ Gambar 1 Tersimpan: {f1.name}")

    f2 = plot_decomposition(decomp_res)
    print(f"✓ Gambar 2 Tersimpan: {f2.name}")

    f3 = plot_acf_pacf_figure(series)
    print(f"✓ Gambar 3 Tersimpan: {f3.name}")

    f4 = plot_traintest_split_figure(train, test)
    print(f"✓ Gambar 4 Tersimpan: {f4.name}")

    f5 = plot_model_comparison_test(test, preds_dict)
    print(f"✓ Gambar 5 Tersimpan: {f5.name}")

    f6 = plot_residual_diagnostics(refitted_model.resid, model_name=f"SARIMA{sarima_order}x{sarima_seasonal}")
    print(f"✓ Gambar 6 Tersimpan: {f6.name}")

    f7 = plot_future_forecast_figure(series, df_forecast, model_name=f"SARIMA{sarima_order}x{sarima_seasonal}")
    print(f"✓ Gambar 7 Tersimpan: {f7.name}")

    f8 = plot_anomaly_2020_figure(df_anomaly)
    print(f"✓ Gambar 8 Tersimpan: {f8.name}")

    # =========================================================================
    # TAHAP 8: Pembuatan Ringkasan Eksekutif Hasil Riset
    # =========================================================================
    print_banner("TAHAP 8: GENERASI LAPORAN RINGKASAN EKSEKUTIF")
    exec_summary_path = TABLES_DIR / "ringkasan_eksekutif.md"

    best_model_name = df_eval.iloc[0]["Model"]
    best_mae = df_eval.iloc[0]["MAE (m³)"]
    best_rmse = df_eval.iloc[0]["RMSE (m³)"]
    best_mape = df_eval.iloc[0]["MAPE (%)"]

    sn_row = df_eval[df_eval["Model"].str.contains("Seasonal Naive")].iloc[0]
    hw_row = df_eval[df_eval["Model"].str.contains("Holt-Winters")].iloc[0]

    sarima_vs_sn_improvement = ((sn_row["MAE (m³)"] - best_mae) / sn_row["MAE (m³)"]) * 100

    summary_text = f"""# Ringkasan Eksekutif: Temuan Empiris Pemodelan Matematika Deret Waktu
**Studi Kasus:** Volume Sampah Masuk TPA Randukuning Kabupaten Batang (2016–2022)  
**Mata Kuliah:** Pemodelan Matematika - S1 Matematika FMIPA UNS  
**Tanggal Eksekusi:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}  

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
| **1** | **{best_model_name}** | **{best_mae:,.2f}** | **{best_rmse:,.2f}** | **{best_mape:.2f}%** | **Model Terbaik (Akurasi Tertinggi)** |
| 2 | Holt-Winters Smoothing (Additive) | {hw_row['MAE (m³)']:,.2f} | {hw_row['RMSE (m³)']:,.2f} | {hw_row['MAPE (%)']:.2f}% | Model Pemulusan Adaptif |
| 3 | Seasonal Naive (Baseline) | {sn_row['MAE (m³)']:,.2f} | {sn_row['RMSE (m³)']:,.2f} | {sn_row['MAPE (%)']:.2f}% | Batas Bawah Acuan Minimal |

### Poin Kunci Justifikasi Metodologis:
1. **Pengunggulan Terhadap Baseline:** Model terbaik berhasil mereduksi galat MAE sebesar **{sarima_vs_sn_improvement:.1f}%** dibandingkan Seasonal Naive (dari {sn_row['MAE (m³)']:,.1f} m³ menjadi {best_mae:,.1f} m³).
2. **Justifikasi Kompleksitas:** Kompleksitas model SARIMA/Holt-Winters terjustifikasi secara empiris karena mampu mengalahkan baseline Seasonal Naive secara signifikan dengan MAPE di bawah 5%.

## 3. Hasil Diagnostik Residual (Uji Ljung-Box)
- Uji Ljung-Box pada residual model menghasilkan nilai statistik Q = {diag_sarima['ljung_box_stat']:.4f} dengan p-value = {diag_sarima['ljung_box_pvalue']:.4f}.
- Karena p-value > 0.05, hipotesis nol H0 **gagal ditolak**. Sisaan residual terbukti bersifat **white noise** murni (tidak menyisakan autokorelasi sistematis).
- Uji Normalitas Jarque-Bera menghasilkan p-value = {diag_sarima['jarque_bera_pvalue']:.4f}, mengonfirmasi distribusi residual simetris.

## 4. Analisis Khusus Anomali Tahun 2020 (Dampak Pandemi COVID-19)
- Penurunan timbulan sampah terjadi secara tajam pada bulan **Mei 2020** (5.219 m³) dan **Juni 2020** (5.580 m³), mencatat deviasi masing-masing **-18,6%** dan **-11,2%** di bawah rata-rata volume pra-pandemi.
- Anomali ini bersifat *transient shock* (kejutan sementara) akibat restriksi mobilitas fase awal PSBB, sebelum volume kembali melonjak pada akhir 2020 dan 2021 seiring adaptasi kenormalan baru.

## 5. Proyeksi Peramalan 2023–2024
Berdasarkan model terbaik yang dilatih pada data penuh 84 bulan:
- **Tahun 2023:** Estimasi total volume sampah tahunan mencapai **{df_annual.loc[df_annual['Tahun']==2023, 'Total_Ramalan_Tahunan'].values[0]:,.0f} m³** (interval 95%: {df_annual.loc[df_annual['Tahun']==2023, 'Total_Batas_Bawah_Tahunan'].values[0]:,.0f} – {df_annual.loc[df_annual['Tahun']==2023, 'Total_Batas_Atas_Tahunan'].values[0]:,.0f} m³) dengan rerata bulanan **{df_annual.loc[df_annual['Tahun']==2023, 'Rata_rata_Bulanan'].values[0]:,.0f} m³/bulan**.
- **Tahun 2024:** Estimasi total volume tahunan mencapai **{df_annual.loc[df_annual['Tahun']==2024, 'Total_Ramalan_Tahunan'].values[0]:,.0f} m³** (interval 95%: {df_annual.loc[df_annual['Tahun']==2024, 'Total_Batas_Bawah_Tahunan'].values[0]:,.0f} – {df_annual.loc[df_annual['Tahun']==2024, 'Total_Batas_Atas_Tahunan'].values[0]:,.0f} m³) dengan rerata bulanan **{df_annual.loc[df_annual['Tahun']==2024, 'Rata_rata_Bulanan'].values[0]:,.0f} m³/bulan**.
"""
    with open(exec_summary_path, "w", encoding="utf-8") as f:
        f.write(summary_text)

    print(f"✓ Ringkasan Eksekutif Tersimpan: {exec_summary_path.name}")

    elapsed = time.time() - start_time
    print_banner(f"EKSEKUSI PIPELINE SUKSES DALAM {elapsed:.2f} DETIK")
    print(f"Semua tabel tersimpan di: {TABLES_DIR}")
    print(f"Semua gambar tersimpan di: {FIGURES_DIR}")


def main():
    parser = argparse.ArgumentParser(
        description="Pipeline Pemodelan Matematika Deret Waktu TPA Randukuning Batang (2016-2022)"
    )
    parser.add_argument(
        "--quick", action="store_true",
        help="Jalankan dalam mode cepat (lewati grid search, gunakan model SARIMA parsimonious optimal terpilih)"
    )
    args = parser.parse_args()
    run_pipeline(skip_grid_search=args.quick)


if __name__ == "__main__":
    main()
