"""
Konfigurasi Global Pemodelan Deret Waktu Tugas 1
Studi Kasus: Volume Sampah Masuk TPA Randukuning Kabupaten Batang (2016–2022)
Mata Kuliah: Pemodelan Matematika - S1 Matematika FMIPA UNS
"""

from pathlib import Path

# ==========================================
# 1. Konfigurasi Direktori & Path Berkas
# ==========================================
SRC_DIR = Path(__file__).resolve().parent
CODE_DIR = SRC_DIR.parent
BASE_DIR = CODE_DIR.parent

DATA_RAW_PATH = BASE_DIR / ".raw" / "volume_sampah_tpa_randukuning_2016_2022.csv"
DATA_PROCESSED_DIR = BASE_DIR / "data"

OUTPUT_DIR = CODE_DIR / "output"
FIGURES_DIR = OUTPUT_DIR / "figures"
TABLES_DIR = OUTPUT_DIR / "tables"
NOTEBOOKS_DIR = CODE_DIR / "notebooks"

# Pastikan folder output dan notebooks otomatis terbentuk
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
TABLES_DIR.mkdir(parents=True, exist_ok=True)
NOTEBOOKS_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================
# 2. Parameter Deret Waktu & Pembagian Data
# ==========================================
SEASONAL_PERIOD = 12            # Siklus musiman tahunan (12 bulan)
TRAIN_END_DATE = "2020-12-01"   # Akhir periode data latih (60 bulan: 2016-2020)
TEST_START_DATE = "2021-01-01"  # Awal periode data uji (24 bulan: 2021-2022)
FORECAST_STEPS = 24             # Horizon peramalan masa depan (2023-2024, 24 bulan)
CONFIDENCE_LEVEL = 0.95         # Tingkat kepercayaan interval prediksi (alpha = 0.05)

# ==========================================
# 3. Ruang Pencarian Grid SARIMA (Parsimonious)
# ==========================================
# Rentang parameter yang efisien dan menghindari overfitting untuk N=60
SARIMA_GRID = {
    "p": [0, 1, 2],
    "d": [0, 1],
    "q": [0, 1, 2],
    "P": [0, 1],
    "D": [0, 1],
    "Q": [0, 1],
    "trends": [None, "c"]
}

# ==========================================
# 4. Pengaturan Visualisasi (Standar Publikasi)
# ==========================================
PLOT_STYLE = {
    "figure.figsize": (11, 5.5),
    "figure.dpi": 300,
    "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica", "sans-serif"],
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
    "axes.labelweight": "semibold",
    "axes.grid": True,
    "grid.alpha": 0.35,
    "grid.linestyle": "--",
    "lines.linewidth": 1.8,
    "lines.markersize": 4.5,
    "legend.fontsize": 10,
    "legend.framealpha": 0.9,
}
