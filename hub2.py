import socket
import threading
import utils

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
        devlistkeys = [k for k in device_list.keys() if device_list[k]["socket"] is not None]
    else:
        devlistkeys = [k for k in device_list.keys()]

    devlist = [f"{ind}: {k}" for ind, k in enumerate(devlistkeys)]

    if not devlist:
        return "--None--"

    return "\n".join(devlist)

def list_devices_get_selection(displayall=False):

    devlistkeysconn = [k for k in device_list.keys() if device_list[k]["socket"] is not None]

    if not devlistkeysconn:
        return None, None, None,"No connected devices"

    devlistconn = [device_list[k] for k in devlistkeysconn]

    print("\nConnected Devices (please select one):")
    print("\n".join([f"{ind}: {k}" for ind, k in enumerate(devlistkeysconn)]))
    if displayall:
        print(f"{len(devlistkeysconn)}: ALL")


    devopt = input("\nSelected device: ")

    try:
        devopt = int(devopt.lower().strip())
    except ValueError:
        return None, None, None,"Invalid input"

    if displayall:
        cond = devopt > len(devlistconn)
    else:
        cond = devopt >= len(devlistconn)

    #Used to be devopt >= len(devlistconn); adding an item for "ALL"
    if devopt < 0 or cond:
        return None, None, None,"Invalid input. Please enter a value from the menu."

    return devopt, devlistconn, devlistkeysconn, "Success"

def send_msg_get_response(msg, devopt, devlistconn, devlistkeysconn):

    # devopt, devlistconn, devlistkeysconn, resmsg = list_devices_get_selection()

    # if not devlistconn:
    #     # print(resmsg)
    #     return None, resmsg

    if not utils.send_encrypted_message(devlistconn[devopt]["socket"], msg, dev_public_key):
        return None,"Failed to send message to device"

    try:
        # Find out if connection was successful
        request = devlistconn[devopt]["socket"].recv(1024)

        if not request:
            device_list[devlistkeysconn[devopt]]["socket"] = None
            return None,"Unable to connect to the device. Aborting..."

    except:
        return None,"Unable to connect to the device. Aborting..."

    request_data = utils.decrypt_message(request, hub_private_key)

    if not ('result' in request_data):
        return None,"Message not understood..."

    return request_data['result'], "Success"

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
    menu['disc'] = "Disconnect device from HUB"
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

                msg = {"action": "get_readings"}
                devopt, devlistconn, devlistkeysconn, resmsg = list_devices_get_selection()
                if not devlistconn:
                    print(resmsg)
                    continue

                result,errmsg = send_msg_get_response(msg, devopt, devlistconn, devlistkeysconn)
                if not result:
                    print(errmsg)
                    continue

                print("Device readings:")
                print(result)

            elif choicekey == 'thres':

                thres = input("Specify threshold: ")

                try:
                    thres = int(thres.lower().strip())
                except ValueError:
                    print("Invalid input")
                    continue

                msg = {"action": "set_thres", "value":thres}
                devopt, devlistconn, devlistkeysconn, resmsg = list_devices_get_selection()
                if not devlistconn:
                    print(resmsg)
                    continue

                result, errmsg = send_msg_get_response(msg, devopt, devlistconn, devlistkeysconn)
                if not result:
                    print(errmsg)
                    continue

                print("Result:" + result)


            elif choicekey == 'act':
                msg = {"action": "set_activate"}
                devopt, devlistconn, devlistkeysconn, resmsg = list_devices_get_selection(displayall=True)
                if not devlistconn:
                    print(resmsg)
                    continue

                if devopt < len(devlistconn):

                    result,errmsg = send_msg_get_response(msg, devopt, devlistconn, devlistkeysconn)
                    if not result:
                        print(errmsg)
                        continue

                else:

                    for ind in range(len(devlistconn)):
                        result, errmsg = send_msg_get_response(msg, ind, devlistconn, devlistkeysconn)
                        if not result:
                            print(errmsg)
                            continue
                        print(f"{devlistkeysconn[ind]} result:" + result)




            elif choicekey == 'deact':
                msg = {"action": "set_deactivate"}

                devopt, devlistconn, devlistkeysconn, resmsg = list_devices_get_selection()
                if not devlistconn:
                    print(resmsg)
                    continue

                result,errmsg = send_msg_get_response(msg, devopt, devlistconn, devlistkeysconn)
                if not result:
                    print(errmsg)
                    continue

                print("Result:" + result)

            elif choicekey == 'on':
                msg = {"action": "set_on"}
                devopt, devlistconn, devlistkeysconn, resmsg = list_devices_get_selection()
                if not devlistconn:
                    print(resmsg)
                    continue

                result,errmsg = send_msg_get_response(msg, devopt, devlistconn, devlistkeysconn)
                if not result:
                    print(errmsg)
                    continue

                print("Result:" + result)

            elif choicekey == 'off':
                msg = {"action": "set_off"}
                devopt, devlistconn, devlistkeysconn, resmsg = list_devices_get_selection()
                if not devlistconn:
                    print(resmsg)
                    continue

                result,errmsg = send_msg_get_response(msg, devopt, devlistconn, devlistkeysconn)
                if not result:
                    print(errmsg)
                    continue

                print("Result:" + result)

            elif choicekey == 'disc':
                msg = {"action": "set_disconnect"}
                devopt, devlistconn, devlistkeysconn, resmsg = list_devices_get_selection()
                if not devlistconn:
                    print(resmsg)
                    continue

                result,errmsg = send_msg_get_response(msg, devopt, devlistconn, devlistkeysconn)
                if not result:
                    print(errmsg)
                    continue

                print("Result:" + result)

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



