import streamlit as st
import numpy as np
import cv2
from PIL import Image
import io

def resize_to_same_height(img1, img2):
    h1 = img1.shape[0]
    h2 = img2.shape[0]
    if h1 != h2:
        scale = h1 / h2
        new_w = int(img2.shape[1] * scale)
        img2 = cv2.resize(img2, (new_w, h1), interpolation=cv2.INTER_AREA)
    return img1, img2

def draw_label(img, label_text, x, y, font=cv2.FONT_HERSHEY_DUPLEX, font_scale=1.2, font_thickness=2):
    text_size, _ = cv2.getTextSize(label_text, font, font_scale, font_thickness)
    text_width, text_height = text_size
    padding = 10
    box_coords = ((x, y - text_height - padding), (x + text_width + padding * 2, y))
    cv2.rectangle(img, box_coords[0], box_coords[1], (0, 0, 0), thickness=-1)
    cv2.putText(img, label_text, (x + padding, y - padding // 2),
                font, font_scale, (255, 255, 255), font_thickness)

def add_labels_with_boxes(img_left, img_right, label_left="Input Image", label_right="Enhanced Image"):
    label_space = 60
    h, w_left = img_left.shape[:2]
    w_right = img_right.shape[1]

    canvas = np.zeros((h + label_space, w_left + w_right, 3), dtype=np.uint8)
    canvas[label_space:, :w_left] = img_left
    canvas[label_space:, w_left:] = img_right

    left_x = (w_left - cv2.getTextSize(label_left, cv2.FONT_HERSHEY_DUPLEX, 1.2, 2)[0][0]) // 2
    draw_label(canvas, label_left, x=left_x, y=40)

    right_x = w_left + (w_right - cv2.getTextSize(label_right, cv2.FONT_HERSHEY_DUPLEX, 1.2, 2)[0][0]) // 2
    draw_label(canvas, label_right, x=right_x, y=40)

    return canvas

# ---------------- Enhancement Functions ----------------
def histogram_equalization_color(img_rgb):
    """Enhance low-light images using CLAHE + Gamma + Color Boost"""
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)

    # Split LAB channels
    l, a, b = cv2.split(lab)

    # Apply CLAHE to L-channel
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)

    # Merge back
    merged_lab = cv2.merge((cl, a, b))
    enhanced_bgr = cv2.cvtColor(merged_lab, cv2.COLOR_LAB2BGR)
    enhanced_rgb = cv2.cvtColor(enhanced_bgr, cv2.COLOR_BGR2RGB)

    # Apply gamma correction
    enhanced_rgb = adjust_gamma(enhanced_rgb, gamma=1.2)

    # ✅ Boost saturation in HSV to restore colors
    hsv = cv2.cvtColor(enhanced_rgb, cv2.COLOR_RGB2HSV).astype("float32")
    hsv[:, :, 1] *= 1.25   # increase saturation by 25%
    hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)

    enhanced_rgb = cv2.cvtColor(hsv.astype("uint8"), cv2.COLOR_HSV2RGB)

    return enhanced_rgb

def adjust_gamma(image, gamma=1.2):
    """Simple gamma correction"""
    invGamma = 1.0 / gamma
    table = np.array([(i / 255.0) ** invGamma * 255
                        for i in np.arange(256)]).astype("uint8")
    return cv2.LUT(image, table)

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Low-Light Image Enhancer", layout="centered")

st.title("📸 Low-Light Image Enhancement")
st.write("Upload a dark image → it will be enhanced using CLAHE + Gamma + Color Boost.")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    input_img = np.array(Image.open(uploaded_file).convert("RGB"))

    enhanced_img = histogram_equalization_color(input_img)

    # Create side-by-side comparison with labels
    img1, img2 = resize_to_same_height(input_img, enhanced_img)
    comparison = add_labels_with_boxes(img1, img2)

    st.subheader("Comparison")
    st.image(comparison, use_column_width=True)

    # Download enhanced version
    pil_enhanced = Image.fromarray(enhanced_img)
    buf = io.BytesIO()
    pil_enhanced.save(buf, format="JPEG")
    byte_im = buf.getvalue()

    st.download_button(
        label="📥 Download Enhanced Image",
        data=byte_im,
        file_name="enhanced.jpg",
        mime="image/jpeg"
    )
else:
    st.info("Upload an image to begin. Try a dark photo from your phone.")