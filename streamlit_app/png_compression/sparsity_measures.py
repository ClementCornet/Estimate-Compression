import streamlit as st
import pandas as pd
import plotly.express as px

def page():
    """
    Sparsity Measures page : list measures, and display correlations with PNG Size
    """
    st.title('Sparsity Measures')

    col1, col2 = st.columns([1.2,1.5])
    with col1:
        st.markdown(open('markdown/measures/sparse_measures.md','r').read())

    with col2:

        df = pd.read_csv('./precomputed/train.csv')
        df2 = df.drop('$Hopkins$', axis=1)\
                    .drop('$Card$', axis=1)\
                    .drop('$Card_{raw}$', axis=1)\
                    .drop('$Card_{raw}^{mono}$', axis=1)\
                    .drop('$GO-\ell^0$', axis=1)\
                    .drop('$GO-\ell^1$', axis=1)\
                    .drop('$GO-\ell^2$', axis=1)\
                    .drop('$GO-\ell^H$', axis=1)\
                    .drop('$DoG-\ell^0$', axis=1)\
                    .drop('$DoG-\ell^1$', axis=1)\
                    .drop('$DoG-\ell^2$', axis=1)\
                    .drop('$DoG-\ell^H$', axis=1)\
                    .drop('$GO-\ell^0_{raw}$', axis=1)\
                    .drop('$GO-\ell^1_{raw}$', axis=1)\
                    .drop('$GO-\ell^2_{raw}$', axis=1)\
                    .drop('$GO-\ell^H_{raw}$', axis=1)\
                    .drop('$DoG-\ell^0_{raw}$', axis=1)\
                    .drop('$DoG-\ell^1_{raw}$', axis=1)\
                    .drop('$DoG-\ell^2_{raw}$', axis=1)\
                    .drop('$DoG-\ell^H_{raw}$', axis=1)
        cor = df2.corr().abs()
        fig = px.imshow(cor.fillna(0)
                        .sort_values('PNG Size', ascending=False, axis=0)
                        .sort_values('PNG Size', ascending=False, axis=1), color_continuous_scale='blues')
        fig.update_coloraxes(showscale=False)
        fig.update_layout(margin=dict(l=0, r=0, t=50, b=0))
        st.components.v1.html(fig.to_html(include_mathjax='cdn'),height=500)