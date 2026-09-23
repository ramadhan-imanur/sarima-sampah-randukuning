"""
Unit & Integration Tests untuk Pipeline Pemodelan Deret Waktu
Tugas 1 Pemodelan Matematika - TPA Randukuning Batang
"""

import sys
from pathlib import Path
import pytest
import numpy as np
import pandas as pd

# Tambahkan direktori root 'code' ke sys.path
CODE_DIR = Path(__file__).resolve().parent.parent
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from src.config import DATA_RAW_PATH, SEASONAL_PERIOD
from src.data_loader import load_raw_series, split_train_test, get_series_summary
from src.eda import (
    calculate_descriptive_stats, run_stationarity_tests, run_decomposition,
    analyze_anomaly_2020
)
from src.models import (
    SeasonalNaiveModel, HoltWintersModel, SARIMAModel
)
from src.evaluation import (
    calculate_metrics, compare_models_performance, run_residual_diagnostics
)
from src.forecast import (
    generate_future_forecast, calculate_annual_projections
)


@pytest.fixture(scope="module")
def raw_series():
    """Fixture untuk memuat deret waktu mentah 84 bulan."""
    assert DATA_RAW_PATH.exists(), f"File data mentah {DATA_RAW_PATH} tidak ditemukan."
    return load_raw_series(DATA_RAW_PATH)


@pytest.fixture(scope="module")
def train_test_split(raw_series):
    """Fixture untuk membagi data latih dan uji."""
    return split_train_test(raw_series)


def test_data_loader(raw_series):
    """Memverifikasi pemuatan dataset memenuhi kriteria integritas data ISO."""
    assert isinstance(raw_series, pd.Series)
    assert len(raw_series) == 84
    assert raw_series.isnull().sum() == 0
    assert (raw_series > 0).all()
    assert raw_series.index.freqstr in ["MS", "<MonthBegin>"]
    assert raw_series.index.min() == pd.Timestamp("2016-01-01")
    assert raw_series.index.max() == pd.Timestamp("2022-12-01")


def test_series_summary(raw_series):
    """Memverifikasi kalkulasi ringkasan metadata deskriptif."""
    meta = get_series_summary(raw_series)
    assert meta["jumlah_observasi"] == 84
    assert meta["nilai_minimum"] > 0
    assert meta["nilai_maksimum"] > meta["nilai_minimum"]
    assert meta["periode_awal"] == "2016-01"
    assert meta["periode_akhir"] == "2022-12"


def test_time_based_split(train_test_split):
    """Memverifikasi partisi temporal 60 bulan latih dan 24 bulan uji."""
    train, test = train_test_split
    assert len(train) == 60
    assert len(test) == 24
    assert train.index.max() < test.index.min()
    assert train.index.max() == pd.Timestamp("2020-12-01")
    assert test.index.min() == pd.Timestamp("2021-01-01")


def test_eda_descriptive_stats(raw_series):
    """Memverifikasi kelengkapan perhitungan 12 statistik deskriptif."""
    df_desc = calculate_descriptive_stats(raw_series)
    assert isinstance(df_desc, pd.DataFrame)
    assert len(df_desc) == 12
    stat_names = df_desc["Statistik"].tolist()
    assert "Rata-rata (Mean, m³)" in stat_names
    assert "Ukuran Sampel (N)" in stat_names


def test_eda_stationarity(raw_series):
    """Memverifikasi pengujian ADF dan KPSS pada level dan differencing."""
    df_stat = run_stationarity_tests(raw_series)
    assert isinstance(df_stat, pd.DataFrame)
    assert len(df_stat) == 3
    # Differencing reguler pertama harus stasioner
    row_d1 = df_stat[df_stat["Transformasi"].str.contains("First Difference")].iloc[0]
    assert row_d1["ADF Kesimpulan"] == "Stasioner"
    assert row_d1["ADF p-value"] < 0.05


def test_eda_decomposition(raw_series):
    """Memverifikasi dekomposisi aditif variansi."""
    dec = run_decomposition(raw_series, period=SEASONAL_PERIOD)
    assert "var_total" in dec
    assert "var_trend" in dec
    assert "var_seasonal" in dec
    assert "var_resid" in dec
    assert dec["rasio_tren"] > 0.30  # Tren mendominasi > 30%
    assert len(dec["faktor_musiman"]) == 12


def test_eda_anomaly_2020(raw_series):
    """Memverifikasi deteksi penurunan volume sampah pada masa awal PSBB 2020."""
    df_anom = analyze_anomaly_2020(raw_series)
    assert len(df_anom) == 12
    # Bulan Mei dan Juni 2020 harus mengalami deviasi negatif
    mei_row = df_anom[df_anom["Bulan"] == "Mei"].iloc[0]
    assert mei_row["Persentase_Deviasi (%)"] < 0


def test_seasonal_naive_model(train_test_split):
    """Memverifikasi fungsionalitas fit dan peramalan Seasonal Naive."""
    train, test = train_test_split
    model = SeasonalNaiveModel(seasonal_period=12).fit(train)
    pred = model.forecast(len(test))
    assert len(pred) == len(test)
    assert (pred.index == test.index).all()
    assert (pred > 0).all()


def test_holt_winters_model(train_test_split):
    """Memverifikasi fungsionalitas fit dan peramalan Holt-Winters."""
    train, test = train_test_split
    model = HoltWintersModel(seasonal_period=12, trend="add", seasonal="add").fit(train)
    pred = model.forecast(len(test))
    assert len(pred) == len(test)
    assert (pred > 0).all()
    params = model.get_params_summary()
    assert "alpha (level)" in params
    assert 0 <= params["alpha (level)"] <= 1


def test_sarima_model(train_test_split):
    """Memverifikasi fungsionalitas fit dan peramalan SARIMA beserta interval konfidensi."""
    train, test = train_test_split
    model = SARIMAModel(order=(1, 0, 1), seasonal_order=(0, 0, 0, 12), trend="c").fit(train)
    pred, conf_int = model.forecast(len(test))
    assert len(pred) == len(test)
    assert len(conf_int) == len(test)
    assert (conf_int["Upper_CI"] >= conf_int["Lower_CI"]).all()
    metrics = model.get_diagnostics_metrics()
    assert "AICc" in metrics
    assert "BIC" in metrics


def test_evaluation_metrics(train_test_split):
    """Memverifikasi validitas kalkulasi metrik peramalan MAE, RMSE, MAPE."""
    train, test = train_test_split
    model = SeasonalNaiveModel(seasonal_period=12).fit(train)
    pred = model.forecast(len(test))

    metrics = calculate_metrics(test, pred, model_name="Seasonal Naive")
    assert metrics["MAE (m³)"] > 0
    assert metrics["RMSE (m³)"] >= metrics["MAE (m³)"]
    assert metrics["MAPE (%)"] > 0
    assert metrics["N_Obs"] == 24


def test_residual_diagnostics(train_test_split):
    """Memverifikasi pengujian residual white noise Ljung-Box."""
    train, test = train_test_split
    model = SARIMAModel(order=(1, 0, 1), seasonal_order=(0, 0, 0, 12), trend="c").fit(train)
    diag = run_residual_diagnostics(model.fitted_res.resid, model_name="SARIMA")
    assert "ljung_box_stat" in diag
    assert "ljung_box_pvalue" in diag
    assert 0.0 <= diag["ljung_box_pvalue"] <= 1.0


def test_future_forecast_and_projections(raw_series):
    """Memverifikasi proyeksi masa depan 24 bulan dan agregasi tahunan."""
    df_fc, _ = generate_future_forecast(
        raw_series,
        order=(1, 0, 1),
        seasonal_order=(0, 0, 0, 12),
        trend="c",
        steps=24
    )
    assert len(df_fc) == 24
    assert df_fc["Periode"].iloc[0] == "2023-01"
    assert df_fc["Periode"].iloc[-1] == "2024-12"

    df_annual = calculate_annual_projections(df_fc)
    assert len(df_annual) == 2
    assert set(df_annual["Tahun"]) == {2023, 2024}
    assert (df_annual["Total_Ramalan_Tahunan"] > 0).all()
