"""Helper script to initially generate Crypto key"""

from cryptography.fernet import Fernet

key = Fernet.generate_key()
print(f"Key: {key}")

with open("../Secrets/enc.key", "wb") as encfile:
    encfile.write(key)