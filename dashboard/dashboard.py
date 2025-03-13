import streamlit as st
import pandas as pd
import plotly.express as px
import gdown

# Unduh data dari Google Drive
file_id = "1FONrAWVZzjN-bwunymP33MNP_fzjpdRz"
url = f"https://drive.google.com/uc?id={file_id}"
csv_path = "main_data.csv"
gdown.download(url, csv_path, quiet=False)

# Load data
df = pd.read_csv(csv_path)

# Konversi kolom tanggal jika tersedia
if "dteday" in df.columns:
    df["dteday"] = pd.to_datetime(df["dteday"])

# Ubah kode musim menjadi nama musim
season_mapping = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
df['season'] = df['season'].map(season_mapping)

# Konversi suhu ke derajat Celsius
df['temp_celsius'] = df['temp'] * 41

df['atemp_celsius'] = df['atemp'] * 50

# Judul Dashboard
st.markdown("<h1 style='text-align: center;'>📊 Dashboard Analisis Penyewaan Sepeda</h1>", unsafe_allow_html=True)
st.markdown("---")  

# **Menambahkan Fitur Interaktif**
st.sidebar.header("Filter Data")

# Filter berdasarkan tanggal
start_date = st.sidebar.date_input("Pilih tanggal mulai", df["dteday"].min())
end_date = st.sidebar.date_input("Pilih tanggal akhir", df["dteday"].max())
df_filtered = df[(df["dteday"] >= pd.Timestamp(start_date)) & (df["dteday"] <= pd.Timestamp(end_date))]

# Filter berdasarkan musim
selected_season = st.sidebar.multiselect("Pilih Musim", df["season"].unique(), default=df["season"].unique())
df_filtered = df_filtered[df_filtered["season"].isin(selected_season)]

# Filter berdasarkan kondisi cuaca
weather_mapping = {1: "Cerah", 2: "Berawan", 3: "Hujan", 4: "Salju"}
df_filtered["weathersit"] = df_filtered["weathersit"].map(weather_mapping)
selected_weather = st.sidebar.multiselect("Pilih Kondisi Cuaca", df_filtered["weathersit"].unique(), default=df_filtered["weathersit"].unique())
df_filtered = df_filtered[df_filtered["weathersit"].isin(selected_weather)]

# **Visualisasi 1: Tren Penyewaan Sepeda Berdasarkan Musim**
st.subheader("🚴‍♂️ Tren Penyewaan Sepeda Berdasarkan Musim")
fig_season = px.bar(df_filtered.groupby("season")["cnt"].mean().reset_index(), x="season", y="cnt", color="season",
                    labels={"cnt": "Rata-rata Penyewaan", "season": "Musim"},
                    title="Rata-rata Penyewaan Sepeda per Musim")
st.plotly_chart(fig_season)
st.markdown("---")

# **Visualisasi 2: Hubungan Suhu dan Penyewaan Sepeda**
st.subheader("🌡️ Hubungan Suhu dan Penyewaan Sepeda")
fig_temp = px.scatter(df_filtered, x="temp_celsius", y="cnt", color="temp_celsius",
                    labels={"cnt": "Jumlah Penyewaan", "temp_celsius": "Suhu (°C)"},
                    title="Korelasi Suhu dan Penyewaan Sepeda")
st.plotly_chart(fig_temp)
st.markdown("---")

# **Visualisasi 3: Pola Penyewaan Sepeda Berdasarkan Hari Kerja & Akhir Pekan**
st.subheader("📅 Pola Penyewaan Sepeda: Hari Kerja vs Akhir Pekan")
df_filtered["day_type"] = df_filtered["workingday"].map({0: "Akhir Pekan", 1: "Hari Kerja"})
fig_workingday = px.bar(df_filtered.groupby("day_type")["cnt"].mean().reset_index(), x="day_type", y="cnt", color="day_type",
                        labels={"cnt": "Rata-rata Penyewaan", "day_type": "Jenis Hari"},
                        title="Rata-rata Penyewaan Sepeda: Hari Kerja vs Akhir Pekan")
st.plotly_chart(fig_workingday)
st.markdown("---")

# **Visualisasi 4: Jam Paling Sibuk dalam Penyewaan Sepeda**
if "hr" in df.columns:
    st.subheader("⏰ Jam Paling Sibuk untuk Penyewaan Sepeda")
    fig_hour = px.line(df_filtered.groupby("hr")["cnt"].mean().reset_index(),
                    x="hr", y="cnt", markers=True,
                    labels={"cnt": "Rata-rata Penyewaan", "hr": "Jam"},
                    title="Rata-rata Penyewaan Sepeda per Jam")
    st.plotly_chart(fig_hour)
    st.markdown("---")

# Footer
st.markdown("<h4 style='text-align: center;'>🚀 Thanks for Watching! 🚀</h4>", unsafe_allow_html=True)
