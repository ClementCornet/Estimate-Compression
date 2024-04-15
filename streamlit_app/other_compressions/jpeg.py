import streamlit as st
import pickle
import json
import pandas as pd
import plotly.express as px
from sklearn.metrics import mean_absolute_percentage_error

def page():
    st.title('Compression with loss : JPEG')
    X_test = pd.read_csv('precomputed/test.csv').drop('PNG Size', axis=1)

    with open('precomputed/jpeg_test.json', 'r') as f:
        jtest = json.load(f)

    models = {}
    for k in jtest.keys():
        with open(f'models/xgb_jpeg_q{k}.pkl', 'rb') as f:
            models[k] = pickle.load(f)


    r2_dict = {k:model.score(X_test, jtest[k]) for k,model in models.items()}

    maep_dict = {
        k:mean_absolute_percentage_error(model.predict(X_test), jtest[k]) for k,model in models.items()
    }

    col1, col2 = st.columns([1.5, 2])

    with col1:
        st.markdown(open('markdown/jpeg.md', 'r').read())

        quality = st.select_slider('Quality Factor', list(jtest.keys()), value='100')

        center_image(f'streamlit_app/assets/im0_q{quality}.jpeg', caption=f'Quality = {quality}')


    with col2:
        r2_tab, maep_tab = st.tabs(['R²', 'MAE%'])

        with r2_tab:
            fig = px.line(
                x=r2_dict.keys(), y=r2_dict.values(),
                title=f'{" "*10}R² obtained with JPEG for different Quality Factors',
                labels={'x': 'Quality Factor', 'y':'R²'}
            )
            fig.add_hline(y=0.92623, line_dash="dash", line_color="green", annotation_text='PNG R² = 0.92623')
            fig.add_hline(y=0.940, line_dash="dash", line_color="skyblue", annotation_text='JPEG2000 R² = 0.940')
            st.plotly_chart(fig, use_container_width=True)

        with maep_tab:
            fig = px.line(
                x=maep_dict.keys(), y=maep_dict.values(),
                title=f'{" "*10}MAE% obtained with JPEG for different Quality Factors',
                labels={'x': 'Quality Factor', 'y':'MAE%'}
            )
            fig.add_hline(y=0.02719, line_dash="dash", line_color="green", annotation_text='PNG MAE% = 2.719%')
            fig.add_hline(y=0.0205, line_dash="dash", line_color="skyblue", annotation_text='JPEG2000 MAE% = 2.05%')
            st.plotly_chart(fig, use_container_width=True)


def center_image(im_path, caption):
    subcols = st.columns([0.5,1,0.5])
    with subcols[1]:
        st.image(im_path, caption=caption, use_column_width=True)