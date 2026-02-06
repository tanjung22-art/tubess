# Dashboard Analisis Kemacetan Lalu Lintas Kota Bandung

## Deskripsi Project
Project ini merupakan sistem analisis tingkat kemacetan lalu lintas di Kota Bandung yang menggunakan teknik web scraping untuk mengumpulkan data dan visualisasi interaktif menggunakan Streamlit.

## Fitur Utama
1. **Web Scraping**: Pengumpulan data kemacetan dari 10 lokasi strategis di Bandung
2. **Dashboard Interaktif**: Visualisasi data dengan berbagai grafik dan peta
3. **Analisis Temporal**: Pola kemacetan berdasarkan waktu (harian, mingguan, jam)
4. **Peta GIS**: Visualisasi geografis tingkat kemacetan
5. **Analisis Rush Hour**: Identifikasi jam-jam sibuk
6. **Export Data**: Download data dalam format CSV

## Struktur File
```
traffic_analysis/
├── scraping_kemacetan_ex.py     # Script untuk scraping data
├── app_visualisasi_dan_gis.py     # Dashboard Streamlit
├── kemacetan.xlsx                  # Dataset hasil scraping
├── requirements.txt                # Dependencies
└── README.md                       # Dokumentasi
```

## Instalasi

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Jalankan Scraping (Opsional - data sudah tersedia)
```bash
python scraping_kemacetan_ex.py
```

### 3. Jalankan Dashboard
```bash
streamlit run app_visualisasi_dan_gis.py
```

## Cara Menggunakan

### Scraping Data
Script `scraping_kemacetan_ex.py` akan:
- Generate data kemacetan untuk 30 hari terakhir
- Mengumpulkan data dari 10 lokasi strategis di Bandung
- Menyimpan hasil dalam format Excel (.xlsx)

### Dashboard
Dashboard menyediakan 5 tab utama:

1. **Analisis Temporal**
   - Tren kemacetan harian
   - Rata-rata per hari dalam seminggu
   - Heatmap jam vs hari

2. **Peta Kemacetan**
   - Visualisasi geografis tingkat kemacetan
   - Detail statistik per lokasi

3. **Analisis Lokasi**
   - Analisis mendalam per lokasi
   - Pola kecepatan harian
   - Distribusi status kemacetan
   - Volume kendaraan

4. **Pola Jam Sibuk**
   - Identifikasi rush hour
   - Top 5 jam tersibuk
   - Perbandingan weekday vs weekend

5. **Data Tabel**
   - Data mentah lengkap
   - Fitur sorting dan filtering
   - Download CSV

### Filter Data
Dashboard dilengkapi filter interaktif:
- **Rentang Tanggal**: Pilih periode data
- **Lokasi**: Pilih satu atau beberapa lokasi
- **Hari**: Filter berdasarkan hari tertentu

## Lokasi yang Dianalisis
1. Jalan Pasteur
2. Jalan Soekarno-Hatta
3. Jalan Dago
4. Jalan Buah Batu
5. Jalan Cibiru
6. Jalan Kopo
7. Jalan Cihampelas
8. Jalan Sukajadi
9. Jalan Ahmad Yani
10. Jalan Riau

## Metrik Utama
- **Kecepatan Rata-rata**: Kecepatan kendaraan dalam km/jam
- **Tingkat Kemacetan**: Skala 1-10 (1=Lancar, 10=Sangat Macet)
- **Volume Kendaraan**: Jumlah kendaraan per jam
- **Indeks Waktu Tempuh**: Rasio waktu tempuh aktual vs normal

## Status Kemacetan
- **Sangat Lancar**: Tingkat kemacetan 1-2
- **Lancar**: Tingkat kemacetan 3-4
- **Ramai**: Tingkat kemacetan 5-6
- **Macet**: Tingkat kemacetan 7-8
- **Sangat Macet**: Tingkat kemacetan 9-10

## Teknologi yang Digunakan
- **Python 3.x**: Bahasa pemrograman utama
- **Pandas**: Manipulasi dan analisis data
- **Streamlit**: Framework dashboard interaktif
- **Plotly**: Library visualisasi data
- **OpenPyXL**: Membaca/menulis file Excel

## Author
Data Science Team - February 2026

## Lisensi
Educational Purpose Only
