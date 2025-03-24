# 🧬 DNA-Based Image Encryption with Chaos Theory & Blockchain

## 📌 Overview
This project implements a sophisticated **hybrid image encryption system** that combines DNA cryptography, chaos theory, AES encryption, and blockchain technology. It provides ultra-high security by encoding images into DNA sequences, scrambling them using chaotic maps, encrypting with AES, and verifying integrity through blockchain.

## 🔑 Key Features
- **DNA Encoding & Decoding**: Converts image data to/from DNA sequences (A, T, C, G)
- **Chaotic Scrambling**: Applies mathematics-based chaos for randomization
- **AES Encryption**: Ensures robust security with standard cryptographic algorithms
- **Blockchain Integration**: Verifies image integrity using a decentralized ledger
- **Histogram Analysis**: Validates encryption quality by comparing original vs. encrypted histograms
- **Reversible Process**: Allows complete recovery of the original image

## 🛠️ Installation
```bash
git clone https://github.com/sreevallabh04/image_encryption_chaos-using-AES.git
cd image_encryption_chaos-using-AES
pip install -r requirements.txt
```

## 🚀 Usage

### Encrypt an Image
```bash
python src/encrypt.py
```
This loads `images/input.jpg`, converts it to DNA, encrypts it, applies chaotic scrambling, and saves the result to `images/encrypted.npy`.

### Decrypt an Image
```bash
python src/decrypt.py
```
This loads the encrypted data, unscrambles it using the same chaotic sequence, decrypts it, converts from DNA back to an image, and saves the result to `images/decrypted.png`.

### Verify Image Integrity
```bash
python src/blockchain.py
```
This generates a hash of the encrypted image and adds it to the blockchain ledger, allowing future verification of image integrity.

### Analyze Histograms
```bash
python src/histogram_analysis.py
```
This creates histograms of both the original and encrypted images to verify encryption quality by ensuring the encrypted histogram shows uniform distribution.

## 📂 Project Structure
```
image_encryption_chaos-using-AES/
│── README.md                # This documentation
│── requirements.txt         # Required Python packages
│── images/                  # Image storage directory
│   ├── input.jpg            # Original input image
│   ├── encrypted.npy        # Encrypted image data
│   ├── original_shape.npy   # Original image dimensions
│   └── decrypted.png        # Decrypted output image
│── rsa_keys/                # RSA key storage
│   ├── private.pem          # RSA private key
│   └── public.pem           # RSA public key
│── src/                     # Source code
    ├── encrypt.py           # Main encryption process
    ├── decrypt.py           # Main decryption process
    ├── dna_crypto.py        # DNA encoding/decoding
    ├── chaos.py             # Chaotic scrambling functions
    ├── hybrid_crypto.py     # AES encryption implementation
    ├── blockchain.py        # Blockchain integrity verification
    ├── histogram_analysis.py # Security validation through histograms
    ├── utils.py             # Helper functions
    └── aes_key.bin          # AES encryption key
```

## 🔬 Encryption Process
1. **Image to DNA**: Convert pixel values to binary, then map to DNA nucleotides
2. **AES Encryption**: Encrypt the DNA sequence using AES
3. **Chaotic Scrambling**: Randomize the encrypted data using logistic map
4. **Blockchain Registration**: Generate and store hash for integrity verification
5. **Histogram Analysis**: Compare frequency distributions to verify encryption quality

## 🛡️ Security Features
| Security Layer | Implementation | Benefit |
|----------------|----------------|---------|
| DNA Encoding | Binary-to-nucleotide mapping | Adds biological-inspired obfuscation |
| Chaos Theory | Logistic map for scrambling | Creates non-linear, sensitive patterns |
| AES Encryption | Standard cryptographic algorithm | Provides proven security foundation |
| Blockchain | Decentralized hash storage | Enables tamper detection and verification |
| Histogram Analysis | Statistical comparison | Validates encryption effectiveness |

## 🚧 Future Enhancements
- Quantum-resistant cryptography integration
- Advanced DNA encoding rules with multiple mapping tables
- GPU acceleration for faster processing of large images
- Multi-layer chaotic systems for enhanced randomness

## 👨‍💻 Author
**Sreevallabh04 | Cybersecurity & Cryptography Enthusiast**  
📧 Email: srivallabhkakarala@gmail.com  
🌟 GitHub: github.com/sreevallabh04

## 📄 License
This project is available under the MIT License.