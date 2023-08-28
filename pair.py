import json
from pyvizio import Vizio

DEVICE_ID = "my_device_id"
DEVICE_NAME = "my_device_name"
DEVICE_TYPE = "tv"  # change to "speaker" if pairing a speaker

def main():
    # Discover Vizio devices on the local network
    vizio_devices = Vizio.discovery_zeroconf(5)
    print(vizio_devices)

    # Pair each device and store the pairing information
    pairing_info = {}
    for device in vizio_devices:
        ip = device.ip
        vizio = Vizio(str(device.id), ip, str(device.name), str(device.model))

        # Start the pairing process
        pair_data = vizio.start_pair()

        if pair_data:
            # For TVs, lookup the PIN code on your TV and note challenge token and type in console
            # For speakers, press the physical "Volume Up" button and note challenge token and type in console
            print(pair_data)
            pin = input(f"Enter the PIN displayed on your {device.name} device: ")
            ch_type = pair_data.ch_type
            token = pair_data.token

            # Finalize the pairing process
            pair_response = vizio.pair(ch_type, token, pin)

            # Store the pairing information for this device
            pairing_info[str(device.name)] = {
                "auth_token": str(pair_response.auth_token),
                "ip":device.ip
            }

    # Save the pairing information to a file
    with open("pairing_info.json", "w") as f:
        json.dump(pairing_info, f)

if __name__ == "__main__":
    main()
