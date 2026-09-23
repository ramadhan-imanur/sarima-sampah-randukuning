"""
Modul Peramalan Horizon Masa Depan (Forecasting) & Analisis Ketidakpastian
Tugas 1 Pemodelan Matematika - TPA Randukuning Batang
"""

from typing import Tuple, Dict, Any, Optional
import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

try:
    from .config import FORECAST_STEPS, CONFIDENCE_LEVEL, SEASONAL_PERIOD
except ImportError:
    from config import FORECAST_STEPS, CONFIDENCE_LEVEL, SEASONAL_PERIOD


def generate_future_forecast(
    full_series: pd.Series,
    order: Tuple[int, int, int],
    seasonal_order: Tuple[int, int, int, int],
    trend: Optional[str] = None,
    steps: int = FORECAST_STEPS,
    alpha: float = 1.0 - CONFIDENCE_LEVEL
) -> Tuple[pd.DataFrame, Any]:
    """
    Melatih ulang model SARIMA terbaik menggunakan keseluruhan data historis
    (84 observasi: 2016–2022) untuk menghasilkan proyeksi ke masa depan
    (2023–2024) beserta rentang interval prediksi 95%.

    Args:
        full_series: Deret waktu lengkap 84 bulan.
        order: Tuple (p, d, q).
        seasonal_order: Tuple (P, D, Q, s).
        trend: Konstanta tren ('c', 't', atau None).
        steps: Jumlah bulan peramalan ke depan (default: 24 bulan).
        alpha: Tingkat signifikansi untuk selang kepercayaan (default: 0.05 untuk 95% CI).

    Returns:
        Tuple[pd.DataFrame, SARIMAXResultsWrapper]:
            DataFrame memuat kolom [Periode, Ramalan_Volume, Lower_CI_95, Upper_CI_95, Rentang_Ketidakpastian]
            dan objek fitted model.
    """
    model = SARIMAX(
        full_series,
        order=order,
        seasonal_order=seasonal_order,
        trend=trend,
        enforce_stationarity=False,
        enforce_invertibility=False
    )
    fitted_res = model.fit(disp=False, maxiter=250)

    forecast_obj = fitted_res.get_forecast(steps=steps)
    mean_forecast = forecast_obj.predicted_mean
    conf_int = forecast_obj.conf_int(alpha=alpha)

    # Bangun tanggal masa depan
    last_date = full_series.index[-1]
    freq = full_series.index.freq or "MS"
    future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=steps, freq=freq)

    df_forecast = pd.DataFrame({
        "Periode": future_dates.strftime("%Y-%m"),
        "Tahun": future_dates.year,
        "Bulan": future_dates.strftime("%B"),
        "Ramalan_Volume (m³)": np.round(mean_forecast.values, 2),
        "Batas_Bawah_95% (m³)": np.round(conf_int.iloc[:, 0].values, 2),
        "Batas_Atas_95% (m³)": np.round(conf_int.iloc[:, 1].values, 2),
    }, index=future_dates)

    df_forecast["Rentang_Interval (m³)"] = np.round(
        df_forecast["Batas_Atas_95% (m³)"].values - df_forecast["Batas_Bawah_95% (m³)"].values, 2
    )

    return df_forecast, fitted_res


def calculate_annual_projections(df_forecast: pd.DataFrame) -> pd.DataFrame:
    """
    Mengakumulasikan proyeksi bulanan menjadi estimasi total volume sampah tahunan.
    """
    annual = df_forecast.groupby("Tahun").agg(
        Total_Ramalan_Tahunan=("Ramalan_Volume (m³)", "sum"),
        Total_Batas_Bawah_Tahunan=("Batas_Bawah_95% (m³)", "sum"),
        Total_Batas_Atas_Tahunan=("Batas_Atas_95% (m³)", "sum"),
        Rata_rata_Bulanan=("Ramalan_Volume (m³)", "mean"),
    ).reset_index()

    annual = annual.round(2)
    return annual
