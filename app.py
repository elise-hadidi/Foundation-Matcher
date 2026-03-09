import streamlit as st
from PIL import Image
import numpy as np
import cv2

st.set_page_config(page_title="🌸 Foundation Shade Matcher 🌸", layout="centered")

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --rose:  #F4A7B9;
    --blush: #FAD4DF;
    --cream: #FFF5F8;
    --petal: #FDEEF3;
    --plum:  #8B3A62;
    --mauve: #C2678D;
    --text:  #4A1942;
    --muted: #A07090;
}

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color: var(--text); }

.stApp {
    background: linear-gradient(135deg, #FFF0F5 0%, #FCE4EC 40%, #F8BBD9 100%);
    min-height: 100vh;
}

#MainMenu, footer, header { visibility: hidden; }

.hero { text-align: center; padding: 2.5rem 1rem 1.2rem; }
.hero::before {
    content: "✿ ✾ ✿";
    display: block;
    font-size: 1rem;
    color: var(--rose);
    letter-spacing: 0.8rem;
    margin-bottom: 0.6rem;
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    font-weight: 700;
    color: var(--plum);
    margin: 0;
    line-height: 1.2;
    text-shadow: 0 2px 12px rgba(139,58,98,0.12);
}
.hero h1 span { color: var(--mauve); font-style: italic; }
.hero p { font-size: 0.98rem; color: var(--muted); margin-top: 0.4rem; font-weight: 300; }

.petal-divider {
    text-align: center; color: var(--rose); font-size: 1rem;
    letter-spacing: 0.6rem; margin: 1.1rem 0; opacity: 0.7;
}

.section-label {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem; color: var(--plum); margin: 1.4rem 0 0.4rem;
}

.pill {
    display: inline-block;
    background: linear-gradient(90deg, var(--rose), var(--blush));
    color: var(--plum); border-radius: 99px; padding: 0.25rem 1rem;
    font-size: 0.8rem; font-weight: 500; letter-spacing: 0.04em;
    box-shadow: 0 2px 8px rgba(194,103,141,0.18);
}

.match-card {
    background: linear-gradient(135deg, #fff0f5, #fce4ec);
    border: 2px solid var(--rose); border-radius: 20px; padding: 1.4rem 1.2rem;
    text-align: center; box-shadow: 0 8px 32px rgba(194,103,141,0.18);
    position: relative; overflow: hidden;
}
.match-card::after {
    content: "♡"; position: absolute; top: -8px; right: 14px;
    font-size: 3.5rem; color: rgba(244,167,185,0.22);
}
.match-card h2 { font-family: 'Playfair Display', serif; font-size: 1.8rem; color: var(--plum); margin: 0.2rem 0 0; }
.match-card .sub { color: var(--muted); font-size: 0.84rem; margin-top: 0.2rem; }

.runner-label {
    font-size: 0.76rem; font-weight: 500; color: var(--mauve);
    text-transform: uppercase; letter-spacing: 0.08em; text-align: center; margin-top: 0.3rem;
}

.tone-box {
    background: rgba(255,255,255,0.6); border-radius: 14px;
    padding: 0.9rem 1.1rem; border: 1px solid var(--blush);
}
.tone-box .lbl { font-size: 0.82rem; color: var(--muted); }
.tone-box .val { font-family: 'Playfair Display', serif; font-size: 1rem; color: var(--plum); font-weight: 600; }

[data-testid="stFileUploader"] > div {
    background: rgba(255,255,255,0.55) !important;
    border: 1.5px dashed var(--rose) !important;
    border-radius: 16px !important;
}
[data-testid="stImage"] img { border-radius: 16px; box-shadow: 0 4px 20px rgba(139,58,98,0.14); }
.stAlert { background: rgba(255,255,255,0.6) !important; border-color: var(--rose) !important; border-radius: 14px !important; color: var(--plum) !important; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🌸 Foundation <span>Shade</span> Matcher 🌸</h1>
    <p>Upload a selfie and find your perfect shade!</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="petal-divider">✿ ✾ ✿</div>', unsafe_allow_html=True)

# ── Upload ────────────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader("Drop your selfie below!", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

    # ── Fix EXIF orientation (handles all rotation/mirror cases) ────────────
    from PIL import ImageOps
    try:
        image = ImageOps.exif_transpose(image)
    except Exception:
        pass
    image_np = np.array(image)
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    st.markdown('<div class="petal-divider">· · ·</div>', unsafe_allow_html=True)

    # ── Face detection ────────────────────────────────────────────────────────
    with st.spinner("Finding your face... 🌸"):
        gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        face_cascade = cv2.CascadeClassifier(cascade_path)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80))
        if len(faces) == 0:
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3, minSize=(50, 50))

    if len(faces) == 0:
        # Still show the (orientation-fixed) selfie even if no face found
        col_img, _ = st.columns([2, 1])
        with col_img:
            st.image(image, caption="Your selfie:", width=400)
        st.warning("😕 Couldn't detect a face — make sure your face is clearly visible and well-lit!")
    else:
        faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
        x, y, w, h = faces[0]

        x1 = x + int(w * 0.20)
        x2 = x + int(w * 0.80)
        y1 = y + int(h * 0.25)
        y2 = y + int(h * 0.80)
        face_roi = image_np[y1:y2, x1:x2]

        # Draw an ellipse outline directly on the selfie to show the detected zone
        preview = image_np.copy()
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        axes = ((x2 - x1) // 2, (y2 - y1) // 2)
        cv2.ellipse(preview, (cx, cy), axes, 0, 0, 360, (244, 167, 185), 4)
        col_img, _ = st.columns([2, 1])
        with col_img:
            st.image(preview, caption="Sampling from inside the oval 🌸", width=400)

        # ── Skin-tone filtering within face ROI ───────────────────────────────
        r = face_roi[:,:,0].astype(int)
        g = face_roi[:,:,1].astype(int)
        b = face_roi[:,:,2].astype(int)
        skin_mask = (
            (r > 70) & (r < 250) &
            (g > 30) & (g < 220) &
            (b > 15) & (b < 210) &
            (r > b) &              # red must beat blue
            (r - b > 8) &          # meaningful red-blue gap
            (r - g < 130) &        # not overly saturated red (excludes jacket)
            ~((r < 80) & (g < 60) & (b < 60))  # exclude very dark pixels (hair/brows)
        )
        skin_pixels = face_roi[skin_mask]

        if len(skin_pixels) < 50:
            st.warning("💔 Face found but couldn't sample enough skin — try better lighting!")
        else:
            with st.spinner("Analysing your skin tone... 🌸"):
                def dominant_skin_color(pixels, n_clusters=3, max_pixels=1500):
                    rng = np.random.default_rng(42)
                    if len(pixels) > max_pixels:
                        pixels = pixels[rng.choice(len(pixels), max_pixels, replace=False)]
                    pixels = pixels.astype(float)
                    centers = pixels[rng.choice(len(pixels), n_clusters, replace=False)].copy()
                    labels = np.zeros(len(pixels), dtype=int)
                    for _ in range(10):
                        dists = np.stack([np.linalg.norm(pixels - c, axis=1) for c in centers], axis=1)
                        labels = np.argmin(dists, axis=1)
                        for k in range(n_clusters):
                            mask = labels == k
                            if mask.sum() > 0:
                                centers[k] = pixels[mask].mean(axis=0)
                    counts = np.bincount(labels, minlength=n_clusters)
                    return centers[np.argmax(counts)].astype(int)

                dc = dominant_skin_color(skin_pixels)

            # ── Detected swatch ───────────────────────────────────────────────
            st.markdown('<p class="section-label">🌸 Your Skin Tone 🌸:</p>', unsafe_allow_html=True)
            swatch_detected = np.zeros((70, 220, 3), dtype=np.uint8)
            swatch_detected[:] = dc
            col_sw, col_info = st.columns([1, 2])
            with col_sw:
                st.image(swatch_detected, width=220)
            with col_info:
                st.markdown(f"""
                <div class="tone-box">
                    <div class="lbl">Detected RGB value</div>
                    <div class="val">({dc[0]}, {dc[1]}, {dc[2]})</div>
    
                </div>
                """, unsafe_allow_html=True)

            # ── Foundation DB ─────────────────────────────────────────────────
            foundation_db = {
                "Fenty 110N": [240, 205, 175], "Fenty 120W": [230, 190, 160],
                "Fenty 140W": [215, 175, 145], "Fenty 185N": [205, 165, 135],
                "Fenty 220N": [200, 160, 130], "Fenty 240W": [185, 148, 118],
                "Fenty 300W": [170, 128, 100], "Fenty 330N": [155, 112,  85],
                "Fenty 360N": [140,  98,  74], "Fenty 390W": [128,  88,  65],
                "Fenty 420N": [120,  80,  60], "Fenty 445W": [100,  65,  48],
                "Fenty 480N": [ 80,  50,  35],
            }

            results = sorted(
                [(s, c, np.linalg.norm(np.array(dc, float) - np.array(c, float)))
                 for s, c in foundation_db.items()],
                key=lambda x: x[2]
            )
            best_shade, best_color, _ = results[0]

            # ── Best match ────────────────────────────────────────────────────
            st.markdown('<div class="petal-divider">✾ ✾ ✾</div>', unsafe_allow_html=True)
            st.markdown('<p class="section-label">🌸 Your Perfect Match 🌸:</p>', unsafe_allow_html=True)

            best_swatch = np.zeros((90, 320, 3), dtype=np.uint8)
            best_swatch[:] = best_color
            col_bs, col_binfo = st.columns([1, 2])
            with col_bs:
                st.image(best_swatch, width=200)
            with col_binfo:
                st.markdown(f"""
                <div class="match-card">
                    <div class="sub">Top recommendation</div>
                    <h2>{best_shade}</h2>
                    <div class="sub">RGB ({best_color[0]}, {best_color[1]}, {best_color[2]})</div>
                </div>
                """, unsafe_allow_html=True)

            # ── Runner-ups ────────────────────────────────────────────────────
            st.markdown('<div class="petal-divider">· · ·</div>', unsafe_allow_html=True)
            st.markdown('<p class="section-label">🌸 Also Close 🌸:</p>', unsafe_allow_html=True)
            cols = st.columns(3)
            for i, (shade, color, _) in enumerate(results[1:4]):
                with cols[i]:
                    s = np.zeros((65, 160, 3), dtype=np.uint8)
                    s[:] = color
                    st.image(s, width=120)
                    st.markdown(f'<div class="runner-label">{shade}</div>', unsafe_allow_html=True)

            st.markdown('<div class="petal-divider">✿ ✾ ✿</div>', unsafe_allow_html=True)
            st.markdown(
                '<p style="text-align:center;color:#A07090;font-size:0.78rem;">'
                'Enjoy your new foundation!!</p>',
                unsafe_allow_html=True
            )