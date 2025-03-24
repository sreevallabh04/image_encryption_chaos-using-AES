import hashlib
import json
import os
import time

BLOCKCHAIN_FILE = "blockchain_ledger.json"

class Blockchain:
    def __init__(self):
        """Initialize the blockchain by loading existing data or creating a new one."""
        if os.path.exists(BLOCKCHAIN_FILE):
            with open(BLOCKCHAIN_FILE, "r") as f:
                self.chain = json.load(f)
        else:
            self.chain = []
            self.create_genesis_block()

    def create_genesis_block(self):
        """Create the first (genesis) block in the blockchain."""
        genesis_block = {
            "index": 0,
            "timestamp": time.time(),
            "previous_hash": "0",
            "image_hash": "GENESIS_BLOCK"
        }
        self.chain.append(genesis_block)
        self.save_blockchain()

    def add_block(self, image_hash):
        """Add a new block to the blockchain with the encrypted image hash."""
        previous_block = self.chain[-1]
        new_block = {
            "index": len(self.chain),
            "timestamp": time.time(),
            "previous_hash": self.hash_block(previous_block),
            "image_hash": image_hash
        }
        self.chain.append(new_block)
        self.save_blockchain()

    def save_blockchain(self):
        """Save the blockchain to a file."""
        with open(BLOCKCHAIN_FILE, "w") as f:
            json.dump(self.chain, f, indent=4)

    def verify_image_integrity(self, image_hash):
        """Verify if the given image hash exists in the blockchain."""
        for block in self.chain:
            if block["image_hash"] == image_hash:
                return True
        return False

    @staticmethod
    def hash_block(block):
        """Generate SHA-256 hash of a block."""
        block_string = json.dumps(block, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

def hash_encrypted_image():
    """Generate SHA-256 hash of the encrypted image."""
    with open("images/encrypted.npy", "rb") as f:
        file_bytes = f.read()
    return hashlib.sha256(file_bytes).hexdigest()

if __name__ == "__main__":
    blockchain = Blockchain()
    image_hash = hash_encrypted_image()
    blockchain.add_block(image_hash)
    print("[✔] Encrypted image hash added to blockchain!")
