import cv2
import numpy as np
import base64
import os

def binary_to_bytes(binary_str):
    """Convert a binary string to bytes"""
    return bytes(int(binary_str[i:i+8], 2) for i in range(0, len(binary_str), 8))

def bytes_to_binary(data_bytes):
    """Convert bytes to a binary string"""
    binary = ""
    for byte in data_bytes:
        binary += format(byte, '08b')
    return binary

def encode_data_length(length, bit_length=32):
    """Encode data length as a binary string of fixed length"""
    return format(length, f'0{bit_length}b')

def decode_data_length(binary_str, bit_length=32):
    """Decode data length from a binary string"""
    return int(binary_str[:bit_length], 2)

def hide_data_in_image(cover_image_path, data, output_path=None):
    """Hide encrypted data in a cover image using LSB steganography
    
    Args:
        cover_image_path: Path to the cover image
        data: String data to hide (base64 encoded encrypted data)
        output_path: Path to save the steganographic image (default: stego_image.png)
    
    Returns:
        Path to the steganographic image
    """
    if output_path is None:
        output_path = "images/stego_image.png"
    
    # Load cover image
    cover_image = cv2.imread(cover_image_path)
    if cover_image is None:
        raise ValueError(f"Could not load cover image from {cover_image_path}")
    
    # Convert data to binary
    binary_data = bytes_to_binary(data.encode())
    
    # Add length header (32 bits / 4 bytes for data length)
    binary_data = encode_data_length(len(binary_data)) + binary_data
    data_length = len(binary_data)
    
    # Check if cover image has enough capacity
    height, width, channels = cover_image.shape
    image_capacity = height * width * channels
    
    if data_length > image_capacity:
        raise ValueError(f"Data too large for cover image. Need {data_length} bits, but image only has {image_capacity} bits capacity")
    
    # Flatten the image for easier processing
    cover_flat = cover_image.flatten()
    
    # Create stego image by embedding data
    stego_flat = cover_flat.copy()
    
    for i in range(data_length):
        # Replace LSB with data bit
        if binary_data[i] == '1':
            stego_flat[i] = stego_flat[i] | 1  # Set LSB to 1
        else:
            stego_flat[i] = stego_flat[i] & ~1  # Set LSB to 0
    
    # Reshape back to image dimensions
    stego_image = stego_flat.reshape(cover_image.shape)
    
    # Save steganographic image
    cv2.imwrite(output_path, stego_image)
    
    return output_path

def extract_data_from_image(stego_image_path):
    """Extract hidden data from a steganographic image
    
    Args:
        stego_image_path: Path to the steganographic image
    
    Returns:
        Extracted data as string
    """
    # Load steganographic image
    stego_image = cv2.imread(stego_image_path)
    if stego_image is None:
        raise ValueError(f"Could not load steganographic image from {stego_image_path}")
    
    # Flatten the image
    stego_flat = stego_image.flatten()
    
    # Extract LSB from each byte to get the binary data
    extracted_bits = ""
    for i in range(32):  # First extract the 32-bit length header
        extracted_bits += '1' if (stego_flat[i] & 1) > 0 else '0'
    
    # Decode data length
    data_length = decode_data_length(extracted_bits)
    
    # Extract the actual data bits
    for i in range(32, 32 + data_length):
        if i < len(stego_flat):
            extracted_bits += '1' if (stego_flat[i] & 1) > 0 else '0'
    
    # Discard length header
    extracted_bits = extracted_bits[32:32+data_length]
    
    # Convert binary to bytes, then to string
    extracted_data = ""
    try:
        extracted_bytes = binary_to_bytes(extracted_bits)
        extracted_data = extracted_bytes.decode()
    except Exception as e:
        print(f"Error decoding extracted data: {str(e)}")
    
    return extracted_data

def hide_encrypted_data(encrypted_data_path, cover_image_path=None, output_path=None):
    """Hide encrypted data file in a cover image
    
    Args:
        encrypted_data_path: Path to the encrypted data file (.npy)
        cover_image_path: Path to cover image (default: a random image from samples)
        output_path: Path to save steganographic image (default: images/stego_image.png)
    
    Returns:
        Path to the steganographic image
    """
    if output_path is None:
        output_path = "images/stego_image.png"
    
    if cover_image_path is None:
        # Default cover image
        cover_image_path = "images/cover.jpg"
        if not os.path.exists(cover_image_path):
            raise ValueError(f"No cover image specified and default cover image not found at {cover_image_path}")
    
    # Load encrypted data
    encrypted_data = np.load(encrypted_data_path, allow_pickle=True)
    
    # Convert to base64 string for hiding
    if isinstance(encrypted_data, np.ndarray):
        # Save array to a temporary binary file
        np.save("images/temp_data.npy", encrypted_data)
        with open("images/temp_data.npy", "rb") as f:
            data_bytes = f.read()
        os.remove("images/temp_data.npy")
    else:
        # Convert to string if not an array
        data_bytes = str(encrypted_data).encode()
    
    # Encode to base64
    base64_data = base64.b64encode(data_bytes).decode()
    
    # Hide in cover image
    stego_path = hide_data_in_image(cover_image_path, base64_data, output_path)
    
    print(f"[✔] Encrypted data hidden in {stego_path}")
    return stego_path

def extract_encrypted_data(stego_image_path, output_path=None):
    """Extract hidden encrypted data from a steganographic image
    
    Args:
        stego_image_path: Path to the steganographic image
        output_path: Path to save extracted data (default: images/extracted_encrypted.npy)
    
    Returns:
        Path to the extracted encrypted data
    """
    if output_path is None:
        output_path = "images/extracted_encrypted.npy"
    
    # Extract hidden data
    base64_data = extract_data_from_image(stego_image_path)
    
    # Decode base64
    data_bytes = base64.b64decode(base64_data)
    
    # Write to temp file then load as numpy array
    with open("images/temp_extracted.npy", "wb") as f:
        f.write(data_bytes)
    
    try:
        # Load as numpy array
        extracted_data = np.load("images/temp_extracted.npy", allow_pickle=True)
        np.save(output_path, extracted_data)
        os.remove("images/temp_extracted.npy")
    except:
        # If not a valid numpy file, save as raw data
        with open(output_path, "wb") as f:
            f.write(data_bytes)
    
    print(f"[✔] Encrypted data extracted to {output_path}")
    return output_path

# If module is run directly, demonstrate steganography
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Image Steganography Tool")
    parser.add_argument("--mode", choices=["hide", "extract"], required=True, 
                        help="Operation mode: hide or extract data")
    parser.add_argument("--data", help="For hide mode: Path to data file to hide")
    parser.add_argument("--cover", help="For hide mode: Path to cover image")
    parser.add_argument("--stego", help="Path to steganographic image (output for hide, input for extract)")
    parser.add_argument("--output", help="For extract mode: Path to save extracted data")
    
    args = parser.parse_args()
    
    try:
        if args.mode == "hide":
            if not args.data:
                args.data = "images/encrypted.npy"
            
            hide_encrypted_data(
                args.data, 
                cover_image_path=args.cover,
                output_path=args.stego
            )
        
        elif args.mode == "extract":
            if not args.stego:
                args.stego = "images/stego_image.png"
            
            extract_encrypted_data(
                args.stego,
                output_path=args.output
            )
    
    except Exception as e:
        print(f"[✘] Error: {str(e)}")