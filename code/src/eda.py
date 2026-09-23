"""
Modul Eksplorasi Data Analitik (EDA) & Uji Statistik
Tugas 1 Pemodelan Matematika - TPA Randukuning Batang
"""

from typing import Dict, Any
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.tsa.stattools import adfuller, kpss, acf, pacf
from statsmodels.tsa.seasonal import seasonal_decompose

try:
    from .config import SEASONAL_PERIOD
except ImportError:
    from config import SEASONAL_PERIOD


def calculate_descriptive_stats(series: pd.Series) -> pd.DataFrame:
    """
    Menghitung statistik deskriptif lengkap deret waktu volume sampah.
    """
    desc = {
        "Ukuran Sampel (N)": int(len(series)),
        "Rata-rata (Mean, m³)": float(np.mean(series)),
        "Deviasi Standar (Std, m³)": float(np.std(series, ddof=1)),
        "Variansi (Var, m⁶)": float(np.var(series, ddof=1)),
        "Nilai Minimum (m³)": float(np.min(series)),
        "Kuartil 1 / Q1 (m³)": float(np.percentile(series, 25)),
        "Median / Q2 (m³)": float(np.median(series)),
        "Kuartil 3 / Q3 (m³)": float(np.percentile(series, 75)),
        "Nilai Maksimum (m³)": float(np.max(series)),
        "Rentang Antarkuartil (IQR, m³)": float(np.percentile(series, 75) - np.percentile(series, 25)),
        "Kemiringan (Skewness)": float(stats.skew(series)),
        "Kurtosis Eksidental": float(stats.kurtosis(series)),
    }
    return pd.DataFrame(list(desc.items()), columns=["Statistik", "Nilai"])


def run_stationarity_tests(series: pd.Series) -> pd.DataFrame:
    """
    Menjalankan pengujian stasioneritas Augmented Dickey-Fuller (ADF)
    dan Kwiatkowski-Phillips-Schmidt-Shin (KPSS) pada:
    1. Deret Asli (Level, d=0)
    2. Diferensiasi Reguler Pertama (First Difference, d=1)
    3. Diferensiasi Musiman (Seasonal Difference, D=1, s=12)
    """
    rows = []

    # 1. Level
    adf_lvl = adfuller(series, autolag="AIC")
    kpss_lvl = kpss(series, regression="c", nlags="auto")
    rows.append({
        "Transformasi": "Deret Asli (Level / d=0)",
        "ADF Stat": round(adf_lvl[0], 4),
        "ADF p-value": round(adf_lvl[1], 4),
        "ADF Kesimpulan": "Non-Stasioner" if adf_lvl[1] > 0.05 else "Stasioner",
        "KPSS Stat": round(kpss_lvl[0], 4),
        "KPSS p-value": round(kpss_lvl[1], 4),
        "KPSS Kesimpulan": "Non-Stasioner" if kpss_lvl[1] < 0.05 else "Stasioner",
    })

    # 2. First Difference (d=1)
    diff1 = series.diff().dropna()
    adf_d1 = adfuller(diff1, autolag="AIC")
    kpss_d1 = kpss(diff1, regression="c", nlags="auto")
    rows.append({
        "Transformasi": "First Difference (d=1)",
        "ADF Stat": round(adf_d1[0], 4),
        "ADF p-value": round(adf_d1[1], 4),
        "ADF Kesimpulan": "Stasioner" if adf_d1[1] <= 0.05 else "Non-Stasioner",
        "KPSS Stat": round(kpss_d1[0], 4),
        "KPSS p-value": round(kpss_d1[1], 4),
        "KPSS Kesimpulan": "Stasioner" if kpss_d1[1] >= 0.05 else "Non-Stasioner",
    })

    # 3. Seasonal Difference (D=1, s=12)
    diff12 = series.diff(SEASONAL_PERIOD).dropna()
    adf_d12 = adfuller(diff12, autolag="AIC")
    kpss_d12 = kpss(diff12, regression="c", nlags="auto")
    rows.append({
        "Transformasi": f"Seasonal Difference (D=1, s={SEASONAL_PERIOD})",
        "ADF Stat": round(adf_d12[0], 4),
        "ADF p-value": round(adf_d12[1], 4),
        "ADF Kesimpulan": "Stasioner" if adf_d12[1] <= 0.05 else "Non-Stasioner",
        "KPSS Stat": round(kpss_d12[0], 4),
        "KPSS p-value": round(kpss_d12[1], 4),
        "KPSS Kesimpulan": "Stasioner" if kpss_d12[1] >= 0.05 else "Non-Stasioner",
    })

    return pd.DataFrame(rows)


def run_decomposition(series: pd.Series, period: int = SEASONAL_PERIOD) -> Dict[str, Any]:
    """
    Melakukan dekomposisi aditif klasik untuk memisahkan komponen
    Tren (Tt), Musiman (St), dan Sisaan/Residual (Rt).
    Menghitung proporsi variansi masing-masing komponen.
    """
    decomp = seasonal_decompose(series, model="additive", period=period)

    trend_clean = decomp.trend.dropna()
    seasonal_clean = decomp.seasonal.dropna()
    resid_clean = decomp.resid.dropna()

    var_total = float(np.var(series))
    var_trend = float(np.var(trend_clean))
    var_seasonal = float(np.var(seasonal_clean))
    var_resid = float(np.var(resid_clean))

    # Faktor musiman bulanan unik (Jan s.d. Des)
    seasonal_monthly = decomp.seasonal.iloc[:period].copy()
    seasonal_monthly.index = [f"Bulan {i+1:02d}" for i in range(period)]

    return {
        "decomposition_object": decomp,
        "var_total": var_total,
        "var_trend": var_trend,
        "var_seasonal": var_seasonal,
        "var_resid": var_resid,
        "rasio_tren": var_trend / var_total,
        "rasio_musiman": var_seasonal / var_total,
        "rasio_residual": var_resid / var_total,
        "faktor_musiman": seasonal_monthly,
    }


def compute_acf_pacf(series: pd.Series, nlags: int = 36) -> pd.DataFrame:
    """
    Menghitung nilai Autocorrelation Function (ACF) dan
    Partial Autocorrelation Function (PACF) hingga lag yang ditentukan.
    """
    acf_vals, acf_confint = acf(series, nlags=nlags, alpha=0.05)
    pacf_vals, pacf_confint = pacf(series, nlags=nlags, alpha=0.05)

    lags = list(range(nlags + 1))
    df_corr = pd.DataFrame({
        "Lag": lags,
        "ACF": acf_vals,
        "ACF_Lower": acf_confint[:, 0] - acf_vals,
        "ACF_Upper": acf_confint[:, 1] - acf_vals,
        "PACF": pacf_vals,
        "PACF_Lower": pacf_confint[:, 0] - pacf_vals,
        "PACF_Upper": pacf_confint[:, 1] - pacf_vals,
    })
    return df_corr


def analyze_anomaly_2020(series: pd.Series) -> pd.DataFrame:
    """
    Analisis komparatif empiris anomali volume sampah tahun 2020
    (awal masa pandemi COVID-19) terhadap rata-rata tahun sebelum (2016-2019)
    dan sesudah (2021-2022).
    """
    df = pd.DataFrame({"Volume": series})
    df["Tahun"] = df.index.year
    df["Bulan"] = df.index.month

    # Volume 2020
    vol_2020 = df[df["Tahun"] == 2020].set_index("Bulan")["Volume"]

    # Rata-rata periode pra-pandemi (2016-2019)
    vol_pre = df[df["Tahun"] < 2020].groupby("Bulan")["Volume"].mean()

    # Rata-rata periode pasca-pandemi (2021-2022)
    vol_post = df[df["Tahun"] > 2020].groupby("Bulan")["Volume"].mean()

    res = pd.DataFrame({
        "Bulan": [
            "Januari", "Februari", "Maret", "April", "Mei", "Juni",
            "Juli", "Agustus", "September", "Oktober", "November", "Desember"
        ],
        "Rata_2016_2019": vol_pre.values,
        "Volume_2020": vol_2020.values,
        "Rata_2021_2022": vol_post.values,
    })
    res["Deviasi_vs_Pra (m³)"] = res["Volume_2020"] - res["Rata_2016_2019"]
    res["Persentase_Deviasi (%)"] = (res["Deviasi_vs_Pra (m³)"] / res["Rata_2016_2019"]) * 100

    return res


if __name__ == "__main__":
    try:
        from .data_loader import load_raw_series
    except ImportError:
        from data_loader import load_raw_series
    s = load_raw_series()
    print("--- Statistik Deskriptif ---")
    print(calculate_descriptive_stats(s).to_string(index=False))
    print("\n--- Uji Stasioneritas ---")
    print(run_stationarity_tests(s).to_string(index=False))
    print("\n--- Dekomposisi ---")
    dec = run_decomposition(s)
    print(f"Rasio Variansi Tren    : {dec['rasio_tren']*100:.2f}%")
    print(f"Rasio Variansi Musiman : {dec['rasio_musiman']*100:.2f}%")
    print(f"Rasio Variansi Residual: {dec['rasio_residual']*100:.2f}%")
