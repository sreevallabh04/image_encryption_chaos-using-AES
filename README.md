# DNA-Based Image Encryption Using Chaos Theory

## 📌 Overview
This project implements **secure image encryption** using **DNA Cryptography and Chaos Theory**. It ensures ultra-high security by encoding images into DNA sequences, scrambling them using chaotic maps, and encrypting them with AES and XOR.

## 🔑 Features
- **DNA Encoding**: Converts image data into DNA sequences (A, T, C, G).
- **Chaotic Scrambling**: Uses mathematical chaos for randomization.
- **AES + XOR Encryption**: Ensures robust security.
- **Reversible Decryption**: Recovers the original image without loss.

## 🛠️ Installation
```bash
git clone https://github.com/sreevallabh04/DNA-Based Image Encryption Using Chaos Theory.git
cd dna-image-encryption
pip install -r requirements.txt
```

## 🚀 Usage
### Encrypt an Image
```bash
python src/encrypt.py
```

### Decrypt the Image
```bash
python src/decrypt.py
```

## 📝 Folder Structure
```
👤 dna-image-encryption
│── 📂 src
│   ├── encrypt.py  # Encryption process
│   ├── decrypt.py  # Decryption process
│   ├── dna_crypto.py  # DNA encoding/decoding logic
│   ├── chaos.py  # Chaotic scrambling functions
│   ├── hybrid_crypto.py  # AES + XOR encryption
│   ├── utils.py  # Helper functions
│── 📂 images
│   ├── original.png
│   ├── encrypted.bin
│   ├── decrypted.png
│── requirements.txt
│── README.md
```

## 📈 Contrast: DNA-Based vs AES + Chaos + Blockchain
| Feature | DNA-Based Encryption | AES + Chaos + Blockchain |
|---------|----------------------|-------------------------|
| Security Level | Ultra-High (Biological Encoding + Chaos) | High (AES + Chaos + Blockchain) |
| Encryption Type | DNA Encoding + Chaos + AES | AES + Chaotic Scrambling |
| Randomness | High (DNA & Chaos combined) | Moderate (Chaos only) |
| Processing Time | Slower (DNA mapping overhead) | Faster (AES-based) |
| Best For | Research, Bio-inspired Security | High-Speed Secure Applications |

## 🔬 Research Significance
- DNA cryptography is a rising field in quantum-secure encryption.
- This project enhances security by integrating biology and mathematics.

## 📝 License
MIT License

