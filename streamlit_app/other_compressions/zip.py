import streamlit as st

def page():
    
    st.header('Compressing files as ZIP')

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(open('markdown/zip/zip.md', 'r').read())
        st.image('streamlit_app/assets/oldway.png', width=400)
    with col2:
        st.markdown(open('markdown/zip/chunks.md', 'r').read())
        #st.warning('Petit graph avec les couleurs par extension? Ou osef parce que c\'est moche?')