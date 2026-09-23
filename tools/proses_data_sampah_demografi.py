#!/usr/bin/env python3
"""
olah_data_sampah_dan_demografi.py
Skrip pemrosesan dan konsolidasi data volume sampah dan kependudukan Kabupaten Batang (2016-2026).
Menghitung korelasi Pearson, laju timbulan per kapita, dan deret waktu terintegrasi.
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, '.raw')
DATA_DIR = os.path.join(BASE_DIR, 'data')

def main():
    print("=== Mengolah Data Sampah & Demografi Batang ===")
    waste_path = os.path.join(RAW_DIR, 'volume_sampah_tpa_randukuning_2016_2022.csv')
    pop_path = os.path.join(DATA_DIR, 'deret_waktu_penduduk_2016_2026.csv')
    
    waste_df = pd.read_csv(waste_path)
    waste_df['Tahun'] = waste_df['Periode'].apply(lambda x: int(x.split('-')[0]))
    waste_annual = waste_df.groupby('Tahun')['Volume_Sampah'].agg(['sum', 'mean']).reset_index()
    waste_annual.columns = ['Tahun', 'Volume_Total_Tahunan_m3', 'Volume_Rata2_Bulanan_m3']
    
    pop_df = pd.read_csv(pop_path)
    merged = pd.merge(waste_annual, pop_df[['Tahun', 'Jumlah_Penduduk_Ribu', 'Laju_Pertumbuhan_Persen']], on='Tahun')
    merged['Penduduk_Jiwa'] = (merged['Jumlah_Penduduk_Ribu'] * 1000).astype(int)
    merged['Volume_Per_Kapita_Tahun_m3'] = (merged['Volume_Total_Tahunan_m3'] / merged['Penduduk_Jiwa']).round(6)
    merged['Timbulan_Liter_Per_Orang_Hari'] = ((merged['Volume_Total_Tahunan_m3'] * 1000) / (merged['Penduduk_Jiwa'] * 365)).round(4)
    merged['Kumulatif_Volume_Sampah_m3'] = merged['Volume_Total_Tahunan_m3'].cumsum()
    
    corr = merged['Jumlah_Penduduk_Ribu'].corr(merged['Volume_Total_Tahunan_m3'])
    print(f"Korelasi Pearson Sampah - Penduduk: {corr:.4f}")
    
    out_path = os.path.join(DATA_DIR, 'sampah_dan_penduduk_2016_2022.csv')
    merged.to_csv(out_path, index=False)
    print(f"Hasil disimpan di: {out_path}")

if __name__ == '__main__':
    main()
