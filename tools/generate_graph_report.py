import json

def main():
    with open('Tugas 1/.neuron/graph.json', 'r', encoding='utf-8') as f:
        g = json.load(f)

    in_deg = {}
    out_deg = {}
    for l in g['links']:
        s = l['source']
        t = l['target']
        out_deg[s] = out_deg.get(s, 0) + 1
        in_deg[t] = in_deg.get(t, 0) + 1

    total_deg = {}
    for n in g['nodes']:
        nid = n['id']
        total_deg[nid] = in_deg.get(nid, 0) + out_deg.get(nid, 0)

    sorted_nodes = sorted(g['nodes'], key=lambda x: total_deg[x['id']], reverse=True)

    report = []
    report.append('# Laporan Knowledge Graph Komprehensif: Tugas 1 Pemodelan Matematika TPA Randukuning Batang\n')
    report.append('**Tanggal Pembaruan**: 2026-09-16  ')
    report.append('**Cakupan**: Seluruh Entitas Data, Formulasi Matematika, Deret Waktu SARIMA, Baseline, Literatur Ilmiah, Kebijakan, dan Manuskrip pada `Tugas 1/`  ')
    report.append('**Standar Aksesibilitas**: 100% Data Teks Terstruktur sesuai pedoman `/media/ramadhan/0C6A-1ABD/AGENTS.md`.\n')
    report.append('---\n')
    report.append('## 1. Ringkasan Metrik Knowledge Graph')
    report.append(f'- **Total Simpul (*Nodes*)**: **{len(g["nodes"])} Simpul**')
    report.append(f'- **Total Relasi Berarah (*Edges / Links*)**: **{len(g["links"])} Relasi**')
    report.append(f'- **Klaster Komunitas Tematik**: **{g["graph"]["total_communities"]} Klaster**')
    report.append('- **Format Penyimpanan**:\n  - Basis Data Graf: [`graph.json`](file:///media/ramadhan/0C6A-1ABD/University/Pemodelan%20Matematika/Tugas%201/.neuron/graph.json)\n  - Laporan Naratif & Struktur Relasi: [`GRAPH_REPORT.md`](file:///media/ramadhan/0C6A-1ABD/University/Pemodelan%20Matematika/Tugas%201/.neuron/GRAPH_REPORT.md)\n')
    report.append('---\n')
    report.append('## 2. Simpul Sentral Utama (*God Nodes* - Titik Konvergensi Relasi Tertinggi)')
    for rank, node in enumerate(sorted_nodes[:7], 1):
        nid = node['id']
        deg = total_deg[nid]
        in_c = in_deg.get(nid, 0)
        out_c = out_deg.get(nid, 0)
        report.append(f'{rank}. **`{node["label"]}`** (*{nid}*) — **{deg} Relasi** (Masuk: {in_c}, Keluar: {out_c})  \n   {node["summary"]}')

    report.append('\n---\n')
    report.append('## 3. Rincian 7 Klaster Komunitas Tematik\n')

    community_names = {
        0: 'Fisik & Dinamika Degradasi Landfill TPA Randukuning',
        1: 'Logistik DLH, Armada & Efisiensi Pengangkutan',
        2: 'Sosio-Demografi, Sensus & Disparitas Spasial 15 Kecamatan',
        3: 'Ekonomi Makro, PDRB, Konsumsi & Industrialisasi KITB',
        4: 'Formulasi Analitik & Komputasi Sistem Dinamik Diferensial',
        5: 'Tata Kelola Kebijakan, Partisipasi Publik & Manuskrip Awal',
        6: 'Pemodelan Deret Waktu SARIMA, Baseline & Validasi Empiris (Kesepakatan Baru catatan1.md)'
    }

    for c_id in range(7):
        c_nodes = [n for n in g['nodes'] if n['community'] == c_id]
        c_name = community_names.get(c_id, f'Komunitas {c_id}')
        report.append(f'### Komunitas {c_id}: {c_name} ({len(c_nodes)} Simpul)')
        for n in c_nodes:
            report.append(f'- **`{n["id"]}`** (*{n["label"]}*): {n["summary"]}')
        report.append('')

    report.append('---\n')
    report.append('## 4. Rincian Relasi Berarah (*Edges / Links*)\n')
    report.append('| Sumber (*Source*) | Relasi (*Predicate*) | Target (*Target*) |')
    report.append('| :--- | :--- | :--- |')
    for l in g['links']:
        report.append(f'| `{l["source"]}` | `{l["relation"]}` | `{l["target"]}` |')

    report.append('\n---\n')
    report.append('## 5. Signifikansi Metodologis Pembaruan Graf (Kesepakatan catatan1.md)\n')
    report.append('Penambahan Komunitas 6 memperluas cakupan graf dari yang sebelumnya berfokus pada sistem dinamik diferensial kontinu menjadi paradigma terpadu yang mencakup pemodelan stokastik deret waktu (*time series*):')
    report.append('1. **Prinsip Falsifikasi Empiris:** Menempatkan `baseline_seasonal_naive` dan `baseline_holt_winters` sebagai pembanding wajib sebelum model `model_sarima_musiman_12` dapat dijustifikasi.')
    report.append('2. **Disiplin Validasi Temporal:** Menghubungkan `skema_validasi_time_split` untuk mencegah *lookahead bias* dalam pemodelan data deret waktu.')
    report.append('3. **Diagnostik Residual Rigor:** Mengintegrasikan `uji_diagnostik_residual_ljung_box` guna memastikan residual model memenuhi syarat keacakan murni (*white noise*).')
    report.append('4. **Evaluasi Anomali Objektif:** Memetakan `analisis_anomali_covid_2020` sebagai bahan investigasi *structural break* tanpa lompatan kesimpulan kausal.')

    with open('Tugas 1/.neuron/GRAPH_REPORT.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report) + '\n')

    print(f'GRAPH_REPORT.md successfully updated! Total nodes: {len(g["nodes"])}, Total links: {len(g["links"])}')

if __name__ == '__main__':
    main()
