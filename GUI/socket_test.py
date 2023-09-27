import socket

def send_update(command, value):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 9999))
    client.send(f"{command}:{value}".encode('utf-8'))
    client.close()

# Example usage:
send_update("update_device_state", "off")
send_update("update_wifi_state", "off")
send_update("update_user_count", "10")
send_update("update_title", "New Title")
send_update("update_text", "New text")

