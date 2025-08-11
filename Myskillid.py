import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Analisis Penjualan SuperStore", layout="wide")
st.title("📊 Dashboard Penjualan SuperStore")
st.markdown("Analisis SuperStore dari Myskill.id | Dibuat oleh Septian 🚀")

# Load data
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1jXq05G-kdxobNkKYuBWszKsnQ_10EiEB/export?format=csv"
    df = pd.read_csv(url, parse_dates=['Order Date'])
    df['Tahun'] = df['Order Date'].dt.year
    return df

df = load_data()
df['Tahun'] = df['Order Date'].dt.year
df['Category'] = df['Product Category']
df['Order Total'] = pd.to_numeric(df['Order Total'], errors='coerce')


# Metrik Utama
total_penjualan = df['Order Total'].sum()
jumlah_transaksi = df.shape[0]
rata2_transaksi = df['Order Total'].mean()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Penjualan", f"Rp {total_penjualan:,.0f}")
col2.metric("📦 Jumlah Transaksi", jumlah_transaksi)
col3.metric("📊 Rata-rata Transaksi", f"Rp {rata2_transaksi:,.0f}")

# Penjualan per Tahun dan Kategori
st.header("📈 Penjualan per Tahun dan Kategori")
penjualan_tahunan = df.groupby(['Tahun', 'Category'])['Order Total'].sum().unstack()
fig, ax = plt.subplots(figsize=(10,6))
penjualan_tahunan.plot(kind='bar', ax=ax)
plt.title('Total Penjualan per Tahun berdasarkan Kategori Produk')
plt.xlabel('Tahun')
plt.ylabel('Total Penjualan (Rp)')
plt.tight_layout()
st.pyplot(fig)

# Kota Terbaik
st.header("🏙️ Kota dengan Penjualan Tertinggi")
penjualan_kota = df.groupby('City')['Order Total'].sum().sort_values(ascending=False).head(10)
fig2, ax2 = plt.subplots(figsize=(8,6))
penjualan_kota.plot(kind='barh', color='green', ax=ax2)
plt.title('Kota dengan Total Penjualan Tertinggi')
plt.xlabel('Total Penjualan (Rp)')
plt.ylabel('Kota')
plt.gca().invert_yaxis()
plt.tight_layout()
st.pyplot(fig2)

kontribusi_customer = df.groupby('Customer Type')['Order Total'].sum().sort_values(ascending=False)


fig = px.bar(kontribusi_customer, 
             x=kontribusi_customer.index, 
             y=kontribusi_customer.values,
             labels={'x': 'Tipe Customer', 'y': 'Total Penjualan'},
             title='Kontribusi Penjualan per Tipe Customer')
st.plotly_chart(fig, use_container_width=True)


# Preview Data
st.header("🔍 Data Tersaring (Preview)")
st.dataframe(df.head(50))


#kredits
st.markdown("---")
st.caption("📌 Dibuat oleh Septian Dharma S S – powered by Streamlit")
