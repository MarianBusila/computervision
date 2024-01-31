import streamlit as st
from ultralytics import YOLO
from pathlib import Path

import settings
import helper

model_path = 'weights/yolov8n.pt'

# Set page layout
st.set_page_config(
    page_title="Object Detection and Tracking using YOLOv8", 
    page_icon="🧊", 
    layout="wide",
    initial_sidebar_state="expanded",
    )

st.title("Object Detection and Tracking using YOLOv8")

# Set sidebar
st.sidebar.header("ML Model Config")

# Model options
model_type = st.sidebar.radio("Select Task", ['Detection', 'Segmentation'])
confidence = float(st.sidebar.slider("Select Model Confidence", 25, 100, 40)) / 100

# Selecting detection or segmentation
if model_type == 'Detection':
    model_path = Path(settings.DETECTION_MODEL)
elif model_type == 'Segmentation':
    model_path = Path(settings.SEGMENTATION_MODEL)

# Load model
try:
    model = YOLO(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)


st.sidebar.header("Image/Video Config")
source_radio = st.sidebar.radio("Select Source", settings.SOURCES_LIST)

# If image is selected
if(source_radio == settings.IMAGE):
    helper.handle_image(confidence, model)
elif source_radio == settings.VIDEO:
    helper.handle_stored_video(confidence, model)