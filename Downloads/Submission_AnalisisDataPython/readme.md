# Proyek Analisis Penyewaan Sepeda

## Deskripsi
Proyek ini bertujuan untuk menganalisis data dari *Bike Sharing Dataset* untuk menjawab dua pertanyaan utama:
1. **Bagaimana hubungan antara suhu, kelembaban, dan kecepatan angin memengaruhi jumlah peminjaman sepeda?**
   - Tujuan: Menganalisis pengaruh faktor cuaca terhadap jumlah peminjaman sepeda.
2. **Bagaimana pola peminjaman sepeda bervariasi selama 24 jam pada hari kerja dibandingkan dengan akhir pekan?**
   - Tujuan: Menentukan jam-jam puncak peminjaman sepeda untuk perencanaan operasional.

Proyek ini mencakup analisis data mendalam dalam notebook Jupyter, visualisasi interaktif, serta pembuatan dashboard dinamis menggunakan Streamlit. Dashboard ini memungkinkan pengguna untuk memfilter data berdasarkan waktu tertentu dan mengunduh hasilnya.

## Cara Menjalankan Dashboard
1. Pastikan Anda berada di direktori proyek: `cd /path/to/ANALISIS-DATA-DENGAN-PYTHON`.
2. Aktifkan virtual environment:
   - macOS/Linux: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`
3. Instal dependensi dengan perintah: `pip install -r requirements.txt`.
4. Jalankan dashboard dengan perintah: `streamlit run dashboard/app.py`.
5. Buka browser dan akses dashboard di `http://localhost:8501`.

## Struktur Direktori
## Cara Menjalankan Proyek

### Prasyarat
- **Python 3.x**
- **Virtual environment** (opsional, disarankan)
- **Library yang diperlukan** (tercantum di `requirements.txt`)

### Langkah-langkah

1. **Kloning Repository**
   - `git clone <repository_url>`
   - `cd <folder_name>`

2. **Siapkan Lingkungan**
   - Buat virtual environment (opsional):
     - `python -m venv venv`
     - macOS/Linux: `source venv/bin/activate`
     - Windows: `venv\Scripts\activate`
   - Instal dependensi: `pip install -r requirements.txt`

3. **Jalankan Notebook**
   - Buka `notebook.ipynb` di Jupyter Notebook atau VSCode untuk melihat analisis lengkap, termasuk visualisasi korelasi dan pola peminjaman.

4. **Jalankan Dashboard**
   - Aktifkan virtual environment (jika digunakan).
   - Jalankan dashboard lokal dengan `streamlit run dashboard/app.py`.
   - Buka browser di `http://localhost:8501` untuk melihat dashboard interaktif.

5. **Akses Online (Opsional)**
   - Kunjungi tautan di `url.txt` untuk mengakses dashboard yang dideploy di Streamlit Community Cloud setelah deployment.

## Fitur Utama
- **Visualisasi Interaktif**:
  - Heatmap korelasi untuk suhu, kelembaban, dan kecepatan angin.
  - Line plot interaktif (Plotly) untuk pola peminjaman per jam.
  - Bar plot untuk perbandingan faktor lingkungan berdasarkan tingkat peminjaman.
- **Filter Dinamis**: Pilih tahun (2011/2012) dan bulan melalui sidebar untuk analisis spesifik.
- **Analisis Lanjutan**: Pengelompokan tingkat peminjaman (Rendah, Sedang, Tinggi) berdasarkan jumlah penyewaan.
- **Fitur Tambahan**: Metrik total penyewaan, rata-rata suhu/kelembaban, dan opsi unduh data dalam format CSV.
- **Desain Profesional**: Layout rapi dengan sidebar, tabs, dan tema yang responsif.

## Insight Utama
- **Pengaruh Faktor Lingkungan**: 
  - Penyewaan tertinggi terjadi pada suhu hangat (~25°C), kelembaban rendah (~0.55), dan kecepatan angin rendah (~0.15).
  - Suhu memiliki korelasi positif kuat (~0.63), sementara kelembaban dan angin memiliki pengaruh negatif lemah.
- **Pola Peminjaman**: 
  - Hari kerja: Puncak pada jam 08:00 dan 17:00-18:00 (commuting, ~400-450 sepeda).
  - Bukan hari kerja: Puncak pada jam 11:00-16:00 (rekreasi, ~300-350 sepeda).
  - Total penyewaan bukan hari kerja jam 11:00-16:00 signifikan untuk perencanaan operasional.
- **Tren Umum**: Kondisi cuaca ideal meningkatkan penyewaan, dengan pola yang stabil pada akhir pekan.

## Cara Deployment ke Streamlit Cloud
1. Buat akun di [Streamlit Community Cloud](https://streamlit.io/cloud).
2. Buat repository GitHub baru atau gunakan yang ada.
3. Hubungkan repository ke Streamlit Cloud, tentukan `dashboard/app.py` sebagai file utama.
4. Tambahkan `requirements.txt` ke repository.