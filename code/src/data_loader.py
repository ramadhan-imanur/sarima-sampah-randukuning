"""
Modul Pemuatan, Validasi, dan Pembagian Deret Waktu
Tugas 1 Pemodelan Matematika - TPA Randukuning Batang
"""

from typing import Tuple, Dict, Any
from pathlib import Path
import pandas as pd

try:
    from .config import DATA_RAW_PATH, TRAIN_END_DATE, TEST_START_DATE
except ImportError:
    from config import DATA_RAW_PATH, TRAIN_END_DATE, TEST_START_DATE


def load_raw_series(filepath: Path = DATA_RAW_PATH) -> pd.Series:
    """
    Memuat dataset volume sampah bulanan dari berkas CSV,
    mengonversi kolom periode ke DatetimeIndex standar bulanan ('MS'),
    serta melakukan validasi integritas data.

    Returns:
        pd.Series: Deret waktu volume sampah (satuan m^3) dengan frekuensi 'MS'.
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Berkas dataset tidak ditemukan di: {filepath}")

    df = pd.read_csv(filepath)

    # Validasi keberadaan kolom wajib
    required_cols = {"Periode", "Volume_Sampah"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Dataset harus memuat kolom {required_cols}, ditemukan: {df.columns.tolist()}")

    # Konversi indeks waktu
    df["Periode"] = pd.to_datetime(df["Periode"], format="%Y-%m")
    df = df.sort_values("Periode").reset_index(drop=True)
    df.set_index("Periode", inplace=True)
    df.index.freq = "MS"

    series = df["Volume_Sampah"].astype(float)
    series.name = "Volume_Sampah"

    # Validasi integritas data
    if len(series) != 84:
        raise ValueError(f"Diharapkan tepat 84 observasi bulanan (2016-2022), ditemukan: {len(series)}")
    if series.isnull().any():
        raise ValueError("Ditemukan nilai hilang (NaN/null) pada deret waktu.")
    if (series <= 0).any():
        raise ValueError("Ditemukan volume bernilai nol atau negatif yang tidak realistis.")

    return series


def split_train_test(
    series: pd.Series,
    train_end: str = TRAIN_END_DATE,
    test_start: str = TEST_START_DATE
) -> Tuple[pd.Series, pd.Series]:
    """
    Membagi deret waktu berdasarkan urutan waktu (Time-Series Split)
    untuk menghindari bias kebocoran informasi (data leakage).

    Args:
        series: Deret waktu volume sampah lengkap.
        train_end: Tanggal akhir data latih (default: 2020-12-01).
        test_start: Tanggal awal data uji (default: 2021-01-01).

    Returns:
        Tuple[pd.Series, pd.Series]: (train_series, test_series).
    """
    train = series.loc[:train_end].copy()
    test = series.loc[test_start:].copy()

    # Memastikan frekuensi terdefinisi pada kedua subset
    train.index.freq = "MS"
    test.index.freq = "MS"

    if len(train) == 0 or len(test) == 0:
        raise ValueError("Pembagian data menghasilkan subset latih atau uji yang kosong.")

    return train, test


def get_series_summary(series: pd.Series) -> Dict[str, Any]:
    """
    Menghasilkan ringkasan metadata deskriptif deret waktu.
    """
    return {
        "jumlah_observasi": len(series),
        "periode_awal": str(series.index.min().strftime("%Y-%m")),
        "periode_akhir": str(series.index.max().strftime("%Y-%m")),
        "nilai_minimum": float(series.min()),
        "nilai_maksimum": float(series.max()),
        "nilai_rata_rata": float(series.mean()),
        "deviasi_standar": float(series.std()),
        "median": float(series.median()),
    }


if __name__ == "__main__":
    s = load_raw_series()
    summary = get_series_summary(s)
    print("Ringkasan Data Sukses Dimuat:")
    for k, v in summary.items():
        print(f"  - {k}: {v}")
    tr, ts = split_train_test(s)
    print(f"Subset Latih (N={len(tr)}): {tr.index.min().strftime('%Y-%m')} s.d. {tr.index.max().strftime('%Y-%m')}")
    print(f"Subset Uji   (N={len(ts)}): {ts.index.min().strftime('%Y-%m')} s.d. {ts.index.max().strftime('%Y-%m')}")
