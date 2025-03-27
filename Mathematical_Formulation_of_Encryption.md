# Mathematical Formulation of Image Encryption Algorithm

I've been working on this DNA-Chaos-AES hybrid encryption system for months now, and I thought it would be helpful to document the actual mathematical formulas behind it. Here's a comprehensive breakdown of how the encryption works, step by step. This should help anyone trying to understand or extend the system.

## Overview of the Encryption Process

Our encryption system combines three powerful techniques:
1. DNA-based encoding
2. Chaos theory for scrambling
3. Standard AES (Advanced Encryption Standard) in CBC mode

The overall encryption flow looks like this:

```
Original Image → Binary Representation → DNA Encoding → 
Chaotic Scrambling → AES-CBC Encryption → Encrypted Output
```

Let's dive into the mathematical details of each step.

## Step 1: DNA Encoding

The DNA encoding process converts binary data into a sequence of nucleotide characters (A, T, C, G). Here's how it works:

### Binary to DNA Mapping
We use the following mapping to convert binary pairs to DNA nucleotides:
- 00 → A
- 01 → T
- 10 → C
- 11 → G

This can be expressed mathematically as a function *D* that maps a binary pair to a DNA nucleotide:

D(b₁b₂) = {
    A if b₁b₂ = 00
    T if b₁b₂ = 01
    C if b₁b₂ = 10
    G if b₁b₂ = 11
}

For an image with pixel values P = [p₁, p₂, ..., pₙ], we first convert each pixel value to its 8-bit binary representation B = [b₁, b₂, ..., b₈ₙ]. Then for each consecutive pair of bits (b₂ᵢ₋₁, b₂ᵢ), we apply the DNA mapping function:

DNA(P) = [D(b₁b₂), D(b₃b₄), ..., D(b₂ₘ₋₁b₂ₘ)]

where m = 4n is the number of binary pairs.

## Step 2: Chaotic Scrambling

We use the logistic map, a chaotic function, to generate a pseudo-random sequence that determines how the DNA-encoded data gets scrambled.

### The Logistic Map

The logistic map is defined by the recurrence relation:

xₙ₊₁ = r·xₙ·(1 - xₙ)

where:
- xₙ is a value between 0 and 1
- r is the parameter that controls the chaotic behavior (we use r = 3.99 to ensure chaotic behavior)
- x₀ is the seed value (we use x₀ = 0.5)

For a DNA sequence of length L, we generate a chaotic sequence X = [x₁, x₂, ..., xₗ] using the logistic map. Then we determine the scrambling indices by sorting the chaotic sequence:

I = argsort(X)

where argsort returns the indices that would sort X in ascending order.

The scrambled DNA sequence is then:

SDNA = [DNA[I₁], DNA[I₂], ..., DNA[Iₗ]]

This effectively shuffles the DNA sequence in a way that can only be reversed if you know the exact parameters (r and x₀) of the logistic map.

## Step 3: AES-CBC Encryption

Finally, we encrypt the scrambled DNA sequence using the AES algorithm in CBC (Cipher Block Chaining) mode.

### AES-CBC Mathematical Foundation

AES is a block cipher that operates on fixed blocks of 128 bits (16 bytes). The CBC mode chains blocks together so that each encrypted block depends on all preceding blocks.

The encryption process can be described as:

1. The plaintext P is padded using PKCS#7 padding to ensure its length is a multiple of the block size (16 bytes).
   
   Let's call the padded plaintext P' = [P'₁, P'₂, ..., P'ₙ] where each P'ᵢ is a 128-bit block.

2. A random 128-bit Initialization Vector (IV) is generated.

3. Each block is encrypted using the following formula:
   
   C₁ = E(K, P'₁ ⊕ IV)
   C₂ = E(K, P'₂ ⊕ C₁)
   ...
   Cₙ = E(K, P'ₙ ⊕ Cₙ₋₁)
   
   where:
   - E(K, X) is the AES encryption function with key K applied to block X
   - ⊕ represents the bitwise XOR operation
   - C₁, C₂, ..., Cₙ are the encrypted blocks

4. The final ciphertext is formed by concatenating the IV with all encrypted blocks:
   
   Ciphertext = IV || C₁ || C₂ || ... || Cₙ

The encrypted data is then encoded in base64 for easy storage and transmission.

## Complete Encryption Process

Here's the step-by-step mathematical formulation of the entire encryption process:

1. For an input image I, convert each pixel value to 8-bit binary: 
   B = Binary(I)

2. Group binary bits into pairs and map to DNA nucleotides:
   DNA = [D(b₁b₂), D(b₃b₄), ..., D(b₂ₘ₋₁b₂ₘ)]

3. Generate chaotic sequence using logistic map:
   x₀ = 0.5, r = 3.99
   xₙ₊₁ = r·xₙ·(1 - xₙ) for n = 0, 1, ..., L-1
   where L is the length of the DNA sequence

4. Compute scrambling indices:
   I = argsort([x₁, x₂, ..., xₗ])

5. Scramble the DNA sequence:
   SDNA = [DNA[I₁], DNA[I₂], ..., DNA[Iₗ]]

6. Convert scrambled DNA to bytes:
   BDNA = UTF8_encode(SDNA)

7. Apply PKCS#7 padding:
   P' = Pad(BDNA)

8. Generate random IV (16 bytes):
   IV = Random(16)

9. For each 16-byte block P'ᵢ in P':
   C₁ = AES_encrypt(K, P'₁ ⊕ IV)
   Cᵢ = AES_encrypt(K, P'ᵢ ⊕ Cᵢ₋₁) for i = 2, 3, ..., n

10. Concatenate IV and encrypted blocks:
    C = IV || C₁ || C₂ || ... || Cₙ

11. Encode in base64:
    EncryptedData = Base64_encode(C)

## Decryption Process

The decryption process reverses these steps:

1. Decode base64:
   C = Base64_decode(EncryptedData)

2. Extract IV and ciphertext:
   IV = C[0:16]
   Ciphertext = C[16:]

3. For each 16-byte block Cᵢ:
   P'₁ = AES_decrypt(K, C₁) ⊕ IV
   P'ᵢ = AES_decrypt(K, Cᵢ) ⊕ Cᵢ₋₁ for i = 2, 3, ..., n

4. Remove padding:
   BDNA = Unpad(P')

5. Convert bytes to string:
   SDNA = UTF8_decode(BDNA)

6. Generate the same chaotic sequence as in encryption:
   x₀ = 0.5, r = 3.99
   xₙ₊₁ = r·xₙ·(1 - xₙ) for n = 0, 1, ..., L-1

7. Compute scrambling indices:
   I = argsort([x₁, x₂, ..., xₗ])

8. Unscramble the DNA sequence:
   DNA = array of length L
   DNA[I₁] = SDNA₁
   DNA[I₂] = SDNA₂
   ...
   DNA[Iₗ] = SDNAₗ

9. Convert DNA back to binary:
   For each nucleotide n in DNA:
   Binary += D⁻¹(n) where D⁻¹ is the inverse mapping:
   D⁻¹(A) = 00
   D⁻¹(T) = 01
   D⁻¹(C) = 10
   D⁻¹(G) = 11

10. Pack binary bits back to bytes and reshape to original image dimensions.

## Security Analysis

The security of this system relies on several factors:

1. **DNA Encoding**: This adds a layer of confusion but isn't the main security feature.

2. **Chaotic Scrambling**: The logistic map is extremely sensitive to initial conditions. Even tiny differences in the parameters (r or x₀) will result in completely different scrambling patterns.

3. **AES-CBC Encryption**: AES is a well-established encryption standard that provides strong security. The CBC mode adds an additional layer of security by chaining blocks together.

The combination of these techniques creates a robust encryption system that's resistant to various attacks. The primary security rests on the AES key, while the chaotic scrambling provides an additional layer that makes statistical analysis of the encrypted data extremely difficult.

---

In practice, I've found this system provides excellent security while maintaining reasonable performance. The most computationally intensive part is the DNA encoding/decoding process, especially for large images. I'm currently working on optimizing this step to improve performance without compromising security.