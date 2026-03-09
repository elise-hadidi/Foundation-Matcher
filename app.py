import streamlit as st
from PIL import Image
import numpy as np
import cv2
from sklearn.cluster import KMeans

st.set_page_config(page_title="AI Foundation Shade Matcher", layout="centered")
st.title("AI Foundation Shade Matcher 💄")
st.write("Upload a selfie and get your closest foundation match!")

# --- Step 1: Upload Image ---
uploaded_file = st.file_uploader("Upload a selfie", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Selfie", use_column_width=True)

    # Convert to OpenCV format
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    pixels = image_cv.reshape((-1,3))

    # --- Step 2: Skin Tone Detection ---
    kmeans = KMeans(n_clusters=3, random_state=42)
    kmeans.fit(pixels)
    dominant_color = kmeans.cluster_centers_[0].astype(int)
    
    st.write(f"Detected dominant color (RGB): {dominant_color}")

    # --- Step 3: Match to Foundation Shades ---
    foundation_db = {
        "Fenty 120": [230, 190, 160],
        "Fenty 240": [200, 160, 130],
        "Fenty 300": [170, 120, 95],
        "Fenty 420": [120, 80, 60]
    }

    def color_distance(c1, c2):
        return np.linalg.norm(np.array(c1) - np.array(c2))

    best_match = None
    smallest_distance = float("inf")

    for shade, color in foundation_db.items():
        dist = color_distance(dominant_color, color)
        if dist < smallest_distance:
            smallest_distance = dist
            best_match = shade

    # --- Step 4: Display Result ---
    st.subheader("Your Recommended Foundation Shade")
    st.write(f"**{best_match}**")

    # Show swatch
    swatch = np.zeros((100, 300, 3), dtype=np.uint8)
    swatch[:] = foundation_db[best_match]
    st.image(cv2.cvtColor(swatch, cv2.COLOR_BGR2RGB), caption=f"{best_match} Swatch", use_column_width=True)