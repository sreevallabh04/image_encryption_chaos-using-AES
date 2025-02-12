import cv2
import numpy as np
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from utils import unpad

# Load RSA Private Key
with open("rsa_keys/private.pem", "rb") as f:
    private_key = RSA.import_key(f.read())

# Load Encrypted AES Key
with open("key.bin", "rb") as key_file:
    encrypted_aes_key = key_file.read()

# Decrypt AES Key using RSA
rsa_cipher = PKCS1_OAEP.new(private_key)
aes_key = rsa_cipher.decrypt(encrypted_aes_key)

print("[✔] AES Key Decrypted Successfully.")

# Read Encrypted Data
with open("images/encrypted.bin", "rb") as file:
    encrypted_data = file.read()

# Decrypt using AES in ECB mode
cipher = AES.new(aes_key, AES.MODE_ECB)
decrypted_data = cipher.decrypt(encrypted_data)

# Unpad the data
unpadded_data = unpad(decrypted_data)

# Convert bytes back to image
original_image = cv2.imread("images/input.jpg", cv2.IMREAD_UNCHANGED)
image_shape = original_image.shape  # Get original shape

image = np.frombuffer(unpadded_data, dtype=np.uint8).reshape(image_shape)

# Save decrypted image
cv2.imwrite("images/decrypted.jpg", image)

print("[✔] Image Decrypted Successfully & Saved as 'images/decrypted.jpg'.")
