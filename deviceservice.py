import socket
import json
import random
import threading
import time
import os

import utils
from device import *

def simulate_data_update():
    #Smart lock in this implementation doesn't have any sensors
    if isinstance(device,SmartLock):
        return

    while running:
        # Simulate data update from sensors
        device.sense()
        time.sleep(5)


if __name__ == "__main__":

    DEVICE_LIST = [SmartLight("Light1", threshold=50),
                  SmartLight("Light2",threshold=30),
                  SmartLight("Light1",threshold=80),
                  MotionSensor("Motion1",threshold=5),
                  MotionSensor("Motion2",threshold=8),
                  MotionSensor("Motion3",threshold=3),
                   SmartLock("Lock1"),
                   SmartLock("Lock2"),
                   SmartLock("Lock3"),
                  Thermostat("Therm1",threshold=23),
                   Thermostat("Therm2", threshold=30),
                  Thermostat("Therm3", threshold=15)
                  ]

    print("IoT Device Simulator.")
    print("The server username and password are hard-coded in this simulation to avoid making you have to type them over and over.")
    print("There is also a pre-defined list of simulated devices that you select from for convenience\n")
    print("Here's the pre-defined list of devices to link into the home:")
    for ind,dev in enumerate(DEVICE_LIST):
        print(f"{ind}: {dev}")
    devopt = int(input("Which device should this program instance simulate?: ").lower().strip())

    if devopt not in range(len(DEVICE_LIST)):
        print("Invalid device option. Please restart the program.")
        exit(1)

    device = DEVICE_LIST[devopt]

    print("\nSo usually, one would have to enter the server credentials. For this demo, this is skipped.")
    print("Rather, the credentials have been created and stored in encrypted format on disk using the './Inits/createecryptedservercredentials.py' script")
    #Load the Fernet key to decrypt the credentials file
    fer_key = utils.load_fernet_key("./Secrets/dev_enc.key")
    creds = utils.load_and_decrypt_fernet(fer_key,"./Secrets/creds.bin")

    print("\n Also, usually the protocol would require exchange of public keys for secure communications.")
    print("In this demo, I am assuming this has been done and the public keys have been generated and exchanged.")
    print("For demo purposes, the hub and devices' keys have been generated using the './Inits/createcryptokeys.py' script.")
    print("They will be loaded from file as relevant and used for communications by the device to the hub")

    hub_pub_key = utils.load_public_key("./Secrets/hub_pub.key")
    _, dev_private_key = utils.load_keys(None, "./Secrets/dev_prv.key")

    # vals = [-10,-5, -1, 1, 4, 5, 6, 7, 6, 5, 4, 5, 6, 7, 9, 10, 11, 23, 6, 5, 4, 5]
    #
    # for val in vals:
    #     print(f"Update to val {val}")
    #     device.set_value(val)
    #     print(device.get_readings())
    #     device.sense(val)
    #     print(device.get_readings())


    #To do: link up with server.

    print("\nAttempting to connect to the HUB using credentials...")
    hub = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        hub.connect(('127.0.0.1', 8080))
    except:
        print("Connection to the HUB failed...")
        hub.close()
        exit(1)

    # Build up the connection message
    connectmsg = {"action":"connect", "devid":device.identifier, 'devtype':device.__class__.__name__}
    # Add in the credentials
    connectmsg.update(creds)

    if utils.send_encrypted_message(hub,connectmsg,pub_key=hub_pub_key):
        print("Connection message sent.")
    else:
        print("Error sending connection message. Exiting...")
        exit(1)

    #Find out if connection was successful
    request = hub.recv(1024)

    if not request:
        print("Unable to connect to the hub. Aborting...")
        exit(1)

    request_data = utils.decrypt_message(request, dev_private_key)

    if not ('result' in request_data) or request_data['result'] != 'success':
        print("Unable to connect to the hub. Aborting...")
        exit(1)


    print("Connected to the HUB")

    running = True

    # Start data simulation thread
    update_thread = threading.Thread(target=simulate_data_update)
    update_thread.daemon = True
    update_thread.start()

    while True:
        try:
            # Receive requests from the HUB
            request = hub.recv(1024)

            if not request:
                break

            request_data = utils.decrypt_message(request,dev_private_key)

            print("Message received from HUB")

            if 'action' in request_data:

                action = request_data['action']

                # menu['thres'] = "Set device threshold"
                # menu['act'] = "Activate device"
                # menu['deact'] = "Deactivate device"
                # menu['on'] = "Switch on device"
                # menu['off'] = "Switch off device"

                if action == 'get_readings':
                    print("Request for readings received from HUB")
                    msg = {"result":device.get_readings()}
                    if utils.send_encrypted_message(hub,msg,hub_pub_key):
                        print("Readings sent to hub")
                    else:
                        print("Sending readings to hub failed!")

                elif action == 'activate':
                    pass
                elif action == 'deactivate':
                    pass
                elif action == 'on':
                    pass
                elif action == 'off':
                    pass

            else:
                print("Message not understood")

                # Process the "get_readings" request and send back a response

                # device.send(response.encode('utf-8'))

        except:
            print("Something went wrong...")
            break

    print("HUB closed connection. Closing...")
    hub.close()