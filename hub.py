"""
This module is the main HUB. It does the following: 1. It runs a server that listens for incoming
connections from devices 2. When a device connects, it checks to see if it is registered; if not it
registers it 3. It acts as a keypad / user interface with which the user can access functions on
connected devices
"""

import json
import socket
import threading

import utils


def handle_device(device_socket, device_address):
    """
    Handles incoming connection requests from devices

    Args:
        device_socket (Socket object): Socket object of the connecting device. device_address (str):
        Address from which the device connected.

    Returns:
        Null
    """

    # Read the incoming message from the connected device socket
    request = device_socket.recv(1024)

    # If the device has disconnected, break out
    if not request:
        return

    # Decrypt the message using the utils.decrypt_message function
    request_data = utils.decrypt_message(request, hub_private_key)

    # If the message contains the 'action' field and the credentials sent through by the device are
    # correct
    if (
        "action" in request_data
        and request_data["user"] == SERVER_USER
        and request_data["pass"] == SERVER_PASS
    ):
        # Get the 'devid' (device id) field in the message
        deviceid = request_data["devid"]

        # If the device id is not registered
        if deviceid not in device_list:
            print(
                f"New {request_data['devtype']} device connected with identifier {deviceid} \
                from {device_address}"
            )

            # Register the device info in the device_list dict Device info stored include the device
            # id, device socket and device type
            device_list[deviceid] = {
                "socket": device_socket,
                "devtype": request_data["devtype"],
            }

            print("Device registered")

            # Call the save_device_list function to save the device_list dict to disk in encrypted
            # format
            if save_device_list():
                # If the operation succeeds, inform user
                print("Device list saved to disk")
            else:
                # If not successful, inform user
                print("Unable to save device list to disk")

        else:  # Otherwise (if the device id IS registered)
            # Obtain the registered device's socket and device type and update these in the
            # device_list dict
            device_list[deviceid] = {
                "socket": device_socket,
                "devtype": request_data["devtype"],
            }
            print(
                f"Registered {request_data['devtype']} device {deviceid} connected from \
                {device_address}."
            )

        # Send a (secure encrypted) message to the device through its socket informing it that
        # connection was successful
        msg = {"result": "success"}
        utils.send_encrypted_message(device_socket, msg, dev_public_key)

    # Otherwise (if the message DID NOT contain the 'action' field OR the credentials sent through
    # by the device are incorrect
    else:
        print(
            f"Connection request from {device_address} invalid (credentials invalid or didn't \
            make connection request)"
        )
        # Send a (secure encrypted) message to the device through its socket informing it of failure
        msg = {"result": "failure"}
        utils.send_encrypted_message(device_socket, msg, dev_public_key)

        # Reject the connection and just break out
        return


def list_all_devices(connected=False):
    """
    Helper function that returns a text list of (connected) devices in the device_list dict.

    Args:
        connected (bool): Whether or not to return connected devices only (or otherwise ALL
        devices).

    Returns:
        str: Numbered list of devices in format "[num]: deviceid" OR "--None--".
    """

    # If displaying connected devices only
    if connected:
        # Generate a list of keys of the devices that have actual sockets (as opposed to having
        # None)
        devlistkeys = [
            k for k in device_list.keys() if device_list[k]["socket"] is not None
        ]
    else:
        # Generate a list of keys of all the devices in the list
        devlistkeys = list(device_list.keys())

    # Use the device keys list to generate a list of strings in the format num: deviceid
    devlist = [f"{ind}: {k}" for ind, k in enumerate(devlistkeys)]

    # If the list is empty, return "--None--"
    if not devlist:
        return "--None--"

    # (Otherwise, if the list was not empty) Join up the list with newlines and return it (ready for
    # printing out)"
    return "\n".join(devlist)


def list_devices_get_selection(displayall=False):
    """
    Helper function that: 1. Displays a numbered list of connected devices in the device_list dict,
    and optionally also a final option in the list "ALL" referring to all devices; 2. Get and return
    the option selected

    Args:
        displayall (bool): Whether or not to display an option "ALL" in the list referring to all
        devices.

    Returns:
            tuple: A tuple containing the following elements: - str: The option selected from the
            list - a number encoded as a string. - list: List containing connected devices. - list:
            List containing keys of connected devices. - str: Message containing any issues
            encountered, to be displayed to user
    """

    # Generate a list of the keys of all connected devices i.e. devices that have a valid socket
    devlistkeysconn = [
        k for k in device_list.keys() if device_list[k]["socket"] is not None
    ]

    # If there are no items in the connected devices keys list, bail out
    if not devlistkeysconn:
        return None, None, None, "No connected devices"

    # Using the connected device keys, generate a list of the actual devices
    devlistconn = [device_list[k] for k in devlistkeysconn]

    # Display the devices list to the screen
    print("\nConnected Devices (please select one):")
    print("\n".join([f"{ind}: {k}" for ind, k in enumerate(devlistkeysconn)]))

    # If displaying the "ALL" option, do so
    if displayall:
        print(f"{len(devlistkeysconn)}: ALL")

    # Get the user's response
    devopt = input("\nSelected device: ")

    # Attempt to convert the user's input to an integer; if this fails, then the user decided to
    # type in some other garbage Then bail out
    try:
        devopt = int(devopt.lower().strip())
    except ValueError:
        return None, None, None, "Invalid input"

    # Ok at this point the user's response has been converted to an integer without issue

    # The if block below checks to make sure that the user's response integer falls in range
    if displayall:
        # If we are displaying the extra ALL option, then the check of invalidity is whether the
        # user typed in (a zero-based index) greater than the number of items in the list E.g. if we
        # have a list of connected devices containing 2 items (2 devices), device 1 will have a
        # displayed index of 0; and device 2 will have a displayed index of 1; ALL will then be
        # index 2 So the check of invalidity is whether the user typed something greater than 2
        # (Which is the list length)
        cond = devopt > len(devlistconn)
    else:
        # If we are not displaying the extra ALL option, then the check of invalidity is whether the
        # user typed in (a zero-based index) greater than equal to the number of items in the list
        # E.g. if we have a list of connected devices containing 2 items (2 devices), device 1 will
        # have a displayed index of 0; and device 2 will have a displayed index of 1; and that's all
        # in the list; So the check of invalidity is whether the user typed something greater than
        # OR equal to 2 (Which is the list length)
        cond = devopt >= len(devlistconn)

    # So if the user typed in a value less than 0 or the condition above is met then bail out; user
    # typed in invalid option
    if devopt < 0 or cond:
        return None, None, None, "Invalid input. Please enter a value from the menu."

    # (Otherwise if the option was valid and in range) return the option chose, the list of devices
    # and the their keys; as well as a success message
    return devopt, devlistconn, devlistkeysconn, "Success"


def send_msg_get_response(msg, devopt, devlistconn, devlistkeysconn):
    """
    Helper function that sends a given message to a given device and retrieves its response.

    Args:
        msg (dict): A dict containing the message to send. devopt (int): Index of the device to send
        the message to. devlistconn (list): List of connected devices into which the devopt index
        applies devlistkeysconn (list): List of keys of the connected devices into which the devopt
        index applies


    Returns:
        Two-tuple: str: The result field returned by the device, to be displayed (or None). str:
        Error message if encountered.
    """

    # Use the utils.send_encrypted_message function to send the message msg to the device socket If
    # that fails, bail out with error message
    if not utils.send_encrypted_message(
        devlistconn[devopt]["socket"], msg, dev_public_key
    ):
        return None, "Failed to send message to device"

    try:
        # Attempt to read from the device
        request = devlistconn[devopt]["socket"].recv(1024)

        # If the read is not successful, set the device socket in the device_list to None i.e. not
        # connected Also, bail out with error message
        if not request:
            device_list[devlistkeysconn[devopt]]["socket"] = None
            return None, "Unable to connect to the device. Aborting..."

    except:
        # If anything goes wrong, bail out with error message
        return None, "Unable to connect to the device. Aborting..."

    # Ok great; message was received from the device successfully... Use utils.decrypt_message to
    # decrypt incoming message
    request_data = utils.decrypt_message(request, hub_private_key)

    # If the message for some reason doesn't contain a result field, bail out with error message
    if not "result" in request_data:
        return None, "Message not understood..."

    # Otherwise (if all is well) return the result field of the response from the device
    return request_data["result"], "Success"


def menu_interface():
    """
    Helper function that displays a menu to the user, receives the user's response, validates it,
    and does the necessary accordingly.

    Returns:
        Nothing.
    """

    # Build the menu as a dict If you (whoever) wants to add any items to the list, you can safely
    # add them in by providing a unique key to each item. It you're not sure what a key is, you may
    # look up dict in Python For each item you add in, you will need to add code in the if statement
    # in the while loop below to handle the action by referring to the unique list item key
    menu = {}
    menu["alldev"] = "List all registered devices"
    menu["condev"] = "List connected devices"
    menu["devread"] = "Get device readings"
    menu["thres"] = "Set device threshold"
    menu["act"] = "Activate device"
    menu["deact"] = "Deactivate device"
    menu["on"] = "Switch on device"
    menu["off"] = "Switch off device"
    menu["disc"] = "Disconnect device from HUB"
    menu["quit"] = "Quit"

    # Get a list of the menu keys to be used to refer to the menu items nice and logically below So
    # this list will contain ['alldev','condev','devread', ..., 'quit'] (see menu above)
    menukeys = list(menu.keys())
    # Build a text of the actual menu in the format: [index]: Menu item text. So menutxt will
    # contain: 0: List all registered devices 1: List connected devices . . (omitted for brevity) .
    # 9: Quit
    menutxt = "\n".join([f"{menukeys.index(k)}: {menu[k]}" for k in menukeys])

    # Keep the menu going until the user quits
    while True:
        # Display the menu
        print("\n\nHUB Interface Menu:")
        print(menutxt + "\n")

        # Get the user's choice
        choice = input("Enter your choice: ")

        # Attempt to convert to an integer or otherwise Raise a ValueError
        try:
            choice = int(choice.lower().strip())
        except ValueError:
            print("Invalid input. Please enter a value from the menu.")
            continue

        # Ok choice is converted, but check to make sure its in range "In range" here depends on how
        # many items are in the list, so it shouldn't be less than 0 (first list item) or greater
        # than the number of items in the list
        if choice < 0 or choice >= len(menukeys):
            print("Invalid input. Please enter a value from the menu.")
            continue

        # This try is just in case something goes wrong while doing any of the operations below
        try:
            # Get the key of the option specified by the user So remember that the keys list will
            # contain ['alldev','condev','devread', ..., 'quit'] (see menu above) So e.g. if user
            # selected 0, choice which is menukeys[choice] will be 'alldev' etc.

            choicekey = menukeys[choice]

            # Ok great, now we can refer to choicekeys to figure out what the user typed in This
            # means that when adding to the menu above, we won't care what index the item is. So we
            # can just add items in there, and even though the indices of items might change we
            # won't have a problem, because we're checking the keys

            # If statement below handling each of the items in the menu. You can scroll up and look
            # at the menu dict to see what each item is/does. Most of the code below just calls the
            # functions that I've already commented before, so most should now be self-explanatory
            if choicekey == "alldev":
                # Display ALL registered devices
                print("Devices:")
                print(list_all_devices())

            elif choicekey == "condev":
                # Display registerded devices that are connected
                print("Connected devices:")
                print(list_all_devices(connected=True))

            elif choicekey == "thres":
                # Option to the set the threshold on a specific device

                # Use the list_devices_get_selection function to: display connected devices and get
                # user's selection Of a device
                (
                    devopt,
                    devlistconn,
                    devlistkeysconn,
                    resmsg,
                ) = list_devices_get_selection()
                if not devlistconn:
                    print(resmsg)
                    continue

                # Read in the user's desired threshold value
                thres = input("Specify threshold: ")

                # Attempt to convert threshold to number or other complain and bail out
                try:
                    thres = int(thres.lower().strip())
                except ValueError:
                    print("Invalid input")
                    continue

                # Ok great, we've got which device and the desired threshold Build a message to send
                # through
                msg = {"action": "set_thres", "value": thres}

                # Use the send_msg_get_response function to send the secure message to the device
                # and gets response
                result, errmsg = send_msg_get_response(
                    msg, devopt, devlistconn, devlistkeysconn
                )
                # If the device is offline or doesn't respond etc. complain and bail out
                if not result:
                    print(errmsg)
                    continue

                # Great; display the result of the operation received by the device
                print("Result: " + result)

            # Otherwise, if the chosen action is any of the ones in the list below
            elif choicekey in ["devread", "act", "deact", "on", "off", "disc"]:
                # So for all these actions, the sequence is the same:
                # 1.  We'll build a message
                # 2.  We'll display a list of connected devices and get the user's selection (which
                # can also be ALL) 3a. If the user chose a specific device, then send the message to
                # that device, retrieve the result and display it 3b. If the user chose ALL, send
                # the message every device, retrieve the result and display it

                # Build a dict of the specific messages for each action
                msgs = {
                    "devread": {"action": "get_readings"},
                    "act": {"action": "set_activate"},
                    "deact": {"action": "set_deactivate"},
                    "on": {"action": "set_on"},
                    "off": {"action": "set_off"},
                    "disc": {"action": "set_disconnect"},
                }
                # Get the message for this specific message
                msg = msgs[choicekey]

                # Display a list of connected devices and get the user's selection which can also be
                # ALL
                (
                    devopt,
                    devlistconn,
                    devlistkeysconn,
                    resmsg,
                ) = list_devices_get_selection(displayall=True)
                # If nothing returned in the list (which could also mean that something went wrong
                # in the function) Display the returned error message
                if not devlistconn:
                    print(resmsg)
                    continue

                # If the option chosen was not the ALL option i.e. a specific device
                if devopt < len(devlistconn):
                    # Use the send_msg_get_response function to send the secure message to the
                    # device and get its response
                    result, errmsg = send_msg_get_response(
                        msg, devopt, devlistconn, devlistkeysconn
                    )

                    # If nothing returned in the list (which could also mean that something went
                    # wrong in the function) Display the returned error message
                    if not result:
                        print(errmsg)
                        continue
                    # Display the result from the device
                    print("Result: " + json.dumps(result))

                    # If this was a disconnection operation then also set the associated device's
                    # socket to None in the device_list, meaning disconnected
                    if choicekey == "disc":
                        device_list[devlistkeysconn[devopt]]["socket"] = None

                else:
                    # For every device in the connected devices list
                    for ind in range(len(devlistconn)):
                        # Use the send_msg_get_response function to send the secure message to this
                        # device and get its response
                        result, errmsg = send_msg_get_response(
                            msg, ind, devlistconn, devlistkeysconn
                        )

                        # If nothing returned in the list (which could also mean that something went
                        # wrong in the function) Display the returned error message
                        if not result:
                            print(errmsg)
                            continue

                        # Display this device's result
                        print(f"{devlistkeysconn[ind]} result: " + json.dumps(result))

                        # If this was a disconnection operation then also set the associated
                        # device's socket to None in the device_list, meaning disconnected
                        if choicekey == "disc":
                            # device_list[devlistkeysconn[devopt]]["socket"].close()
                            device_list[devlistkeysconn[ind]]["socket"] = None

            # Quit option
            elif choicekey == "quit":
                print("Quiting...")

                # Code below: get a list of all devices that are connected i.e. socket is not None
                # Then loop through them and close() them
                devlistkeys = [
                    k
                    for k in device_list.keys()
                    if device_list[k]["socket"] is not None
                ]
                devlist = [device_list[k] for k in devlistkeys]
                for dev in devlist:
                    dev["socket"].close()

                # And finally, close the hub's connection as well
                hub.close()
                # Break out of the while loop
                break
        except:
            print("Something went wrong.")


def load_device_list():
    """
    Helper function that loads and decrypts the device_list from disk (which would contain the
    device ids and device types), and builds and returns a dict of ALL registered devices where each
    device's key is its device id, and each entry is itself a dict containing fields 'socket' which
    is initially None, and devtype which is the device type. E.g. might be something like (so you
    can visualize it): { 'smartlight1': {'socket':None, 'devtype':'SmartLight'}, 'motionsensor2':
    {'socket':None, 'devtype':'MotionSensor'} }


    Args:
        None.

    Returns:
        dict: Either dict of all registered devices or {}
    """

    # Load and decrypt device list from disk.
    devlist = utils.load_and_decrypt_fernet(fer_key, "./stored_devices.bin")

    if not devlist:
        # If the list is empty i.e. either file not found or list is empty, return empty dict
        return {}

    # Build the list as specified above
    return {k: {"socket": None, "devtype": devlist[k]["devtype"]} for k in devlist}


def save_device_list():
    """
    Helper function that builds, encrypts and saves and a dict of ALL registered devices where each
    device's key is its device id, and associated value is the devtype which is the device type.
    E.g. might be something like (so you can visualize it): { 'smartlight1': 'SmartLight',
    'motionsensor2': 'MotionSensor' }

    Args:
        Nothing.

    Returns:
        Result of the save operation.
    """

    # Build dict to save
    devlist = {k: {"devtype": device_list[k]["devtype"]} for k in device_list.keys()}

    # Call the utils.encrypt_and_save_fernet function to encrypt and save the dict to disk and
    # return its value
    return utils.encrypt_and_save_fernet(devlist, fer_key, "./stored_devices.bin")


if __name__ == "__main__":
    # Server credentials. Note that these need to match whatever encrypted credentials were
    # generated using 'initialise.py' file
    SERVER_USER = "user1"
    SERVER_PASS = "user1password"

    print("Simulated IoT Device Controller HUB")
    print("This device listens for connection requests by smart IoT devices")
    print("It 'registers' these devices once they request to connect the first time")
    print("It also allows the user to get access to the device functions\n\n")

    print(
        "\n Also, usually the protocol would require exchange of public keys for secure \
            communications."
    )
    print(
        "In this demo, we are assuming this has been done and the public keys have been generated \
            and exchanged."
    )
    print(
        "For demo purposes, the hub and all devices public keys have been generated using the \
            './initialise.py' script."
    )
    print(
        "They will be loaded from file by hub and devices and used for communications"
    )
    # Load the HUB private key for decryption of communications
    _, hub_private_key = utils.load_keys(None, "./Secrets/hub_prv.key")
    # Load the device public key for encryption of communications
    dev_public_key, _ = utils.load_keys("./Secrets/dev_pub.key", None)
    # Load the fernet key for enc/decryption of the saved devices list
    fer_key = utils.load_fernet_key("./Secrets/dev_enc.key")

    # Check to make sure that the keys are not None which means either they weren't found or
    # couldn't be loaded for whatever reason, meaning nothing can continue; no keys, no HUB
    try:
        assert (
            hub_private_key is not None
        ), "No HUB private key found. Please generate it by running './initialise.py'"
        assert (
            dev_public_key is not None
        ), "No device public key found. Please generate it by running './initialise.py'"
        assert (
            fer_key is not None
        ), "No encryption key found. Please generate it by running './initialise.py'"
    except Exception as e:
        print(f"\n\nERROR: key(s) not found: {e}")
        print("Exiting...")
        exit(1)

    # Load the device list
    device_list = load_device_list()

    # Start the menu interface in a separate thread
    menu_thread = threading.Thread(target=menu_interface)
    menu_thread.daemon = True
    menu_thread.start()

    # Use socket to set up this HUB server
    hub = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hub.bind(("127.0.0.1", 8080))
    hub.listen(5)

    # Continuously wait for client connection requests and handle them appropriately
    while True:
        try:
            client_socket, client_address = hub.accept()

            # Message received; create a new thread and handover this request to the handle_device
            # function to handle it
            device_thread = threading.Thread(
                target=handle_device, args=(client_socket, client_address)
            )
            device_thread.start()
        except:
            break
