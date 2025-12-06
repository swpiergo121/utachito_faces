#!/usr/bin/env python3


import cv2

# Load your images
image1_path = "images/triste.png"
image2_path = "images/feliz.png"
image3_path = "images/molesto.png"

# Store images in a list
images = [image1_path, image2_path, image3_path]
index = 0  # Start with the first image


# Define fixed display size
DISPLAY_WIDTH = 1080
DISPLAY_HEIGHT = 1080

cv2.namedWindow("Image Viewer", cv2.WINDOW_AUTOSIZE)


def resize_image(img):
    return cv2.resize(img, (DISPLAY_WIDTH, DISPLAY_HEIGHT))


while True:
    # Display current image
    img = resize_image(cv2.imread(images[index]))
    cv2.imshow("Image Viewer", img)

    # Wait for key press (adjust delay as needed, e.g., 30 ms)
    key = cv2.waitKey(30) & 0xFF

    if key == 27:  # ESC key to exit
        break
    elif key == ord("a") or key == 81:  # Left arrow key (may vary by system)
        index = (index - 1) % len(images)  # Previous image (circular)
    elif key == ord("d") or key == 83:  # Right arrow key (may vary by system)
        index = (index + 1) % len(images)  # Next image (circular)

cv2.destroyAllWindows()
