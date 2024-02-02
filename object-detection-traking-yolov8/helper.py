from ultralytics import YOLO
import streamlit as st
import cv2
import pafy
import settings
import PIL
from pytube import YouTube


def _display_detected_frames(confidence, model, st_frame, image):
    # resize image to standard size
    image = cv2.resize(image, (720, int(720 * (9/16))))

    # detect objects in the image
    res = model.predict(image, conf=confidence)

    # plot the detected objects
    res_plotted = res[0].plot()[:, :, ::-1]
    st_frame.image(res_plotted, caption = 'Detected Video', channels="BGR", use_column_width=True)

def handle_youtube_video(confidence, model):
    source_youtube = st.sidebar.text_input("YouTube Video URL", "https://www.youtube.com/watch?v=9bZkp7q19f0")

    col1, col2 = st.columns(2)
    with col1:
        st.video(source_youtube)

    with col2:
        if st.sidebar.button('Detect video objects'):
            yt = YouTube(source_youtube)
            stream = yt.streams.filter(file_extension="mp4", res=720).first()
            _handle_video_capture(confidence, model, stream.url)

def handle_stored_video(confidence, model):
    source_vid = st.sidebar.selectbox("Choose Video", list(settings.VIDEOS_DICT.keys()))

    col1, col2 = st.columns(2)
    with col1:
        with open(settings.VIDEOS_DICT[source_vid], 'rb') as video_file:
            video_bytes = video_file.read()

            if video_bytes:
                st.video(video_bytes)

    with col2:
        if st.sidebar.button('Detect video objects'):
            _handle_video_capture(confidence, model, str(settings.VIDEOS_DICT[source_vid]))

def _handle_video_capture(confidence, model, path):
    try:
        vid_cap = cv2.VideoCapture(path)
        st_frame = st.empty()
        while(vid_cap.isOpened()):
            success, image = vid_cap.read()
            if success:
                _display_detected_frames(confidence, model, st_frame, image)
            else:
                vid_cap.release()
                break

    except Exception as e:
        st.sidebar.error("Error loading video. " + str(e))

def handle_image(confidence, model):
    source_img = st.sidebar.file_uploader("Choose Image", type=['png', 'jpg', 'jpeg'])

    col1, col2 = st.columns(2)

    with col1:
        if source_img is not None:
            uploaded_image = PIL.Image.open(source_img)
            st.image(uploaded_image, caption='Uploaded Image', use_column_width=True)

    with col2:
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