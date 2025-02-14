import cv2
import numpy as np
import matplotlib.pyplot as plt

def save_histogram(image, title, filename, color_mode="gray"):
    """Compute and save the histogram of an image."""
    plt.figure(figsize=(8, 5))
    if color_mode == "gray":
        hist = cv2.calcHist([image], [0], None, [256], [0, 256])
        plt.plot(hist, color='black')
    else:
        colors = ('b', 'g', 'r')
        for i, color in enumerate(colors):
            hist = cv2.calcHist([image], [i], None, [256], [0, 256])
            plt.plot(hist, color=color)
    
    plt.title(title)
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")
    plt.xlim([0, 256])
    plt.grid()
    
    # Save histogram as an image instead of displaying it
    plt.savefig(filename)
    plt.close()

# Load Original Image
original_image = cv2.imread("images/input.jpg", cv2.IMREAD_UNCHANGED)
if original_image is None:
    print("Error: Original image not found.")
else:
    if len(original_image.shape) == 2:
        save_histogram(original_image, "Original Image Histogram", "histograminput.jpg", color_mode="gray")
    else:
        save_histogram(original_image, "Original Image Histogram", "histograminput.jpg", color_mode="color")

# Load Encrypted Image Data
with open("images/encrypted.bin", "rb") as f:
    encrypted_bytes = np.frombuffer(f.read(), dtype=np.uint8)

# Save Histogram of Encrypted Data Directly
save_histogram(encrypted_bytes, "Encrypted Image Histogram", "histogramencrypted.png", color_mode="gray")

print("[✔] Histogram analysis completed. Saved as 'histograminput.jpg' and 'histogramencrypted.png'.")
