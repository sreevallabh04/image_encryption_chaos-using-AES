from Crypto.Cipher import AES

# Pad the data to be a multiple of AES block size (16 bytes)
def pad(data):
    padding_length = 16 - (len(data) % 16)
    return data + bytes([padding_length]) * padding_length

# Remove padding after decryption
def unpad(data):
    return data[:-data[-1]]
