"""
Modul Evaluasi Akurasi Out-of-Sample & Diagnostik Residual
Tugas 1 Pemodelan Matematika - TPA Randukuning Batang
"""

from typing import Dict, Any, List
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.diagnostic import acorr_ljungbox

try:
    from .config import SEASONAL_PERIOD
except ImportError:
    from config import SEASONAL_PERIOD


def calculate_metrics(actual: pd.Series, predicted: pd.Series, model_name: str = "") -> Dict[str, Any]:
    """
    Menghitung tiga metrik utama performa peramalan out-of-sample:
    1. MAE (Mean Absolute Error, m³)
    2. RMSE (Root Mean Squared Error, m³)
    3. MAPE (Mean Absolute Percentage Error, %)
    """
    # Pastikan data sejajar secara kronologis
    common_idx = actual.index.intersection(predicted.index)
    if len(common_idx) == 0:
        raise ValueError("Indeks tanggal antara actual dan predicted tidak memiliki irisan.")

    y_act = actual.loc[common_idx].values
    y_pred = predicted.loc[common_idx].values

    n = len(y_act)
    errors = y_act - y_pred

    mae = float(np.mean(np.abs(errors)))
    rmse = float(np.sqrt(np.mean(errors ** 2)))
    mape = float(np.mean(np.abs(errors / y_act)) * 100)

    # Indikator bias arah ramalan (Mean Error / ME)
    me = float(np.mean(errors))

    return {
        "Model": model_name,
        "N_Obs": n,
        "MAE (m³)": round(mae, 2),
        "RMSE (m³)": round(rmse, 2),
        "MAPE (%)": round(mape, 2),
        "ME (m³)": round(me, 2),
    }


def compare_models_performance(
    actual: pd.Series,
    predictions: Dict[str, pd.Series]
) -> pd.DataFrame:
    """
    Menghasilkan tabel komparasi performa beberapa model pada data pengujian.
    """
    records = []
    for model_name, pred_series in predictions.items():
        metrics = calculate_metrics(actual, pred_series, model_name=model_name)
        records.append(metrics)

    df_comp = pd.DataFrame(records)
    # Urutkan berdasarkan MAE terkecil
    df_comp = df_comp.sort_values("MAE (m³)").reset_index(drop=True)
    return df_comp


def run_residual_diagnostics(residuals: pd.Series, model_name: str = "SARIMA") -> Dict[str, Any]:
    """
    Melakukan pengujian formal terhadap sisaan/residual (e_t = Y_t - Y_hat_t):
    1. Uji Ljung-Box untuk autokorelasi (H0: White Noise, kriteria p > 0.05)
    2. Uji Normalitas Jarque-Bera & Shapiro-Wilk
    3. Statistik deskriptif residual (Rata-rata, Variansi, Skewness, Kurtosis)
    """
    clean_resid = residuals.dropna()
    n = len(clean_resid)

    # 1. Uji Ljung-Box pada lag musiman (6, 12, 18, 24)
    test_lags = [l for l in [6, 12, 18, 24] if l < n // 2]
    if not test_lags:
        test_lags = [max(1, min(10, n // 3))]

    lb_test = acorr_ljungbox(clean_resid, lags=test_lags, return_df=True)

    # Ambil evaluasi lag utama s=12 atau lag terbesar yang diuji
    primary_lag = 12 if 12 in lb_test.index else lb_test.index[-1]
    lb_stat = float(lb_test.loc[primary_lag, "lb_stat"])
    lb_pval = float(lb_test.loc[primary_lag, "lb_pvalue"])
    is_white_noise = lb_pval > 0.05

    # 2. Uji Normalitas
    jb_stat, jb_pval = stats.jarque_bera(clean_resid)
    shapiro_stat, shapiro_pval = stats.shapiro(clean_resid)

    # 3. Statistik Deskriptif Residual
    mean_res = float(np.mean(clean_resid))
    std_res = float(np.std(clean_resid, ddof=1))
    skew_res = float(stats.skew(clean_resid))
    kurt_res = float(stats.kurtosis(clean_resid))

    return {
        "model_name": model_name,
        "n_residual": n,
        "primary_lag": primary_lag,
        "ljung_box_stat": round(lb_stat, 4),
        "ljung_box_pvalue": round(lb_pval, 4),
        "is_white_noise": is_white_noise,
        "ljung_box_table": lb_test,
        "jarque_bera_stat": round(float(jb_stat), 4),
        "jarque_bera_pvalue": round(float(jb_pval), 4),
        "shapiro_stat": round(float(shapiro_stat), 4),
        "shapiro_pvalue": round(float(shapiro_pval), 4),
        "mean_residual": round(mean_res, 4),
        "std_residual": round(std_res, 4),
        "skewness": round(skew_res, 4),
        "kurtosis": round(kurt_res, 4),
    }


def format_diagnostics_report(diag: Dict[str, Any]) -> str:
    """
    Menghasilkan ringkasan naratif hasil diagnostik residual dalam format teks ilmiah.
    """
    wn_status = "LOLOS (White Noise Terpenuhi)" if diag["is_white_noise"] else "TIDAK LOLOS (Sisaan Masih Berautokorelasi)"
    report = f"""### Diagnostik Residual Model {diag['model_name']}
- **Ukuran Sisaan (N):** {diag['n_residual']} observasi
- **Rata-rata Residual:** {diag['mean_residual']:.2f} m³ (Ideal: mendekati 0)
- **Deviasi Standar:** {diag['std_residual']:.2f} m³
- **Kemiringan (Skewness):** {diag['skewness']:.4f}
- **Uji Ljung-Box (Lag {diag['primary_lag']}):**
  - Q-Statistic: {diag['ljung_box_stat']:.4f}
  - p-value: {diag['ljung_box_pvalue']:.4f}
  - Status Kelayakan: **{wn_status}** (p > 0.05)
- **Uji Normalitas Jarque-Bera:**
  - JB-Stat: {diag['jarque_bera_stat']:.4f} (p-value: {diag['jarque_bera_pvalue']:.4f})
"""
    return report
