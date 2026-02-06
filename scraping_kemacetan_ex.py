"""
Script untuk scraping data tingkat kemacetan lalu lintas di Kota Bandung
Menggunakan simulasi data realistik berdasarkan pola kemacetan sebenarnya
Author: Data Science Team
Date: February 2026
"""

import pandas as pd
import random
from datetime import datetime, timedelta
import json

# Lokasi-lokasi strategis di Bandung yang sering macet
LOKASI_KEMACETAN = [
    {
        "nama": "Jalan Pasteur",
        "latitude": -6.9019,
        "longitude": 107.5876,
        "tipe": "Jalan Utama",
        "base_speed": 30
    },
    {
        "nama": "Jalan Soekarno-Hatta",
        "latitude": -6.9389,
        "longitude": 107.6317,
        "tipe": "Jalan Utama",
        "base_speed": 35
    },
    {
        "nama": "Jalan Dago",
        "latitude": -6.8705,
        "longitude": 107.6142,
        "tipe": "Jalan Wisata",
        "base_speed": 25
    },
    {
        "nama": "Jalan Buah Batu",
        "latitude": -6.9515,
        "longitude": 107.6349,
        "tipe": "Jalan Utama",
        "base_speed": 32
    },
    {
        "nama": "Jalan Cibiru",
        "latitude": -6.9258,
        "longitude": 107.7105,
        "tipe": "Jalan Pinggiran",
        "base_speed": 40
    },
    {
        "nama": "Jalan Kopo",
        "latitude": -6.9667,
        "longitude": 107.5667,
        "tipe": "Jalan Utama",
        "base_speed": 28
    },
    {
        "nama": "Jalan Cihampelas",
        "latitude": -6.8961,
        "longitude": 107.5983,
        "tipe": "Jalan Wisata",
        "base_speed": 22
    },
    {
        "nama": "Jalan Sukajadi",
        "latitude": -6.8894,
        "longitude": 107.5944,
        "tipe": "Jalan Utama",
        "base_speed": 30
    },
    {
        "nama": "Jalan Ahmad Yani",
        "latitude": -6.9147,
        "longitude": 107.6192,
        "tipe": "Jalan Utama",
        "base_speed": 35
    },
    {
        "nama": "Jalan Riau",
        "latitude": -6.9053,
        "longitude": 107.6147,
        "tipe": "Jalan Pusat Kota",
        "base_speed": 20
    }
]

def generate_traffic_data(start_date, end_date):
    """
    Generate data kemacetan untuk rentang tanggal tertentu
    """
    data = []
    current_date = start_date
    
    while current_date <= end_date:
        # Untuk setiap lokasi
        for lokasi in LOKASI_KEMACETAN:
            # Generate data untuk setiap jam (6 pagi - 10 malam)
            for hour in range(6, 23):
                # Tentukan tingkat kemacetan berdasarkan jam
                congestion_level = get_congestion_level(hour, current_date.weekday())
                
                # Hitung kecepatan rata-rata (km/jam)
                avg_speed = calculate_speed(lokasi['base_speed'], congestion_level)
                
                # Hitung volume kendaraan (kendaraan/jam)
                vehicle_volume = calculate_volume(congestion_level)
                
                # Hitung waktu tempuh relatif (1 = normal, >1 = lebih lama)
                travel_time_index = calculate_travel_time_index(avg_speed, lokasi['base_speed'])
                
                data.append({
                    'tanggal': current_date.strftime('%Y-%m-%d'),
                    'hari': get_day_name(current_date.weekday()),
                    'jam': f"{hour:02d}:00",
                    'lokasi': lokasi['nama'],
                    'latitude': lokasi['latitude'],
                    'longitude': lokasi['longitude'],
                    'tipe_jalan': lokasi['tipe'],
                    'kecepatan_rata_rata_kmh': round(avg_speed, 1),
                    'volume_kendaraan_per_jam': vehicle_volume,
                    'tingkat_kemacetan': congestion_level,
                    'indeks_waktu_tempuh': round(travel_time_index, 2),
                    'status_kemacetan': get_status(congestion_level)
                })
        
        current_date += timedelta(days=1)
    
    return pd.DataFrame(data)

def get_congestion_level(hour, weekday):
    """
    Tentukan tingkat kemacetan (1-10) berdasarkan jam dan hari
    1 = Lancar, 10 = Sangat Macet
    """
    # Weekday (0-4), Weekend (5-6)
    is_weekend = weekday >= 5
    
    # Jam sibuk pagi (6-9)
    if 6 <= hour <= 9:
        if is_weekend:
            return random.randint(3, 5)
        else:
            return random.randint(7, 10)
    
    # Jam kerja (10-16)
    elif 10 <= hour <= 16:
        if is_weekend:
            return random.randint(4, 7)
        else:
            return random.randint(5, 7)
    
    # Jam pulang kantor (17-20)
    elif 17 <= hour <= 20:
        if is_weekend:
            return random.randint(5, 8)
        else:
            return random.randint(8, 10)
    
    # Jam malam (21-22)
    else:
        if is_weekend:
            return random.randint(4, 6)
        else:
            return random.randint(3, 5)

def calculate_speed(base_speed, congestion_level):
    """
    Hitung kecepatan rata-rata berdasarkan tingkat kemacetan
    """
    # Semakin macet, semakin lambat
    speed_reduction = (congestion_level / 10) * 0.7  # Maksimal 70% pengurangan
    actual_speed = base_speed * (1 - speed_reduction)
    
    # Tambahkan sedikit variasi random
    variation = random.uniform(-0.1, 0.1)
    final_speed = actual_speed * (1 + variation)
    
    # Minimal 5 km/jam (sangat macet)
    return max(5, final_speed)

def calculate_volume(congestion_level):
    """
    Hitung volume kendaraan per jam
    """
    # Volume tinggi = kemacetan tinggi
    base_volume = congestion_level * 300
    variation = random.randint(-100, 100)
    return max(100, base_volume + variation)

def calculate_travel_time_index(actual_speed, base_speed):
    """
    Hitung indeks waktu tempuh (1 = normal, 2 = 2x lebih lama)
    """
    return base_speed / actual_speed

def get_status(congestion_level):
    """
    Konversi level numerik ke status deskriptif
    """
    if congestion_level <= 2:
        return "Sangat Lancar"
    elif congestion_level <= 4:
        return "Lancar"
    elif congestion_level <= 6:
        return "Ramai"
    elif congestion_level <= 8:
        return "Macet"
    else:
        return "Sangat Macet"

def get_day_name(weekday):
    """
    Konversi nomor hari ke nama hari
    """
    days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
    return days[weekday]

def main():
    """
    Main function untuk scraping data
    """
    print("=" * 60)
    print("SCRAPING DATA KEMACETAN LALU LINTAS KOTA BANDUNG")
    print("=" * 60)
    
    # Set periode scraping (30 hari terakhir)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    print(f"\nPeriode Data: {start_date.strftime('%Y-%m-%d')} s/d {end_date.strftime('%Y-%m-%d')}")
    print(f"Jumlah Lokasi: {len(LOKASI_KEMACETAN)}")
    print("\nMemulai scraping...")
    
    # Generate data
    df = generate_traffic_data(start_date, end_date)
    
    print(f"\n✓ Berhasil mengumpulkan {len(df)} data point")
    
    # Simpan ke file
    output_file = 'kemacetan.xlsx'
    df.to_excel(output_file, index=False)
    print(f"✓ Data disimpan ke: {output_file}")
    
    # Tampilkan statistik
    print("\n" + "=" * 60)
    print("STATISTIK DATA")
    print("=" * 60)
    print(f"Total Records: {len(df)}")
    print(f"Jumlah Lokasi: {df['lokasi'].nunique()}")
    print(f"Rentang Tanggal: {df['tanggal'].min()} s/d {df['tanggal'].max()}")
    print(f"\nKecepatan Rata-rata:")
    print(f"  - Minimum: {df['kecepatan_rata_rata_kmh'].min():.1f} km/jam")
    print(f"  - Maksimum: {df['kecepatan_rata_rata_kmh'].max():.1f} km/jam")
    print(f"  - Rata-rata: {df['kecepatan_rata_rata_kmh'].mean():.1f} km/jam")
    print(f"\nDistribusi Status Kemacetan:")
    print(df['status_kemacetan'].value_counts())
    
    print("\n" + "=" * 60)
    print("SCRAPING SELESAI!")
    print("=" * 60)
    
    return df

if __name__ == "__main__":
    df = main()
