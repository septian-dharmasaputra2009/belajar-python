import streamlit as st
import pandas as pd
import plotly.express as px

# Load data dari Supabase (gunakan URL file CSV)
DATA_URL = "https://qtzeycchkhbrqbzbgzrh.supabase.co/storage/v1/object/public/perpustakaan//youtube_dummy_data.csv"

#load data
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, parse_dates=['upload_date'])
    return df

df = load_data()

#judul, & deskripsi
st.title("📊 YouTube Channel Dashboard")
st.markdown("Analisis performa video berdasarkan data dummy YouTube. Dibuat oleh Septian 🚀")

# Pilihan filter channel
channels = df['channel'].unique()
channel_choice = st.selectbox("Pilih Channel", options=channels)

# Filter berdasarkan pilihan
filtered_df = df[df['channel'] == channel_choice]

#metric card
col1, col2, col3 = st.columns(3)
col1.metric("Total Views", f"{filtered_df['views'].sum():,}")
col2.metric("Total Likes", f"{filtered_df['likes'].sum():,}")
col3.metric("Jumlah Video", len(filtered_df))

# analisis tambahan
# Like-to-view ratio
filtered_df['like_ratio'] = filtered_df['likes'] / filtered_df['views']
best_ratio = filtered_df.sort_values('like_ratio', ascending=False).iloc[0]
st.markdown(f"📈 **Video dengan rasio like tertinggi:** {best_ratio['video_title']} ({best_ratio['like_ratio']:.2%})")

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

# === Visualisasi 4: Like Ratio ===
filtered_df['like_ratio'] = filtered_df['likes'] / filtered_df['views']
fig4 = px.histogram(filtered_df, x='like_ratio', nbins=20,
                    title='👍 Distribusi Like-to-View Ratio')
st.plotly_chart(fig4, use_container_width=True)

# === Visualisasi 5: Tren Views ===
df_time = filtered_df.copy()
df_time['upload_date'] = pd.to_datetime(df_time['upload_date'])
df_time = df_time.groupby('upload_date')['views'].sum().reset_index()
fig5 = px.line(df_time, x='upload_date', y='views',
               title="📅 Tren Views per Tanggal Upload")
st.plotly_chart(fig5, use_container_width=True)

# Statistik ringkas
st.metric("📈 Total Views", f"{df['views'].sum():,}")
st.metric("👍 Total Likes", f"{df['likes'].sum():,}")
st.metric("📊 Rata-rata Views", f"{df['views'].mean():,.2f}")
st.metric("❤️ Rata-rata Likes", f"{df['likes'].mean():,.2f}")

# Info tambahan st.subheader("📌 Insight Singkat")
top_video = filtered_df.loc[filtered_df['views'].idxmax()]
st.markdown(f"**Video paling populer:** `{top_video['video_title']}` dengan **{top_video['views']} views**")

#kredits
st.markdown("---")
st.caption("📌 Dibuat oleh Septian Dharma – powered by Streamlit & Plotly")