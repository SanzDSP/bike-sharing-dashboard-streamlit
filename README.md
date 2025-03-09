# 📊 Bike Sharing Dashboard

Dashboard ini dibuat menggunakan **Streamlit** untuk menganalisis data penyewaan sepeda berdasarkan faktor cuaca, musim, dan waktu.

---

## 🚀 Cara Menjalankan Dashboard

### 1️⃣ **Persiapan Awal**
Sebelum menjalankan dashboard, pastikan Anda sudah menginstal **Python** dan **pip**.

- **Clone repository ini**
  ```sh
  git clone https://github.com/SanzDSP/bike-sharing-dashboard-streamlit.git
  cd bike-sharing-dashboard-streamlit
  ```

- **Buat virtual environment (opsional, tapi direkomendasikan)**
  ```sh
  python -m venv venv
  source venv/bin/activate  # Untuk macOS/Linux
  venv\Scripts\activate  # Untuk Windows
  ```

- **Install dependensi**
  ```sh
  pip install -r requirements.txt
  ```

---

### 2️⃣ **Menjalankan Dashboard**

- **Jalankan perintah berikut:**
  ```sh
  streamlit run dashboard.py
  ```
- **Dashboard akan terbuka otomatis di browser** atau dapat diakses di alamat:
  ```
  http://localhost:8501
  ```

---

### 3️⃣ **Struktur Proyek**
```
submission
├── dashboard
│   ├── dashboard.py  # Script utama untuk Streamlit
│   ├── main_data.csv  # Dataset utama (diunduh otomatis dari Google Drive)
├── data
│   ├── data_1.csv
│   └── data_2.csv
├── notebook.ipynb  # Notebook analisis data
├── requirements.txt  # Dependensi Python yang dibutuhkan
├── README.md  # Panduan (Anda berada disini!)
```

---

## 📂 **Data**
Dataset penyewaan sepeda berasal dari **Bike Sharing Dataset** dan akan diunduh otomatis menggunakan `gdown` dari Google Drive saat dashboard dijalankan.

---

## 🛠 **Troubleshooting**
Jika terjadi error saat menjalankan dashboard, coba langkah berikut:

1. **Pastikan Streamlit dan package terinstal**
   ```sh
   pip install streamlit pandas plotly gdown
   ```
2. **Gunakan virtual environment untuk menghindari konflik library**
3. **Cek apakah dataset berhasil diunduh di folder `dashboard/`**

---

🚀 **Enjoy analyzing bike sharing trends with this interactive dashboard!** 🚀