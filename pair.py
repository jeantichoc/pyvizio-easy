import json
import platform
import random

from pyvizio import Vizio

def get_computer_name():
    # Get the hostname from the environment variable
    computer_name = platform.node()
    # Remove the ".local" at the end of the hostname
    if computer_name.endswith(".local"):
        computer_name = computer_name[:-6]
    return computer_name + "-pyvizio"

def main():
    # Discover Vizio devices on the local network
    vizio_devices = Vizio.discovery_zeroconf(5)
    #print(vizio_devices)

    # Get the local computer name for ids and visibility
    computer_name=get_computer_name()

    # Pair each device and store the pairing information
    pairing_info = {}
    for index, device in enumerate(vizio_devices):
        ip = device.ip
        id = computer_name + "-" + str(index) + "-" + str(random.randint(1000000, 9999999))
        vizio = Vizio(id, ip, computer_name)

        # Start the pairing process
        pair_data = vizio.start_pair()

        if pair_data:
            # For TVs, lookup the PIN code on your TV and note challenge token and type in console
            # For speakers, press the physical "Volume Up" button and note challenge token and type in console
            pin = input(f"Enter the PIN displayed on your {device.name} device: ")
            ch_type = pair_data.ch_type
            token = pair_data.token

            # Finalize the pairing process
            pair_response = vizio.pair(ch_type, token, pin)

            # Store the pairing information for this device
            pairing_info[str(device.name)] = {
                "id": str(id), 
                "auth_token": str(pair_response.auth_token),
                "type":str(vizio.device_type),           
                "ip":ip
            }

    # Save the pairing information to a file
    with open("pairing_info.json", "w") as f:
        json.dump(pairing_info, f)

if __name__ == "__main__":
    main()
