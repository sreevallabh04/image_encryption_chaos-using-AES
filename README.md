🔒 Image Encryption Using AES + Chaos Theory + RSA
Hybrid Cryptographic System for Secure Image Encryption
📌 Overview
This project implements secure image encryption using a Hybrid Cryptographic Approach that combines:
✅ AES (Advanced Encryption Standard) for encrypting image data.
✅ Chaotic Key Generation using the logistic map to create unpredictable AES keys.
✅ RSA Encryption to protect the AES key from exposure.

This ensures high security, making it difficult for attackers to extract image information even if the encrypted data is intercepted.

📂 Project Structure
sreevallabh04-image_encryption_chaos-using-aes/
│── README.md           # Project documentation
│── blockchain.py       # (Optional) Blockchain integration (To Be Implemented)
│── chaos.py            # Generates chaotic AES keys
│── decrypt.py          # Decrypts the image using AES
│── encrypt.py          # Encrypts the image using AES
│── hybrid_crypto.py    # Generates RSA keys & handles AES key encryption
│── requirements.txt    # Required Python libraries
│── utils.py            # Helper functions for padding/unpadding
│── rsa_keys/           # Stores RSA keys
│   ├── private.pem     # RSA Private Key (Keep this secret)
│   ├── public.pem      # RSA Public Key (Used to encrypt AES key)
│── images/
│   ├── input.jpg       # Original image to be encrypted
│   ├── encrypted.bin   # Encrypted image file
│   ├── decrypted.jpg   # Decrypted image file
│── key.bin             # Encrypted AES key (protected with RSA)

 How It Works
AES Encrypts the Image

The image is converted to raw byte data.
It is padded to make its size a multiple of 16 bytes.
AES encrypts the padded data using a chaotic key.
RSA Secures the AES Key

The AES key is generated using a chaotic logistic map.
The AES key is encrypted using RSA (public key) and stored securely.
Decryption Process

The AES key is decrypted using RSA (private key).
The image is decrypted using the recovered AES key.

🚀 Installation & Setup
🔹 Step 1: Install Required Libraries
Install dependencies using: pip install -r requirements.txt
If you don’t have a requirements.txt, manually install: pip install pycryptodome opencv-python numpy

🔹 Step 2: Generate RSA Keys
Before encryption, generate the RSA key pair: python hybrid_crypto.py
This creates:

rsa_keys/public.pem → Used for encrypting AES keys.
rsa_keys/private.pem → Used for decrypting AES keys.

🔹 Step 3: Encrypt an Image
Place an image in the images/ folder and run: python encrypt.py
This will:
✅ Generate a chaotic AES key.
✅ Encrypt the AES key with RSA and store it in key.bin.
✅ Encrypt the image and save it as images/encrypted.bin.

🔹 Step 4: Decrypt the Image: python decrypt.py
This will:
✅ Decrypt the AES key using RSA.
✅ Use the key to decrypt the image.
✅ Save the decrypted image as images/decrypted.jpg.

🔹 Future Improvements
✔ Upgrade to AES-GCM instead of ECB (removes patterns in encrypted images).
✔ Integrate Blockchain to store encrypted image hashes for integrity verification.
✔ Use Chaotic Pixel Shuffling before encryption for added security.

📜 License
This project is open-source and free to use for educational purposes.

👨‍💻 Author
Developed by [Sreevallabh]
For inquiries, contact [srivallabhkakarala@gmail.com]
