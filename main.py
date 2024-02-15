import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df

st.title('Dashboard Analisis E-commerce')

# Membaca data dari file CSV
data_customer = load_data("https://raw.githubusercontent.com/fiendess/analisis-ecommerce-UAS/main/customers_dataset.csv")
data_order =load_data("https://raw.githubusercontent.com/fiendess/analisis-ecommerce-UAS/main/orders_dataset.csv")
data_produk = load_data('https://raw.githubusercontent.com/fiendess/analisis-ecommerce-UAS/main/products_dataset.csv')
data_order_item = load_data('https://raw.githubusercontent.com/fiendess/analisis-ecommerce-UAS/main/order_items_dataset.csv')
data_order_payment = load_data('https://raw.githubusercontent.com/fiendess/analisis-ecommerce-UAS/main/order_payments_dataset.csv')
data_geolocation = load_data('https://raw.githubusercontent.com/fiendess/analisis-ecommerce-UAS/main/geolocation_dataset.csv')
data_order_reviews = load_data('https://raw.githubusercontent.com/fiendess/analisis-ecommerce-UAS/main/order_reviews_dataset.csv')
data_sellers = load_data('https://raw.githubusercontent.com/fiendess/analisis-ecommerce-UAS/main/sellers_dataset.csv')


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

# Merge dataset order_merged_with_items dengan dataset data_produk berdasarkan product_id
merged_data = pd.merge(pd.merge(order_merged_with_items, data_produk, on='product_id'), data_customer, on='customer_id')
# Konversi kolom 'order_purchase_timestamp' jadi tipe data datetime
merged_data['order_purchase_timestamp'] = pd.to_datetime(merged_data['order_purchase_timestamp'])

# Filter data untuk produk dengan kategori Computet Accessories dan kota Rio de Janeiro
filtered_columns = ['order_id','product_category_name', 'order_purchase_timestamp', 'customer_city','order_status']
filtered_data = merged_data[(merged_data['product_category_name'] == 'informatica_acessorios') & 
                            (merged_data['customer_city'] == 'rio de janeiro') & 
                            ((merged_data['order_purchase_timestamp'].dt.year == 2016) |
                             (merged_data['order_purchase_timestamp'].dt.year == 2017) |
                             (merged_data['order_purchase_timestamp'].dt.year == 2018))]


# Hitung jumlah pelanggan yang membeli produk dengan kategori Computer Accessories
jumlah_pelanggan_CA = filtered_data['customer_id'].nunique()

# Hitung banyaknya order yang delivered, shipped, cancelled
order_delivered = filtered_data[filtered_data['order_status'] == 'delivered'].shape[0]
order_cancelled = filtered_data[filtered_data['order_status'] == 'canceled'].shape[0]
order_shipped = filtered_data[filtered_data['order_status'] == 'shipped'].shape[0]

# Filter data untuk kota Rio de Janeiro
RJ_data = merged_data[merged_data['customer_city'] == 'rio de janeiro']

# Hitung jumlah total pelanggan dari kota Rio de Janeiro yang belanja seluruh kategori
total_pelanggan_RJ = RJ_data['customer_id'].nunique()

# Hitung proporsi jumlah pelanggan terhadap pembelian produk
proporsi = jumlah_pelanggan_CA / total_pelanggan_RJ * 100

############################################################################################
df_order = pd.DataFrame(data_order)

jumlah_delivered = df_order['order_status'].value_counts().get('delivered', 0)
jumlah_shipped = df_order['order_status'].value_counts().get('shipped', 0)
jumlah_canceled= df_order['order_status'].value_counts().get('canceled', 0)

# Mengonversi kolom timestamp ke format datetime Pandas
for col in df_order.columns[3:]:
    df_order[col] = pd.to_datetime(df_order[col])

# Mengubah timestamp menjadi hanya tahun
for col in df_order.columns[3:]:
    df_order[col] = df_order[col].dt.year

# Menghitung jumlah order yang dibatalkan
cancelled_orders_2016 = df_order[(df_order['order_status'] == 'canceled') & (df_order['order_purchase_timestamp'] == 2016)]
jumlah_cancelled_orders_2016 = len(cancelled_orders_2016)

cancelled_orders_2017 = df_order[(df_order['order_status'] == 'canceled') & (df_order['order_purchase_timestamp'] == 2017)]
jumlah_cancelled_orders_2017 = len(cancelled_orders_2017)

cancelled_orders_2018 = df_order[(df_order['order_status'] == 'canceled') & (df_order['order_purchase_timestamp'] == 2018)]
jumlah_cancelled_orders_2018 = len(cancelled_orders_2018)


#Tabs
tab1, tab2, tab3 = st.tabs(["Overview", "Penjualan", "Pelanggan"])


with tab1:
    st.header("Dashboard Overview")
    st.write("Ringkasan tentang kinerja E-Commerce secara keseluruhan.")

    year = st.sidebar.selectbox(
        label='Pilih Tahun',
        options=total_revenue_per_year.index
    )
    st.write(f"Total Pendapatan Tahun {year}: {total_revenue_per_year[year]}")
    st.write(f"Jumlah Pelanggan Tahun {year}: {unique_customers_per_year[year]}")
    st.write(f"Jumlah Produk Terjual Tahun {year}: {total_products_sold_per_year[year]}")

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


    # kategori pada produk yang paling banyak dibeli
    fig = px.bar(merged_data['product_category_name'].value_counts(), x=merged_data['product_category_name'].value_counts().values, y=merged_data['product_category_name'].value_counts().index, orientation='h', title='Jumlah Produk Terjual per Kategori')
    fig.update_layout(xaxis_title='Jumlah Produk Terjual', yaxis_title='Kategori Produk')
    st.plotly_chart(fig)

    # menampilkan kategori produk yang paling banyak dibeli
    kategori_terbanyak = merged_data['product_category_name'].value_counts().idxmax()
    st.write(f"Kategori Produk yang Paling Banyak Dibeli: {kategori_terbanyak}")

    order_status_counts = filtered_data['order_status'].value_counts()

    # Buat histogram menggunakan Plotly
    fig = go.Figure(data=[go.Bar(x=order_status_counts.index, y=order_status_counts.values)])

    # Atur layout
    fig.update_layout(title='Status Order untuk Produk Komputer Aksesoris dari Rio de Janeiro (2016-2018)',
                    xaxis_title='Status Order',
                    yaxis_title='Jumlah Order')

    # Tampilkan histogram
    st.plotly_chart(fig)

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
    selected_year = st.sidebar.selectbox(
        label='Pilih Tahun',
        options=[2016, 2017, 2018],
        key='select_year'  
    )

    # Filter data berdasarkan tahun yang dipilih
    filtered_data_selected_year = filtered_data[filtered_data['order_purchase_timestamp'].dt.year == selected_year]

    st.write(f"Visualisasi terkait penjualan untuk tahun {selected_year} berdasarkan waktu, produk, dan segmentasi pelanggan.")

    # Membuat histogram dengan plotly
    fig = px.histogram(filtered_data_selected_year, x='order_purchase_timestamp', nbins=20, title=f'Distribusi Waktu Pembelian untuk Produk Komputer Aksesoris dari Rio de Janeiro pada Tahun {selected_year}')
    fig.update_layout(xaxis_title='Waktu Pembelian', yaxis_title='Jumlah Pembelian')
    fig.update_xaxes(tickangle=45)

    # Menampilkan plot menggunakan st.plotly_chart()
    st.plotly_chart(fig)

with tab3:
    st.header("Segmentasi Pelanggan")
    st.write("Visualisasi terkait segmentasi pelanggan berdasarkan atribut seperti frekuensi pembelian, nilai transaksi, atau geografi.")

    labels = ['Pelanggan yang membeli produk Comp~uter Accessories', 'Pelanggan yg membeli kategori Lainnya']
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

with tab2:

    st.header("Status pesanan keseluruhan")

    fig = go.Figure()
    fig.add_trace(go.Bar(x=['Terkirim'],
                        y=[jumlah_delivered],
                        marker_color='green', name='Total: '+ str(jumlah_delivered)))
    fig.add_trace(go.Bar(x=['Dikirim'],
                        y=[jumlah_shipped],
                        marker_color='blue', name='Total: '+ str(jumlah_shipped)))
    fig.add_trace(go.Bar(x=['Dibatalkan'],
                        y=[jumlah_canceled],
                        marker_color='red', name='Total: '+ str(jumlah_canceled)))

    fig.update_layout(title='Jumlah Pesanan',
                    xaxis_title='Status Pesanan',
                    yaxis_title='Jumlah')

    st.plotly_chart(fig)
    st.write(f"Pesanan yang dikirim: {jumlah_shipped}")
    st.write(f"Pesanan yang terkirim: {jumlah_delivered}")
    st.write(f"Pesanan yang dibatalkan: {jumlah_canceled}")


with tab2:

    st.header("Status pesanan yang di batalkan pada tahun 2016, 2017, dan 2018")

    fig = go.Figure()
    fig.add_trace(go.Bar(x=['Tahun 2016'],
                        y=[jumlah_cancelled_orders_2016],
                        marker_color='grey', name='Tahun 2016: '+ str(jumlah_cancelled_orders_2016)))
    fig.add_trace(go.Bar(x=['Tahun 2017'],
                        y=[jumlah_cancelled_orders_2017],
                        marker_color='grey', name='Tahun 2017: '+ str(jumlah_cancelled_orders_2017)))
    fig.add_trace(go.Bar(x=['Tahun 2018'],
                        y=[jumlah_cancelled_orders_2018],
                        marker_color='grey', name='Tahun 2018: '+ str(jumlah_cancelled_orders_2018)))

    fig.update_layout(title='Jumlah Pesanan',
                    xaxis_title='Status Pesanan',
                    yaxis_title='Jumlah')

    st.plotly_chart(fig)
    st.write(f"Pesanan yang di batalkan pada tahun 2016: {jumlah_cancelled_orders_2016}")
    st.write(f"Pesanan yang di batalkan pada tahun 2017: {jumlah_cancelled_orders_2017}")
    st.write(f"Pesanan yang di batalkan pada tahun 2018: {jumlah_cancelled_orders_2018}")
 
    st.write('<hr>', unsafe_allow_html=True)
    
    # Visualisasi sederhana tren penjualan dari waktu ke waktu
    st.subheader("Analisis Tren Penjualan")
    fig_trend = px.line(total_revenue_per_year, title='Tren Total Pendapatan dari Waktu ke Waktu')
    fig_trend.update_layout(xaxis_title='Tahun', yaxis_title='Total Pendapatan')
    
    # Menambahkan label langsung di atas titik data pada sumbu y
    for year, revenue in total_revenue_per_year.items():
        fig_trend.add_annotation(x=year, y=revenue, text=f'{revenue}', showarrow=True, arrowhead=1)
    
    st.plotly_chart(fig_trend) 