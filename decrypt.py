import cv2
import numpy as np
from Crypto.Cipher import AES
from utils import load_key, unpad

# Load AES key
key = load_key()

# Read Encrypted Data
with open("images/encrypted.bin", "rb") as file:
    encrypted_data = file.read()

# Decrypt using AES in ECB mode
cipher = AES.new(key, AES.MODE_ECB)
decrypted_data = cipher.decrypt(encrypted_data)

# Unpad the data
unpadded_data = unpad(decrypted_data)

# Convert bytes back to image
original_image = cv2.imread("images/input.jpg", cv2.IMREAD_UNCHANGED)
image_shape = original_image.shape  # Get original shape

image = np.frombuffer(unpadded_data, dtype=np.uint8).reshape(image_shape)

# Save decrypted image
cv2.imwrite("images/decrypted.jpg", image)

print("[✔] Image decrypted successfully and saved as 'images/decrypted.jpg'.")
