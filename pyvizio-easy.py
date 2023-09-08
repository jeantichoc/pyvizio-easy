import json
import os
import sys
import platform
import random
import argparse

from pyvizio import Vizio

# Get the path to the directory containing the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the pairing information file
paired_devices_json = os.path.join(script_dir, "pyvizio-easy.json")

def get_computer_name():
    # Get the hostname from the environment variable
    computer_name = platform.node()
    # Remove the ".local" at the end of the hostname
    if computer_name.endswith(".local"):
        computer_name = computer_name[:-6]
    return computer_name + "-pyvizio"


def load_device_info(device_name):
    try:
        # Load pairing information from file
        with open(paired_devices_json, "r") as f:
            pairing_info = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error: The {paired_devices_json} file is empty or does not exist.")
        sys.exit(1)

    # Get the device information
    device_info = pairing_info[device_name]
    device_id = device_info["id"]
    device_ip = device_info["ip"]
    auth_token = device_info["auth_token"]
    device_type = device_info["type"]

    return device_id, device_ip, auth_token, device_type


def update_device_ip(device_name, device_ip):
    # Load pairing information from file
    with open(paired_devices_json, "r") as f:
        pairing_info = json.load(f)

    # Update the pairing information with the new IP address
    pairing_info[device_name]["ip"] = device_ip
    with open(paired_devices_json, "w") as f:
        json.dump(pairing_info, f)

def discover_device_ip(device_name):
    # Discover Vizio devices on the local network
    vizio_devices = Vizio.discovery_zeroconf(5)

    # Find the device with the specified name
    for device in vizio_devices:
        if device.name == device_name:
            return device.ip

    return None

def update_ip_if_necessary(vizio):
    if vizio_connected(vizio):
        return

    print(f"No device detected at ip {vizio.ip}")   
    print(f"Looking for a new ip for {vizio.name}")   
    # Try to discover the new IP address of the device
    new_ip = discover_device_ip(vizio.name)
    if not new_ip:
        print(f"Could not find a device with the name {vizio.name}")
        exit(1)

    # Update the pairing information with the new IP address

    print(f"Changing ip for {vizio.name} {vizio.ip} to {new_ip}")   
    update_device_ip(vizio.name, new_ip)

    # Create a new Vizio object for the device with the updated IP address
    vizio.ip = new_ip


def vizio_connected(vizio) -> bool:
    success = getattr(vizio, "get_power_state")()
    return success is not None

def get_vizio_device(device_name) -> Vizio:
    # Load the device information
    device_id, device_ip, auth_token, device_type = load_device_info(device_name)

    # Create a Vizio object for the device
    vizio = Vizio(device_id, device_ip, device_name, auth_token,device_type,2)

    update_ip_if_necessary(vizio)
    return vizio


def execute_command(device_name, command, *args):
    # Get the Vizio object for the device
    vizio = get_vizio_device(device_name)

    # Try to execute the command
    success = getattr(vizio, command)(*args)
    print(success)

def pair():
    # Discover Vizio devices on the local network
    vizio_devices = Vizio.discovery_zeroconf()

    # Get the local computer name for ids and visibility
    computer_name = get_computer_name()

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
            if not hasattr(pair_response, 'auth_token'):
                print("pairing failed")
                vizio.stop_pair()
            else:
                print("token received")
                pairing_info[str(device.name)] = {
                    "id": str(id),
                    "auth_token": str(pair_response.auth_token),
                    "type": str(vizio.device_type),
                    "ip": ip
                }

    # Save the pairing information to a file
    print("storring paired devices in $paired_devices_json")
    with open(paired_devices_json, "w") as f:
        json.dump(pairing_info, f)

def usage():
    print('Setup:')
    print('python3 pvvizio-easy.py pair\t\tPair with all Vizio devices detected')
    print('python3 pvvizio-easy.py help\t\tShow this help message')
    print('')
    print('Usage:')
    print('python3 pvvizio-easy.py <device_name> <command> [args*] \t run the command on the specified device name')
    print('')
    print('Examples:')
    print('python3 pvvizio-easy.py TV vol_up')
    print('python3 pvvizio-easy.py TV vol_down')
    print('python3 pvvizio-easy.py TV set_input hdmi4')


if __name__ == "__main__":

    if any(arg == 'help' or arg == '--help' for arg in sys.argv[1:]):
        usage()
        print("toto")
        exit()

    if any(arg == 'pair' or arg == '--pair' for arg in sys.argv[1:]):
        pair()
        exit()

    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("device_name", help="The name of the device to control")
    parser.add_argument("command", help="The name of the command to execute")
    parser.add_argument("args", nargs="*", help="The arguments to pass to the command")
    args = parser.parse_args()

    # Execute the command on the specified device
    execute_command(args.device_name, args.command, *args.args)
