'''
This module simulates IoT devices (currently MotionSensor, SmartLight, SmartLock and Thermostat).
While it can be customized, for demo purposes, we've provided a list of pre-defined devices (which can be seamlessly added to)
It does the following:
1. The user can specify one of the pre-defined devices to simulate
2. The simulated device then attempts to connect to the HUB (which should be already running)
3. If connection is successful, the device then waits for requests/instructions from the HUB and executes them as they come in

Note: multiple instances of this module can be run at the same time to simulate multiple devices connecting to the HUB
Also note: because this is a simulation, it is possible to select the same device in two or more instances of this script e.g.
selecting Light1 in both/all; the HUB will simply take the most recent copy and connect to that
'''

import socket
import threading
import time

import utils
from device import *

def simulate_data_update():
    """
    Simulate data updates to the sensor of the selected device at regular intervals.
    This function runs in a separate thread
    """
    #Smart lock in this implementation doesn't have any sensors, so do nothing if it is
    if isinstance(device,SmartLock):
        return

    while running:
        # Simulate data update from sensors
        device.sense()
        time.sleep(5)


if __name__ == "__main__":

    #This is the pre-defined list of sensors. Feel free to add to it, ensuring that
    #the identifiers are unique
    DEVICE_LIST = [SmartLight("Light1", threshold=50),
                  SmartLight("Light2",threshold=30),
                  SmartLight("Light3",threshold=80),
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

    # Display numbered list with format: index: Device E.g. will be:
    #
    #     0: SmartLight| {"identifier": "Light1", "status": "active", "threshold": 50, "switch": "on", "brightness": 90}
    #     1: SmartLight| {"identifier": "Light2", "status": "active", "threshold": 30, "switch": "on", "brightness": 90}
    #     2: SmartLight| {"identifier": "Light3", "status": "active", "threshold": 80, "switch": "on", "brightness": 90}
    #     3: MotionSensor| {"identifier": "Motion1", "status": "active", "threshold": 5, "switch": "on", "motion": 0}
    #         .
    #         .
    #         .
    #     10: Thermostat| {"identifier": "Therm2", "status": "active", "threshold": 30, "switch": "on", "temp": 15.0}
    #     11: Thermostat| {"identifier": "Therm3", "status": "active", "threshold": 15, "switch": "on", "temp": 15.0}

    for ind,dev in enumerate(DEVICE_LIST):
        print(f"{ind}: {dev}")

    #Get the user's chosen device
    devopt = input("Which device should this program instance simulate?: ")

    #Attempt to convert the option to an integer, if it fails, bail out. Game over.
    try:
        devopt = int(devopt.lower().strip())
    except ValueError:
        print("Invalid device option. Please restart the program.")
        exit(1)

    # If the integer entered doesn't match with the items in the list bail out. Game over.
    if devopt not in range(len(DEVICE_LIST)):
        print("Invalid device option. Please restart the program.")
        exit(1)

    # Get the actual device selected; this is the device for this instance.
    device = DEVICE_LIST[devopt]

    print("\nSo usually, one would have to enter the server credentials. For this demo, for convenience and demo purposes this is skipped.")
    print("Rather, the credentials have been created and stored in encrypted format on disk using the './Inits/createecryptedservercredentials.py' script")
    print("They will be loaded, decrypted and used")


    #Load the Fernet key to decrypt the credentials file
    fer_key = utils.load_fernet_key("./Secrets/dev_enc.key")


    print("\n Also, usually the protocol would require exchange of public keys for secure communications.")
    print("In this demo, we are assuming this has been done and the public keys have been generated and exchanged.")
    print("For demo purposes, the hub and devices' keys have been generated using the './Inits/initializeAll.py' script.")
    print("They will be loaded from file as relevant and used for communications by the device to the hub")
    print("Finally, for demo purposes, we are assuming that all the devices will use the same private/public key")

    #Load the HUB public key and device private key for encryption purposes
    hub_pub_key = utils.load_public_key("./Secrets/hub_pub.key")
    #Load the device private key for decryption purposes
    _, dev_private_key = utils.load_keys(None, "./Secrets/dev_prv.key")

    #Check to make sure that the keys are not None which means either they weren't found or couldn't be loaded for
    #whatever reason, meaning nothing can continue; no keys, no Device service (or HUB)
    try:
        assert hub_pub_key is not None, "No HUB public key found. Please generate it by running './Inits/initializeAll.py'"
        assert dev_private_key is not None, "No device private key found. Please generate it by running './Inits/initializeAll.py'"
        assert fer_key is not None, "No encryption key found. Please generate it by running './Inits/initializeAll.py'"
    except Exception as e:
        print(f"\n\nERROR: key(s) not found: {e}")
        print("Exiting...")
        exit(1)

    #Load and decrypt the credentials from file
    creds = utils.load_and_decrypt_fernet(fer_key,"./Secrets/creds.bin")

    print("\nAttempting to connect to the HUB using credentials...")
    hub = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #If connection works, great; if not, close and exit.
    try:
        hub.connect(('127.0.0.1', 8080))
    except:
        print("Connection to the HUB failed...")
        hub.close()
        exit(1)

    # Build up the connection message
    # This will look something like this (IF light2 was selected from the list above):
    # {'action':'connect', 'devid':'Light2', 'devtype':'SmartLight'}
    connectmsg = {"action":"connect", "devid":device.identifier, 'devtype':device.__class__.__name__}

    # Add in the server credentials to the connection message
    connectmsg.update(creds)

    #Use the utils.send_encrypted_message function to encrypt and send the message
    #If it works, great. If not, bail out.
    if utils.send_encrypted_message(hub,connectmsg,pub_key=hub_pub_key):
        print("Connection message sent.")
    else:
        print("Error sending connection message. Exiting...")
        exit(1)

    #Message was sent, now get a response from the HUB
    request = hub.recv(1024)

    #If the connection is lost, bail out.
    if not request:
        print("Unable to connect to the hub. Aborting...")
        exit(1)

    #Decrypt the response from the HUB
    request_data = utils.decrypt_message(request, dev_private_key)

    #If the response doesn't contain the 'result' field or it does but the result is not 'success', bail out.
    if not ('result' in request_data) or request_data['result'] != 'success':
        print("Unable to connect to the hub. Aborting...")
        exit(1)


    print("Connected to the HUB")

    running = True

    # Start data simulation thread
    update_thread = threading.Thread(target=simulate_data_update)
    update_thread.daemon = True
    update_thread.start()

    # Continuously wait for HUB requests and handle them appropriately
    while True:
        try:
            # Receive requests from the HUB
            request = hub.recv(1024)

            if not request:
                break

            #Decrypt the message
            request_data = utils.decrypt_message(request,dev_private_key)

            print("Message received from HUB")

            if 'action' in request_data:

                action = request_data['action']


                if action == 'get_readings':
                    #Retreieve the device readings
                    print("Request for readings received from HUB")
                    msg = {"result":device.get_readings()}
                    if utils.send_encrypted_message(hub,msg,hub_pub_key):
                        print("Responded to HUB")
                    else:
                        print("Responding to hub failed!")

                elif action == 'set_thres':
                    #Set the device threshold
                    print("Request to set threshold received from HUB")
                    device.set_threshold(request_data['value'])
                    msg = {"result":"success"}
                    if utils.send_encrypted_message(hub,msg,hub_pub_key):
                        print("Responded to HUB")
                    else:
                        print("Responding to hub failed!")

                elif action == 'set_activate':
                    #Activate the device
                    #note that activation has different effects on the different devices in this simulation
                    #For SmartLight, it activates the automatic light sensor, so it will start using the threshold to turn on/off the light
                    #For MotionSensor and Thermostat it will start the device using the given threshold to issue alerts / adjust temperature
                    #For SmartLock this disables the lock and unlock functions
                    print("Request to set activate received from HUB")

                    if device.status == "active":
                        res = "already active"
                    else:
                        device.activate()
                        res = "success"

                    msg = {"result": res}
                    if utils.send_encrypted_message(hub, msg, hub_pub_key):
                        print("Responded to HUB")
                    else:
                        print("Responding to hub failed!")

                elif action == 'set_deactivate':
                    #Deactivate the device
                    #note that deactivation has different effects on the different devices in this simulation
                    #For SmartLight, it deactivates the automatic light sensor, so it will just remain either on or off depending on what it was
                    #For MotionSensor and Thermostat it will stop the device from using the given threshold
                    #For SmartLock this disables the lock and unlock functions
                    print("Request to set deactivate received from HUB")

                    if device.status == "deactive":
                        res = "already deactive"
                    else:
                        device.deactivate()
                        res = "success"

                    msg = {"result": res}
                    if utils.send_encrypted_message(hub, msg, hub_pub_key):
                        print("Responded to HUB")
                    else:
                        print("Responding to hub failed!")

                elif action == 'set_on':

                    #Turn on mean different things to the different devices in this simulation
                    #For SmartLight, it means deactivate the automatic light sensor and set it
                    #to on
                    #For MotionSensor and Thermostat it means start sensing motion/temperature
                    #For SmartLock it means lock, but only if the lock status is 'active'

                    print("Request to turn on received from HUB")
                    res = ""

                    if isinstance(device,SmartLight):
                        device.deactivate()
                        device.switch_on()
                        res = "Manual override (threshold deactivated); lighted switched on"

                    elif isinstance(device,MotionSensor):

                        if device.switch == "on":
                            res = "already on"
                        else:
                            device.switch_on()
                            res = "success - motion sensor engaged"

                    elif isinstance(device, SmartLock):
                        if device.status == "deactive":
                            res = "failure - lock is deactive"
                        else:
                            if device.switch == "on":
                                res = "already locked"
                            else:
                                device.lock()
                                res = "success - lock engaged"

                    elif isinstance(device, Thermostat):

                            if device.switch == "on":
                                res = "already on"
                            else:
                                device.switch_on()
                                res = "success - thermostat engaged"

                    #Send the response back to the HUB
                    msg = {"result": res}
                    if utils.send_encrypted_message(hub, msg, hub_pub_key):
                        print("Responded to HUB")
                    else:
                        print("Responding to hub failed!")

                elif action == 'set_off':
                    #Turn off means different things to the different devices in this simulation
                    #For SmartLight, it means deactivate the automatic light sensor and set it
                    #to off
                    #For MotionSensor and Thermostat it means stop sensing motion/temperature
                    #For SmartLock it means unlock, but only if the lock status is 'active'

                    print("Request to turn off received from HUB")
                    res = ""

                    if isinstance(device,SmartLight):
                        device.deactivate()
                        device.switch_off()
                        res = "Manual override (threshold deactivated); lighted switched off"

                    elif isinstance(device,MotionSensor):

                        if device.switch == "off":
                            res = "already off"
                        else:
                            device.switch_off()
                            res = "success - motion sensor disengaged"

                    elif isinstance(device, SmartLock):

                        if device.status == "deactive":
                            res = "failure - lock is deactive"
                        else:
                            if device.switch == "off":
                                res = "already unlocked"
                            else:
                                device.unlock()
                                res = "success - lock disengaged"


                    elif isinstance(device, Thermostat):
                        if device.switch == "off":
                            res = "already off"
                        else:
                            device.switch_off()
                            res = "success - thermostat disengaged"

                    #Send the result back to the HUB
                    msg = {"result": res}
                    if utils.send_encrypted_message(hub, msg, hub_pub_key):
                        print("Responded to HUB")
                    else:
                        print("Responding to hub failed!")

                elif action == "set_disconnect":
                    #Disconnect this device from the HUB. Close and shut down.
                    print("Request to disconnect received from HUB")
                    running = False

                    msg = {"result": "success"}
                    if utils.send_encrypted_message(hub, msg, hub_pub_key):
                        print("Responded to HUB. Shutting down...")
                    else:
                        print("Responding to hub failed! Oh oh!")

                    hub.close()
                    break

            else:
                print("Message not understood")

        except:
            print("Something went wrong...")
            running = False
            break

    print("HUB closed connection. Closing...")
    hub.close()