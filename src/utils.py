import cv2
import numpy as np

# Load image as RGB
def load_image(path):
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Image at {path} not found.")
    return cv2.resize(image, (256, 256))  # Resize to ensure consistency

# Save image
def save_image(path, image):
    cv2.imwrite(path, image)

# Save encrypted data
def save_file(path, data):
    with open(path, "w") as f:
        f.write(data)

# Load encrypted data
def load_file(path):
    with open(path, "r") as f:
        return f.read()
