"""
Modul Visualisasi Publikasi Ilmiah (8 Gambar Berkualitas Tinggi 300 DPI)
Tugas 1 Pemodelan Matematika - TPA Randukuning Batang
"""

from typing import Dict, Any, Optional
from pathlib import Path
import matplotlib
matplotlib.use("Agg")  # Backend non-interaktif untuk rendering gambar stabil
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

try:
    from .config import FIGURES_DIR, PLOT_STYLE, SEASONAL_PERIOD
except ImportError:
    from config import FIGURES_DIR, PLOT_STYLE, SEASONAL_PERIOD


def apply_custom_style():
    """Menerapkan konfigurasi estetika visual standar publikasi ilmiah."""
    plt.rcParams.update(PLOT_STYLE)


def plot_timeseries_overview(series: pd.Series, output_path: Optional[Path] = None) -> Path:
    """
    Gambar 1: Gambaran Umum Deret Waktu Volume Sampah Bulanan 2016-2022 (84 Bulan)
    dengan Penandaan Tren dan Area Anomali 2020.
    """
    apply_custom_style()
    fig, ax = plt.subplots(figsize=(12, 5.5))

    # Plot deret waktu aktual
    ax.plot(series.index, series.values, color="#1f4e79", marker="o", markersize=4, label="Volume Sampah Aktual (m³)")

    # Garis tren linear sederhana sebagai referensi visual
    x_num = mdates.date2num(series.index)
    poly = np.polyfit(x_num, series.values, deg=1)
    trend_vals = np.polyval(poly, x_num)
    ax.plot(series.index, trend_vals, color="#d9534f", linestyle="--", linewidth=1.6, label=f"Garis Tren Linear (+{(trend_vals[-1]-trend_vals[0])/len(series):.1f} m³/bulan)")

    # Highlight area anomali pandemi 2020
    ax.axvspan(pd.Timestamp("2020-03-01"), pd.Timestamp("2020-07-01"), color="#f0ad4e", alpha=0.25, label="Anomali Pembatasan Pandemi (Mar–Jul 2020)")

    # Titik ekstrem terendah dan tertinggi
    min_date = series.idxmin()
    min_val = series.min()
    max_date = series.idxmax()
    max_val = series.max()

    ax.annotate(
        f"Minimum: {int(min_val):,} m³\n({min_date.strftime('%b %Y')})",
        xy=(min_date, min_val),
        xytext=(min_date + pd.DateOffset(months=3), min_val + 600),
        arrowprops=dict(arrowstyle="->", color="#c9302c", lw=1.2),
        fontweight="semibold",
        color="#c9302c",
        fontsize=9
    )

    ax.annotate(
        f"Maksimum: {int(max_val):,} m³\n({max_date.strftime('%b %Y')})",
        xy=(max_date, max_val),
        xytext=(max_date - pd.DateOffset(months=16), max_val - 400),
        arrowprops=dict(arrowstyle="->", color="#2e7d32", lw=1.2),
        fontweight="semibold",
        color="#2e7d32",
        fontsize=9
    )

    ax.set_title("Dinamika Deret Waktu Volume Sampah Masuk TPA Randukuning Batang (2016–2022)", pad=14)
    ax.set_xlabel("Periode Pengamatan (Tahun & Bulan)", labelpad=10)
    ax.set_ylabel("Volume Sampah Masuk (m³)", labelpad=10)

    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[4, 7, 10]))

    ax.set_ylim(2500, 9500)
    ax.legend(loc="upper left")
    plt.tight_layout()

    out = output_path or (FIGURES_DIR / "fig01_timeseries_overview.png")
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


def plot_decomposition(decomp_res: Any, output_path: Optional[Path] = None) -> Path:
    """
    Gambar 2: Dekomposisi 4-Panel (Observed, Trend, Seasonal, Residual).
    """
    apply_custom_style()
    decomp = decomp_res["decomposition_object"]

    fig, axes = plt.subplots(4, 1, figsize=(12, 9), sharex=True)

    axes[0].plot(decomp.observed.index, decomp.observed.values, color="#1f4e79", lw=1.6)
    axes[0].set_ylabel("Observed\n(m³)", fontweight="semibold")
    axes[0].set_title("Dekomposisi Aditif Deret Waktu Volume Sampah (Siklus Musiman s = 12)", pad=12)

    axes[1].plot(decomp.trend.index, decomp.trend.values, color="#d9534f", lw=2.0)
    axes[1].set_ylabel("Trend\n(m³)", fontweight="semibold")

    axes[2].plot(decomp.seasonal.index, decomp.seasonal.values, color="#2e7d32", lw=1.6)
    axes[2].set_ylabel("Seasonal\n(m³)", fontweight="semibold")

    axes[3].scatter(decomp.resid.index, decomp.resid.values, color="#555555", s=18, alpha=0.8)
    axes[3].axhline(0, color="black", linestyle="--", lw=1)
    axes[3].set_ylabel("Residual\n(m³)", fontweight="semibold")
    axes[3].set_xlabel("Periode Pengamatan", labelpad=8)

    for ax in axes:
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[7]))

    plt.tight_layout()
    out = output_path or (FIGURES_DIR / "fig02_decomposition.png")
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


def plot_acf_pacf_figure(series: pd.Series, output_path: Optional[Path] = None, nlags: int = 36) -> Path:
    """
    Gambar 3: Fungsi Autokorelasi (ACF) dan Autokorelasi Parsial (PACF) Lag 1–36.
    """
    apply_custom_style()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), sharex=True)

    plot_acf(series, ax=ax1, lags=nlags, title="Autocorrelation Function (ACF) - Deret Asli", color="#1f4e79", vlines_kwargs={"colors": "#1f4e79"})
    plot_pacf(series, ax=ax2, lags=nlags, title="Partial Autocorrelation Function (PACF) - Deret Asli", color="#d9534f", vlines_kwargs={"colors": "#d9534f"}, method="ywm")

    # Tambahkan penanda lag tahunan (12, 24, 36)
    for ax in (ax1, ax2):
        for season_lag in [12, 24, 36]:
            ax.axvline(season_lag, color="#9c27b0", linestyle=":", alpha=0.6, lw=1.2)
        ax.set_ylabel("Koefisien Korelasi", fontweight="semibold")

    ax2.set_xlabel("Lag (Bulan)", labelpad=8)
    ax2.set_xticks(range(0, nlags + 1, 3))

    plt.tight_layout()
    out = output_path or (FIGURES_DIR / "fig03_acf_pacf.png")
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


def plot_traintest_split_figure(train: pd.Series, test: pd.Series, output_path: Optional[Path] = None) -> Path:
    """
    Gambar 4: Visualisasi Pembagian Data Latih (2016-2020) vs Data Uji (2021-2022).
    """
    apply_custom_style()
    fig, ax = plt.subplots(figsize=(11, 5))

    ax.plot(train.index, train.values, color="#1f4e79", marker="o", markersize=4, label=f"Data Latih / Training Set (Jan 2016 – Des 2020, N={len(train)})")
    ax.plot(test.index, test.values, color="#2e7d32", marker="s", markersize=4, label=f"Data Uji / Testing Set (Jan 2021 – Des 2022, N={len(test)})")

    # Garis batas pisah
    cutoff_date = pd.Timestamp("2020-12-15")
    ax.axvline(cutoff_date, color="#d9534f", linestyle="--", lw=2, label="Batas Pemisahan Berbasis Waktu (Time Split)")

    ax.set_title("Skema Pembagian Data Berbasis Waktu (Out-of-Sample Validation)", pad=12)
    ax.set_xlabel("Periode Waktu", labelpad=8)
    ax.set_ylabel("Volume Sampah (m³)", labelpad=8)

    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.legend(loc="upper left")

    plt.tight_layout()
    out = output_path or (FIGURES_DIR / "fig04_traintest_split.png")
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


def plot_model_comparison_test(
    test: pd.Series,
    predictions: Dict[str, pd.Series],
    output_path: Optional[Path] = None
) -> Path:
    """
    Gambar 5: Perbandingan Kinerja Peramalan Aktual Uji vs Seasonal Naive vs Holt-Winters vs SARIMA.
    """
    apply_custom_style()
    fig, ax = plt.subplots(figsize=(12, 5.5))

    # Realisasi aktual
    ax.plot(test.index, test.values, color="black", marker="o", lw=2.2, label="Realisasi Aktual (Testing Data)")

    color_map = {
        "Seasonal Naive": ("#d9534f", ":", "^"),
        "Holt-Winters": ("#ff9800", "-.", "v"),
        "SARIMA": ("#1f4e79", "--", "s"),
    }

    for name, pred in predictions.items():
        # Cari styling berdasarkan substring nama model
        c, ls, mk = ("#555555", "--", "o")
        for key, val in color_map.items():
            if key.lower() in name.lower():
                c, ls, mk = val
                break
        ax.plot(pred.index, pred.values, color=c, linestyle=ls, marker=mk, markersize=5, lw=1.8, label=name)

    ax.set_title("Perbandingan Performa Peramalan Out-of-Sample pada Periode Uji (2021–2022)", pad=14)
    ax.set_xlabel("Bulan Pengujian (24 Bulan)", labelpad=10)
    ax.set_ylabel("Volume Sampah (m³)", labelpad=10)

    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))

    ax.legend(loc="upper left")
    plt.tight_layout()

    out = output_path or (FIGURES_DIR / "fig05_test_comparison.png")
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


def plot_residual_diagnostics(residuals: pd.Series, model_name: str, output_path: Optional[Path] = None) -> Path:
    """
    Gambar 6: 4-in-1 Panel Diagnostik Residual Model SARIMA Terbaik
    (Standardized Residuals, Histogram & KDE vs Normal, Q-Q Plot, dan ACF Correlogram).
    """
    apply_custom_style()
    fig, axes = plt.subplots(2, 2, figsize=(12, 8.5))
    clean_resid = residuals.dropna()
    std_resid = (clean_resid - np.mean(clean_resid)) / np.std(clean_resid, ddof=1)

    # 1. Standardized Residuals
    axes[0, 0].plot(clean_resid.index, std_resid.values, color="#1f4e79", lw=1.4)
    axes[0, 0].axhline(0, color="black", linestyle="--", lw=1)
    axes[0, 0].axhline(2, color="red", linestyle=":", lw=1)
    axes[0, 0].axhline(-2, color="red", linestyle=":", lw=1)
    axes[0, 0].set_title("Sisaan Terstandarisasi (Standardized Residuals)", fontsize=11, fontweight="bold")
    axes[0, 0].set_ylabel("Galat Standar", fontweight="semibold")
    axes[0, 0].xaxis.set_major_locator(mdates.YearLocator())
    axes[0, 0].xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    # 2. Histogram & KDE vs N(0,1)
    axes[0, 1].hist(std_resid.values, bins=12, density=True, color="#4682b4", alpha=0.5, edgecolor="black", label="Histogram Residual")
    x_norm = np.linspace(-3.5, 3.5, 200)
    axes[0, 1].plot(x_norm, stats.norm.pdf(x_norm, 0, 1), color="#d9534f", lw=2, label="Kurva Normal Teoretis N(0,1)")
    kde = stats.gaussian_kde(std_resid.values)
    axes[0, 1].plot(x_norm, kde(x_norm), color="#1f4e79", lw=1.8, linestyle="--", label="KDE Empiris")
    axes[0, 1].set_title("Distribusi & Kerapatan Densitas Residual", fontsize=11, fontweight="bold")
    axes[0, 1].set_xlabel("Nilai Standar", fontweight="semibold")
    axes[0, 1].legend(fontsize=8, loc="upper right")

    # 3. Normal Q-Q Plot
    (osm, osr), (slope, intercept, r) = stats.probplot(std_resid.values, dist="norm")
    axes[1, 0].scatter(osm, osr, color="#1f4e79", s=20, alpha=0.85)
    axes[1, 0].plot(osm, slope * np.array(osm) + intercept, color="#d9534f", lw=1.8, label=f"R² = {r**2:.3f}")
    axes[1, 0].set_title("Normal Quantile-Quantile (Q-Q) Plot", fontsize=11, fontweight="bold")
    axes[1, 0].set_xlabel("Kuantil Teoretis", fontweight="semibold")
    axes[1, 0].set_ylabel("Kuantil Sampel", fontweight="semibold")
    axes[1, 0].legend(fontsize=9, loc="upper left")

    # 4. Correlogram ACF Residual
    nlags = min(20, len(clean_resid) // 2)
    plot_acf(clean_resid, ax=axes[1, 1], lags=nlags, title=f"Korelogram Autokorelasi Residual (Lag 1–{nlags})", color="#2e7d32", vlines_kwargs={"colors": "#2e7d32"})
    axes[1, 1].set_xlabel("Lag (Bulan)", fontweight="semibold")
    axes[1, 1].set_ylabel("ACF", fontweight="semibold")

    fig.suptitle(f"Uji Diagnostik Sisaan (Residual Diagnostics): {model_name}", fontsize=13, fontweight="bold", y=0.995)
    plt.tight_layout()

    out = output_path or (FIGURES_DIR / "fig06_residual_diagnostics.png")
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


def plot_future_forecast_figure(
    history: pd.Series,
    df_forecast: pd.DataFrame,
    model_name: str,
    output_path: Optional[Path] = None
) -> Path:
    """
    Gambar 7: Peramalan Masa Depan 2023–2024 beserta Pita Interval Ketidakpastian 95%.
    """
    apply_custom_style()
    fig, ax = plt.subplots(figsize=(12, 5.5))

    # Data historis
    ax.plot(history.index, history.values, color="#1f4e79", marker="o", markersize=3.5, lw=1.8, label="Realisasi Historis DLH (2016–2022, N=84)")

    # Titik ramalan masa depan
    forecast_dates = pd.to_datetime(df_forecast["Periode"], format="%Y-%m")
    ax.plot(forecast_dates, df_forecast["Ramalan_Volume (m³)"].values, color="#d9534f", marker="s", markersize=4.5, lw=2.0, label=f"Proyeksi Model {model_name} (2023–2024)")

    # Pita interval konfidensi 95%
    ax.fill_between(
        forecast_dates,
        df_forecast["Batas_Bawah_95% (m³)"].values,
        df_forecast["Batas_Atas_95% (m³)"].values,
        color="#d9534f",
        alpha=0.22,
        label="Interval Prediksi 95% (Rentang Ketidakpastian)"
    )

    # Garis pemisah masa historis dan masa depan
    cutoff = pd.Timestamp("2022-12-15")
    ax.axvline(cutoff, color="#333333", linestyle="--", lw=1.5, label="Batas Data Historis vs Peramalan")

    ax.set_title(f"Proyeksi Peramalan Volume Sampah TPA Randukuning Periode 2023–2024", pad=14)
    ax.set_xlabel("Tahun Pengamatan & Peramalan", labelpad=8)
    ax.set_ylabel("Volume Sampah Bulanan (m³)", labelpad=8)

    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[7]))

    ax.legend(loc="upper left")
    plt.tight_layout()

    out = output_path or (FIGURES_DIR / "fig07_future_forecast.png")
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


def plot_anomaly_2020_figure(df_anomaly: pd.DataFrame, output_path: Optional[Path] = None) -> Path:
    """
    Gambar 8: Kurva Profil Bulanan Komparatif Anomali 2020 vs Pra-2020 & Pasca-2020.
    """
    apply_custom_style()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7.5), sharex=True)

    bulan_labels = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Ags", "Sep", "Okt", "Nov", "Des"]
    x = np.arange(len(bulan_labels))

    # Panel 1: Kurva Volume Bulanan
    ax1.plot(x, df_anomaly["Rata_2016_2019"], color="#1f4e79", marker="o", lw=1.8, label="Rata-rata Pra-Pandemi (2016–2019)")
    ax1.plot(x, df_anomaly["Volume_2020"], color="#d9534f", marker="s", lw=2.2, label="Volume Realisasi Tahun 2020 (Pandemi)")
    ax1.plot(x, df_anomaly["Rata_2021_2022"], color="#2e7d32", marker="^", lw=1.8, label="Rata-rata Pasca-Pandemi (2021–2022)")

    # Highlight drop Mei-Juni 2020
    ax1.axvspan(3.8, 5.2, color="#f0ad4e", alpha=0.3, label="Penurunan Tajam Fase Awal PSBB (Mei–Jun 2020)")

    ax1.set_title("Analisis Komparatif Pola Musiman Bulanan: Anomali Tahun 2020", pad=12)
    ax1.set_ylabel("Volume Sampah (m³)", fontweight="semibold")
    ax1.legend(loc="lower right")

    # Panel 2: Deviasi Persentase 2020 terhadap Pra-Pandemi
    dev_pct = df_anomaly["Persentase_Deviasi (%)"].values
    bar_colors = ["#d9534f" if v < 0 else "#2e7d32" for v in dev_pct]
    ax2.bar(x, dev_pct, color=bar_colors, alpha=0.75, edgecolor="black", width=0.55)
    ax2.axhline(0, color="black", linestyle="-", lw=1)
    ax2.set_ylabel("Deviasi (%) vs Pra-Pandemi", fontweight="semibold")
    ax2.set_xlabel("Bulan", labelpad=8)
    ax2.set_xticks(x)
    ax2.set_xticklabels(bulan_labels)

    for i, val in enumerate(dev_pct):
        offset = 1.0 if val >= 0 else -2.5
        ax2.text(i, val + offset, f"{val:+.1f}%", ha="center", fontsize=8.5, fontweight="semibold")

    ax2.set_ylim(-30, 20)
    plt.tight_layout()

    out = output_path or (FIGURES_DIR / "fig08_anomaly_2020.png")
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out
