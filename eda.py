import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# 1️⃣ Set theme and default figure size
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 5)

# 2️⃣ Function to map rating to sentiment
def map_rating_to_sentiment(r):
    if r >= 4:
        return "positive"
    elif r <= 2:
        return "negative"
    else:
        return "neutral"

def run():
    # Header
    st.write('# Google Play Store Reviews Analysis')

    # Background
    st.write('# Background')
    st.markdown('''
        This dataset contains 6,000 user reviews of the Messenger app from Google Play Store.
        The goal of this exploratory data analysis (EDA) is to understand the distribution
        of ratings, sentiments, review lengths, and highlight patterns in user feedback.
    ''')

    # Load dataset
    data = pd.read_csv('dataset.csv')

    # Create sentiment column from rating/score
    if 'score' in data.columns:
        data['sentiment'] = data['score'].apply(map_rating_to_sentiment)
    elif 'Rating' in data.columns:
        data['sentiment'] = data['Rating'].apply(map_rating_to_sentiment)
    else:
        st.warning("No 'score' or 'Rating' column found in dataset!")
    
    # Show dataset
    st.write('# Dataset')
    st.dataframe(data.head())

    # EDA
    st.write("# Exploratory Data Analysis")

    # Rating Distribution
    rating_col = 'score' if 'score' in data.columns else 'Rating'
    st.write('## Rating Distribution')
    fig = plt.figure(figsize=(10,4))
    sns.countplot(x=rating_col, data=data)
    plt.title('Distribution of Ratings')
    st.pyplot(fig)
    st.markdown('''
        The countplot above shows the distribution of user ratings from 1 to 5 stars.
        
        Insights:
        1. Most users tend to give ratings in the higher range (4-5 stars), indicating general satisfaction.
        2. Lower ratings may indicate negative experiences or issues with the app.
        3. Understanding rating distribution helps identify patterns of user satisfaction.
    ''')

    # Sentiment Distribution
    if 'sentiment' in data.columns:
        st.write('## Sentiment Distribution')
        fig = plt.figure(figsize=(10,4))
        sns.countplot(x='sentiment', data=data)
        plt.title('Distribution of Sentiments')
        st.pyplot(fig)
        st.markdown('''
            This chart shows the distribution of sentiment labels (Positive, Neutral, Negative).
            
            Insights:
            1. Majority of reviews are positive, reflecting user satisfaction.
            2. Negative reviews highlight areas for potential improvement.
            3. Sentiment analysis can be used to monitor app performance and user feedback trends.
        ''')

    # Review Length Distribution
    review_col = 'content'  # gunakan kolom content
    st.write('## Review Length Distribution')

    # Buat kolom review_length
    data['review_length'] = data[review_col].astype(str).apply(len)

    # Histogram review lengths
    fig = plt.figure(figsize=(10,4))
    sns.histplot(data['review_length'], bins=20, kde=True)
    plt.title('Histogram of Review Lengths')
    st.pyplot(fig)
    st.markdown('''
        The histogram shows the distribution of review text lengths.
        
        Insights:
        1. Most reviews are short, often under 200 characters.
        2. Longer reviews may contain more detailed feedback or issues.
        3. Understanding review lengths helps in preprocessing text for NLP tasks.
    ''')

    # Scatter: Rating vs Review Length
    st.write('## Rating vs Review Length')
    fig_px = px.scatter(
        data, 
        x=rating_col,  # pastikan rating_col sudah didefinisikan sebelumnya
        y='review_length', 
        color='sentiment' if 'sentiment' in data.columns else None,
        hover_data=['App', review_col] if 'App' in data.columns else [review_col]
    )
    st.plotly_chart(fig_px)
    st.markdown('''
        This scatter plot shows the relationship between user ratings and review lengths.
        
        Insights:
        1. We can see whether higher or lower ratings tend to have longer reviews.
        2. Hovering over points allows inspection of specific reviews for more context.
    ''')


    # Top Apps by Review Count
    if 'App' in data.columns:
        st.write('## Top Apps by Review Count')
        top_apps = data['App'].value_counts().head(10)
        fig = plt.figure(figsize=(8,4))
        sns.barplot(x=top_apps.index, y=top_apps.values)
        plt.xticks(rotation=45)
        plt.title('Top 10 Apps by Number of Reviews')
        st.pyplot(fig)
        st.markdown('''
            The bar chart shows the apps with the highest number of reviews.
            
            Insights:
            1. Apps with more reviews likely have a larger user base.
            2. Review count can correlate with app popularity and reliability of sentiment analysis.
        ''')

if __name__ == '__main__':
    run()
