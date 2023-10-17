import socket
import json
import random
import threading
import time
import os

# Simulated device data
device_data = {
    'light': {
        'status': 'off',  #Whether the light is on or off
        'intensity': 95, #The intensity of ambient light in the room
        'threshold': 80, #The intensity threshold, beyond (and including) which the light will be turned off automatically
    },
}

def save_preferences(file_path, prefs_json):
    # Securely write the JSON to a file
    try:
        with open(file_path, 'w') as file:
            file.write(prefs_json)
        print("Light preferences saved to " + file_path)
    except Exception as e:
        print("Error:", str(e))

def load_preferences(file_path):
    try:
        with open(file_path, 'r') as file:
            prefs_json = json.load(file)
        return prefs_json
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error loading preferences from {file_path}: {str(e)}")
    return None

# Function to handle client requests
def handle_client(client_socket):
    while True:
        request = client_socket.recv(1024)
        if not request:
            break

        request_data = json.loads(request.decode('utf-8'))

        if 'action' in request_data:
            action = request_data['action']

            if action == 'get_intensity':
                print("Retrieving light intensity: %s" % (device_data['light']['intensity']))
                response = json.dumps({'intensity': device_data['light']['intensity']})
                client_socket.send(response.encode('utf-8'))

            elif action == 'get_status':
                print("Retrieving light status: %s" % (device_data['light']['status']))
                response = json.dumps({'status': device_data['light']['status']})
                client_socket.send(response.encode('utf-8'))

            elif action == 'set_status':
                if 'status' in request_data:
                    print("Setting light status: " + request_data['status'])
                    device_data['light']['status'] = request_data['status']
                response = json.dumps(device_data['light']['status'])
                client_socket.send(response.encode('utf-8'))

            elif action == 'set_threshold':
                if 'threshold' in request_data:
                    device_data['light']['threshold'] = request_data['threshold']
                response = json.dumps({'threshold': device_data['light']['threshold']})
                client_socket.send(response.encode('utf-8'))

            elif action == 'save_preferences':
                response = json.dumps({'threshold': device_data['light']['threshold']})
                save_preferences(prefs_file_path,response)
                client_socket.send(response.encode('utf-8'))

    client_socket.close()


# Simulate data updates
def simulate_data_update():
    while True:
        # Simulate data from sensors
        device_data['light']['intensity'] = device_data['light']['intensity'] + random.randint(-3, 3)

        if device_data['light']['intensity'] >= device_data['light']['threshold'] and device_data['light']['status'] == 'on':
            device_data['light']['status'] = 'off'
        if device_data['light']['intensity'] < device_data['light']['threshold'] and device_data['light']['status'] == 'off':
            device_data['light']['status'] = 'on'

        time.sleep(5)

def connect_to_hub():
    hub = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        hub.connect(hub_address)

        #Formulate connection message
        message = json.dumps({'action':'connect', 'deviceid':deviceid,'devicetype':list(device_data.keys())[0]})

        # Send the message
        hub.send(message.encode('utf-8'))

        response_data = hub.recv(1024).decode('utf-8')
        if response_data:
            response = json.loads(response_data)
            return response['connect']
        else:
                return None

    except Exception as e:
        return None
    finally:
        hub.close()

prefs_file_path = 'lightprefs.json'
server_address = ('localhost', 5000)
hub_address = ('localhost', 8080)

print("Simulated IoT Light Device")

if os.path.exists(prefs_file_path):
    if input("Load preferences from file? (Y/N): ").lower().strip() == "Y":
        response = load_preferences(prefs_file_path)

        if response is None:
            print("Error loading preferences from file. Loading default preferences.")
        else:
            device_data['light']['threshold'] = response['threshold']

# loadprefs = input("")

print("\nAttempting to connect to HUB:")
deviceid = input("Enter unique ID for this device: ")
hubresponse = connect_to_hub()

if hubresponse is None:
    print("Failed to connect to the hub. Aborting...")
    exit(1)
if hubresponse == 'reject':
    print("HUB rejected the request. Aborting...")
    exit(1)

print("Connected to HUB\n")
# Create a socket server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(server_address)
print("Listening on port %s..." % server_address[1])
server.listen(5)

# Start data simulation thread
update_thread = threading.Thread(target=simulate_data_update)
update_thread.daemon = True
update_thread.start()



print("is listening on port 5000...")

while True:
    client_socket, addr = server.accept()
    print(f"Accepted connection from {addr}")
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
