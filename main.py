import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

st.title('Dashboard Analisis E-commerce')

# Membaca data dari file CSV
data_customer = pd.read_csv('customers_dataset.csv')
data_order = pd.read_csv('orders_dataset.csv')
data_produk = pd.read_csv('products_dataset.csv')
data_order_item = pd.read_csv('order_items_dataset.csv')
data_order_payment = pd.read_csv('order_payments_dataset.csv')
data_geolocation = pd.read_csv('geolocation_dataset.csv')
data_order_reviews = pd.read_csv('order_reviews_dataset.csv')
data_sellers = pd.read_csv('sellers_dataset.csv')


# Cleaning data


#Pre processing data

# Merge dataset data_order dengan dataset order_items_data berdasarkan order_id
order_merged_with_items = pd.merge(data_order, data_order_item, on='order_id')

# Konversi kolom 'order_purchase_timestamp' ke tipe data datetime
order_merged_with_items['order_purchase_timestamp'] = pd.to_datetime(order_merged_with_items['order_purchase_timestamp'])

# Ekstraksi tahun dari kolom 'order_purchase_timestamp'
order_merged_with_items['year'] = order_merged_with_items['order_purchase_timestamp'].dt.year

# Hitung total pendapatan per tahun
total_revenue_per_year = order_merged_with_items.groupby('year')['price'].sum()

# Hitung jumlah pelanggan unik per tahun
unique_customers_per_year = order_merged_with_items.groupby('year')['customer_id'].nunique()

# Hitung jumlah produk terjual per tahun
total_products_sold_per_year = order_merged_with_items.groupby('year').size()

merged_data = pd.merge(pd.merge(order_merged_with_items, data_produk, on='product_id'), data_customer, on='customer_id')
# Konversi kolom 'order_purchase_timestamp' jadi tipe data datetime
merged_data['order_purchase_timestamp'] = pd.to_datetime(merged_data['order_purchase_timestamp'])
# Filter data untuk produk dengan kategori Computet Accessories dan kota Rio de Janeiro pada tahun 2018
filtered_columns = ['order_id','product_category_name', 'order_purchase_timestamp', 'customer_city','order_status']
filtered_data = merged_data[(merged_data['product_category_name'] == 'informatica_acessorios') & 
                            (merged_data['customer_city'] == 'rio de janeiro') & 
                            (merged_data['order_purchase_timestamp'].dt.year == 2018)]

# Hitung jumlah pelanggan yang membeli produk dengan kategori Computer Accessories
jumlah_pelanggan_CA = filtered_data['customer_id'].nunique()

# Hitung banyaknya order yang delivered, shipped, cancelled
order_delivered = filtered_data[filtered_data['order_status'] == 'delivered']
order_cancelled = filtered_data[filtered_data['order_status'] == 'canceled']
order_shipped = filtered_data[filtered_data['order_status'] == 'shipped']

# Filter data untuk kota Rio de Janeiro
RJ_data = merged_data[merged_data['customer_city'] == 'rio de janeiro']

# Hitung jumlah total pelanggan dari kota Rio de Janeiro yang belanja seluruh kategori
total_pelanggan_RJ = RJ_data['customer_id'].nunique()

# Hitung proporsi jumlah pelanggan terhadap pembelian produk
proporsi = jumlah_pelanggan_CA / total_pelanggan_RJ * 100


#Tabs
tab1, tab2, tab3 = st.tabs(["Overview", "Penjualan", "Pelanggan"])


with tab1:
    st.header("Dashboard Overview")
    st.write("Ringkasan tentang kinerja E-Commerce secara keseluruhan.")

    fig = go.Figure()
    fig.add_trace(go.Bar(x=total_revenue_per_year.index, y=total_revenue_per_year.values, name='Total Pendapatan'))
    fig.add_trace(go.Bar(x=unique_customers_per_year.index, y=unique_customers_per_year.values, name='Jumlah Pelanggan'))
    fig.add_trace(go.Bar(x=total_products_sold_per_year.index, y=total_products_sold_per_year.values, name='Jumlah Produk Terjual'))
    # Layout grafik
    fig.update_layout(barmode='group', title='Ringkasan Kinerja Bisnis', xaxis_title='Tahun', yaxis_title='Jumlah')

    # Tampilkan grafik 
    st.plotly_chart(fig)

    # Tampilkan hasil
    for year in total_revenue_per_year.index:
        st.write(f"Total Pendapatan Tahun {year}: {total_revenue_per_year[year]}")
        st.write(f"Jumlah Pelanggan Tahun {year}: {unique_customers_per_year[year]}")
        st.write(f"Jumlah Produk Terjual Tahun {year}: {total_products_sold_per_year[year]}")


    # kategori pada produk yang paling banyak dibeli dengan menggunakan bar chart
    fig = px.bar(merged_data['product_category_name'].value_counts(), x=merged_data['product_category_name'].value_counts().values, y=merged_data['product_category_name'].value_counts().index, orientation='h', title='Jumlah Produk Terjual per Kategori')
    fig.update_layout(xaxis_title='Jumlah Produk Terjual', yaxis_title='Kategori Produk')
    st.plotly_chart(fig)

    # menampilkan kategori produk yang paling banyak dibeli
    kategori_terbanyak = merged_data['product_category_name'].value_counts().idxmax()
    st.write(f"Kategori Produk yang Paling Banyak Dibeli: {kategori_terbanyak}")

    st.write('<hr>', unsafe_allow_html=True)
    
    # Analisis Perubahan Persentase Pendapatan dari Tahun Sebelumnya
    st.subheader("Perubahan Persentase Pendapatan dari Tahun Sebelumnya")
    revenue_change = total_revenue_per_year.pct_change() * 100
    fig_revenue_change = px.bar(x=revenue_change.index, y=revenue_change.values, 
                                title='Perubahan Persentase Pendapatan dari Tahun Sebelumnya')
    fig_revenue_change.update_layout(xaxis_title='Tahun', yaxis_title='Perubahan Persentase Pendapatan (%)')
    st.plotly_chart(fig_revenue_change)
    

with tab2:
    st.header("Penjualan")
    st.write("Visualisasi terkait penjualan berdasarkan waktu, produk, dan segmentasi pelanggan.")
    # Membuat histogram dengan plotly
    fig = px.histogram(filtered_data, x='order_purchase_timestamp', nbins=20, title='Distribusi Waktu Pembelian untuk Produk Komputer Aksesoris dari Rio de Janeiro pada Tahun 2018')
    fig.update_layout(xaxis_title='Waktu Pembelian', yaxis_title='Jumlah Pembelian')
    fig.update_xaxes(tickangle=45)

    # Menampilkan plot menggunakan st.plotly_chart()
    st.plotly_chart(fig)
    
    st.write('<hr>', unsafe_allow_html=True)
    
    # Visualisasi sederhana tren penjualan dari waktu ke waktu
    st.subheader("Analisis Tren Penjualan")
    fig_trend = px.line(total_revenue_per_year, title='Tren Total Pendapatan dari Waktu ke Waktu')
    fig_trend.update_layout(xaxis_title='Tahun', yaxis_title='Total Pendapatan')
    
    # Menambahkan label langsung di atas titik data pada sumbu y
    for year, revenue in total_revenue_per_year.items():
        fig_trend.add_annotation(x=year, y=revenue, text=f'{revenue}', showarrow=True, arrowhead=1)
    
    st.plotly_chart(fig_trend)

with tab3:
    st.header("Segmentasi Pelanggan")
    st.write("Visualisasi terkait segmentasi pelanggan berdasarkan atribut seperti frekuensi pembelian, nilai transaksi, atau geografi.")

    labels = ['Pelanggan yang membeli produk Computer Accessories', 'Pelanggan yg membeli kategori Lainnya']
    sizes = [proporsi, 100 - proporsi]  
    colors = ['lightcoral', 'lightblue']

    # Membuat objek figure
    fig = go.Figure(data=[go.Pie(labels=labels, 
                                values=sizes, 
                                textinfo='label+percent', 
                                marker=dict(colors=colors))])

    # Layout
    fig.update_layout(title='Proporsi Pelanggan Computer Accessories dari Total Pelanggan di Kota Rio de Janeiro')

    # Menampilkan pie chart
    st.plotly_chart(fig)
    
    st.write('<hr>', unsafe_allow_html=True)
    
    # Analisis Rata-rata Pendapatan per Pelanggan
    st.subheader("Rata-rata Pendapatan per Pelanggan")
    avg_revenue_per_customer = total_revenue_per_year / unique_customers_per_year
    fig_avg_revenue_per_customer = px.bar(x=avg_revenue_per_customer.index, y=avg_revenue_per_customer.values, 
                                           title='Rata-rata Pendapatan per Pelanggan dari Waktu ke Waktu')
    fig_avg_revenue_per_customer.update_layout(xaxis_title='Tahun', yaxis_title='Rata-rata Pendapatan per Pelanggan')
    st.plotly_chart(fig_avg_revenue_per_customer)


with st.sidebar:
 st.sidebar.markdown("Dashboard")

 # selectbox untuk memilih tahun penjualan yang ingin ditampilkan
year = st.sidebar.selectbox(
        label='Pilih Tahun',
        options=total_revenue_per_year.index
    )
st.write(f"Total Pendapatan Tahun {year}: {total_revenue_per_year[year]}")
st.write(f"Jumlah Pelanggan Tahun {year}: {unique_customers_per_year[year]}")
st.write(f"Jumlah Produk Terjual Tahun {year}: {total_products_sold_per_year[year]}")

    # slider untuk memilih range nilai 
 

#  values = st.slider(
#  label='Select a range of values',
#  min_value=0, max_value=100, value=(0, 100)
# )
#  st.write('Values:', values)

 