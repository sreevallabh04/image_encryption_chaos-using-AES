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
encrypted_data = np.load("images/encrypted.npy", allow_pickle=True)

# Convert to a form suitable for histogram analysis
# Check if encrypted data is a scalar or 0-dimensional array
if encrypted_data.ndim == 0:
    # If scalar, convert the string to a list of ASCII values
    encrypted_str = str(encrypted_data.item())
    encrypted_bytes = np.array([ord(c) for c in encrypted_str], dtype=np.uint8)
elif isinstance(encrypted_data.item(0) if encrypted_data.size > 0 else None, (str, bytes, np.bytes_)):
    # If array of strings/bytes, convert each to ASCII values
    encrypted_bytes = np.array([ord(c) for c in ''.join(encrypted_data.tolist())], dtype=np.uint8)
else:
    # If already numerical, just flatten and ensure uint8 type
    encrypted_bytes = np.array(encrypted_data).flatten().astype(np.uint8)

# Save Histogram of Encrypted Data Directly
save_histogram(encrypted_bytes, "Encrypted Image Histogram", "histogramencrypted.png", color_mode="gray")

print("[✔] Histogram analysis completed. Saved as 'histograminput.jpg' and 'histogramencrypted.png'.")
