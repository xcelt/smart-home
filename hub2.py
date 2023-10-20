import socket
import json
import random
import threading
import time
import os
from cryptography.fernet import Fernet
import utils
from device import *

def print_out(d):
    pass
    # print(d)

def handle_device(device_socket, device_address):
    # while True:
    #     client_socket, client_address = hub.accept()
    #
    #     device_thread = threading.Thread(target=handle_device, args=(client_socket, client_address))
    #     device_thread.start()

    request = device_socket.recv(1024)

    if not request:
        return

    request_data = utils.decrypt_message(request, hub_private_key)
    # request_data = json.loads(request.decode('utf-8'))

    if 'action' in request_data and request_data['user']==server_user and request_data['pass']==server_pass:
        deviceid = request_data['devid']
        if deviceid not in device_list:
            print_out(f"New {request_data['devtype']} device connected with identifier {deviceid} from {device_address}")
            device_list[deviceid] = {"socket":device_socket,"devtype":request_data['devtype']}

            print_out(f"Device registered")

            if save_device_list():
                print_out("Device list saved to disk")
            else:
                print_out("Unable to save device list to disk")
        else:
            device_list[deviceid] = {"socket":device_socket,"devtype":request_data['devtype']}
            print_out(f"Registered {request_data['devtype']} device {deviceid} connected from {device_address}.")


        msg = {"result": "success"}
        utils.send_encrypted_message(device_socket,msg,dev_public_key)


    else:
        print_out(f"Connection request from {device_address} invalid (credentials invalid or didn't make connection request)")
        msg = {"result":"failure"}
        utils.send_encrypted_message(device_socket,msg,dev_public_key)
        return


    # while True:
    #     request = device_socket.recv(1024).decode('utf-8')
    #     if not request:
    #         break
    #     # Handle requests sent by the device
    #     if request == "get_readings":
    #         # Forward the request to the device
    #         device_socket.send("Request: get_readings".encode('utf-8'))
    #
    # # Device disconnected
    # device_list[deviceid] = None
    # print(f"Device {deviceid} disconnected.")
    # device_socket.close()

def list_all_devices(connected=False):

    if connected:
        devlist = [f"{ind}: {k}" for ind, k in enumerate(device_list.keys()) if device_list[k]["socket"] is not None]
    else:
        devlist = [f"{ind}: {k}" for ind, k in enumerate(device_list.keys())]

    if not devlist:
        return "--None--"

    return "\n".join(devlist)



def menu_interface():
    menu = {}
    menu['alldev'] = "List all registered devices"
    menu['condev'] = "List connected devices"
    menu['devread'] = "Get device readings"
    menu['thres'] = "Set device threshold"
    menu['act'] = "Activate device"
    menu['deact'] = "Deactivate device"
    menu['on'] = "Switch on device"
    menu['off'] = "Switch off device"
    menu['quit'] = "Quit"

    menukeys = list(menu.keys())
    menutxt = "\n".join([f"{menukeys.index(k)}: {menu[k]}" for k in menukeys])

    while True:
        print("\n\nHUB Interface Menu:")
        print(menutxt + "\n")

        choice = input("Enter your choice: ")

        try:
            choice = int(choice.lower().strip())
        except ValueError:
            print("Invalid input. Please enter a value from the menu.")
            continue

        if choice < 0 or choice >= len(menukeys):
            print(f"Invalid input. Please enter a value from the menu.")
            continue

        try:
            choicekey = menukeys[choice]

            if choicekey == "alldev":
                print("Devices:")
                print(list_all_devices())

            elif choicekey == 'condev':
                print("Connected devices:")
                print(list_all_devices(connected=True))

            elif choicekey == 'devread':

                devlistkeys = [k for k in device_list.keys() if device_list[k]["socket"] is not None]
                devlist = [device_list[k] for k in devlistkeys]
                if not devlist:
                    print("No connected devices")
                    continue

                print("Connected Devices:")
                print(list_all_devices(connected=True))

                devopt = input("Select device: ")

                try:
                    devopt = int(devopt.lower().strip())
                except ValueError:
                    print("Invalid input.")
                    continue


                if devopt < 0 or devopt >= len(devlist):
                    print(f"Invalid input. Please enter a value from the menu.")
                    continue

                msg = {"action":"get_readings"}
                if not utils.send_encrypted_message(devlist[devopt]["socket"],msg,dev_public_key):
                   print("Failed to send message to device")
                   continue

                try:
                    # Find out if connection was successful
                    request = devlist[devopt]["socket"].recv(1024)

                    if not request:
                        print("Unable to connect to the device. Aborting...")
                        device_list[devlistkeys[devopt]]["socket"] = None
                        continue

                except:
                    print("Unable to connect to the device. Aborting...")
                    continue

                request_data = utils.decrypt_message(request, hub_private_key)

                if not ('result' in request_data):
                    print("Unable to connect to the hub. Aborting...")
                    continue

                print("Device readings:")
                print(request_data['result'])



            elif choicekey == 'thres':
                print("Set threshold")

            elif choicekey == 'act':
                print("Activate")

            elif choicekey == 'deact':
                print("Deactivate")

            elif choicekey == 'on':
                print("Switch on")

            elif choicekey == 'off':
                print("Switch off")

            elif choicekey == 'quit':
                print("Quiting...")
                devlistkeys = [k for k in device_list.keys() if device_list[k]["socket"] is not None]
                devlist = [device_list[k] for k in devlistkeys]
                for dev in devlist:
                    dev['socket'].close()
                hub.close()
                break
        except:
            print("Something went wrong.")

def load_device_list():
    devlist = utils.load_and_decrypt_fernet(fer_key, "./stored_devices.bin")

    if not devlist:
        return {}
    else:
        return {k:{"socket":None, "devtype":devlist[k]["devtype"]} for k in devlist}

def save_device_list():

    devlist = {k:{"devtype":device_list[k]["devtype"]} for k in device_list.keys()}

    return utils.encrypt_and_save_fernet(devlist, fer_key, "./stored_devices.bin")

    # device_list[deviceid] = {"socket":device_socket,"devtype":request_data['devtype']}



if __name__ == "__main__":

    server_user = "user1"
    server_pass = "user1password"

    print("Simulated IoT Device Controller HUB")
    print("This device listens for connection requests by smart IoT devices")
    print("It 'registers' these devices once they request to connect the first time")
    print("It also allows the user to get access to the device functions\n\n")

    print("\n Also, usually the protocol would require exchange of public keys for secure communications.")
    print("In this demo, I am assuming this has been done and the public keys have been generated and exchanged.")
    print("For demo purposes, the hub and all devices public keys have been generated using the './Inits/createcryptokeys.py' script.")
    print("They will be loaded from file by hub and devices and used for communications")
    # Load the private key for decryption of communications
    _, hub_private_key = utils.load_keys(None, "./Secrets/hub_prv.key")
    dev_public_key, _ = utils.load_keys("./Secrets/dev_pub.key", None)
    fer_key = utils.load_fernet_key("./Secrets/dev_enc.key")


    device_list = load_device_list()


    # Start the menu interface in a separate thread
    menu_thread = threading.Thread(target=menu_interface)
    menu_thread.daemon = True
    menu_thread.start()

    hub = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hub.bind(('127.0.0.1', 8080))
    hub.listen(5)

    while True:
        try:
            client_socket, client_address = hub.accept()

            device_thread = threading.Thread(target=handle_device, args=(client_socket, client_address))
            device_thread.start()
        except:
            break



