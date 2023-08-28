# pyvizio-easy

A Python script to easily control Vizio devices.

## Requirements

This script requires the `pyvizio` library. You can install it by running the pip command :  
```
pip install pyvizio
```
Or you can find it here : https://github.com/raman325/pyvizio/tree/master/pyvizio

## Pairing

You must paired the devices first, run the following command:

```
python3 pvvizio-easy.py pair
```

This will pair the script with all Vizio devices detected in your LAN.

## Usage

To control a device, run the following command:

```
python3 pvvizio-easy.py <device_name> <command> [args*]
```

This will run the specified command on the specified device name.

## Examples

Here are some examples of how to use the script:

- To increase the volume on a device named "TV":

```
python3 pvvizio-easy.py TV vol_up
```

- To decrease the volume on a device named "TV":

```
python3 pvvizio-easy.py TV vol_down
```

- To set the input on a device named "TV" to HDMI 4:

```
python3 pvvizio-easy.py TV set_input hdmi4
```


I hope this helps! Let me know if you need any further assistance. 😊
