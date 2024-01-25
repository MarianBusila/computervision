import os
import streamlit as st
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates as im_coordinates
import numpy as np
import cv2
from background_remover import remove_background
import base64

# set layout
st.set_page_config(layout="wide")

def set_background(image_file):
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    style = f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{b64_encoded});
            background-size: cover;
        }}
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)


set_background('./bg.jpg')


col01, col02 = st.columns(2)

# file uploader

file = col02.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

# read image
if file is not None:
   
    image_width = 880
    image = Image.open(file).convert('RGB')
    image = image.resize((image_width, int(image.height * image_width / image.width)))

    # create buttons
    col1, col2 = col02.columns(2)

    placeholder0 = col02.empty()
    with placeholder0:
        value = im_coordinates(image)
        if value is not None:
            x, y = value['x'], value['y']
            print(value)

    if col1.button('Original', use_container_width=True):
        placeholder0.empty()
        placeholder1 = col02.empty()
        with placeholder1:
            col02.image(image, use_column_width=True)

    if col2.button('Remove Background', type='primary', use_container_width=True):
        placeholder0.empty()
        placeholder2 = col02.empty()

        filename = 'br_{}_{}_{}.png'.format(file.name.split('.')[0], x, y)
        if os.path.exists(filename):
            # load from saved file, when already processed
            result_image = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
        else:
            result_image = remove_background(np.asarray(image), x, y)
            cv2.imwrite(filename, result_image)
        
        with placeholder2:
            col02.image(result_image, use_column_width=True)

            

    # visualize image
    # click on image to select x, y coordinates

    # remove background
