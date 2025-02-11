import cv2
import numpy as np
from Crypto.Cipher import AES
from chaos import generate_chaotic_key
from utils import pad, save_key

# Generate Chaotic AES Key
key = generate_chaotic_key()
save_key(key)

# Load Image
image = cv2.imread("images/input.jpg", cv2.IMREAD_UNCHANGED)

# Convert image to bytes
image_bytes = image.tobytes()

# Pad the data
padded_data = pad(image_bytes)

# Encrypt using AES in ECB mode
cipher = AES.new(key, AES.MODE_ECB)
encrypted_data = cipher.encrypt(padded_data)

# Save encrypted data
with open("images/encrypted.bin", "wb") as file:
    file.write(encrypted_data)

print("[✔] Image encrypted successfully and saved as 'images/encrypted.bin'.")
