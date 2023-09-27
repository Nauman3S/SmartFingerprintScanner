import serial
import time
import serial.tools.list_ports
import threading
from socket_handler import *

def find_esp32_port():
    
    #automatic port detection
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if "CP2102" in port.description or "Silicon Labs" in port.description:  # ESP32 uses the CP2102 USB to UART bridge
            return port.device
    return None

esp32_port = find_esp32_port()
send_update("update_device_state", "off")#default state
while esp32_port==None:
    esp32_port = find_esp32_port()

if esp32_port:
    print(f"ESP32 found on port: {esp32_port}")
    send_update("update_device_state", "on")
else:
    print("ESP32 not found!")

ser = serial.Serial(esp32_port, 115200)  # Replace 'COM_PORT' with your port, e.g., 'COM3' or '/dev/ttyUSB0'
time.sleep(2)  # Wait for the serial connection to initialize

def callback(payload):
    """This function is called when new data arrives."""
    print(f"Callback triggered with payload: {payload}")
    if("Connected to:"in payload):
        print("wifi connected")
    elif("Can't connect to:" in payload):
        print("wifi not connected")
    elif("networks" in payload):
        to_send=payload.replace("networks;","")
        send_update("update_networks_list", to_send)

    # For demonstration, let's send a response back
    # serial_publish(f"Acknowledged: {payload}")

def serial_publish(payload):
    """Send data to the serial port."""
    ser.write((payload + '\n').encode())

def serial_handler():
    """Continuously check for available data on the serial port."""
    while True:
        if ser.in_waiting:
            try:
                data = ser.readline().decode('utf-8').strip()
            except:
                a=0#do nothing
            callback(data)
        time.sleep(0.1)  # Short delay to prevent excessive CPU usage

# Start the serial handler in a separate thread
threading.Thread(target=serial_handler, daemon=True).start()

# Main loop
while True:
    # Your main loop code here
    # For demonstration, let's send a message every 5 seconds
    serial_publish("Hello from Python!")
    time.sleep(10)
    serial_publish("network;MagentaWLAN-48UN;40236121546890174076")
