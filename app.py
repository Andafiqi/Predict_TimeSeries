import streamlit as st
import pickle

# Load the trained model
model = pickle.load(open('modelrf1.pkl', 'rb'))

def predict(year):
    year = int(year)
    prediction = model.predict([[year]])
    return {
        'Schizophrenia_disorders': prediction[0][0],
        'Depressive_disorders': prediction[0][1],
        'Anxiety_disorders': prediction[0][2],
        'Bipolar_disorders': prediction[0][3],
        'Eating_disorders': prediction[0][4]
    }

# Streamlit UI
st.title('Prediksi Time Series')

year = st.text_input('Masukkan Tahun:')
if st.button('Prediksi'):
    if year.isdigit():
        prediction = predict(year)
        st.subheader('Hasil Prediksi:')
        st.write('Schizophrenia disorders:', prediction['Schizophrenia_disorders'])
        st.write('Depressive disorders:', prediction['Depressive_disorders'])
        st.write('Anxiety disorders:', prediction['Anxiety_disorders'])
        st.write('Bipolar disorders:', prediction['Bipolar_disorders'])
        st.write('Eating disorders:', prediction['Eating_disorders'])
    else:
        st.error('Tahun harus berupa angka.')
