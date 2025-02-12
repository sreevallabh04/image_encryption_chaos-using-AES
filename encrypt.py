import cv2
import numpy as np
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from chaos import generate_chaotic_key
from utils import pad

# Generate Chaotic AES Key
aes_key = generate_chaotic_key()

# Load RSA Public Key
with open("rsa_keys/public.pem", "rb") as f:
    public_key = RSA.import_key(f.read())

# Encrypt AES key using RSA
rsa_cipher = PKCS1_OAEP.new(public_key)
encrypted_aes_key = rsa_cipher.encrypt(aes_key)

# Save encrypted AES key
with open("key.bin", "wb") as key_file:
    key_file.write(encrypted_aes_key)

print("[✔] AES Key Encrypted & Saved as 'key.bin'")

# Load Image
image = cv2.imread("images/input.jpg", cv2.IMREAD_UNCHANGED)

# Convert image to bytes
image_bytes = image.tobytes()

# Pad the data
padded_data = pad(image_bytes)

# Encrypt using AES in ECB mode
cipher = AES.new(aes_key, AES.MODE_ECB)
encrypted_data = cipher.encrypt(padded_data)

# Save encrypted data
with open("images/encrypted.bin", "wb") as file:
    file.write(encrypted_data)

print("[✔] Image Encrypted Successfully & Saved as 'images/encrypted.bin'.")
