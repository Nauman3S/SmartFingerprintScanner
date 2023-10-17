#!/bin/bash

# Define paths
BASE_DIR=~/SmartFPS
GUI_DIR="${BASE_DIR}/SmartFingerprintScanner-main/GUI"
GUI_PATH="${GUI_DIR}/tk_ui.py"
SERIAL_HANDLER="${BASE_DIR}/SmartFingerprintScanner-main/GUI/serial_handler.py"

# Function to check if a process is running
is_process_running() {
    local process_name="$1"
    pgrep -f "$process_name" >/dev/null
    return $?
}

# Function to check if the socket server is listening on the expected port (assuming port 9999)
is_socket_server_ready() {
    netstat -tuln | grep -q ":9999 "
    return $?
}

# Kill existing processes if they are running
if is_process_running "$GUI_PATH"; then
    pkill -f "$GUI_PATH"
    echo "Existing Python GUI process killed."
fi

if is_process_running "$SERIAL_HANDLER"; then
    pkill -f "$SERIAL_HANDLER"
    echo "Existing serial_handler program process killed."
fi

# Start the socket server (Python3 based tkinter GUI)
echo "Starting socket server..."

# Change to GUI directory to ensure relative paths in the Python script work correctly
cd "$GUI_DIR"
DISPLAY=:0 python3 "$GUI_PATH" &

# Wait for the socket server to be ready
echo "Waiting for the socket server to be ready..."
while ! is_socket_server_ready; do
    sleep 1
done
echo "Socket server started."

# Start the serial_handler program
echo "Starting serial_handler program..."
DISPLAY=:0 python3 "$SERIAL_HANDLER" &

echo "All programs have been executed."
