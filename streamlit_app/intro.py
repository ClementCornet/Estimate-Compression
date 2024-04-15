import streamlit as st

def page():
    
    st.title("Inferring actual compression performance from data sparsity measures")    

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(open('markdown/abstract.md').read())
        st.markdown(open('markdown/tableofcontents.md').read())
    with col2:
        st.write(' \n \n \n \n ')
        st.image("https://blog.fileformat.com/fr/compression/lossy-and-lossless-compression-algorithms/images/compression-algorithms.png")