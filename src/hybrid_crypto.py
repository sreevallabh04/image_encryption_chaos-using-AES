from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

SECRET_KEY = b"my_super_secret!"  # Must be 16 bytes

def encrypt_dna(dna_sequence):
    """ Encrypt DNA sequence using AES """
    cipher = AES.new(SECRET_KEY, AES.MODE_ECB)
    encrypted = cipher.encrypt(pad(dna_sequence.encode(), AES.block_size))
    return base64.b64encode(encrypted).decode()

def decrypt_dna(encrypted_dna):
    """ Decrypt DNA sequence using AES """
    cipher = AES.new(SECRET_KEY, AES.MODE_ECB)
    decrypted_padded = cipher.decrypt(base64.b64decode(encrypted_dna))
    return unpad(decrypted_padded, AES.block_size).decode()
