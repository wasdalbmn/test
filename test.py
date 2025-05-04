import streamlit as st

st.title("Kalkulator Estimasi Proyek")

luas = st.number_input("Masukkan luas tanah (m²)")
harga = st.number_input("Masukkan harga per m² (Rp)")
biaya = st.number_input("Masukkan biaya pembangunan (Rp)")
margin = st.number_input("Masukkan margin keuntungan (%)")

if st.button("Hitung Estimasi"):
    nilai_dasar = (luas * harga) + biaya
    nilai_akhir = nilai_dasar + (nilai_dasar * margin / 100)
    st.success(f"Estimasi nilai proyek: Rp {nilai_akhir:,.0f}")
