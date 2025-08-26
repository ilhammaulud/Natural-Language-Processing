import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from PIL import Image


def run():
    # Header
    st.write('# Cybersecurity Session Data Analysis')

    # Latar belakang
    st.write('# Latar Belakang')
    st.markdown('''
        Dataset ini berisi informasi sesi login pengguna yang digunakan untuk
        menganalisis potensi serangan siber. Fitur-fitur mencakup ukuran paket,
        jenis protokol, jumlah percobaan login, reputasi IP, dan aktivitas
        yang tidak biasa.
    ''')

    # Dataset
    data = pd.read_csv('dataset.csv')



    # Tampilkan dataset
    st.write('# Dataset')
    st.dataframe(data)

    # EDA
    st.write("# Exploratory Data Analysis")

    # Distribusi Network Packet Size
    st.write('## Distribusi Network Packet Size')
    fig = plt.figure(figsize=(10,4))
    sns.histplot(data['network_packet_size'], kde=True, bins=10)
    plt.title('Histogram of Network Packet Size')
    st.pyplot(fig)
    st.markdown('''
        Dari visualisasi distribusi network_packet_size yang ditampilkan, 
        terlihat pola sebaran ukuran paket jaringan pada seluruh sesi. Histogram menunjukkan frekuensi kemunculan setiap rentang 
        ukuran paket, sementara garis KDE memberikan gambaran trend kepadatan data secara lebih halus.
        
        Berdasarkan grafik:

        1. Mayoritas sesi memiliki ukuran paket yang berada pada rentang tertentu, yang tampak sebagai puncak distribusi.
        2. Sebaran data menunjukkan variasi ukuran paket; ada beberapa paket dengan ukuran yang jauh dari mayoritas, yang kemungkinan merupakan outlier atau kondisi jaringan yang tidak biasa.
        3. Distribusi ini membantu memahami karakteristik lalu lintas jaringan dan dapat menjadi acuan awal untuk deteksi anomali atau serangan siber, karena paket dengan ukuran ekstrem dapat menunjukkan aktivitas yang mencurigakan.
        4. Secara keseluruhan, visualisasi ini memberikan insight mengenai frekuensi dan pola umum ukuran paket jaringan, yang penting dalam proses feature analysis sebelum diterapkan ke model machine learning.
    ''')

    # Distribusi IP Reputation Score
    st.write('## Distribusi IP Reputation Score')
    fig = plt.figure(figsize=(10,4))
    sns.histplot(data['ip_reputation_score'], kde=True, bins=10)
    plt.title('Histogram of IP Reputation Score')
    st.pyplot(fig)
    st.markdown('''
        Visualisasi histogram ip_reputation_score menunjukkan sebaran skor reputasi IP dari seluruh sesi yang dianalisis. 
        Garis KDE memberikan gambaran kepadatan distribusi secara lebih halus.

        Berdasarkan grafik:

        1. Mayoritas IP memiliki skor yang berada pada rentang tertentu, menandakan sebagian besar sesi berasal dari IP dengan reputasi baik hingga sedang.
        2. Ada beberapa IP dengan skor ekstrem, baik rendah maupun tinggi, yang dapat dianggap sebagai outlier atau potensi sumber risiko tinggi.
        3. Distribusi ini membantu dalam memahami profil keamanan jaringan dan bisa menjadi fitur penting untuk model prediksi risiko serangan siber.
        4. Secara keseluruhan, visualisasi ini memberikan insight mengenai pola umum reputasi IP yang berguna untuk analisis lebih lanjut, termasuk identifikasi sesi yang berpotensi berisiko tinggi.
    ''')

    # Jumlah session berdasarkan protocol type
    st.write('## Protocol Type Count')
    fig = plt.figure(figsize=(6,4))
    sns.countplot(x='protocol_type', data=data)
    plt.title('Protocol Type Distribution')
    st.pyplot(fig)
    st.markdown('''
        Visualisasi countplot ini menampilkan jumlah sesi berdasarkan jenis protokol (protocol_type) yang digunakan dalam dataset.
        
        Dari grafik:

        1. Terlihat distribusi masing-masing protokol, misalnya TCP, UDP, atau ICMP, menunjukkan protokol mana yang paling sering digunakan.
        2. Jika satu protokol mendominasi jumlah sesi, hal ini dapat memberikan insight mengenai alur lalu lintas jaringan dan potensi titik lemah keamanan.
        3. Perbedaan jumlah sesi antar protokol juga bisa membantu dalam penentuan strategi monitoring dan proteksi, misalnya fokus pada protokol yang lebih banyak digunakan untuk deteksi intrusi.
        4. Secara keseluruhan, grafik ini memberikan pemahaman awal mengenai karakteristik lalu lintas jaringan berdasarkan jenis protokol, yang berguna sebagai input dalam analisis risiko atau model prediksi serangan siber.
    ''')

    # Plotly scatter: IP Reputation vs Failed Logins
    st.write('## IP Reputation vs Failed Logins')
    fig_px = px.scatter(data, x='ip_reputation_score', y='failed_logins', color='protocol_type',
                        hover_data=['session_id', 'browser_type'])
    st.plotly_chart(fig_px)
    st.markdown('''
        Visualisasi scatter plot ini menunjukkan hubungan antara skor reputasi IP (ip_reputation_score) dengan jumlah login gagal (failed_logins), diwarnai berdasarkan protocol_type.
        
        Dari plot ini:

        1. Kita dapat melihat pola distribusi login gagal terhadap skor reputasi IP, misalnya apakah IP dengan skor rendah cenderung memiliki lebih banyak percobaan login gagal.
        2. Warna berdasarkan protocol_type membantu mengidentifikasi protokol mana yang lebih sering mengalami login gagal.
        3. Fitur hover_data seperti session_id dan browser_type memungkinkan pemeriksaan detail sesi tertentu untuk analisis lebih mendalam.
        4. Secara keseluruhan, scatter plot ini memberikan insight awal mengenai korelasi potensi ancaman dengan reputasi IP dan pola login yang mencurigakan, yang penting untuk deteksi intrusi siber dan analisis risiko.
    ''')

    # Heatmap korelasi numerik
    st.write('## Korelasi Fitur Numerik')
    fig = plt.figure(figsize=(8,5))
    sns.heatmap(data[['network_packet_size','login_attempts','session_duration',
                      'ip_reputation_score','failed_logins']].corr(),
                annot=True, cmap='coolwarm')
    plt.title('Correlation Heatmap')
    st.pyplot(fig)
    st.markdown('''
    Berdasarkan hasil analisis korelasi antar fitur, diperoleh temuan sebagai berikut:

    1. Tingkat Korelasi Rendah Secara Umum

        Semua nilai korelasi antar fitur berada sangat dekat dengan nol, berkisar antara -0.0135 hingga 0.0216. Hal ini menunjukkan bahwa secara linear, tidak ada hubungan kuat antar fitur pada dataset ini.

    2. Pasangan Fitur dengan Korelasi Positif Tertinggi

        * session_duration dengan network_packet_size memiliki korelasi 0.02165 — meskipun tertinggi di tabel, nilainya tetap sangat kecil sehingga hubungannya hampir tidak signifikan.

        * failed_logins dengan ip_reputation_score memiliki korelasi 0.01561, yang juga termasuk lemah.

    3. Pasangan Fitur dengan Korelasi Negatif

        * network_packet_size dengan failed_logins memiliki korelasi -0.01167, menunjukkan hubungan negatif yang sangat lemah.

        * login_attempts dengan failed_logins memiliki korelasi -0.01350, yang berarti sedikit indikasi bahwa semakin banyak upaya login, jumlah gagal login justru sedikit menurun, tetapi nilainya terlalu kecil untuk diambil kesimpulan kuat.

    4. Implikasi terhadap Modeling

        * Korelasi yang rendah antar fitur ini mengindikasikan bahwa tidak ada masalah multikolinearitas signifikan di dataset.

        * Fitur-fitur yang ada kemungkinan memberikan informasi yang relatif unik, sehingga semuanya masih layak dipertimbangkan dalam proses pemodelan tanpa risiko redundansi yang tinggi.
    ''')


if __name__ == '__main__':
    run()
