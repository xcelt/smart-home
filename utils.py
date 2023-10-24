"""
Module with helper functions, mainly for encrypted/decrypted messages and sending/retreiving messages
"""

import json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

def load_fernet_key(fernet_key_file):
    '''
    Loads the previously created Fernet key used to encrypt/decrypt saved devices.

    Args:
        fernet_key_file (str): Path to the file containing the Fernet key.

    Returns:
        bytes: The Fernet key as bytes, or None if the file is not found.
    '''
    try:  # try retrieving the Fernet encryption key from bin file
        with open(fernet_key_file, "rb") as encfile:
            enc_key = encfile.read()
        return enc_key
    except OSError:  # if file not found
        return None

def load_and_decrypt_fernet(fer_key, filename):
        '''
        Loads and decrypts data from a file using a Fernet key.

        Args:
        fer_key (bytes): Fernet key for decryption.
        filename (str): Path to the file to decrypt and load.

        Returns:
        dict: Decrypted data as a dictionary, or None if the file is not found.
        '''

        try:
            # Load the encrypted data from the file
            with open(filename, 'rb') as file:
                encrypted_data = file.read()

            # Initialize a Fernet cipher with the key
            cipher_suite = Fernet(fer_key)

            # Decrypt and deserialize the data
            decrypted_data = cipher_suite.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode('utf-8'))

        except:  # file not found
            return None

def encrypt_and_save_fernet(data, enc_key, filename):
    '''
    Encrypts and stores data to a file using a Fernet key.

    Args:
        data (dict): Data to be encrypted and saved.
        enc_key (bytes): Fernet key for encryption.
        filename (str): Path to the file to save the encrypted data.

    Returns:
        bool: True if encryption and saving are successful, False otherwise.
    '''
    try:
        cipher_suite = Fernet(enc_key)

        encrypted_data = cipher_suite.encrypt(json.dumps(data).encode('utf-8'))

        # Store the encrypted data to a file
        with open(filename, 'wb') as file:
            file.write(encrypted_data)

        return True

    except:
        return False

def load_public_key(public_key_file):
    '''
        Load a public key from a file.

        Args:
            public_key_file (str): Path to the file containing the public key in PEM format.

        Returns:
            cryptography.hazmat.backends.interfaces.RSAPublicKey: The loaded public key, or None if an error occurs.
    '''
    try:
        with open(public_key_file, 'rb') as public_key_file:
            public_key_pem = public_key_file.read()
            public_key = serialization.load_pem_public_key(public_key_pem, backend=default_backend())

        return public_key

    except Exception as e:
        print(f"Error loading public key: {e}")
        return None

def load_keys(public_key_file=None, private_key_file=None):
    '''
        Load public and private keys from files.

        Args:
            public_key_file (str, optional): Path to the file containing the public key in PEM format.
            private_key_file (str, optional): Path to the file containing the private key in PEM format.

        Returns:
            tuple: A tuple containing the loaded public and private keys (RSAPublicKey, RSAPrivateKey), or (None, None) if an error occurs.
    '''
    try:
        public_key = None
        if public_key_file:
            # Load the public key from the specified file
            with open(public_key_file, 'rb') as public_key_file:
                public_key_pem = public_key_file.read()
                public_key = serialization.load_pem_public_key(public_key_pem, backend=default_backend())

        private_key = None
        if private_key_file:
            # Load the private key from the specified file
            with open(private_key_file, 'rb') as private_key_file:
                private_key_pem = private_key_file.read()
                private_key = serialization.load_pem_private_key(private_key_pem, backend=default_backend(), password=None)

        return public_key, private_key
    except Exception as e:
        # print(f"Error loading keys: {e}")
        return None, None


def decrypt_message(enc_msg, private_key):
    '''
        Decrypt an encrypted message using a private key.

        Args:
            enc_msg (bytes): The encrypted message to decrypt.
            private_key (RSAPrivateKey): The private key for decryption.

        Returns:
            dict: The decrypted message as a dictionary, or None if decryption fails.
        '''
    try:
        # Decrypt the message using the private key
        decrypted_message = private_key.decrypt(
            enc_msg,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),  # Use hashes.SHA256()
                algorithm=hashes.SHA256(),  # Use hashes.SHA256()
                label=None
            )
        )

        return json.loads(decrypted_message.decode('utf-8'))

    except (ValueError, Exception) as e:
        print(f"Error decrypting message: {e}")
        return None

# Function to create and encrypt a message
def encrypt_message(msg, pub_key):
    '''
        Encrypt a message using an RSA public key.

        Args:
            msg (dict): The message to encrypt as a dictionary.
            pub_key (RSAPublicKey): The RSA public key for encryption.

        Returns:
            bytes: The encrypted message, or None if encryption fails.
        '''
    try:
        # Create the message as a JSON object
        message = json.dumps(msg).encode('utf-8')

        # Encrypt the message using the RSA public key
        encrypted_message = pub_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return encrypted_message

    except Exception as e:
        return None


def encrypt_and_save(data, pub_key, output_filename):
    '''
        Encrypt data using a public key and save it to a file.

        Args:
            data (dict): The data to encrypt and save as a dictionary.
            pub_key (RSAPublicKey): The RSA public key for encryption.
            output_filename (str): Path to the file where the encrypted data will be saved.

        Returns:
            bool: True if encryption and saving are successful, False otherwise.
        '''
    try:
        # Convert data to JSON if it's a dictionary
        #data = json.dumps(data).encode('utf-8')

        # Encrypt the data using the public key
        encrypted_data = encrypt_message(data, pub_key)

        # Write the encrypted data to the specified file
        with open(output_filename, 'wb') as output_file:
            output_file.write(encrypted_data)

        return True

    except Exception as e:
        return False


def load_and_decrypt(input_filename, private_key):
    '''
        Load encrypted data from a file and decrypt it using a private key.

        Args:
            input_filename (str): Path to the file containing the encrypted data.
            private_key (RSAPrivateKey): The RSA private key for decryption.

        Returns:
            str: The decrypted data as a string, or None if decryption fails.
        '''
    try:
        # Read the encrypted data from the input file
        with open(input_filename, 'rb') as input_file:
            encrypted_data = input_file.read()

        # Decrypt the data using the private key
        decrypted_data = private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=padding.ALGO_SHA256),
                algorithm=padding.ALGO_SHA256,
                label=None
            )
        )

        return decrypted_data.decode('utf-8')

    except Exception as e:
        return None

# Function to create, encrypt, and send a message
def send_encrypted_message(client_sock, msg, pub_key):
    '''
        Create, encrypt, and send a message through a socket using an RSA public key.

        Args:
            client_sock (socket): The socket for sending the encrypted message.
            msg (dict): The message to send as a dictionary.
            pub_key (RSAPublicKey): The RSA public key for encryption.

        Returns:
            bool: True if sending is successful, False otherwise.
        '''
    try:
        # Create the message as a JSON object
        #message = json.dumps(msg).encode('utf-8')

        # Encrypt the message using the RSA public key
        encrypted_message = encrypt_message(msg,pub_key)

        # Send the encrypted message
        client_sock.send(encrypted_message)

        return True

    except Exception as e:
        return False


# Testing out functions
# if __name__ == "__main__":
#
#     # Load the keys
#     public_key, private_key = load_keys("./Secrets/hub_pub.key","./Secrets/hub_prv.key")
#
#     somemsg = {"something":"123","somethingelse":"456"}
#     encmsg = encrypt_message(somemsg,public_key)
#
#     print(f"Encrypted message: {encmsg}")
#
#     decmsg = decrypt_message(encmsg, private_key)
#     print(f"Decrypted message: {decmsg}")
#
#     if public_key and private_key:
#         print("Keys loaded successfully.")
#     else:
#         print("Failed to load keys.")