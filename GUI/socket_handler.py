import socket
import threading

def data_received_callback(data):
    print(f"Data received from server: {data}")

def receive_data_from_server(client_socket):
    response = client_socket.recv(1024).decode('utf-8')
    if response:
        data_received_callback(response)

def send_update(command, value):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 9999))
    client.send(f"{command}:{value}".encode('utf-8'))
    
    # Start a new thread to receive data from the server
    threading.Thread(target=receive_data_from_server, args=(client,)).start()

# Example usage:
# send_update("update_device_state", "on")

# Example usage:
# send_update("update_device_state", "off")
# send_update("update_wifi_state", "off")
# send_update("update_user_count", "10")
# send_update("update_title", "New Title")
# send_update("update_text", "New text")

