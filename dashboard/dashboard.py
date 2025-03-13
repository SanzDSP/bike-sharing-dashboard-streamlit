import streamlit as st
import pandas as pd
import plotly.express as px
import gdown

# ID file dari Google Drive
file_id = "1FONrAWVZzjN-bwunymP33MNP_fzjpdRz"
url = f"https://drive.google.com/uc?id={file_id}"
csv_path = "main_data.csv"
gdown.download(url, csv_path, quiet=False)

# Load data
df = pd.read_csv(csv_path)

# Konversi kolom tanggal ke format datetime
df["dteday"] = pd.to_datetime(df["dteday"])

# Ubah kode musim menjadi nama musim
season_mapping = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
df['season'] = df['season'].map(season_mapping)

# Konversi suhu ke Celsius
df['temp_celsius'] = df['temp'] * 41

def create_dashboard():
    st.title("📊 Dashboard Analisis Penyewaan Sepeda")
    st.sidebar.header("Filter Data")
    
    # 1️⃣ Filter berdasarkan tanggal
    start_date = st.sidebar.date_input("Pilih tanggal mulai", df["dteday"].min())
    end_date = st.sidebar.date_input("Pilih tanggal akhir", df["dteday"].max())
    
    # 2️⃣ Filter berdasarkan musim
    selected_season = st.sidebar.multiselect("Pilih musim", df["season"].unique(), default=df["season"].unique())
    
    # 3️⃣ Filter berdasarkan kondisi cuaca
    selected_weather = st.sidebar.multiselect("Pilih kondisi cuaca", df["weathersit"].unique(), default=df["weathersit"].unique())
    
    # Terapkan filter
    df_filtered = df[(df["dteday"] >= pd.to_datetime(start_date)) &
                     (df["dteday"] <= pd.to_datetime(end_date)) &
                     (df["season"].isin(selected_season)) &
                     (df["weathersit"].isin(selected_weather))]
    
    # 📌 Visualisasi Tren Penyewaan Sepeda Berdasarkan Musim
    st.subheader("🚴‍♂️ Penyewaan Sepeda Berdasarkan Musim")
    fig_season = px.bar(df_filtered.groupby("season")["cnt"].sum().reset_index(),
                        x="season", y="cnt", color="season",
                        labels={"cnt": "Total Penyewaan", "season": "Musim"},
                        title="Total Penyewaan Sepeda per Musim")
    st.plotly_chart(fig_season)
    
    # 📌 Hubungan Suhu dan Penyewaan Sepeda
    st.subheader("🌡️ Hubungan Suhu dan Penyewaan Sepeda")
    fig_temp = px.scatter(df_filtered, x="temp_celsius", y="cnt", color="temp_celsius",
                          labels={"cnt": "Jumlah Penyewaan", "temp_celsius": "Suhu (°C)"},
                          title="Korelasi Suhu dan Penyewaan Sepeda")
    st.plotly_chart(fig_temp)
    
    # 📌 Penyewaan Sepeda Berdasarkan Hari
    st.subheader("📅 Pola Penyewaan Sepeda")
    df_filtered["day_type"] = df_filtered["workingday"].map({0: "Akhir Pekan", 1: "Hari Kerja"})
    fig_workingday = px.bar(df_filtered.groupby("day_type")["cnt"].sum().reset_index(),
                             x="day_type", y="cnt", color="day_type",
                             labels={"cnt": "Total Penyewaan", "day_type": "Jenis Hari"},
                             title="Penyewaan Sepeda: Hari Kerja vs Akhir Pekan")
    st.plotly_chart(fig_workingday)
    
    # 📌 Jam Paling Sibuk dalam Penyewaan Sepeda
    st.subheader("⏰ Jam Paling Sibuk untuk Penyewaan Sepeda")
    if "hr" in df.columns:
        fig_hour = px.line(df_filtered.groupby("hr")["cnt"].mean().reset_index(),
                           x="hr", y="cnt", markers=True,
                           labels={"cnt": "Rata-rata Penyewaan", "hr": "Jam"},
                           title="Rata-rata Penyewaan Sepeda per Jam")
        st.plotly_chart(fig_hour)
    
    st.markdown("---")
    st.markdown("<h4 style='text-align: center;'>🚀 Terima kasih telah menggunakan dashboard ini! 🚀</h4>", unsafe_allow_html=True)

if __name__ == "__main__":
    create_dashboard()
