import streamlit as st
import pydicom
import numpy as np
import cv2
from PIL import Image

st.set_page_config(layout="wide")
st.title("🩻 Multi-Slice DICOM Viewer (Streamlit)")

uploaded_files = st.sidebar.file_uploader(
    "Upload multiple DICOM files", type=["dcm"], accept_multiple_files=True
)

if uploaded_files:
    try:
        slices = [pydicom.dcmread(f) for f in uploaded_files]
        slices.sort(key=lambda x: int(getattr(x, 'InstanceNumber', 0)))
        images = [s.pixel_array.astype(np.float32) for s in slices]


    try:
        num_slices = len(images)
        if num_slices > 1:
            slice_idx = st.sidebar.slider("Select Slice", 0, num_slices - 1, 0)
        else:
            slice_idx = 0
            st.info("Only one slice uploaded, slice scrolling disabled.")

    # more code here...

    except Exception as e:
        st.error(f"⚠️ Error reading DICOM files: {e}")



        brightness = st.sidebar.slider("Brightness", -100, 100, 0)
        contrast = st.sidebar.slider("Contrast", 1, 3, 1)
        zoom = st.sidebar.slider("Zoom", 1, 5, 1)
        blur = st.sidebar.checkbox("Apply Blur")
        edge = st.sidebar.checkbox("Edge Detection")

        img = images[slice_idx].copy()


        img = img * contrast + brightness
        img = np.clip(img, 0, 255)

        h, w = img.shape
        zh, zw = h // zoom, w // zoom
        img = img[h//2 - zh//2:h//2 + zh//2, w//2 - zw//2:w//2 + zw//2]
        img = cv2.resize(img, (w, h), interpolation=cv2.INTER_CUBIC)


        if blur:
            img = cv2.GaussianBlur(img, (5, 5), 0)
        if edge:
            img = cv2.Canny(img.astype(np.uint8), 50, 150)


        img_display = Image.fromarray(img.astype(np.uint8))
        st.image(img_display, caption=f"Slice {slice_idx + 1}/{len(images)}", use_column_width=True)

    except Exception as e:
        st.error(f"⚠️ Error reading DICOM files: {e}")
else:
    st.info("👈 Upload multiple DICOM (.dcm) files using the sidebar to begin.")

