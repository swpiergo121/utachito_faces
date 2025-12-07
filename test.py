#!/usr/bin/env python3

from PIL import Image
import cv2
import numpy as np

# Image paths
image1_path = "images/triste.png"
image2_path = "images/feliz.png"
image3_path = "images/molesto.png"


# Load and convert images to RGB to ensure consistent mode
def load_image(path):
    img = Image.open(path)
    if img.mode != "RGB":
        img = img.convert("RGB")  # Eliminate palette (P), grayscale (L), or RGBA issues
    return img


pil_images = [load_image(image1_path), load_image(image2_path), load_image(image3_path)]

# Define fixed display size
DISPLAY_SIZE = (1080, 1080)

# Resize all images to the same size
resized_images = [
    img.resize(DISPLAY_SIZE, Image.Resampling.LANCZOS) for img in pil_images
]
index = 0

# Setup OpenCV windows
cv2.namedWindow("Image Viewer", cv2.WINDOW_AUTOSIZE)
cv2.namedWindow("Blending Animation", cv2.WINDOW_AUTOSIZE)


def pil_to_cv2(pil_img):
    """Convert PIL RGB image to OpenCV BGR format"""
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)


while True:
    # Show current image
    cv2.imshow("Image Viewer", pil_to_cv2(resized_images[index]))

    key = cv2.waitKey(30) & 0xFF
    if key == 27:  # ESC to exit
        break

    new_index = -1
    if key == ord("a") or key == 81:  # Left arrow
        new_index = (index - 1) % len(resized_images)
    elif key == ord("d") or key == 83:  # Right arrow
        new_index = (index + 1) % len(resized_images)

    if new_index == -1:
        continue  # No valid navigation key

    # Crossfade animation
    img1 = resized_images[index]
    img2 = resized_images[new_index]
    frames = []

    for alpha in np.linspace(0, 1, 12):  # 30-frame blend
        blended = Image.blend(img1, img2, alpha)
        frames.append(blended)

    # Play animation
    for frame in frames:
        cv2.imshow("Blending Animation", pil_to_cv2(frame))
        if cv2.waitKey(30) == 27:
            break

    index = new_index

cv2.destroyAllWindows()
