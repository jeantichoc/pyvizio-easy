import argparse
import vizio_utils

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("device_name", help="The name of the device to control")
parser.add_argument("command", help="The name of the command to execute")
parser.add_argument("args", nargs="*", help="The arguments to pass to the command")
args = parser.parse_args()

# Execute the command on the specified device
vizio_utils.execute_command(args.device_name, args.command, *args.args)
