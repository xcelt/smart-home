import socket
import json
import random
import threading
import time
import os
from cryptography.fernet import Fernet

# Function to handle client requests
def handle_client(client_socket):
    while True:
        request = client_socket.recv(1024)
        if not request:
            break

        request_data = json.loads(request.decode('utf-8'))


        if 'action' in request_data:
            action = request_data['action']

            if action == 'connect':
                print("Connection request from: Device ID: %s, Device Type:%s" % (request_data['deviceid'],request_data['devicetype']))

                if request_data['deviceid'] in device_list:
                    print("Device is already registered.")
                    response = json.dumps({'connect': 'ok'})
                else:
                    if input("Accept the connection and register device (Y/N)? ").lower().strip() == "y":
                        device_list[request_data['deviceid']] = request_data['devicetype']
                        store_saved_devices(enc_key=enc_key,device_list=device_list)
                        response = json.dumps({'connect': 'ok'})
                    else:
                        print("Connection request rejected.")
                        response = json.dumps(({'connect': 'reject'}))

                client_socket.send(response.encode('utf-8'))


        #     elif action == 'get_status':
        #         print("Retrieving light status: %s" % (device_data['light']['status']))
        #         response = json.dumps({'status': device_data['light']['status']})
        #         client_socket.send(response.encode('utf-8'))
        #
        #     elif action == 'set_status':
        #         if 'status' in request_data:
        #             print("Setting light status: " + request_data['status'])
        #             device_data['light']['status'] = request_data['status']
        #         response = json.dumps(device_data['light']['status'])
        #         client_socket.send(response.encode('utf-8'))
        #
        #     elif action == 'set_threshold':
        #         if 'threshold' in request_data:
        #             device_data['light']['threshold'] = request_data['threshold']
        #         response = json.dumps({'threshold': device_data['light']['threshold']})
        #         client_socket.send(response.encode('utf-8'))
        #
        #     elif action == 'save_preferences':
        #         response = json.dumps({'threshold': device_data['light']['threshold']})
        #         save_preferences(prefs_file_path,response)
        #         client_socket.send(response.encode('utf-8'))

    client_socket.close()

def load_crypt_key():
    '''Loads the previously created Fernet key used to encrypt/decrypt saved devices.'''
    try:  # try retrieving the Fernet encryption key from bin file
        with open("Secrets/enc.key", "rb") as encfile:
            enc_key = encfile.read()
    except OSError:  # if file not found
        return None
    return enc_key

def store_saved_devices(enc_key, device_list):
    '''Encrypts and stores device_list to disk'''
    cipher_suite = Fernet(enc_key)

    encrypted_data = cipher_suite.encrypt(str(device_list).encode())

    # Store the encrypted data to a file
    with open('Secrets/device_list.bin', 'wb') as file:
        file.write(encrypted_data)


def load_saved_devices(enc_key):
    '''Loads and decrypts list of previously registered devices'''

    try:
        # Load the encrypted data from the file
        with open('Secrets/device_list.bin', 'rb') as file:
            encrypted_data = file.read()

        # Initialize a Fernet cipher with the key
        cipher_suite = Fernet(enc_key)

        # Decrypt and deserialize the data
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        device_list = eval(decrypted_data.decode())

        return device_list

    except OSError: # file not found
        return {}


#{'deviceid':deviceid,'devicetype':list(device_data.keys())[0]}

prefs_file_path = 'lightprefs.json'
hub_address = ('localhost', 8080)

print("Simulated IoT Device Controller")
print("This device listens for connection requests by other devices")
print("It 'registers' these devices once they request to connect the first time\n\n")

print("Loading encryption key")
enc_key = load_crypt_key()

if enc_key is None:
    print("Unable to locate/load encryption key.\nHint: In this demo, you can create it with ./Inits/createkey.py")
    exit(1)

print("Loading up devices list")
device_list = load_saved_devices(enc_key)

# Create a socket server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(hub_address)
server.listen(5)

print("is listening on port %s..." % hub_address[1])

while True:
    client_socket, addr = server.accept()
    print(f"Accepted connection from {addr}")
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()