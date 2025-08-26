# import libraries
import streamlit as st
import eda, predict

# bagian dalam sidebar
with st.sidebar:
    st.write("# Page Navigation")

    # toggle pilih halaman
    page = st.selectbox("Pilih Halaman", ("EDA", 'Predict Rating'))

    # test
    st.write(f'Halaman yang dituju {page}')

    st.write('## About')
    # magic
    '''
    Page ini berisikan informasi mengenai sesi aktivitas jaringan pengguna, termasuk detail seperti ukuran paket data, 
    jenis protokol yang digunakan, jumlah percobaan login, durasi sesi, metode enkripsi yang diterapkan, 
    skor reputasi IP, jumlah kegagalan login, tipe browser, serta indikator akses pada waktu yang tidak biasa. 
    Data ini bertujuan untuk membantu mengidentifikasi pola-pola aktivitas mencurigakan yang dapat mengindikasikan
    adanya serangan siber atau pelanggaran keamanan.
    '''

# bagian luar sidebar
if page == 'EDA':
    eda.run()

else:
    predict.run()