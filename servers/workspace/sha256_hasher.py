
import hashlib

def generate_sha256_hash(text):
    """Generates the SHA256 hash of a given text."""
    sha256_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
    return sha256_hash

name = "Aswin Pratapsingh"
hashed_name = generate_sha256_hash(name)
print(f"The SHA256 hash of \"{name}\" is: {hashed_name}")
