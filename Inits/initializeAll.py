import json
import socket
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes  # Add this import

from cryptography.fernet import Fernet

import utils


def generate_and_save_fernet_key(keyfile):
    try:
        key = Fernet.generate_key()
        print(f"Key: {key}")

        with open(keyfile, "wb") as encfile:
            encfile.write(key)
        return True
    except:
        return False

def generate_and_save_keys(public_key_file, private_key_file):
    # Generate an RSA key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Extract the public key in PEM format
    public_key = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Extract the private key in PEM format
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Write the public key to the specified file
    with open(public_key_file, 'wb') as public_key_file:
        public_key_file.write(public_key)

    # Write the private key to the specified file
    with open(private_key_file, 'wb') as private_key_file:
        private_key_file.write(private_key_pem)

print("Generating hub and device RSA keys")
generate_and_save_keys("../Secrets/hub_pub.key","../Secrets/hub_prv.key")
generate_and_save_keys("../Secrets/dev_pub.key","../Secrets/dev_prv.key")

print("Generating hub and device fernet encryption keys")
generate_and_save_fernet_key("../Secrets/hub_enc.key")
generate_and_save_fernet_key("../Secrets/dev_enc.key")


server_user = "user1"
server_pass = "user1password"

credentials = {'user':server_user, 'pass':server_pass}

# public_key, private_key = utils.load_keys("../Secrets/pub.key","../Secrets/prv.key")
fer_key = utils.load_fernet_key("../Secrets/dev_enc.key")


if utils.encrypt_and_save_fernet(credentials, fer_key, "../Secrets/creds.bin"):
    print("Credentials created and saved to 'Secrets/creds.bin'")