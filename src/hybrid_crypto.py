from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import os

# Key file location
KEY_FILE = "src/aes_key.bin"
KEY_SIZE = 16  # 128 bits - more reliable across implementations
IV_SIZE = 12   # GCM nonce size

def generate_or_load_key():
    """Generate a new key or load existing key"""
    if os.path.exists(KEY_FILE):
        # Load existing key
        with open(KEY_FILE, "rb") as f:
            key = f.read()
        
        # Check if key has correct length, regenerate if not
        if len(key) != KEY_SIZE:
            print(f"[!] Existing key has incorrect length ({len(key)} bytes). Regenerating...")
            key = get_random_bytes(KEY_SIZE)
            with open(KEY_FILE, "wb") as f:
                f.write(key)
    else:
        # Generate new random key
        key = get_random_bytes(KEY_SIZE)
        # Save key to file
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    
    return key

def encrypt_dna(dna_sequence):
    """Encrypt DNA sequence using AES-GCM mode"""
    # Get key
    key = generate_or_load_key()
    
    # Convert to bytes if string
    if isinstance(dna_sequence, str):
        plaintext = dna_sequence.encode('utf-8')
    else:
        # Handle numpy array or other sequence
        plaintext = ''.join(str(x) for x in dna_sequence).encode('utf-8')
    
    # Generate random nonce
    nonce = get_random_bytes(IV_SIZE)
    
    # Create cipher
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    
    # Encrypt data
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    
    # Format: nonce + tag + ciphertext
    encrypted_data = nonce + tag + ciphertext
    
    # Convert to base64 string for storage
    return base64.b64encode(encrypted_data).decode('utf-8')

def decrypt_dna(encrypted_data):
    """Decrypt DNA sequence using AES-GCM mode"""
    # Get key
    key = generate_or_load_key()
    
    # If input is string (most likely scenario)
    if isinstance(encrypted_data, str):
        encoded_data = encrypted_data
    else:
        # Handle numpy array or other object
        encoded_data = str(encrypted_data.item()) if hasattr(encrypted_data, 'item') else str(encrypted_data)
    
    # Decode base64
    data = base64.b64decode(encoded_data)
    
    # Extract components
    nonce = data[:IV_SIZE]  
    tag = data[IV_SIZE:IV_SIZE+16]  # GCM tag is 16 bytes
    ciphertext = data[IV_SIZE+16:]
    
    # Create cipher
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    
    # Decrypt and verify
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    
    # Return as string
    return plaintext.decode('utf-8')

# If module is run directly, generate a new key
if __name__ == "__main__":
    key = generate_or_load_key()
    print(f"[✔] AES key generated and saved to {KEY_FILE}")
    print(f"[ℹ] Key length: {len(key) * 8} bits")