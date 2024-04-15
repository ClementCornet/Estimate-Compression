import streamlit as st
import pickle
import plotly.express as px
import pandas as pd

def page():
    st.title('Another Lossless image compression : JPEG2000')
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown(open('markdown/jpeg2000.md', 'r').read())

        #st.warning('Rajouter un visuel qqch? Comp PNG?')
        res_df = pd.DataFrame()
        res_df['Compression'] = ['PNG', 'JPEG2000']
        res_df['R²'] = [0.926, 0.940]
        res_df['MAE%'] = [2.719, 2.]

        subcols_barchart()

    
    with col2:
        model = pickle.load(open('models/lasso_jp2.pkl','rb'))
        fig = px.bar(y=model.feature_names_in_, x=model.coef_, orientation='h', 
                     labels={'y':'','x':'Coefficients'}, title='Lasso Coefficients for JPEG2000')
        fig.update_traces(marker_color='#0068c9')
        st.components.v1.html(fig.to_html(include_mathjax='cdn'),height=500)



def subcols_barchart():
    col12, col22, _ = st.columns([1, 1, 0.3])
    with col12:
        fig = px.bar(x=['PNG', 'JPEG2000'], y=[0.926, 0.940], color=['PNG', 'JPEG2000'], labels={'x':'Compression', 'y':'R²'})
        fig.update_layout(margin=dict(t=0, r=0, l=0, b=0), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with col22:
        fig = px.bar(x=['PNG', 'JPEG2000'], y=[2.719, 2.05], color=['PNG', 'JPEG2000'], labels={'x':'Compression', 'y':'MAE%'})
        fig.update_layout(margin=dict(t=0, r=0, l=0, b=0), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
