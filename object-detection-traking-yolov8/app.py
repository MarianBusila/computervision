import streamlit as st
import PIL
from ultralytics import YOLO

model_path = 'weights/yolov8n.pt'

# Set page layout
st.set_page_config(
    page_title="Object Detection and Tracking using YOLOv8", 
    page_icon="🧊", 
    layout="wide",
    initial_sidebar_state="expanded",
    )

# Set sidebar
with st.sidebar:
    st.header("Image/Video Config")
    # add file uploader
    source_img = st.sidebar.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])

    # model options
    confidence = float(st.slider("Select Model Confidence", 25, 100, 40)) / 100

st.title("Object Detection and Tracking using YOLOv8")

col1, col2 = st.columns(2)

with col1:
    if source_img is not None:
        uploaded_image = PIL.Image.open(source_img)
        st.image(uploaded_image, caption='Uploaded Image', use_column_width=True)

try:
    model = YOLO(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)

if st.sidebar.button('Detect objects'):
    res = model.predict(uploaded_image, conf=confidence)
    boxes = res[0].boxes
    res_plotted = res[0].plot()[:, :, ::-1]
    with col2:
        st.image(res_plotted, caption='Detected Image', use_column_width=True)
        try:
            with st.expander("Detection results"):
                for box in boxes:
                    st.write(box.xywh)
        except Exception as ex:
            st.write("No image is uploaded yet.")