from Crypto.Cipher import AES
import os

# Pad the data to be a multiple of AES block size (16 bytes)
def pad(data):
    padding_length = 16 - (len(data) % 16)
    return data + bytes([padding_length]) * padding_length

# Remove padding after decryption
def unpad(data):
    return data[:-data[-1]]

# Save key to a file
def save_key(key, filename="key.bin"):
    with open(filename, "wb") as f:
        f.write(key)

# Load key from file
def load_key(filename="key.bin"):
    with open(filename, "rb") as f:
        return f.read()
