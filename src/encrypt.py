import cv2
import numpy as np
import os
import argparse
from dna_crypto import image_to_dna
from hybrid_crypto import encrypt_dna, generate_or_load_key
from chaos import scramble_pixels
from steganography import hide_encrypted_data

def encrypt_image(image_path, output_dir="images", use_steganography=False, cover_image=None):
    """
    Encrypt an image using the enhanced DNA-Chaos-AES hybrid cryptosystem
    
    Args:
        image_path: Path to the input image
        output_dir: Directory to save encrypted outputs
        use_steganography: Whether to hide the encrypted data in a cover image
        cover_image: Path to cover image for steganography (optional)
    
    Returns:
        Path to the encrypted data or steganographic image
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Load image
    print(f"[1/5] Loading image from {image_path}...")
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image from {image_path}")
    
    # Convert image to DNA sequence
    print("[2/5] Converting image to DNA sequence...")
    dna_sequence, original_shape = image_to_dna(image)
    
    # Apply chaotic scrambling before encryption
    print("[3/5] Applying chaotic scrambling...")
    scrambled_dna = scramble_pixels(dna_sequence)
    
    # Encrypt scrambled DNA sequence
    print("[4/5] Encrypting DNA sequence using AES-CBC...")
    encrypted_dna = encrypt_dna(scrambled_dna)
    
    # Save encrypted data and original shape
    encrypted_path = os.path.join(output_dir, "encrypted.npy")
    shape_path = os.path.join(output_dir, "original_shape.npy")
    
    np.save(encrypted_path, encrypted_dna)
    np.save(shape_path, original_shape)
    
    print(f"[✔] Encrypted data saved to {encrypted_path}")
    
    # Apply steganography if requested
    if use_steganography:
        print("[5/5] Hiding encrypted data using steganography...")
        stego_path = os.path.join(output_dir, "stego_image.png")
        hide_encrypted_data(encrypted_path, cover_image_path=cover_image, output_path=stego_path)
        return stego_path
    else:
        print("[5/5] Skipping steganography (not requested)")
        return encrypted_path

def setup_crypto_environment():
    """
    Set up the cryptographic environment by ensuring key is generated
    """
    try:
        # Generate/load AES key
        generate_or_load_key()
        print("[✔] Cryptographic environment initialized successfully")
    except Exception as e:
        print(f"[✘] Error setting up cryptographic environment: {str(e)}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enhanced DNA-Chaos-AES Image Encryption")
    parser.add_argument("--image", default="images/input.jpg", help="Path to input image")
    parser.add_argument("--output-dir", default="images", help="Directory to save encrypted outputs")
    parser.add_argument("--steganography", action="store_true", help="Hide encrypted data in a cover image")
    parser.add_argument("--cover", help="Path to cover image for steganography")
    
    args = parser.parse_args()
    
    try:
        # Setup cryptographic environment (generate keys/parameters if needed)
        setup_crypto_environment()
        
        # Encrypt the image
        output_path = encrypt_image(
            args.image,
            output_dir=args.output_dir,
            use_steganography=args.steganography,
            cover_image=args.cover
        )
        
        print(f"[✔] Image Encrypted Successfully!")
        if args.steganography:
            print(f"[ℹ] Encrypted data hidden in: {output_path}")
        else:
            print(f"[ℹ] Encrypted data saved to: {output_path}")
            print(f"[ℹ] To decrypt: python src/decrypt.py")
            print(f"[ℹ] To hide in another image: python src/steganography.py --mode hide --data {output_path}")
    
    except Exception as e:
        print(f"[✘] Encryption failed: {str(e)}")