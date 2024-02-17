import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from streamlit_option_menu import option_menu
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

 # Filter data berdasarkan kota yang dipilih oleh user pada sidebar
selected_city = st.sidebar.selectbox(
label='Pilih Kota',
options=merged_data['customer_city'].unique(),
key='select_city'
)

 # Filter data berdasarkan kategori informatica_acessorios dan kota yang dipilih
filtered_data_city = merged_data[(merged_data['product_category_name'] == 'informatica_acessorios') & 
                                                            (merged_data['customer_city'] == selected_city) &
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


# Hitung jumlah pelanggan yang membeli produk dengan kategori informatica_acessorios dan kota yang dipilih
jumlah_pelanggan_city = filtered_data_city['customer_id'].nunique()

# Hitung proporsi jumlah pelanggan terhadap total pelanggan dari kota yang dipilih
proporsi_city = jumlah_pelanggan_city / total_pelanggan_RJ * 100



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

#Overview
with tab1:
    st.header("Dashboard Overview")
    st.write("Ringkasan tentang kinerja E-Commerce secara keseluruhan.")
    st.caption("**10122286 - Didan Rahmana**")
    year = st.sidebar.selectbox(
        label='Pilih Tahun',
        options=total_revenue_per_year.index
        
    )

    # Plot total pendapatan per tahun
    fig_revenue = go.Figure(data=go.Bar(x=total_revenue_per_year.index, y=total_revenue_per_year.values))
    fig_revenue.update_layout(title='Total Pendapatan per Tahun', xaxis_title='Tahun', yaxis_title='Total Pendapatan')

    # Menampilkan grafik
    st.plotly_chart(fig_revenue)

    # Menambahkan subheader
    st.subheader("Informasi Analisis")
    st.write(f"Total Pendapatan Tahun {year}: {total_revenue_per_year[year]}")
    # Membuat ekspander untuk penjelasan analisis
    with st.expander("Penjelasan Analisis Informasi"):
        st.write("Dari informasi visualisasi di atas, dapat dilihat bahwa total pendapatan meningkat dari tahun ke tahun. Ini menunjukkan bahwa bisnis berkembang dan menghasilkan lebih banyak pendapatan dari waktu ke waktu. Ini dapat digunakan untuk mempertimbangkan strategi untuk mempertahankan pertumbuhan ini, atau bahkan meningkatkannya lebih lanjut.")


    # Plot jumlah pelanggan unik per tahun
    fig_customers = go.Figure(data=go.Bar(x=unique_customers_per_year.index, y=unique_customers_per_year.values))
    fig_customers.update_layout(title='Jumlah Pelanggan Unik per Tahun', xaxis_title='Tahun', yaxis_title='Jumlah Pelanggan')

    # Plot jumlah produk terjual per tahun
    fig_products = go.Figure(data=go.Bar(x=total_products_sold_per_year.index, y=total_products_sold_per_year.values))
    fig_products.update_layout(title='Jumlah Produk Terjual per Tahun', xaxis_title='Tahun', yaxis_title='Jumlah Produk Terjual')
 
    st.plotly_chart(fig_customers)
    st.write(f"Jumlah Pelanggan Tahun {year}: {unique_customers_per_year[year]}")
    with st.expander("Penjelasan Analisis Infomasi"):
        
        st.write("Dari informasi visualisasi di atas, dapat dilihat bahwa jumlah pelanggan unik juga meningkat dari tahun ke tahun. Ini menunjukkan bahwa bisnis menarik lebih banyak pelanggan dari waktu ke waktu. ")
    st.plotly_chart(fig_products)

   
  
    st.write(f"Jumlah Produk Terjual Tahun {year}: {total_products_sold_per_year[year]}")
    with st.expander("Penjelasan Analisis Infomasi"):
        st.write("Dari informasi visualisasi di atas, dapat dilihat bahwa jumlah produk yang terjual juga meningkat dari tahun ke tahun. Ini menunjukkan bahwa bisnis berhasil menjual lebih banyak produk dari waktu ke waktu. Ini dapat digunakan untuk mempertimbangkan strategi untuk mempertahankan pertumbuhan ini, atau bahkan meningkatkannya lebih lanjut.")


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

   # Gabungkan dataset
    merged_data = pd.merge(pd.merge(data_order, data_order_item, on='order_id'), data_customer, on='customer_id')

    # Ekstraksi fitur yang relevan
    features = merged_data[['price', 'order_item_id']]

    # Hitung total pembayaran
    merged_data['total_payment'] = merged_data['price'] * merged_data['order_item_id']


    # Inisialisasi model klastering
    kmeans = KMeans(n_clusters=3, random_state=42)

    # Latih model
    kmeans.fit(features)

    # Prediksi klaster untuk setiap pelanggan
    merged_data['cluster'] = kmeans.predict(features)

    # Visualisasi hasil klastering menggunakan Plotly
    fig = px.scatter(merged_data, x='total_payment', y='order_item_id', color='cluster',
                    title='Klastering Pelanggan Berdasarkan Perilaku Pembelian')

    st.plotly_chart(fig)

    # Menampilkan hasil klastering
    with st.expander("Hasil Klastering Pelanggan"):
        st.write("Hasil klastering menunjukkan bahwa pelanggan dapat dikelompokkan menjadi 3 kelompok berdasarkan perilaku pembelian mereka. Kelompok 0 menunjukkan pelanggan dengan pembelian yang sedikit dan total pembayaran yang rendah, kelompok 1 menunjukkan pelanggan dengan pembelian yang sedang dan total pembayaran yang sedang, dan kelompok 2 menunjukkan pelanggan dengan pembelian yang banyak dan total pembayaran yang tinggi.")


#Penjualan
with tab2:
    st.header("Penjualan")

    st.caption("**10122286 - Didan Rahmana**")
    st.write("Visualisasi terkait penjualan berdasarkan waktu, produk, dan segmentasi pelanggan.")
    selected_year = st.sidebar.selectbox(
        label='Pilih Tahun Penjualan',
        options=[2016, 2017, 2018],
        key='select_year'  
    )

    # Filter data berdasarkan tahun yang dipilih
    filtered_data_selected_year = filtered_data[filtered_data['order_purchase_timestamp'].dt.year == selected_year]

    # Membuat histogram dengan plotly
    fig = px.histogram(filtered_data_selected_year, x='order_purchase_timestamp', nbins=20, title=f'Distribusi Waktu Pembelian untuk Produk Komputer Aksesoris dari Rio de Janeiro pada Tahun {selected_year}')
    fig.update_layout(xaxis_title='Waktu Pembelian', yaxis_title='Jumlah Pembelian')
    fig.update_xaxes(tickangle=45)

    # Menampilkan plot menggunakan st.plotly_chart()
    st.plotly_chart(fig)

    st.caption("**10122480 - Paska Damarkus Sinaga**")
    st.subheader("Informasi Analisis")
    st.markdown("**Analisis Terhadap 10 Kota Dengan Seller & Customer Paling Banyak**")
    with st.expander("Tujuan Analisis Infomasi Tersebut"):
            st.write("Dengan mengetahui kota mana yang memiliki jumlah pelanggan dan penjual terbanyak, Anda dapat mengalokasikan sumber daya dan upaya pemasaran Anda dengan lebih efisien. Misalnya, jika suatu kota memiliki jumlah penjual yang tinggi tetapi pelanggan yang rendah, Anda mungkin ingin meningkatkan upaya pemasaran Anda di kota tersebut.")
            st.write("Analisis ini dapat membantu Anda memahami dinamika pasar Anda dengan lebih baik. Anda dapat mengetahui di mana penjual dan pelanggan Anda berada, dan bagaimana mereka berinteraksi satu sama lain.")

    # Mencari jumlah seller di berbagai kota
    city = data_sellers['seller_city'].value_counts()
    
    # Mancari Jumlah Seller paling banyak
    city_head = city.head(10)

    # Mencari 10 kota dengan penjual paling sedikit
    city_tail = city.tail(10)

        # Warna untuk diagram kotak
    colors = plt.cm.Paired(np.arange(len(city_head)))

        
    st.markdown("---")
    st.subheader("Diagram Lingkaran Jumlah Seller di Kota-Kota Teratas")

        # Ambil data untuk diagram lingkaran
    top_seller_cities = city_head.index
    top_seller_counts = city_head.values

        # Buat diagram lingkaran
    fig = go.Figure(data=[go.Pie(labels=top_seller_cities, values=top_seller_counts, textinfo='percent', 
                             marker_colors=colors, hole=.3)])
    fig.update_layout(title='Persentase Jumlah Seller di Kota-Kota Teratas')

    # Tampilkan diagram lingkaran
    st.plotly_chart(fig)

    st.markdown("---")
    st.subheader("Analisis Tambahan")

    st.write("Dari analisis yang dilakukan, kita dapat melihat bahwa Sao Paulo menjadi kota dengan jumlah penjual dan pelanggan terbanyak. Hal ini menunjukkan bahwa Sao Paulo memiliki potensi pasar yang besar dan aktif dalam industri e-commerce. Strategi pemasaran yang difokuskan di kota ini dapat memberikan hasil yang signifikan.")
    st.write("Selain itu, terdapat korelasi positif antara jumlah penjual dan pelanggan di tiap kota, yang menunjukkan bahwa semakin banyak penjual, kemungkinan besar akan ada juga lebih banyak pelanggan. Oleh karena itu, mengembangkan jaringan penjual dapat menjadi strategi yang efektif untuk meningkatkan pangsa pasar.")
    st.write("Untuk mengoptimalkan strategi pemasaran, perlu dilakukan analisis lebih lanjut mengenai preferensi pelanggan dan kebutuhan pasar di tiap kota. Dengan pemahaman yang lebih mendalam tentang karakteristik pasar lokal, Anda dapat mengarahkan upaya pemasaran Anda dengan lebih tepat dan efisien.")


    

#Pelanggan
with tab3:
    st.header("Pelanggan")
    st.caption("**10122286 - Didan Rahmana**")

    labels = ['Pelanggan yang membeli produk Computer Accessories', 'Pelanggan yg membeli kategori Lainnya']
    sizes = [proporsi_city, 100 - proporsi_city]  
    colors = ['lightcoral', 'lightblue']

    # Membuat objek figure
    fig = go.Figure(data=[go.Pie(labels=labels, 
                                values=sizes, 
                                textinfo='label+percent', 
                                marker=dict(colors=colors))])
    # Layout
    fig.update_layout(title='Proporsi Pelanggan Computer Accessories dari Total Pelanggan di Kota {}'.format(selected_city), title_x=0.5, title_y=0.9, title_xanchor='center', title_font=dict(size=20))

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

    
     # Tampilkan hasil
    st.write(f"Jumlah Pelanggan yang Membeli Produk informatica_acessorios di Kota {selected_city}: {jumlah_pelanggan_city}")
    st.write(f"Proporsi Jumlah Pelanggan terhadap Total Pelanggan dari Kota {selected_city}: {proporsi_city}%")              

    #dwi
    st.write('<hr>', unsafe_allow_html=True)

    # Analisis Perubahan Persentase Pendapatan dari Tahun Sebelumnya
    st.subheader("Perubahan Persentase Pendapatan dari Tahun Sebelumnya")
    st.caption("**10122282 - Dwi Andriani Azi**")
    revenue_change = total_revenue_per_year.pct_change() * 100
    fig_revenue_change = px.bar(x=revenue_change.index, y=revenue_change.values, 
                                title='Perubahan Persentase Pendapatan dari Tahun Sebelumnya')
    fig_revenue_change.update_layout(xaxis_title='Tahun', yaxis_title='Perubahan Persentase Pendapatan (%)')
    st.plotly_chart(fig_revenue_change)


    st.write('<hr>', unsafe_allow_html=True)

    # Visualisasi sederhana tren penjualan dari waktu ke waktu
    st.subheader("Analisis Tren Penjualan")
    fig_trend = px.line(total_revenue_per_year, title='Tren Total Pendapatan dari Waktu ke Waktu')
    fig_trend.update_layout(xaxis_title='Tahun', yaxis_title='Total Pendapatan')

    # Menambahkan label langsung di atas titik data pada sumbu y
    for year, revenue in total_revenue_per_year.items():
        fig_trend.add_annotation(x=year, y=revenue, text=f'{revenue}', showarrow=True, arrowhead=1)

    st.plotly_chart(fig_trend)

    st.write('<hr>', unsafe_allow_html=True)

    # Analisis Rata-rata Pendapatan per Pelanggan
    st.subheader("Rata-rata Pendapatan per Pelanggan")
    avg_revenue_per_customer = total_revenue_per_year / unique_customers_per_year
    fig_avg_revenue_per_customer = px.bar(x=avg_revenue_per_customer.index, y=avg_revenue_per_customer.values, 
                                           title='Rata-rata Pendapatan per Pelanggan dari Waktu ke Waktu')
    fig_avg_revenue_per_customer.update_layout(xaxis_title='Tahun', yaxis_title='Rata-rata Pendapatan per Pelanggan')
    st.plotly_chart(fig_avg_revenue_per_customer)

    #farras
    
    def analisis_farras(data_customer,data_sellers):

        # Mencari jumlah customer di berbagai kota
        customer_city = data_customer['customer_city'].value_counts()

        # Mengurutkan dan mencari 5 kota teratas dengan customer terbanyak
        customer_city_head = customer_city.head(5)

        # mencari 5 kota dengan jumlah seller paling sedikit
        customer_city_tail = customer_city.tail(5)

        # Mencari jumlah seller di berbagai kota
        seller_city = data_sellers['seller_city'].value_counts()

        # Mancari Jumlah Seller paling banyak
        seller_city_head = seller_city.head(5)

        # Mencari 5 kota dengan penjual paling sedikit
        seller_city_tail = seller_city.tail(5)
        
        #==========================================================================
        
        st.caption("**10122299 - Farras Abiyyu D**")
        st.subheader("Informasi Analisis")
        st.markdown("**Analisis Terhadap 5 Kota Dengan Seller & Customer Paling Banyak**")
        with st.expander("Tujuan Analisis Infomasi Tersebut"):
            st.write("Dengan mengetahui kota mana yang memiliki jumlah pelanggan dan penjual terbanyak, Anda dapat mengalokasikan sumber daya dan upaya pemasaran Anda dengan lebih efisien. Misalnya, jika suatu kota memiliki jumlah penjual yang tinggi tetapi pelanggan yang rendah, Anda mungkin ingin meningkatkan upaya pemasaran Anda di kota tersebut.")
            st.write("Analisis ini dapat membantu Anda memahami dinamika pasar Anda dengan lebih baik. Anda dapat mengetahui di mana penjual dan pelanggan Anda berada, dan bagaimana mereka berinteraksi satu sama lain.")

        #===========================================================================
        st.markdown("---")
        st.subheader("Grafik 5 Kota Dengan Seller Paling Banyak")

        warna = ['green','lightgreen','lightgreen','lightgreen','yellow']

        # Plot seller
        plt.bar(seller_city_head.index, seller_city_head.values, color=warna)
        plt.xticks(seller_city_head.index, rotation=90)
        plt.title('5 Kota dengan Penjual Terbanyak')

        col1,col2 = st.columns(2)
        with col1:
            st.write("**Top 5 Penjual Terbanyak**")
            st.dataframe(seller_city_head)
        with col2:
            st.write("**Top 5 Penjual Paling Dedikit**")
            st.dataframe(seller_city_tail)

        # Menampilkan Visualisasi
        st.pyplot(plt)
        
        with st.expander("Penjelasan Mengenai Visualisasi"):
            st.write("Sao Paulo adalah kota dengan jumlah penjual terbanyak, dengan total 694 penjual. Ini menunjukkan bahwa Sao Paulo adalah pusat utama aktivitas penjualan. Curitiba dan Rio de Janeiro berada di posisi kedua dan ketiga, dengan 127 dan 96 penjual masing-masing. Meskipun jumlahnya jauh lebih rendah dibandingkan dengan Sao Paulo, kedua kota ini masih menunjukkan aktivitas penjualan yang signifikan.")
            st.write("Di sisi lain, Belo Horizonte dan Ribeirao Preto memiliki jumlah penjual yang lebih sedikit, dengan 68 dan 52 penjual masing-masing. Ini mungkin menunjukkan bahwa ada ruang untuk pertumbuhan di kedua kota ini. Secara keseluruhan, data ini menunjukkan bahwa sebagian besar penjual Anda berada di Sao Paulo, sementara kota-kota lainnya memiliki jumlah penjual yang jauh lebih sedikit. Anda mungkin ingin mempertimbangkan strategi untuk menjangkau penjual potensial di kota-kota dengan jumlah penjual yang lebih rendah.")
        #==============================================================================

        st.markdown("---")
        st.subheader("Grafik 5 Kota dengan Customer Terbanyak")
        col3,col4 = st.columns(2)
        with col3:
            st.write("**Top 5 Penjual Terbanyak**")
            st.dataframe(customer_city_head)
        with col4:
            st.write("**Top 5 Penjual Paling Dedikit**")
            st.dataframe(customer_city_tail)

        # Display the plot in Streamlit
        st.pyplot(plt)

        with st.expander("Penjelasan Mengenai Visualisasi"):
            st.write("Berdasarkan visualisasi, Sao Paulo adalah kota dengan jumlah pelanggan terbanyak, dengan total 15,540 pelanggan. Jumlah ini jauh melampaui kota lainnya, menunjukkan bahwa Sao Paulo adalah pusat utama aktivitas pelanggan Anda. Rio de Janeiro berada di posisi kedua dengan 6,882 pelanggan, namun jumlah ini masih jauh di bawah Sao Paulo.")
            st.write("Di sisi lain, Curitiba, Brasilia, dan Belo Horizonte memiliki jumlah pelanggan yang lebih sedikit, dengan 1,521, 2,131, dan 2,773 pelanggan masing-masing. Meskipun jumlahnya lebih rendah, ini menunjukkan bahwa ada peluang untuk pertumbuhan di ketiga kota ini. Secara keseluruhan, data ini menunjukkan bahwa sebagian besar pelanggan Anda berada di Sao Paulo dan Rio de Janeiro, sementara kota-kota lainnya memiliki jumlah pelanggan yang jauh lebih sedikit. ")

    analisis_farras(data_customer,data_sellers)

     #Ryan

    #Mencari jumlah customer di berbagai provinsi
    customer_state = data_customer['customer_state'].value_counts()

    # Mengurutkan dan mencari 10 kota teratas dengan customer terbanyak
    customer_state_head = customer_state.head(10)

    st.caption("**10122479 - Ryan Akbar Ramadhan**")
    st.subheader("Informasi Analisis")
    st.markdown("**Analisis Terhadap Jumlah Pelanggan dari berbagai provinsi**")
    with st.expander("Tujuan Analisis Infomasi Tersebut"):
        st.write("Akan dapat diketahui berapa banyak pelanggan dari berbagai provinsi, kita dapat menggunakan informasi ini untuk mengupayakan agar meningkatkan pemasaran di provinsi yang jumlah pelanggannya sedikit")

    #===========================================================================
    st.markdown("---")
    st.subheader("Grafik Jumlah Pelanggan dari berbagai provinsi")

    # Plot customer
    warnaBar = ['#00563B','darkgreen','green','#02a633','lightgreen']
    plt.title('10 Provinsi Beserta Pelanggannya')
    plt.bar(customer_state_head.index, customer_state_head.values, color=warnaBar)
    plt.xticks(customer_state_head.index, rotation=0)

    st.write("**Provinsi Beserta Jumlah Pelanggannya**")
    st.dataframe(customer_state)

    # Menampilkan Visualisasi
    st.pyplot(plt)

    with st.expander("Penjelasan Mengenai Visualisasi"):
        st.write("Dapat dilihat pada grafik bahwa, Provinsi SP merupakan Provinsi yang memiliki jumlah pelanggan paling banyak, yaitu sebanyak 41.746 Pelanggan.")
        st.write("Jumlah Pelanggan tersebut hampir 4 kali lipat dari jumlah pelanggan yang ada di Provinsi RJ dan MG, Perbedaan yang sangat tinggi dibandingkan jumlah pelanggan di provinsi lainnya.")

    


with tab2:
    
    st.header("Status pesanan keseluruhan")
    st.caption("**10122290 - Muhamad Haerul Anwar**")
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




