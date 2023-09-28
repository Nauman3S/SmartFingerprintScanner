import serial
import time
import serial.tools.list_ports
import threading
import socket
import sys

ser=0
def data_received_callback(data):
    print(f"Data received from server: {data}")
    if 'network;' in data:
        serial_publish(data)
    elif 'get_wifi' in data:
        serial_publish(data)

def receive_data_from_server(client_socket):
    while True:
        try:
            response = client_socket.recv(1024).decode('utf-8')
            if response:
                data_received_callback(response)
        except socket.error as e:
            print(f"Socket error: {e}")
            client_socket.close()  # Close the client socket
            time.sleep(5)  # Wait for a while before attempting to reconnect
            send_update("some_command", "some_value")  # Attempt to reconnect
            break

def send_update(command, value):
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("127.0.0.1", 9999))
            client.send(f"{command}:{value}".encode('utf-8'))
            threading.Thread(target=receive_data_from_server, args=(client,)).start()
            break
        except socket.error as e:
            print(f"Connection error: {e}. Retrying in 5 seconds...")
            time.sleep(5)
def find_esp32_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if "CP2102" in port.description or "Silicon Labs" in port.description:
            return port.device
    return None

def check_port_availability():
    global ser
    while True:
        esp32_port = find_esp32_port()
        if esp32_port:
            try:
                # Close the serial port if it's open
                if ser and ser.is_open:
                    ser.close()
                    time.sleep(1)  # Give it a moment to close

                print(f"ESP32 found on port: {esp32_port}")
                send_update("update_device_state", "on")
                ser = serial.Serial(esp32_port, 115200)
                time.sleep(2)
                break
            except serial.SerialException:
                print("Error connecting to ESP32. Retrying...")
                time.sleep(5)
        else:
            print("ESP32 not found!")
            send_update("update_device_state", "off")
            time.sleep(5)


def callback(payload):
    print(f"Callback triggered with payload: {payload}")
    if "Connected to WiFi!" in payload:
        send_update("update_wifi_state", "on")
    elif "Can't connect to WiFi" in payload:
        send_update("update_wifi_state", "off")
    elif "Can't connect to:" in payload:
        print("wifi not connected")
        send_update("update_wifi_state", "off")
    elif "networks" in payload:
        to_send = payload.replace("networks;", "")
        send_update("update_networks_list", to_send)

def serial_publish(payload):
    try:
        ser.write((payload + '\n').encode())
    except:
        print("Error sending data to ESP32. Retrying connection...")
        check_port_availability()

def serial_handler():
    global ser
    while True:
        try:
            if ser.in_waiting:
                data = ser.readline().decode('utf-8').strip()
                callback(data)
            time.sleep(0.1)
        except serial.SerialException:
            print("ESP32 connection lost. Reconnecting...")
            check_port_availability()
            time.sleep(5)

check_port_availability()
threading.Thread(target=serial_handler, daemon=True).start()

while True:
    try:
    # serial_publish("Hello from Python!")
        time.sleep(10)
    except KeyboardInterrupt:
        print("\nExiting program...")
        # Add any cleanup code here if needed
        sys.exit(0)
        
