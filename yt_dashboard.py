import streamlit as st
import pandas as pd
import plotly.express as px

# Load data dari Supabase (gunakan URL file CSV)
DATA_URL = "https://qtzeycchkhbrqbzbgzrh.supabase.co/storage/v1/object/public/perpustakaan//youtube_dummy_data.csv"

#judul
st.title("📊 YouTube Channel Dashboard")
st.markdown("Analisis performa video berdasarkan data dummy YouTube. Dibuat oleh Septian 🚀")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, parse_dates=['upload_date'])
    return df

df = load_data()

# Pilihan filter channel
channels = df['channel'].unique()
channel_choice = st.selectbox("Pilih Channel", options=channels)

# Filter berdasarkan pilihan
filtered_df = df[df['channel'] == channel_choice]

# Tampilkan tabel
st.subheader("📋 Data Video")
st.dataframe(filtered_df)

# Grafik: Views per video
fig1 = px.bar(filtered_df, x='video_title', y='views', title='📈 Jumlah Views per Video')
st.plotly_chart(fig1)

# Grafik: Likes per video
fig2 = px.bar(filtered_df, x='video_title', y='likes', title='👍 Likes per Video', color='likes')
st.plotly_chart(fig2)

# Grafik: Perbandingan Likes dan Views
fig3 = px.scatter(filtered_df, x='views', y='likes', title ='💡 Likes vs Views', hover_name='video_title', size='likes', color='video_title')
st.plotly_chart(fig3)

# Statistik ringkas
st.metric("📈 Total Views", f"{df['views'].sum():,}")
st.metric("👍 Total Likes", f"{df['likes'].sum():,}")
st.metric("📊 Rata-rata Views", f"{df['views'].mean():,.2f}")
st.metric("❤️ Rata-rata Likes", f"{df['likes'].mean():,.2f}")

# Info tambahan st.subheader("📌 Insight Singkat")
top_video = filtered_df.loc[filtered_df['views'].idxmax()]
st.markdown(f"**Video paling populer:** `{top_video['video_title']}` dengan **{top_video['views']} views**")