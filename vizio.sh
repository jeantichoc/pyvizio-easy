#!/bin/bash

# Get the directory containing this script
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Check if the correct number of arguments was provided
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 DEVICE_NAME COMMAND [ARGS...]"
    exit 1
fi

# Get the arguments
device_name="$1"
command="$2"
shift 2
args=("$@")

cd "$script_dir"

# Call the Python script with the provided arguments
python3 "$script_dir/vizio.py" "$device_name" "$command" "${args[@]}"
