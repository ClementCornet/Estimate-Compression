import streamlit as st
import pandas as pd
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.linear_model import Lasso
import plotly.express as px
from sklearn.preprocessing import StandardScaler
import sklearn
import pickle

from helpers.images import get_images


def page():

    """
    Build a simple Lasso Regressor, using Sparsity Measurements, Cardinality and Hopkins, to predict PNG Size
    """
    
    im_test = get_images('test')
    
    df_train = pd.read_csv('./precomputed/train.csv').clip(lower=-1e300, upper=1e300)
    df_test = pd.read_csv('./precomputed/test.csv').clip(lower=-1e300, upper=1e300)

    scaler = sklearn.preprocessing.StandardScaler()

    cols = df_train.drop('PNG Size', axis=1).columns

    X_train = scaler.fit_transform(df_train.drop('PNG Size', axis=1))
    X_test = scaler.transform(df_test.drop('PNG Size', axis=1))
    X_train = pd.DataFrame(X_train, columns=cols)
    X_test = pd.DataFrame(X_test, columns=cols)

    y_train = df_train['PNG Size']
    y_test = df_test['PNG Size']

    col1, col2 = st.columns([1,0.7])

    with col1:
        st.markdown('''Predict PNG Size using sparsity measurements. Lasso Regression, using $\lambda=0.5$.
                    This time, using the image processing metrics ''')

        with open('models/third_predictor_png.pkl', 'rb') as f:
            model = pickle.load(f)

        pred = model.predict(X_test)

        fig = px.scatter(
            x=pred, y=y_test, 
            trendline='ols', trendline_color_override='red',
            labels={
                     "x": "Predicted",
                     "y": "PNG Size",
                 },
            title=f'R² = {model.score(X_test, y_test):_.3f}\t\t|\t\tMAE% = {100*mean_absolute_percentage_error(pred, y_test):_.3f}%',
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('Note than with a XGBoost regressor, with even reach $R^2 = 0.926$ and MAE% $= 2.719\%$')


    with col2:

        t1, t2 = st.tabs(['Features Importance', 'Error Histogram'])
        with t1:
            coeff = pd.DataFrame()
            coeff['Feature'] =  model.feature_names_in_
            coeff['coeff'] = model.coef_
            coeff.sort_values('coeff')
            fig = px.bar(coeff[coeff['coeff']**2>10], y='Feature', x='coeff', orientation='h', labels={
                'Feature' : '',
                'coeff' : 'Coefficients'
            }, title='Lasso Regression Coefficients')
            fig.update_traces(marker_color='#0068c9')
            st.components.v1.html(fig.to_html(include_mathjax='cdn'),height=500)
        
            

        with t2:
            fig = px.histogram(pred/y_test - 1, title='Error histogram')
            fig.update_layout(showlegend=False)
            fig.update(layout_showlegend=False)
            st.plotly_chart(fig, use_container_width=True)


