# 🔐 Image Encryption with Chaos & AES | Blockchain Integrity

> **A hybrid encryption framework integrating AES, Chaos Theory, and Blockchain for secure image encryption & verification.**

---

## 🚀 Features

👉 **AES + Chaos-based Encryption** - Ensures strong encryption using AES combined with chaotic maps.  
👉 **Hybrid Cryptography (AES + RSA)** - Uses RSA to securely exchange AES keys.  
👉 **Blockchain Integration** - Verifies image integrity using blockchain-based ledger.  
👉 **Histogram Analysis** - Compares original vs. encrypted image for security validation.  
👉 **Secure Key Storage** - RSA keys and AES keys securely managed.  

---

## 📂 Project Structure

```
sreevallabh04-image_encryption_chaos-using-aes/
│── README.md                # This file 🌜
│── encrypt.py               # Image encryption module 🔒
│── decrypt.py               # Image decryption module 🔓
│── chaos.py                 # Chaos-based key generation 🌪️
│── hybrid_crypto.py         # Hybrid AES + RSA encryption 🔑
│── blockchain.py            # Blockchain verification for integrity ⛓️
│── histogram_analysis.py    # Histogram comparison 🖼️
│── utils.py                 # Helper utilities 🫠
│── key.bin                  # AES encryption key 🔑
│── blockchain_ledger.json   # Blockchain ledger data 🌜
│── images/
│   └── encrypted.bin        # Encrypted image file 📁
│── rsa_keys/
│   ├── private.pem          # RSA Private Key 🛥️
│   └── public.pem           # RSA Public Key 🔑
```

---

## 🔧 Setup & Installation

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Run Encryption
```bash
python encrypt.py --input images/sample.png --output images/encrypted.bin
```

### 3️⃣ Run Decryption
```bash
python decrypt.py --input images/encrypted.bin --output images/decrypted.png
```

### 4️⃣ Verify Integrity via Blockchain
```bash
python blockchain.py --verify images/encrypted.bin
```

### 📊 Histogram Analysis
Run this command to compare original vs. encrypted images:
```bash
python histogram_analysis.py --input images/sample.png --encrypted images/encrypted.bin
```
**Output:** Two histogram images will be generated:
- `histogramoriginal.png`
- `histogramencrypted.png`

---

## 🛡️ Security & Cryptographic Techniques

| Method         | Description |
|---------------|------------|
| **AES-256**   | Symmetric encryption for image data 🔐 |
| **Chaos Maps** | Pseudorandom chaotic sequences for key generation 🌪️ |
| **RSA-4096**   | Asymmetric encryption for AES key exchange 🔑 |
| **Blockchain** | Integrity verification using decentralized ledger ⛓️ |

---

## 🤖 Future Enhancements

🔹 Quantum-Safe Cryptography (Post-Quantum Algorithms)  
🔹 Advanced Blockchain Consensus (PoW / PoS)  
🔹 Homomorphic Encryption for Secure Computation  

---

## 👨‍💻 Author
**Sreevallabh04 | Cybersecurity & Cryptography Enthusiast**  
📧 Email: srivallabhkakarala@gmail.com  
🌟 GitHub: github.com/sreevallabh04  

---

## 🔐 "Encrypt, Secure, and Trust Your Data." 🚀

---

## 📚 License
This project is Open Source!

---

