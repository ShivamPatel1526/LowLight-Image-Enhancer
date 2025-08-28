# 📸 Low-Light Image Enhancer

A simple web app to enhance dark or low-light images using **CLAHE (Contrast Limited Adaptive Histogram Equalization)**, **Gamma Correction**, and **Color Boosting**.  

Built with **Python**, **OpenCV**, **PIL**, and **Streamlit**.

---

## Features

- Enhances low-light images for better visibility.
- Boosts colors and saturation to restore natural tones.
- Side-by-side comparison of the original and enhanced image.
- Download the enhanced image in JPEG format.
- Simple and user-friendly interface.

---

## Demo

![demo](demo_image_placeholder.png)  
*Upload a dark image and see the enhancement side by side.*

---

## How It Works

1. Upload a low-light image.
2. The app applies:
   - CLAHE to the L-channel of the LAB color space to enhance brightness.
   - Gamma correction to improve contrast.
   - Saturation boost in HSV space to restore colors.
3. A comparison of the original and enhanced image is displayed.
4. Download the enhanced image with a single click.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/low-light-image-enhancer.git
cd low-light-image-enhancer
