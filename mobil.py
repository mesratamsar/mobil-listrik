import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Dashboard Analisis Mobil Listrik", page_icon="\ud83d\ude97", layout="wide")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_excel("mobil_listrik_mobil123_multi_brand_fiks_new.xlsx", sheet_name="Sheet1")
    # Normalisasi kondisi
    df['Kondisi'] = df['Kondisi'].apply(lambda x: 'Baru' if 'new' in x.lower() or 'baru' in x.lower() else 'Bekas')
    df['Brand_Model'] = df['Brand'].astype(str).str.strip() + " " + df['Model'].astype(str).str.strip()
    return df

df = load_data()

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("Filter Data")

brands = df['Brand'].unique()
selected_brand = st.sidebar.multiselect("Pilih Brand", options=brands, default=brands)

kondisi_list = df['Kondisi'].unique()
selected_kondisi = st.sidebar.multiselect("Pilih Kondisi", options=kondisi_list, default=kondisi_list)

year_min, year_max = int(df['Tahun'].min()), int(df['Tahun'].max())
selected_year = st.sidebar.slider("Pilih Tahun", year_min, year_max, (year_min, year_max))

# Filter Data
filtered_df = df[(df['Brand'].isin(selected_brand)) &
                 (df['Kondisi'].isin(selected_kondisi)) &
                 (df['Tahun'] >= selected_year[0]) &
                 (df['Tahun'] <= selected_year[1])]

# =========================
# DASHBOARD LAYOUT
# =========================
st.title("\ud83d\ude97 Dashboard Analisis Mobil Listrik Indonesia")
st.markdown("### Data dari Mobil123")

# ---- METRICS ----
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Listing", len(filtered_df))
col2.metric("Jumlah Brand", filtered_df['Brand'].nunique())
col3.metric("Jumlah Model", filtered_df['Model'].nunique())
col4.metric("Jumlah Dealer", filtered_df['Dealer'].nunique())

# =========================
# VISUALISASI HARGA PER BRAND
# =========================
st.subheader("Median Harga per Brand")
agg_brand = (filtered_df.groupby('Brand')['Harga (IDR)']
             .median()
             .sort_values(ascending=False))

fig1, ax1 = plt.subplots()
ax1.barh(agg_brand.index, agg_brand.values)
ax1.set_xlabel('Median Harga (IDR)')
ax1.set_ylabel('Brand')
ax1.invert_yaxis()
st.pyplot(fig1)

# =========================
# TOP DEALER
# =========================
st.subheader("Top 20 Dealer dengan Listing Terbanyak")
top_dealer = (filtered_df.groupby('Dealer')
                .size()
                .sort_values(ascending=False)
                .head(20))

fig2, ax2 = plt.subplots()
ax2.bar(top_dealer.index, top_dealer.values)
ax2.set_xticklabels(top_dealer.index, rotation=90)
ax2.set_ylabel('Jumlah Listing')
ax2.set_xlabel('Dealer')
st.pyplot(fig2)

# =========================
# DISTRIBUSI TAHUN PRODUKSI
# =========================
st.subheader("Distribusi Tahun Produksi")

dist_year = filtered_df['Tahun'].value_counts().sort_index()
fig3, ax3 = plt.subplots()
ax3.bar(dist_year.index.astype(str), dist_year.values)
ax3.set_xlabel('Tahun')
ax3.set_ylabel('Jumlah Listing')
st.pyplot(fig3)

# =========================
# BOX PLOT HARGA BARU VS BEKAS
# =========================
st.subheader("Sebaran Harga Baru vs Bekas")

data_box = [filtered_df[filtered_df['Kondisi']=="Baru"]['Harga (IDR)'],
            filtered_df[filtered_df['Kondisi']=="Bekas"]['Harga (IDR)']]
fig4, ax4 = plt.subplots()
ax4.boxplot(data_box, labels=["Baru", "Bekas"], showfliers=False)
ax4.set_ylabel('Harga (IDR)')
st.pyplot(fig4)

# =========================
# TABEL DETAIL DATA
# =========================
st.subheader("Data Listing")
st.dataframe(filtered_df)

