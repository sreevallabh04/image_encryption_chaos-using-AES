from Crypto.PublicKey import RSA

def generate_rsa_keys():
    """Generate RSA key pair and save them as public.pem & private.pem."""
    key = RSA.generate(2048)  # 2048-bit RSA key
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    # Save the private key
    with open("rsa_keys/private.pem", "wb") as priv_file:
        priv_file.write(private_key)

    # Save the public key
    with open("rsa_keys/public.pem", "wb") as pub_file:
        pub_file.write(public_key)

    print("[✔] RSA Key Pair Generated & Saved in 'rsa_keys/'")

if __name__ == "__main__":
    generate_rsa_keys()
