# import libraries
import streamlit as st
import eda, predict

# Sidebar
with st.sidebar:
    st.write("# Page Navigation")

    # Page selection
    page = st.selectbox("Select Page", ("EDA", "Predict Sentiment"))

    st.write(f'Current Page: {page}')

    st.write('## About')
    st.markdown('''
    This app allows you to explore Google Play Store reviews and predict user sentiment.
    
    **EDA Page:** Explore the dataset of 6,000 Messenger app reviews, visualize rating distribution, review lengths, sentiment distribution, and identify patterns in user feedback.
    
    **Predict Sentiment Page:** Enter a new review and predict its sentiment using the trained ANN model.
    ''')

# Main content
if page == 'EDA':
    eda.run()
else:
    predict.run()
