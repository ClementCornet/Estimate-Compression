import streamlit as st
import pickle
import json
import plotly.express as px
from sklearn.metrics import mean_absolute_percentage_error

from helpers.measures import *
from helpers.images import paeth
from PIL import Image
import cv2

def page():
    st.title('Test with Camera')
    
    with open('precomputed/jpeg_test.json', 'r') as f:
        jtest = json.load(f)

    jpegmodels = {}
    for k in jtest.keys():
        with open(f'models/xgb_jpeg_q{k}.pkl', 'rb') as f:
            jpegmodels[k] = pickle.load(f)
    
    with open(f'models/png_xgb.pkl', 'rb') as f:
        png_model = pickle.load(f)
    with open(f'models/xgb_jp2.pkl', 'rb') as f:
        jp2_model = pickle.load(f)

    col1, col2 = st.columns([1.5, 2])

    with col1:
        #st.markdown('Blablabla on test avec tous')
        img_file_buffer = st.camera_input("Take a picture")


            
    with col2:
        if img_file_buffer is not None:
            img = Image.open(img_file_buffer)
            img_array = np.array(img)
            im_raw = cv2.resize(img_array, dsize=(32, 32), interpolation=cv2.INTER_CUBIC).reshape((32,32,3))#.transpose(2,1,0)
            
            image_png_size = get_png_size(im_raw)
            image_jp2_size = get_jpeg2000_size(im_raw)
            image_jpeg_sizes = {k:get_jpeg_size(im_raw, int(k)) for k in jtest.keys()}
            
            im_paeth = paeth(im_raw.transpose(2,1,0))

            image_features = np.array([
                    [image_hopkins(im_raw)],
                    [shannon_entropy(im_paeth)],
                    [modified_shannon_entropy(im_paeth)],
                    [l0_norm(im_paeth)],
                    [l1_norm(im_paeth)],
                    [l2_l1_ratio(im_paeth)],
                    [sparse_log(im_paeth)],
                    [kurtosis_4(im_paeth)],
                    [gaussian_entropy(im_paeth)],
                    [hoyer(im_paeth)],
                    [gini(im_paeth)],
                    [gini(im_raw)],
                    [card_image(im_paeth)],
                    [card_image(im_raw)],
                    [card_image_mono(im_raw)],
                    [dog_l0(im_raw)],
                    [dog_l1(im_raw)],
                    [dog_l2(im_raw)],
                    [dog_hs(im_raw)],
                    [greyopening_l0(im_raw)],
                    [greyopening_l1(im_raw)],
                    [greyopening_l2(im_raw)],
                    [greyopening_hs(im_raw)],
                    [dog_l0(im_paeth)],
                    [dog_l1(im_paeth)],
                    [dog_l2(im_paeth)],
                    [dog_hs(im_paeth)],
                    [greyopening_l0(im_paeth)],
                    [greyopening_l1(im_paeth)],
                    [greyopening_l2(im_paeth)],
                    [greyopening_hs(im_paeth)],
                    [sparse_tanh(im_paeth, 0.5, 2)],
                    [l0_epsilon(im_paeth, 0.005)],
                    [lp_norm(im_paeth, 2)],
                    [lp_neg(im_paeth, 0.5)]
                ]).T
            
            

            png_pred = png_model.predict(image_features)
            #st.write('PNG', png_pred, image_png_size)

            jp2_pred = jp2_model.predict(image_features)
            #st.write('JPEG2000', jp2_pred, image_jp2_size)

            pred_dict = {}
            pred_dict['PNG'] = (png_pred[0], image_png_size)
            pred_dict['JPEG2000'] = (jp2_pred[0], image_jp2_size)

            for k,v in jpegmodels.items():
                jpeg_pred = jpegmodels[k].predict(image_features)
                #st.write(f'JPEG, Q={k}', jpeg_pred, image_jpeg_sizes[k])

                pred_dict[f'JPEG, Q={k}'] = (jpeg_pred[0], image_jpeg_sizes[k])

            import plotly.graph_objects as go

            preds_df = pd.DataFrame()
            preds_df['Compression'] = pred_dict.keys()
            preds_df['Prediction'] = [float(pred_dict[k][0]) for k in pred_dict]
            preds_df['Real Size'] = [float(pred_dict[k][1]) for k in pred_dict]

            fig = go.Figure(data=[go.Bar(
                name = 'Prediction',
                x = preds_df['Compression'],
                y = preds_df['Prediction']
            ), go.Bar(
                name = 'Real Size',
                x = preds_df['Compression'],
                y = preds_df['Real Size']
            )
            ])

            fig.update_layout(title='Predicted Size vs Real Size for different compression')
            st.plotly_chart(fig, use_container_width=True)