# Standard Streamlit imports
import streamlit as st
st.set_page_config(page_title='Sparse #4', layout="wide")
import warnings
warnings.filterwarnings('ignore')

from streamlit_app import intro, final_page
from streamlit_app.png_compression import motiv_method, sparsity_measures, first_predictor, clustering_pov, \
                                        second_predictor, image_processing, third_predictor
from streamlit_app.other_compressions import zip, jpeg2000, jpeg

with st.sidebar:
    st.title('Sparse Models Project #4')

    choice = st.selectbox('Section',[
        'Introduction',
        'PNG : Motivation & Methodology',
        'PNG : Sparsity Measures',
        'PNG : First Predictor',
        'PNG : A clustering point of view',
        'PNG : Second Predictor',
        'PNG : Image Transformations',
        'PNG : Third Predictor',
        'Other : ZIP',
        'Other : Lossless JPEG2000',
        'Other : Compression with loss, JPEG',
        'Final Demonstration'
    ])


if choice == 'Introduction':
    intro.page()
elif choice == 'PNG : Motivation & Methodology':
    motiv_method.page()
elif choice == 'PNG : Sparsity Measures':
    sparsity_measures.page()
elif choice == 'PNG : First Predictor':
    first_predictor.page()
elif choice == 'PNG : A clustering point of view':
    clustering_pov.page()
elif choice == 'PNG : Second Predictor':
    second_predictor.page()
elif choice == 'PNG : Image Transformations':
    image_processing.page()
elif choice == 'PNG : Third Predictor':
    third_predictor.page()
elif choice == 'Other : ZIP':
    zip.page()
elif choice == 'Other : Lossless JPEG2000':
    jpeg2000.page()
elif choice == 'Other : Compression with loss, JPEG':
    jpeg.page()
elif choice == 'Final Demonstration':
    final_page.page()