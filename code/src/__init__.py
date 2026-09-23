"""
Paket Pemodelan Matematika: Dinamika & Peramalan Deret Waktu
Volume Sampah Masuk TPA Randukuning Batang (2016–2022)
Program Studi S1 Matematika FMIPA Universitas Sebelas Maret (UNS)
"""

from .config import (
    BASE_DIR, CODE_DIR, SRC_DIR, DATA_RAW_PATH, DATA_PROCESSED_DIR,
    OUTPUT_DIR, FIGURES_DIR, TABLES_DIR, NOTEBOOKS_DIR,
    SEASONAL_PERIOD, TRAIN_END_DATE, TEST_START_DATE, FORECAST_STEPS, CONFIDENCE_LEVEL,
    SARIMA_GRID, PLOT_STYLE
)

from .data_loader import (
    load_raw_series, split_train_test, get_series_summary
)

from .eda import (
    calculate_descriptive_stats, run_stationarity_tests, run_decomposition,
    compute_acf_pacf, analyze_anomaly_2020
)

from .models import (
    SeasonalNaiveModel, HoltWintersModel, SARIMAModel, grid_search_sarima
)

from .evaluation import (
    calculate_metrics, compare_models_performance, run_residual_diagnostics,
    format_diagnostics_report
)

from .forecast import (
    generate_future_forecast, calculate_annual_projections
)

from .visualization import (
    apply_custom_style, plot_timeseries_overview, plot_decomposition,
    plot_acf_pacf_figure, plot_traintest_split_figure, plot_model_comparison_test,
    plot_residual_diagnostics, plot_future_forecast_figure, plot_anomaly_2020_figure
)

__all__ = [
    # Config
    "BASE_DIR", "CODE_DIR", "SRC_DIR", "DATA_RAW_PATH", "DATA_PROCESSED_DIR",
    "OUTPUT_DIR", "FIGURES_DIR", "TABLES_DIR", "NOTEBOOKS_DIR",
    "SEASONAL_PERIOD", "TRAIN_END_DATE", "TEST_START_DATE", "FORECAST_STEPS", "CONFIDENCE_LEVEL",
    "SARIMA_GRID", "PLOT_STYLE",
    # Data Loader
    "load_raw_series", "split_train_test", "get_series_summary",
    # EDA
    "calculate_descriptive_stats", "run_stationarity_tests", "run_decomposition",
    "compute_acf_pacf", "analyze_anomaly_2020",
    # Models
    "SeasonalNaiveModel", "HoltWintersModel", "SARIMAModel", "grid_search_sarima",
    # Evaluation
    "calculate_metrics", "compare_models_performance", "run_residual_diagnostics",
    "format_diagnostics_report",
    # Forecast
    "generate_future_forecast", "calculate_annual_projections",
    # Visualization
    "apply_custom_style", "plot_timeseries_overview", "plot_decomposition",
    "plot_acf_pacf_figure", "plot_traintest_split_figure", "plot_model_comparison_test",
    "plot_residual_diagnostics", "plot_future_forecast_figure", "plot_anomaly_2020_figure"
]
