import streamlit as st
import sqlite3
import os
from datetime import datetime

# --- Setup SQLite ---
conn = sqlite3.connect("data_proyek.db", check_same_thread=False)
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS proyek (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        luas REAL,
        harga REAL,
        biaya REAL,
        margin REAL,
        estimasi REAL,
        nama_file TEXT
    )
''')
conn.commit()

# --- Streamlit UI ---
st.title("Kalkulator Estimasi Proyek + Upload File")

luas = st.number_input("Masukkan luas tanah (m²)", min_value=0.0)
harga = st.number_input("Masukkan harga per m² (Rp)", min_value=0.0)
biaya = st.number_input("Masukkan biaya pembangunan (Rp)", min_value=0.0)
margin = st.number_input("Masukkan margin keuntungan (%)", min_value=0.0)

uploaded_file = st.file_uploader("Upload file terkait (opsional)")

if st.button("Hitung Estimasi & Simpan"):
    nilai_dasar = (luas * harga) + biaya
    nilai_akhir = nilai_dasar + (nilai_dasar * margin / 100)

    # --- Simpan file jika ada ---
    file_name = ""
    if uploaded_file is not None:
        os.makedirs("uploads", exist_ok=True)
        file_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uploaded_file.name}"
        with open(os.path.join("uploads", file_name), "wb") as f:
            f.write(uploaded_file.read())

    # --- Simpan ke database ---
    c.execute('''
        INSERT INTO proyek (timestamp, luas, harga, biaya, margin, estimasi, nama_file)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        datetime.now().isoformat(),
        luas, harga, biaya, margin, nilai_akhir, file_name
    ))
    conn.commit()

    st.success(f"Estimasi nilai proyek: Rp {nilai_akhir:,.0f}")
    st.info("Data berhasil disimpan ke database.")

# --- Tampilkan semua data yang tersimpan (opsional) ---
with st.expander("Lihat Data Tersimpan"):
    data = c.execute("SELECT * FROM proyek").fetchall()
    for row in data:
        st.write(row)
