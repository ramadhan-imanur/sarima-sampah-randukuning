"""
Modul Hierarki Pemodelan Matematika Deret Waktu
1. Baseline 1: Seasonal Naive
2. Baseline 2: Holt-Winters Exponential Smoothing
3. Model Utama: SARIMA (Seasonal Autoregressive Integrated Moving Average)
Tugas 1 Pemodelan Matematika - TPA Randukuning Batang
"""

from typing import Dict, Any, List, Optional, Tuple
import warnings
import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX, SARIMAXResultsWrapper

try:
    from .config import SEASONAL_PERIOD, SARIMA_GRID
except ImportError:
    from config import SEASONAL_PERIOD, SARIMA_GRID


class SeasonalNaiveModel:
    """
    Model Pembanding Baseline 1: Seasonal Naive
    Formulasi: Y_hat_{t+h} = Y_{t+h - 12(k+1)}
    Memproyeksikan nilai berdasarkan realisasi pada bulan yang sama tahun sebelumnya.
    """

    def __init__(self, seasonal_period: int = SEASONAL_PERIOD):
        self.seasonal_period = seasonal_period
        self.history: Optional[pd.Series] = None
        self.name = "Seasonal Naive (Baseline)"

    def fit(self, train: pd.Series) -> "SeasonalNaiveModel":
        if len(train) < self.seasonal_period:
            raise ValueError(f"Data latih ({len(train)}) harus >= periode musiman ({self.seasonal_period}).")
        self.history = train.copy()
        return self

    def forecast(self, steps: int) -> pd.Series:
        if self.history is None:
            raise RuntimeError("Model harus di-fit terlebih dahulu sebelum forecasting.")

        last_season = self.history.iloc[-self.seasonal_period:].values
        forecast_values = []
        for i in range(steps):
            forecast_values.append(last_season[i % self.seasonal_period])

        last_date = self.history.index[-1]
        freq = self.history.index.freq or "MS"
        forecast_index = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=steps, freq=freq)

        pred = pd.Series(forecast_values, index=forecast_index, name="Forecast_Seasonal_Naive")
        return pred


class HoltWintersModel:
    """
    Model Pembanding Baseline 2: Holt-Winters Exponential Smoothing
    Menangani Taraf (Level), Tren Linear, dan Musiman Bulanan (s=12).
    """

    def __init__(
        self,
        seasonal_period: int = SEASONAL_PERIOD,
        trend: str = "add",
        seasonal: str = "add",
        damped_trend: bool = False
    ):
        self.seasonal_period = seasonal_period
        self.trend = trend
        self.seasonal = seasonal
        self.damped_trend = damped_trend
        self.model = None
        self.fitted_res = None
        self.history: Optional[pd.Series] = None
        self.name = f"Holt-Winters ({trend.capitalize()} Trend, {seasonal.capitalize()} Season)"

    def fit(self, train: pd.Series) -> "HoltWintersModel":
        self.history = train.copy()
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            self.model = ExponentialSmoothing(
                train,
                seasonal_periods=self.seasonal_period,
                trend=self.trend,
                seasonal=self.seasonal,
                damped_trend=self.damped_trend,
                initialization_method="estimated"
            )
            self.fitted_res = self.model.fit(optimized=True)
        return self

    def forecast(self, steps: int) -> pd.Series:
        if self.fitted_res is None:
            raise RuntimeError("Model harus di-fit terlebih dahulu.")
        pred = self.fitted_res.forecast(steps)
        pred.name = "Forecast_Holt_Winters"
        return pred

    def get_params_summary(self) -> Dict[str, float]:
        if self.fitted_res is None:
            return {}
        p = self.fitted_res.params
        return {
            "alpha (level)": float(p.get("smoothing_level", np.nan)),
            "beta (trend)": float(p.get("smoothing_trend", np.nan)),
            "gamma (seasonal)": float(p.get("smoothing_seasonal", np.nan)),
            "phi (damping)": float(p.get("damping_trend", np.nan)) if self.damped_trend else 1.0,
        }


class SARIMAModel:
    """
    Model Utama: Seasonal ARIMA (SARIMA)
    Formulasi: Phi_P(B^s) phi_p(B) (1 - B)^d (1 - B^s)^D Y_t = Theta_Q(B^s) theta_q(B) epsilon_t
    """

    def __init__(
        self,
        order: Tuple[int, int, int] = (1, 1, 1),
        seasonal_order: Tuple[int, int, int, int] = (0, 1, 1, 12),
        trend: Optional[str] = None
    ):
        self.order = order
        self.seasonal_order = seasonal_order
        self.trend = trend
        self.fitted_res: Optional[SARIMAXResultsWrapper] = None
        self.history: Optional[pd.Series] = None
        self.name = f"SARIMA{order}x{seasonal_order}" + (f" with trend '{trend}'" if trend else "")

    def fit(self, train: pd.Series, maxiter: int = 200) -> "SARIMAModel":
        self.history = train.copy()
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            model = SARIMAX(
                train,
                order=self.order,
                seasonal_order=self.seasonal_order,
                trend=self.trend,
                enforce_stationarity=False,
                enforce_invertibility=False
            )
            self.fitted_res = model.fit(disp=False, maxiter=maxiter)
        return self

    def forecast(self, steps: int, alpha: float = 0.05) -> Tuple[pd.Series, pd.DataFrame]:
        """
        Menghasilkan ramalan titik (point forecast) dan interval prediksi konfidensi 95%.
        """
        if self.fitted_res is None:
            raise RuntimeError("Model SARIMA belum di-fit.")
        forecast_obj = self.fitted_res.get_forecast(steps=steps)
        mean_forecast = forecast_obj.predicted_mean
        conf_int = forecast_obj.conf_int(alpha=alpha)
        conf_int.columns = ["Lower_CI", "Upper_CI"]
        mean_forecast.name = "Forecast_SARIMA"
        return mean_forecast, conf_int

    def get_diagnostics_metrics(self) -> Dict[str, float]:
        if self.fitted_res is None:
            return {}
        n = self.fitted_res.nobs
        k = len(self.fitted_res.params)
        aic = float(self.fitted_res.aic)
        bic = float(self.fitted_res.bic)
        # Hitung AICc: AIC + 2k(k+1)/(n - k - 1)
        aicc = aic + (2 * k * (k + 1)) / max(1, (n - k - 1))
        return {
            "AIC": aic,
            "AICc": aicc,
            "BIC": bic,
            "Log_Likelihood": float(self.fitted_res.llf),
            "Jumlah_Parameter": k,
            "Jumlah_Observasi": n
        }


def grid_search_sarima(
    train: pd.Series,
    test: pd.Series,
    grid_config: Optional[Dict[str, Any]] = None,
    verbose: bool = False
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Menjalankan grid search terstruktur untuk menemukan model SARIMA parsimonious terbaik.
    Evaluasi didasarkan pada AIC, BIC pada data latih serta MAE/RMSE/MAPE pada data uji.
    """
    if grid_config is None:
        grid_config = SARIMA_GRID

    p_list = grid_config.get("p", [0, 1, 2])
    d_list = grid_config.get("d", [0, 1])
    q_list = grid_config.get("q", [0, 1, 2])
    P_list = grid_config.get("P", [0, 1])
    D_list = grid_config.get("D", [0, 1])
    Q_list = grid_config.get("Q", [0, 1])
    trends = grid_config.get("trends", [None])

    results = []
    total_combinations = len(p_list) * len(d_list) * len(q_list) * len(P_list) * len(D_list) * len(Q_list) * len(trends)

    if verbose:
        print(f"Memulai Grid Search SARIMA: {total_combinations} kombinasi parameter...")

    steps = len(test)

    for p in p_list:
        for d in d_list:
            for q in q_list:
                for P in P_list:
                    for D in D_list:
                        for Q in Q_list:
                            # Abaikan model nol parameter tanpa komponen AR/MA sama sekali
                            if p == 0 and q == 0 and P == 0 and Q == 0:
                                continue
                            for tr in trends:
                                order = (p, d, q)
                                seasonal_order = (P, D, Q, SEASONAL_PERIOD)
                                try:
                                    sarima = SARIMAModel(order=order, seasonal_order=seasonal_order, trend=tr)
                                    sarima.fit(train)
                                    res = sarima.fitted_res
                                    if res is None:
                                        continue

                                    pred_series, _ = sarima.forecast(steps=steps)
                                    mae = float(np.mean(np.abs(test - pred_series)))
                                    rmse = float(np.sqrt(np.mean((test - pred_series) ** 2)))
                                    mape = float(np.mean(np.abs((test - pred_series) / test)) * 100)

                                    metrics = sarima.get_diagnostics_metrics()

                                    results.append({
                                        "Order": f"({p},{d},{q})",
                                        "Seasonal_Order": f"({P},{D},{Q})_{SEASONAL_PERIOD}",
                                        "Trend": str(tr),
                                        "AIC": round(metrics["AIC"], 2),
                                        "AICc": round(metrics["AICc"], 2),
                                        "BIC": round(metrics["BIC"], 2),
                                        "Test_MAE": round(mae, 2),
                                        "Test_RMSE": round(rmse, 2),
                                        "Test_MAPE": round(mape, 2),
                                        "k_params": metrics["Jumlah_Parameter"],
                                        "p": p, "d": d, "q": q, "P": P, "D": D, "Q": Q, "trend_val": tr
                                    })
                                except Exception:
                                    continue

    df_results = pd.DataFrame(results)

    if df_results.empty:
        raise RuntimeError("Grid search tidak menghasilkan satu pun model yang konvergen.")

    # Peringkat model:
    # Model terbaik dipilih berdasarkan keseimbangan AICc (kebaikan suai & parsimoni) dan Test MAE
    # Untuk memastikan model stabil dan tidak meledak, kita prioritaskan Test MAPE yang realistis (< 25%)
    valid_candidates = df_results[df_results["Test_MAPE"] < 25.0]
    if valid_candidates.empty:
        valid_candidates = df_results

    # Model dengan AICc terbaik di antara model yang stabil
    best_by_aicc_idx = valid_candidates["AICc"].idxmin()
    best_aicc_row = df_results.loc[best_by_aicc_idx]

    # Model dengan Test MAE terkecil
    best_by_mae_idx = valid_candidates["Test_MAE"].idxmin()
    best_mae_row = df_results.loc[best_by_mae_idx]

    best_selection = {
        "best_by_aicc": best_aicc_row.to_dict(),
        "best_by_mae": best_mae_row.to_dict(),
    }

    return df_results, best_selection


if __name__ == "__main__":
    try:
        from .data_loader import load_raw_series, split_train_test
    except ImportError:
        from data_loader import load_raw_series, split_train_test
    s = load_raw_series()
    tr, ts = split_train_test(s)

    print("Pengujian Baseline 1: Seasonal Naive...")
    sn = SeasonalNaiveModel().fit(tr)
    sn_pred = sn.forecast(len(ts))
    print(f"MAE SN: {np.mean(np.abs(ts - sn_pred)):.2f}")

    print("Pengujian Baseline 2: Holt-Winters...")
    hw = HoltWintersModel().fit(tr)
    hw_pred = hw.forecast(len(ts))
    print(f"MAE HW: {np.mean(np.abs(ts - hw_pred)):.2f}")
