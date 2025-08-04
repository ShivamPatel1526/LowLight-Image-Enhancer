import cv2
import numpy as np
import os

def resize_to_same_height(img1, img2):
    h1 = img1.shape[0]
    h2 = img2.shape[0]
    if h1 != h2:
        scale = h1 / h2
        new_w = int(img2.shape[1] * scale)
        img2 = cv2.resize(img2, (new_w, h1), interpolation=cv2.INTER_AREA)
    return img1, img2

def resize_to_fit_screen(img, max_width=1000, max_height=700):
    h, w = img.shape[:2]
    if w > max_width or h > max_height:
        scale = min(max_width / w, max_height / h)
        img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
    return img

def draw_label(img, label_text, x, y, font=cv2.FONT_HERSHEY_DUPLEX, font_scale=1.8, font_thickness=3):
    text_size, _ = cv2.getTextSize(label_text, font, font_scale, font_thickness)
    text_width, text_height = text_size
    padding = 10

    box_coords = (
        (x, y - text_height - padding),
        (x + text_width + padding * 2, y)
    )
    cv2.rectangle(img, box_coords[0], box_coords[1], (0, 0, 0), thickness=-1)

    cv2.putText(img, label_text, (x + padding, y - padding // 2), font, font_scale, (255, 255, 255), font_thickness)

def add_labels_with_boxes(img_left, img_right, label_left="Input Image", label_right="Enhanced Image"):
    label_space = 100
    h, w_left = img_left.shape[:2]
    w_right = img_right.shape[1]

    canvas = np.zeros((h + label_space, w_left + w_right, 3), dtype=np.uint8)
    canvas[label_space:, :w_left] = img_left
    canvas[label_space:, w_left:] = img_right

    left_x = (w_left - cv2.getTextSize(label_left, cv2.FONT_HERSHEY_DUPLEX, 1.8, 3)[0][0]) // 2
    draw_label(canvas, label_left, x=left_x, y=70)

    right_x = w_left + (w_right - cv2.getTextSize(label_right, cv2.FONT_HERSHEY_DUPLEX, 1.8, 3)[0][0]) // 2
    draw_label(canvas, label_right, x=right_x, y=70)

    return canvas

def histogram_equalization_color(img_path):
    img = cv2.imread(img_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv[:, :, 2] = cv2.equalizeHist(hsv[:, :, 2])
    enhanced_img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    output_dir = "C:\\Users\\90shi\\Downloads\\Output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "enhanced_colored.jpg")
    cv2.imwrite(output_path, enhanced_img)

    img, enhanced_img = resize_to_same_height(img, enhanced_img)
    labeled_combined = add_labels_with_boxes(img, enhanced_img)
    resized_display = resize_to_fit_screen(labeled_combined)

    cv2.imshow("Comparison", resized_display)
    print(f"Enhanced image saved at: {output_path}")
    return enhanced_img

image_path = "C:\\Users\\90shi\\Downloads\\IMG20241206161626.jpg"
histogram_equalization_color(image_path)

cv2.waitKey(0)
cv2.destroyAllWindows()