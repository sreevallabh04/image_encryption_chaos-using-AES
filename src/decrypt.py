import cv2
import numpy as np
import os
import argparse
from dna_crypto import dna_to_image
from hybrid_crypto import decrypt_dna, generate_or_load_key
from chaos import unscramble_pixels
from steganography import extract_encrypted_data

def decrypt_image(encrypted_path=None, shape_path=None, output_path=None, stego_image=None):
    """
    Decrypt an image using the enhanced DNA-Chaos-AES hybrid cryptosystem
    
    Args:
        encrypted_path: Path to the encrypted data file
        shape_path: Path to the file containing original image shape
        output_path: Path to save the decrypted image
        stego_image: Path to steganographic image (if using steganography)
    
    Returns:
        Path to the decrypted image
    """
    if output_path is None:
        output_path = "images/decrypted.png"
    
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract data from steganographic image if provided
    if stego_image is not None:
        print(f"[1/6] Extracting hidden data from {stego_image}...")
        extracted_path = "images/extracted_encrypted.npy"
        extract_encrypted_data(stego_image, output_path=extracted_path)
        encrypted_path = extracted_path
    
    # Load encrypted data
    print(f"[2/6] Loading encrypted data from {encrypted_path}...")
    encrypted_data = np.load(encrypted_path, allow_pickle=True)
    
    # Load original shape
    if shape_path is None:
        shape_path = "images/original_shape.npy"
    print(f"[3/6] Loading original shape from {shape_path}...")
    original_shape = np.load(shape_path, allow_pickle=True)
    
    # REORDERED: First decrypt the AES-GCM encrypted data
    print("[4/6] Decrypting DNA sequence using AES-GCM...")
    decrypted_dna = decrypt_dna(encrypted_data)
    
    # Then unscramble the decrypted data
    print("[5/6] Applying chaotic unscrambling...")
    unscrambled_dna = unscramble_pixels(decrypted_dna)
    
    # Convert DNA back to image
    print("[6/6] Converting DNA back to image...")
    decrypted_image = dna_to_image(unscrambled_dna, original_shape)
    
    # Save decrypted image
    cv2.imwrite(output_path, decrypted_image)
    
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enhanced DNA-Chaos-AES Image Decryption")
    parser.add_argument("--encrypted", default="images/encrypted.npy", help="Path to encrypted data file")
    parser.add_argument("--shape", default="images/original_shape.npy", help="Path to original shape file")
    parser.add_argument("--output", default="images/decrypted.png", help="Path to save decrypted image")
    parser.add_argument("--stego", help="Path to steganographic image (if using steganography)")
    
    args = parser.parse_args()
    
    try:
        # Ensure AES key is loaded
        generate_or_load_key()
        
        # Decrypt the image
        output_path = decrypt_image(
            encrypted_path=args.encrypted,
            shape_path=args.shape,
            output_path=args.output,
            stego_image=args.stego
        )
        
        print(f"[✔] Image Decrypted Successfully & Stored in '{output_path}'")
    
    except Exception as e:
        print(f"[✘] Decryption failed: {str(e)}")