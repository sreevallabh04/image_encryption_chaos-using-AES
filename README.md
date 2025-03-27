# 🧬 Enhanced DNA-Based Image Encryption with Chaos Theory & Blockchain

## 📌 Overview
This project implements a sophisticated **hybrid image encryption system** that combines DNA cryptography, chaos theory, AES encryption, and blockchain technology with several advanced security enhancements. The system provides ultra-high security by encoding images into DNA sequences using dynamic rule switching, scrambling them using multiple chaotic maps, encrypting with standard AES (CBC mode), hiding encrypted data using steganography, and verifying integrity through blockchain.

## 🔄 Recent Enhancements
- **Standard AES Encryption**: Implemented AES-CBC mode for enhanced security
- **Dynamic DNA Encoding**: Implemented multiple rule sets with key-based rule switching
- **Hybrid Chaotic System**: Integrated four different chaotic maps for stronger scrambling
- **Steganography Support**: Added capability to hide encrypted data in cover images
- **Improved Key Management**: Password-based key derivation with salting and iteration
- **Enhanced Command-Line Interface**: More flexible options for all features

## 🔑 Key Features
- **Advanced DNA Encoding & Decoding**: Converts image data to/from DNA sequences (A, T, C, G) using multiple dynamic rule sets
- **Hybrid Chaotic Scrambling**: Applies multiple chaos maps (logistic, sine, tent, cubic) for enhanced randomization
- **AES-CBC Encryption**: Ensures robust security with industry-standard encryption
- **Steganography**: Hides encrypted data within ordinary-looking images
- **Blockchain Integration**: Verifies image integrity using a decentralized ledger
- **Histogram Analysis**: Validates encryption quality by comparing original vs. encrypted histograms
- **Reversible Process**: Allows complete recovery of the original image

## 🛠️ Installation
```bash
git clone https://github.com/sreevallabh04/image_encryption_chaos-using-AES.git
cd image_encryption_chaos-using-AES
pip install -r requirements.txt
```

## 🚀 Basic Usage

### Encrypt an Image
```bash
python src/encrypt.py --image images/input.jpg
```
This loads the specified image, converts it to DNA, encrypts it, applies chaotic scrambling, and saves the result to `images/encrypted.npy`.

### Decrypt an Image
```bash
python src/decrypt.py
```
This loads the encrypted data, unscrambles it, decrypts it, converts from DNA back to an image, and saves the result to `images/decrypted.png`.

## 🔐 Advanced Usage

### Encrypt with Steganography
```bash
python src/encrypt.py --image images/input.jpg --steganography --cover images/cover.jpg
```
This encrypts the image and hides the encrypted data inside a cover image, saving the result as `images/stego_image.png`.

### Decrypt from Steganographic Image
```bash
python src/decrypt.py --stego images/stego_image.png
```
This extracts the hidden encrypted data from the steganographic image, decrypts it, and saves the result to `images/decrypted.png`.

### Run Steganography Separately
```bash
# Hide encrypted data in a cover image
python src/steganography.py --mode hide --data images/encrypted.npy --cover images/cover.jpg

# Extract encrypted data from a steganographic image
python src/steganography.py --mode extract --stego images/stego_image.png
```

### Generate New Encryption Keys
```bash
# Generate a new AES key
python src/hybrid_crypto.py

# Generate new DNA encoding rules
python src/dna_crypto.py

# Generate new chaos parameters
python src/chaos.py
```

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
│   ├── decrypted.png        # Decrypted output image
│   └── stego_image.png      # Steganographic image (if used)
│── blockchain_ledger.json   # Blockchain storage file
│── src/                     # Source code
    ├── encrypt.py           # Main encryption process
    ├── decrypt.py           # Main decryption process
    ├── dna_crypto.py        # Enhanced DNA encoding/decoding with dynamic rules
    ├── chaos.py             # Hybrid chaotic scrambling with multiple maps
    ├── hybrid_crypto.py     # AES-CBC encryption implementation
    ├── steganography.py     # LSB steganography to hide encrypted data
    ├── blockchain.py        # Blockchain integrity verification
    ├── histogram_analysis.py # Security validation through histograms
    ├── utils.py             # Helper functions
    ├── aes_key.bin          # AES encryption key (generated)
    ├── dna_rules.key        # DNA rule switching key (generated)
    └── chaos_params.bin     # Chaotic system parameters (generated)
```

## 🔬 Enhanced Encryption Process
1. **Image to DNA**: Convert pixel values to binary, then map to DNA nucleotides using dynamic rule switching
2. **AES-CBC Encryption**: Encrypt the DNA sequence using standard AES encryption
3. **Hybrid Chaotic Scrambling**: Randomize the encrypted data using multiple chaotic maps
4. **Steganography (Optional)**: Hide encrypted data in an ordinary-looking cover image
5. **Blockchain Registration**: Generate and store hash for integrity verification
6. **Histogram Analysis**: Compare frequency distributions to verify encryption quality

## 🛡️ Security Features
| Security Layer | Implementation | Benefit |
|----------------|----------------|---------|
| Dynamic DNA Encoding | Multiple rule sets with key-based switching | Prevents statistical analysis attacks |
| Hybrid Chaos Theory | Four chaotic maps (logistic, sine, tent, cubic) | Provides complex non-linear scrambling |
| AES-CBC Encryption | Standard block cipher encryption with proper key derivation | Ensures confidentiality with industry-proven encryption |
| Steganography | LSB hiding in cover images | Adds security through obscurity |
| Blockchain | Decentralized hash storage | Enables tamper detection and verification |
| Histogram Analysis | Statistical comparison | Validates encryption effectiveness |

## 📐 Mathematical Formulation

This section provides the mathematical foundation behind the encryption process.

### DNA Encoding

The DNA encoding process maps binary pairs to DNA nucleotides:

```
D(b₁b₂) = {
    A if b₁b₂ = 00
    T if b₁b₂ = 01
    C if b₁b₂ = 10
    G if b₁b₂ = 11
}
```

For an image with pixel values P, we convert each pixel to 8-bit binary and apply the DNA mapping function:

```
DNA(P) = [D(b₁b₂), D(b₃b₄), ..., D(b₂ₘ₋₁b₂ₘ)]
```

### Chaotic Scrambling

We use the logistic map to generate a pseudo-random sequence for scrambling:

```
xₙ₊₁ = r·xₙ·(1 - xₙ)
```

where r = 3.99 (chaotic regime) and x₀ = 0.5 (seed value). The scrambling indices are:

```
I = argsort([x₁, x₂, ..., xₗ])
```

The scrambled DNA sequence is then:

```
SDNA = [DNA[I₁], DNA[I₂], ..., DNA[Iₗ]]
```

### AES-CBC Encryption

The AES-CBC encryption process can be described mathematically as:

1. Pad the plaintext P to ensure its length is a multiple of 16 bytes
2. Generate a random 16-byte Initialization Vector (IV)
3. Encrypt each block using:
   ```
   C₁ = E(K, P'₁ ⊕ IV)
   C₂ = E(K, P'₂ ⊕ C₁)
   ...
   Cₙ = E(K, P'ₙ ⊕ Cₙ₋₁)
   ```
   where E(K,X) is the AES encryption function and ⊕ is bitwise XOR

4. The final ciphertext is:
   ```
   Ciphertext = IV || C₁ || C₂ || ... || Cₙ
   ```

For more detailed mathematical explanation, see the `Mathematical_Formulation_of_Encryption.md` file.

## 🚧 Future Improvements
- Quantum-resistant cryptography integration
- GPU acceleration for faster processing of large images
- Multi-layer watermarking for copyright protection
- Distributed blockchain verification network
- Real-time encryption for video streams

## 👨‍💻 Author
**Sreevallabh04 | Cybersecurity & Cryptography Enthusiast**  
📧 Email: srivallabhkakarala@gmail.com  
🌟 GitHub: github.com/sreevallabh04

## 📄 License
This project is available under the MIT License.