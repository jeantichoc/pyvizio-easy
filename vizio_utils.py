import json
from pyvizio import Vizio

def load_device_info(device_name):
    # Load pairing information from file
    with open("pairing_info.json", "r") as f:
        pairing_info = json.load(f)

    # Get the device information
    device_info = pairing_info[device_name]
    device_id = device_info["id"]
    device_ip = device_info["ip"]
    auth_token = device_info["auth_token"]
    device_type = device_info["type"]

    return device_id, device_ip, auth_token, device_type

def update_device_ip(device_name, device_ip):
    # Load pairing information from file
    with open("pairing_info.json", "r") as f:
        pairing_info = json.load(f)

    # Update the pairing information with the new IP address
    pairing_info[device_name]["ip"] = device_ip
    with open("pairing_info.json", "w") as f:
        json.dump(pairing_info, f)

def discover_device_ip(device_name):
    # Discover Vizio devices on the local network
    vizio_devices = Vizio.discovery_zeroconf(5)

    # Find the device with the specified name
    for device in vizio_devices:
        if device.name == device_name:
            return device.ip

    return None

def handle_error(device_name, vizio):
    # Try to discover the new IP address of the device
    device_ip = discover_device_ip(device_name)
    if not device_ip:
        print(f"Could not find a device with the name {device_name}")
        exit(1)

    # Update the pairing information with the new IP address
    update_device_ip(device_name, device_ip)

    # Create a new Vizio object for the device with the updated IP address
    vizio.ip = device_ip

def execute_command(device_name, command, *args):
    # Load the device information
    device_id, device_ip, auth_token, device_type = load_device_info(device_name)

    # Create a Vizio object for the device
    vizio = Vizio(device_id, device_ip, device_name, auth_token,device_type,5)

    # Try to execute the command
    success = getattr(vizio, command)(*args)
    if not success:
        handle_error(device_name, vizio)
        success = getattr(vizio, command)(*args)
        if not success:
            print(f"Failed to execute command {command} on {device_name}")
            exit(1)
