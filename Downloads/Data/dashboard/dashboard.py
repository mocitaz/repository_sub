import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Bike Sharing Analytics Dashboard 🚲",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk tampilan modern
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
    }
    .stApp {
        background-color: #141922;
    }
    .sidebar .sidebar-content {
        background-color: #2c3e50;
        color: #ecf0f1;
    }
    .sidebar .sidebar-content .stButton>button {
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 5px 15px;
    }
    .sidebar .sidebar-content .stButton>button:hover {
        background-color: #2980b9;
    }
    .stTabs [data-baseweb="tab-list"] {
        background-color: #34495e;
        border-radius: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #ecf0f1;
        font-size: 16px;
        padding: 10px 20px;
        background-color: #34495e;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #2980b9;
    }
    .stTabs [data-baseweb="tab--selected"] {
        background-color: #3498db;
        color: white;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Judul dan Deskripsi dengan Animasi Sederhana
st.markdown("""
    <h1 style="text-align: center; color: #ffff; animation: fadeIn 1s;">
        Bike Sharing Analytics Dashboard 🚲
    </h1>
    <p style="text-align: center; color: #7f8c8d;">
        Analisis data peminjaman sepeda berdasarkan faktor lingkungan dan pola waktu.<br>
        <small>Powered by Streamlit | Dibuat oleh Luthfi Fauzi</small>
    </p>
    <style>
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    </style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    day_df = pd.read_csv("data/day.csv")
    hour_df = pd.read_csv("data/hour.csv")
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    day_df['temp_celsius'] = day_df['temp'] * 41
    return day_df, hour_df

day_df, hour_df = load_data()

# Sidebar untuk Filter
with st.sidebar:
    st.header("⚙️ Filter Data")
    start_date = st.date_input("Tanggal Mulai", value=day_df['dteday'].min(), min_value=day_df['dteday'].min(), max_value=day_df['dteday'].max())
    end_date = st.date_input("Tanggal Selesai", value=day_df['dteday'].max(), min_value=day_df['dteday'].min(), max_value=day_df['dteday'].max())
    filtered_day_df = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & (day_df['dteday'] <= pd.to_datetime(end_date))]
    filtered_hour_df = hour_df[(hour_df['dteday'] >= pd.to_datetime(start_date)) & (hour_df['dteday'] <= pd.to_datetime(end_date))]
    
    # Tombol Reset
    if st.button("Reset Filter"):
        st.experimental_rerun()

    # Download Data
    st.header("📥 Download Data")
    csv = filtered_day_df.to_csv(index=False)
    st.download_button(
        label="Unduh Data Harian",
        data=csv,
        file_name=f"bike_sharing_data_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Container untuk Metrik
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        total_rentals = filtered_day_df['cnt'].sum()
        st.metric("Total Penyewaan", f"{total_rentals:,}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        avg_temp = filtered_day_df['temp_celsius'].mean().round(2)
        st.metric("Rata-rata Suhu (°C)", f"{avg_temp}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        avg_hum = (filtered_day_df['hum'] * 100).mean().round(2)
        st.metric("Rata-rata Kelembaban (%)", f"{avg_hum}")
        st.markdown('</div>', unsafe_allow_html=True)

# Tabs untuk Navigasi
tab1, tab2, tab3 = st.tabs(["📊 Korelasi Lingkungan", "⏰ Pola Peminjaman", "🔍 Analisis Lanjutan"])

# Tab 1: Korelasi Faktor Lingkungan
with tab1:
    st.header("Korelasi Faktor Lingkungan dengan Peminjaman Sepeda")
    correlation = filtered_day_df[['temp_celsius', 'hum', 'windspeed', 'cnt']].corr()
    fig1 = plt.figure(figsize=(10, 6))
    sns.heatmap(correlation, annot=True, cmap='YlGnBu', vmin=-1, vmax=1, center=0, fmt='.2f')
    plt.title('Matriks Korelasi', fontsize=14, pad=10)
    st.pyplot(fig1)
    
    with st.expander("Detail Insight"):
        st.markdown("""
            - **Suhu**: Korelasi positif kuat (~0.63) dengan peminjaman, optimal pada 15-25°C.
            - **Kelembaban**: Korelasi negatif lemah (~-0.32), tinggi kelembaban mengurangi kenyamanan.
            - **Kecepatan Angin**: Korelasi negatif sangat lemah (~-0.18), dampak minimal.
        """)

# Tab 2: Pola Peminjaman
with tab2:
    st.header("Pola Peminjaman Sepeda per Jam")
    hourly_pattern = filtered_hour_df.groupby(['hr', 'workingday'])['cnt'].mean().reset_index()
    hourly_pattern['day_type'] = hourly_pattern['workingday'].map({1: 'Hari Kerja', 0: 'Bukan Hari Kerja'})
    
    fig2 = px.line(hourly_pattern, 
                   x='hr', y='cnt', color='day_type',
                   title='Pola Peminjaman: Hari Kerja vs Bukan Hari Kerja',
                   labels={'hr': 'Jam', 'cnt': 'Rata-rata Peminjaman', 'day_type': 'Tipe Hari'},
                   template='plotly_dark')
    fig2.update_layout(xaxis=dict(tickmode='linear', tick0=0, dtick=1), showlegend=True)
    st.plotly_chart(fig2, use_container_width=True)
    
    # Hitung total penyewaan pada bukan hari kerja jam 11-16
    non_working_rentals_11_16 = filtered_hour_df[(filtered_hour_df['workingday'] == 0) & 
                                                (filtered_hour_df['hr'].between(11, 16))]['cnt'].sum()
    
    # Hitung total penyewaan pada hari kerja jam 8
    working_rentals_8am = filtered_hour_df[(filtered_hour_df['workingday'] == 1) & 
                                           (filtered_hour_df['hr'] == 8)]['cnt'].sum()
    
    # Hitung total penyewaan pada hari kerja jam 17-18
    working_rentals_5pm_6pm = filtered_hour_df[(filtered_hour_df['workingday'] == 1) & 
                                             (filtered_hour_df['hr'].between(17, 18))]['cnt'].sum()
    
    # Tampilkan metrik dalam dua kolom
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Total Penyewaan Hari Kerja(08:00)", f"{working_rentals_8am:,} sepeda")
        st.markdown('</div>', unsafe_allow_html=True)

        st.write("")

        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Total Penyewaan Hari Kerja (17:00-18)", f"{working_rentals_5pm_6pm:,} sepeda")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Total Penyewaan Bukan Hari Kerja (11:00-16:00)", f"{non_working_rentals_11_16:,} sepeda")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with st.expander("Detail Insight"):
        st.markdown("""
            - **Hari Kerja**: Puncak pada jam 8 dan 17-18 (commuting).
            - **Bukan Hari Kerja**: Puncak pada jam 11-16 (rekreasi).
        """)

# Tab 3: Analisis Lanjutan
with tab3:
    st.header("Analisis Lanjutan: Pengelompokan Tingkat Peminjaman")
    Q1 = filtered_day_df['cnt'].quantile(0.25)
    Q3 = filtered_day_df['cnt'].quantile(0.75)
    
    def categorize_rental_level(cnt):
        if cnt < Q1:
            return 'Rendah'
        elif Q1 <= cnt <= Q3:
            return 'Sedang'
        else:
            return 'Tinggi'
    
    filtered_day_df['rental_level'] = filtered_day_df['cnt'].apply(categorize_rental_level)
    rental_level_analysis = filtered_day_df.groupby('rental_level')[['temp_celsius', 'hum', 'windspeed']].mean().reset_index()
    
    # Visualisasi perbandingan
    fig3 = plt.figure(figsize=(18, 5))
    fig3.subplots_adjust(wspace=0.3)
    axes = fig3.subplots(1, 3)
    sns.barplot(x='rental_level', y='temp_celsius', data=rental_level_analysis, order=['Rendah', 'Sedang', 'Tinggi'], ax=axes[0], palette='Blues')
    axes[0].set_title('Rata-rata Suhu (°C)', fontsize=12)
    sns.barplot(x='rental_level', y='hum', data=rental_level_analysis, order=['Rendah', 'Sedang', 'Tinggi'], ax=axes[1], palette='Blues')
    axes[1].set_title('Rata-rata Kelembaban', fontsize=12)
    sns.barplot(x='rental_level', y='windspeed', data=rental_level_analysis, order=['Rendah', 'Sedang', 'Tinggi'], ax=axes[2], palette='Blues')
    axes[2].set_title('Rata-rata Kecepatan Angin', fontsize=12)
    for ax in axes:
        ax.set_xlabel('')
        ax.set_ylabel('')
    st.pyplot(fig3)
    
    with st.expander("Detail Insight"):
        st.markdown("""
            - **Tingkat Tinggi**: Suhu ~25°C, Kelembaban ~0.55, Angin ~0.15.
            - **Tingkat Rendah**: Suhu ~10°C, Kelembaban ~0.65, Angin ~0.20.
            - Kondisi hangat dan rendah kelembaban/angin mendukung peminjaman tinggi.
        """)

    # Tampilkan Data Mentah
    if st.checkbox("Tampilkan Data Mentah"):
        st.dataframe(filtered_day_df)

# Footer
st.markdown("---")
st.markdown('<p style="text-align: center; color: #7f8c8d;">© 2025 Luthfi Fauzi | Email: luthfafiwork@gmail.com</p>', unsafe_allow_html=True)

# Jalankan dengan: streamlit run app.py
