"""
Dashboard Visualisasi dan Analisis Kemacetan Lalu Lintas Kota Bandung
Menggunakan Streamlit untuk interface interaktif
Author: Data Science Team
Date: February 2026
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Kemacetan Bandung",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 5px;
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load data dari file Excel"""
    try:
        df = pd.read_excel('kemacetan.xlsx')
        df['datetime'] = pd.to_datetime(df['tanggal'] + ' ' + df['jam'])
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def main():
    # Header
    st.markdown('<div class="main-header">🚗 Dashboard Analisis Kemacetan Lalu Lintas<br>Kota Bandung</div>', 
                unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    if df is None:
        st.error("Gagal memuat data. Pastikan file 'curah_hujan_bandung.xlsx' ada di direktori yang sama.")
        return
    
    # Sidebar - Filter
    st.sidebar.header("🔍 Filter Data")
    
    # Filter tanggal
    date_range = st.sidebar.date_input(
        "Pilih Rentang Tanggal",
        value=(df['datetime'].min().date(), df['datetime'].max().date()),
        min_value=df['datetime'].min().date(),
        max_value=df['datetime'].max().date()
    )
    
    # Filter lokasi
    selected_locations = st.sidebar.multiselect(
        "Pilih Lokasi",
        options=df['lokasi'].unique(),
        default=df['lokasi'].unique()
    )
    
    # Filter hari
    selected_days = st.sidebar.multiselect(
        "Pilih Hari",
        options=df['hari'].unique(),
        default=df['hari'].unique()
    )
    
    # Apply filters
    if len(date_range) == 2:
        mask = (
            (df['datetime'].dt.date >= date_range[0]) &
            (df['datetime'].dt.date <= date_range[1]) &
            (df['lokasi'].isin(selected_locations)) &
            (df['hari'].isin(selected_days))
        )
        filtered_df = df[mask]
    else:
        filtered_df = df
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_speed = filtered_df['kecepatan_rata_rata_kmh'].mean()
        st.metric(
            "Kecepatan Rata-rata",
            f"{avg_speed:.1f} km/jam",
            delta=f"{avg_speed - df['kecepatan_rata_rata_kmh'].mean():.1f}",
            delta_color="normal"
        )
    
    with col2:
        avg_congestion = filtered_df['tingkat_kemacetan'].mean()
        st.metric(
            "Tingkat Kemacetan Rata-rata",
            f"{avg_congestion:.1f}/10",
            delta=f"{avg_congestion - df['tingkat_kemacetan'].mean():.1f}",
            delta_color="inverse"
        )
    
    with col3:
        avg_volume = filtered_df['volume_kendaraan_per_jam'].mean()
        st.metric(
            "Volume Kendaraan",
            f"{int(avg_volume):,} /jam",
            delta=f"{int(avg_volume - df['volume_kendaraan_per_jam'].mean()):,}"
        )
    
    with col4:
        avg_travel_time = filtered_df['indeks_waktu_tempuh'].mean()
        st.metric(
            "Indeks Waktu Tempuh",
            f"{avg_travel_time:.2f}x",
            delta=f"{avg_travel_time - df['indeks_waktu_tempuh'].mean():.2f}",
            delta_color="inverse"
        )
    
    # Tabs untuk berbagai visualisasi
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Analisis Temporal", 
        "🗺️ Peta Kemacetan", 
        "📈 Analisis Lokasi",
        "⏰ Pola Jam Sibuk",
        "📋 Data Tabel"
    ])
    
    with tab1:
        st.header("Analisis Pola Kemacetan Berdasarkan Waktu")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Grafik tren harian
            daily_trend = filtered_df.groupby('tanggal').agg({
                'tingkat_kemacetan': 'mean',
                'kecepatan_rata_rata_kmh': 'mean'
            }).reset_index()
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=daily_trend['tanggal'],
                y=daily_trend['tingkat_kemacetan'],
                mode='lines+markers',
                name='Tingkat Kemacetan',
                line=dict(color='#e74c3c', width=2)
            ))
            fig.update_layout(
                title='Tren Tingkat Kemacetan Harian',
                xaxis_title='Tanggal',
                yaxis_title='Tingkat Kemacetan (1-10)',
                hovermode='x unified',
                template='plotly_white'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Grafik per hari dalam seminggu
            day_avg = filtered_df.groupby('hari')['tingkat_kemacetan'].mean().reset_index()
            day_order = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
            day_avg['hari'] = pd.Categorical(day_avg['hari'], categories=day_order, ordered=True)
            day_avg = day_avg.sort_values('hari')
            
            fig = px.bar(
                day_avg,
                x='hari',
                y='tingkat_kemacetan',
                title='Rata-rata Kemacetan per Hari',
                color='tingkat_kemacetan',
                color_continuous_scale='Reds',
                labels={'tingkat_kemacetan': 'Tingkat Kemacetan'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Heatmap jam vs hari
        st.subheader("Heatmap Kemacetan: Jam vs Hari")
        
        heatmap_data = filtered_df.pivot_table(
            values='tingkat_kemacetan',
            index='jam',
            columns='hari',
            aggfunc='mean'
        )
        
        # Reorder columns - hanya gunakan hari yang ada di data
        day_order = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
        available_days = [day for day in day_order if day in heatmap_data.columns]
        heatmap_data = heatmap_data[available_days]
        
        fig = px.imshow(
            heatmap_data,
            labels=dict(x="Hari", y="Jam", color="Tingkat Kemacetan"),
            x=heatmap_data.columns,
            y=heatmap_data.index,
            color_continuous_scale='RdYlGn_r',
            aspect="auto"
        )
        fig.update_layout(title='Pola Kemacetan Berdasarkan Jam dan Hari')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.header("Peta Sebaran Kemacetan di Kota Bandung")
        
        # Aggregate data per lokasi
        location_stats = filtered_df.groupby(['lokasi', 'latitude', 'longitude']).agg({
            'tingkat_kemacetan': 'mean',
            'kecepatan_rata_rata_kmh': 'mean',
            'volume_kendaraan_per_jam': 'mean',
            'status_kemacetan': lambda x: x.mode()[0]
        }).reset_index()
        
        location_stats['size'] = location_stats['tingkat_kemacetan'] * 5
        
        # Peta scatter
        fig = px.scatter_mapbox(
            location_stats,
            lat='latitude',
            lon='longitude',
            size='size',
            color='tingkat_kemacetan',
            hover_name='lokasi',
            hover_data={
                'tingkat_kemacetan': ':.1f',
                'kecepatan_rata_rata_kmh': ':.1f',
                'volume_kendaraan_per_jam': ':,.0f',
                'status_kemacetan': True,
                'latitude': False,
                'longitude': False,
                'size': False
            },
            color_continuous_scale='RdYlGn_r',
            size_max=30,
            zoom=11,
            mapbox_style='open-street-map',
            title='Peta Tingkat Kemacetan per Lokasi'
        )
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabel detail lokasi
        st.subheader("Detail Statistik per Lokasi")
        location_display = location_stats.copy()
        location_display = location_display.rename(columns={
            'lokasi': 'Lokasi',
            'tingkat_kemacetan': 'Tingkat Kemacetan',
            'kecepatan_rata_rata_kmh': 'Kecepatan Rata-rata (km/jam)',
            'volume_kendaraan_per_jam': 'Volume Kendaraan (per jam)',
            'status_kemacetan': 'Status'
        })
        location_display = location_display[['Lokasi', 'Tingkat Kemacetan', 
                                             'Kecepatan Rata-rata (km/jam)', 
                                             'Volume Kendaraan (per jam)', 'Status']]
        location_display['Tingkat Kemacetan'] = location_display['Tingkat Kemacetan'].round(1)
        location_display['Kecepatan Rata-rata (km/jam)'] = location_display['Kecepatan Rata-rata (km/jam)'].round(1)
        location_display = location_display.sort_values('Tingkat Kemacetan', ascending=False)
        
        st.dataframe(location_display, hide_index=True, use_container_width=True)
    
    with tab3:
        st.header("Analisis Detail per Lokasi")
        
        # Pilih lokasi untuk analisis detail
        selected_location = st.selectbox(
            "Pilih Lokasi untuk Analisis Detail",
            options=filtered_df['lokasi'].unique()
        )
        
        location_data = filtered_df[filtered_df['lokasi'] == selected_location]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Tren kecepatan
            hourly_speed = location_data.groupby('jam')['kecepatan_rata_rata_kmh'].mean().reset_index()
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=hourly_speed['jam'],
                y=hourly_speed['kecepatan_rata_rata_kmh'],
                mode='lines+markers',
                fill='tozeroy',
                name='Kecepatan',
                line=dict(color='#3498db', width=2)
            ))
            fig.update_layout(
                title=f'Pola Kecepatan Harian - {selected_location}',
                xaxis_title='Jam',
                yaxis_title='Kecepatan (km/jam)',
                hovermode='x unified',
                template='plotly_white'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Distribusi status kemacetan
            status_dist = location_data['status_kemacetan'].value_counts()
            
            fig = px.pie(
                values=status_dist.values,
                names=status_dist.index,
                title=f'Distribusi Status Kemacetan - {selected_location}',
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Volume kendaraan per jam
        st.subheader("Volume Kendaraan Sepanjang Hari")
        hourly_volume = location_data.groupby('jam')['volume_kendaraan_per_jam'].mean().reset_index()
        
        fig = px.bar(
            hourly_volume,
            x='jam',
            y='volume_kendaraan_per_jam',
            title=f'Volume Kendaraan per Jam - {selected_location}',
            color='volume_kendaraan_per_jam',
            color_continuous_scale='Blues',
            labels={'volume_kendaraan_per_jam': 'Volume (kendaraan/jam)'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.header("Analisis Jam Sibuk (Rush Hour)")
        
        # Identifikasi jam tersibuk
        rush_hours = filtered_df.groupby('jam').agg({
            'tingkat_kemacetan': 'mean',
            'kecepatan_rata_rata_kmh': 'mean',
            'volume_kendaraan_per_jam': 'mean'
        }).reset_index().sort_values('tingkat_kemacetan', ascending=False)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Grafik tingkat kemacetan per jam
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=rush_hours['jam'],
                y=rush_hours['tingkat_kemacetan'],
                name='Tingkat Kemacetan',
                marker_color='crimson'
            ))
            
            fig.update_layout(
                title='Tingkat Kemacetan Rata-rata per Jam',
                xaxis_title='Jam',
                yaxis_title='Tingkat Kemacetan (1-10)',
                template='plotly_white',
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Top 5 Jam Tersibuk")
            top_5_rush = rush_hours.head(5)[['jam', 'tingkat_kemacetan']].copy()
            top_5_rush.columns = ['Jam', 'Tingkat Kemacetan']
            top_5_rush['Tingkat Kemacetan'] = top_5_rush['Tingkat Kemacetan'].round(2)
            top_5_rush.index = range(1, 6)
            st.dataframe(top_5_rush, use_container_width=True)
        
        # Perbandingan weekday vs weekend
        st.subheader("Perbandingan Weekday vs Weekend")
        
        filtered_df['is_weekend'] = filtered_df['hari'].isin(['Sabtu', 'Minggu'])
        
        comparison = filtered_df.groupby(['jam', 'is_weekend'])['tingkat_kemacetan'].mean().reset_index()
        comparison['Tipe Hari'] = comparison['is_weekend'].map({True: 'Weekend', False: 'Weekday'})
        
        fig = px.line(
            comparison,
            x='jam',
            y='tingkat_kemacetan',
            color='Tipe Hari',
            title='Perbandingan Kemacetan: Weekday vs Weekend',
            labels={'tingkat_kemacetan': 'Tingkat Kemacetan', 'jam': 'Jam'},
            color_discrete_map={'Weekday': '#e74c3c', 'Weekend': '#3498db'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.header("Data Mentah")
        
        # Filter dan sort options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sort_by = st.selectbox(
                "Urutkan berdasarkan",
                options=['tanggal', 'tingkat_kemacetan', 'kecepatan_rata_rata_kmh', 'volume_kendaraan_per_jam']
            )
        
        with col2:
            sort_order = st.radio("Urutan", options=['Ascending', 'Descending'])
        
        with col3:
            n_records = st.number_input("Tampilkan jumlah baris", min_value=10, max_value=1000, value=100, step=10)
        
        # Display data
        display_df = filtered_df.sort_values(
            sort_by, 
            ascending=(sort_order == 'Ascending')
        ).head(n_records)
        
        display_columns = [
            'tanggal', 'hari', 'jam', 'lokasi', 'tipe_jalan',
            'kecepatan_rata_rata_kmh', 'volume_kendaraan_per_jam',
            'tingkat_kemacetan', 'status_kemacetan', 'indeks_waktu_tempuh'
        ]
        
        st.dataframe(
            display_df[display_columns],
            hide_index=True,
            use_container_width=True
        )
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Data (CSV)",
            data=csv,
            file_name=f"data_kemacetan_bandung_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>Dashboard Analisis Kemacetan Lalu Lintas Kota Bandung</p>
        <p>Data Science Team | February 2026</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()