import streamlit as st
import numpy as np
import pickle
import tensorflow as tf
from tensorflow import keras

# 1. Load pipeline model
@st.cache_resource
def load_model():
    return keras.models.load_model("best_ann_baseline_pipeline.keras")

# 2. Load mapping label
@st.cache_resource
def load_mappings():
    with open("label_mappings.pkl", "rb") as f:
        mappings = pickle.load(f)
    return mappings["label2id"], mappings["id2label"]

model_loaded = load_model()
label2id, id2label = load_mappings()

def run():
    st.title("📊 Sentiment Analysis Prediction")

    st.write("Masukkan teks untuk diprediksi sentimennya menggunakan model ANN")

    # Form input teks
    with st.form("sentiment_form"):
        input_texts = st.text_area(
            "Masukkan teks (pisahkan dengan enter untuk banyak data):",
            placeholder="Contoh:\nI really love this product!\nBad.\nLove this apk!"
        )
        submit = st.form_submit_button("Predict")

    if submit:
        if not input_texts.strip():
            st.warning("Tolong isi teks terlebih dahulu.")
        else:
            # Split input jadi list
            sample_texts = [t.strip() for t in input_texts.split("\n") if t.strip()]

            # Bentuk tensor (batch_size, 1)
            sample_texts_tensor = tf.constant(sample_texts)[:, tf.newaxis]

            # Prediksi
            pred_probs = model_loaded.predict(sample_texts_tensor)
            pred_classes = np.argmax(pred_probs, axis=1)

            # Hasil
            results = []
            for text, cls_id, probs in zip(sample_texts, pred_classes, pred_probs):
                results.append({
                    "Teks": text,
                    "Prediksi Sentimen": id2label[cls_id],
                    "Probabilitas": float(probs[cls_id])
                })

            st.subheader("📌 Hasil Prediksi")
            st.dataframe(results, use_container_width=True)

if __name__ == "__main__":
    run()
