import streamlit as st
import pandas as pd
import joblib

# Load model
with open('XGBoost_best_model.joblib', 'rb') as file_1:
    model = joblib.load(file_1)

def run():
    st.write('# Predict Cyber Attack Risk')

    # form inference
    with st.form("my_form"):
        st.write('### Isi dengan data sesi pengguna')

        session_id = st.text_input('Session ID', placeholder='SID_99999')
        network_packet_size = st.number_input('Network Packet Size (bytes)', min_value=0, value=600)
        protocol_type = st.selectbox('Protocol Type', ['TCP', 'UDP', 'ICMP', 'Other'])
        login_attempts = st.number_input('Login Attempts', min_value=0, value=10)
        session_duration = st.number_input('Session Duration (seconds)', min_value=0, value=30)
        encryption_used = st.selectbox('Encryption Used', ['None', 'SSL', 'TLS', 'Other'])
        ip_reputation_score = st.number_input('IP Reputation Score (0-1)', min_value=0.0, max_value=1.0, value=0.8, step=0.01)
        failed_logins = st.number_input('Failed Logins', min_value=0, value=8)
        browser_type = st.selectbox('Browser Type', ['Chrome', 'Firefox', 'Edge', 'Safari', 'Unknown'])
        unusual_time_access = st.selectbox('Unusual Time Access', [0, 1])

        submit = st.form_submit_button('Predict')

    # inference dataset
    data_inf = {
        'session_id': session_id,
        'network_packet_size': network_packet_size,
        'protocol_type': protocol_type,
        'login_attempts': login_attempts,
        'session_duration': session_duration,
        'encryption_used': encryption_used,
        'ip_reputation_score': ip_reputation_score,
        'failed_logins': failed_logins,
        'browser_type': browser_type,
        'unusual_time_access': unusual_time_access
    }

    data_inf = pd.DataFrame([data_inf])

    # predict
    try:
      if submit:
          result = model.predict(data_inf)
          if result[0] == 0 :
              x = 'Normal'
          else :
              x = 'Attack Detected'
          st.write(f'# Predicted Risk: {x}')
          st.dataframe(
              data_inf.T.reset_index().rename(columns={0: 'Value', 'index': 'Field'}),
              height=500
          )
      else:
          print('Tolong Submit')
    except Exception as e:
        st.error(f"Terjadi error saat prediksi: {e}")

if __name__ == '__main__':
    run()
