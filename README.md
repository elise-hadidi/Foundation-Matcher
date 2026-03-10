# AI Foundation Shade Matcher

Live Demo: https://foundation-matchee-26qwxhdldgdxbpniawgmcg.streamlit.app/

A computer vision web app that analyses your selfie and recommends your closest **Fenty Beauty foundation shade** — built with Python, OpenCV, and Streamlit.

<img width="1235" height="690" alt="Screenshot 2026-03-09 at 3 16 48 PM" src="https://github.com/user-attachments/assets/e5d2e93f-8297-4ea5-a894-2ee106c10af5" />


---

## How It Works

1. **Upload a selfie** — drop any JPG or PNG photo
2. **Face detection** — OpenCV's Haar cascade locates your face and draws a sampling oval over the cheek/forehead region, excluding hair and background
3. **Skin tone extraction** — a lightweight k-means clustering algorithm (pure NumPy, no sklearn) finds the dominant skin colour within the detected face region
4. **Shade matching** — your skin tone RGB is compared against 13 Fenty Beauty Pro Filt'r shades using Euclidean distance in RGB space, returning your closest match plus three runner-ups

---

## App Screenshots

### Landing page
<img width="1235" height="690" alt="Screenshot 2026-03-09 at 3 16 48 PM" src="https://github.com/user-attachments/assets/bcaa90ea-fbcf-4945-a45f-d192b1f4370a" />


### Upload & face detection
<img width="1230" height="690" alt="Screenshot 2026-03-09 at 3 16 24 PM" src="https://github.com/user-attachments/assets/abe8a083-9e36-470d-9ade-12d1e60fe808" />


### Shade results
<img width="1232" height="688" alt="Screenshot 2026-03-09 at 3 16 37 PM" src="https://github.com/user-attachments/assets/05b33491-c201-429a-a33d-5ac019a45f86" />


---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Web app framework |
| OpenCV | Face detection (Haar cascade) + image processing |
| Pillow | Image loading & EXIF orientation correction |
| NumPy | Skin pixel filtering & custom k-means clustering |

---

## Running Locally

```bash
# 1. Clone the repo
git clone https://github.com/elise-hadidi/foundation-shade-matcher.git
cd foundation-shade-matcher

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Features

- **Automatic EXIF orientation correction** — selfies from iPhone/Android display right-side up
- **Face-region-only sampling** — avoids hair, background, and clothing by sampling only within the detected face oval
- **Works across skin tones** — skin filter tuned to capture a wide range of undertones (warm, olive, neutral, deep)
- **13-shade Fenty database** — covers shades 110N through 480N
- **Top 4 results** — shows your best match plus 3 runner-up swatches with RGB values
- **Custom pink UI** — built with Playfair Display + DM Sans, blush gradient background, and glassmorphism cards

---

## Project Structure

```
Foundation-Matcher/
├── app.py              # Main Streamlit app
├── requirements.txt    # Python dependencies
└── README.md
```
