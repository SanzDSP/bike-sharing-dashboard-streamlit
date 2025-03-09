import streamlit as st
import pandas as pd
import plotly.express as px
import gdown
# Berdasarkan import package pastikan sudah melukan instalasi dengan 'pip install streamlit plotly pandas gdown'


# Load data untuk run di local atau github, untuk direktori bisa diubah saja untuk penyesuaian
# Ubah path pada teks dalam apit tanda petik 1 (r'tambahkan path file main data disini') dan hapus # untuk uncomment
#df = pd.read_csv(r'isi path disini\submission\dashboard\main_data.csv')

# Mengambil data dari drive karena lebih praktis, jika memakai path diatas maka comment baris di bawah ini hingga ke baris load data
url = f"https://drive.google.com/file/d/1FONrAWVZzjN-bwunymP33MNP_fzjpdRz/view?usp=sharing"

# Unduh dan baca file CSV
csv_path = "main_data.csv"
gdown.download(url, csv_path, quiet=False)

# Load data
df = pd.read_csv(csv_path)

# Konversi kolom tanggal sebagai antisipasi jika ada
if "dteday" in df.columns:
    df["dteday"] = pd.to_datetime(df["dteday"])

# **1️⃣ Ubah Kode Musim Menjadi Nama Musim agar mudah diobservasi**
season_mapping = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
df['season'] = df['season'].map(season_mapping)

# **2️⃣ Konversi Suhu ke Derajat Celsius untuk memperjelas rentang**
df['temp_celsius'] = df['temp'] * 41  # Suhu dalam rentang 0-41°C
df['atemp_celsius'] = df['atemp'] * 50  # Suhu terasa (feels-like)

# Judul Dashboard
st.markdown(
    "<h1 style='text-align: center;'>📊 Dashboard Analisis Penyewaan Sepeda</h1>",
    unsafe_allow_html=True
)
st.markdown("---")  # **Pembatas**

# Sidebar untuk filter
st.sidebar.header("Filter Data")
selected_source = st.sidebar.radio("Pilih Kategori Data", ["Semua", "Harian", "Jam"])

# Filter berdasarkan pilihan kategori
if selected_source == "Harian":
    df_filtered = df[df["source"] == "day"]
elif selected_source == "Jam":
    df_filtered = df[df["source"] == "hour"]
else:
    df_filtered = df  # "Semua" -> Gunakan seluruh data

# **3️⃣ Visualisasi Tren Penyewaan Sepeda Berdasarkan Musim**
st.subheader("🚴‍♂️ Tren Penyewaan Sepeda Berdasarkan Musim")
fig_season = px.box(df_filtered, x="season", y="cnt", color="season",
                    labels={"cnt": "Jumlah Penyewaan", "season": "Musim"},
                    title="Distribusi Penyewaan Sepeda per Musim")
st.plotly_chart(fig_season)
st.markdown("---")  # **Pembatas**

# **4️⃣ Hubungan antara Suhu dan Jumlah Penyewaan Sepeda**
st.subheader("🌡️ Hubungan Suhu dan Penyewaan Sepeda")
fig_temp = px.scatter(df_filtered, x="temp_celsius", y="cnt", color="temp_celsius",
                    labels={"cnt": "Jumlah Penyewaan", "temp_celsius": "Suhu (°C)"},
                    title="Korelasi Suhu dan Penyewaan Sepeda")
st.plotly_chart(fig_temp)
st.markdown("---")  # **Pembatas**

# **5️⃣ Pola Penyewaan Sepeda Berdasarkan Hari Kerja & Akhir Pekan**
st.subheader("📅 Pola Penyewaan Sepeda: Hari Kerja vs Akhir Pekan")
df_filtered["day_type"] = df_filtered["workingday"].map({0: "Akhir Pekan", 1: "Hari Kerja"})
fig_workingday = px.box(df_filtered, x="day_type", y="cnt", color="day_type",
                    labels={"cnt": "Jumlah Penyewaan", "day_type": "Jenis Hari"},
                    title="Distribusi Penyewaan Sepeda: Hari Kerja vs Akhir Pekan")
st.plotly_chart(fig_workingday)
st.markdown("---")  # **Pembatas**

# **6️⃣ Jam Paling Sibuk dalam Penyewaan Sepeda**
if selected_source in ["Semua", "Jam"] and "hr" in df.columns:
    st.subheader("⏰ Jam Paling Sibuk untuk Penyewaan Sepeda")
    fig_hour = px.line(df[df["source"] == "hour"].groupby("hr")["cnt"].mean().reset_index(),
                    x="hr", y="cnt", markers=True,
                    labels={"cnt": "Rata-rata Penyewaan", "hr": "Jam"},
                    title="Rata-rata Penyewaan Sepeda per Jam")
    st.plotly_chart(fig_hour)
    st.markdown("---")  # **Pembatas**

# Footer
st.markdown(
    "<h4 style='text-align: center;'>🚀 Thanks for Watching! 🚀</h4>",
    unsafe_allow_html=True
)
