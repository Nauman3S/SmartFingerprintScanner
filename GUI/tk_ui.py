import tkinter as tk
from tkinter import ttk
from datetime import datetime
from PIL import Image, ImageTk
from tkinter import simpledialog
import os
import time
import socket
import threading

device_connected=1
wifi_connected=0
# Array of network names
networks = ["Network1", "Network2", "Network3"]
# Function to handle client connections
def handle_client(client_socket):
    global device_connected,wifi_connected,wifi_status, title_label,text_label, nfc_icon, wifi_icon, wifi_label, scan_label, scan_icon, title_label,text_label, device_icon
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break

        # Split the received data
        command, value = data.split(':')

        if command == "update_user_count":
            user_count_label.config(text="Users: " + str(value))
        elif command == "update_title":
            title_label.config(text=value)
        elif command == "update_text":
            text_label.config(text=value)


        elif command == "update_nfc_icon":
            nfc_icon = ImageTk.PhotoImage(Image.open(os.path.join("icons",value)).convert("RGBA").resize((34, 34)))
            nfc_label.config(image=nfc_icon)
        
        elif command == "update_warning":
            scan_icon = ImageTk.PhotoImage(Image.open(os.path.join("icons","warning.png")).convert("RGBA").resize((66, 66)))
            scan_label.config(image=scan_icon)
            error,action=value.split(';')
            title_label.config(text=error)
            text_label.config(text=action)
            title_text_check_visibility(True)

        elif command == "update_wifi_state":
            if('off' in value):
                wifi_icon = ImageTk.PhotoImage(Image.open(os.path.join("icons","wifi_off.png")).convert("RGBA").resize((24, 24)))
                wifi_label.config(image=wifi_icon)
                wifi_status.config(text="WiFi: Not Connected")
                wifi_connected=0
            else:
                wifi_icon = ImageTk.PhotoImage(Image.open(os.path.join("icons","wifi.png")).convert("RGBA").resize((24, 24)))
                wifi_label.config(image=wifi_icon)
                wifi_status.config(text="WiFi: Connected")
                wifi_connected=1
        elif command == "update_device_state":
            if('off' in value):
                device_icon = ImageTk.PhotoImage(Image.open(os.path.join("icons","device_not.png")).convert("RGBA").resize((34, 34)))
                device_label.config(image=device_icon)
                device_status.config(text="Device: Not Connected")
                device_connected=0
            else:
                device_icon = ImageTk.PhotoImage(Image.open(os.path.join("icons","device.png")).convert("RGBA").resize((34, 34)))
                device_label.config(image=device_icon)
                device_status.config(text="Device: Connected")
                device_connected=1
                
        elif command == "update_username":
            title_label.config(text=value)
            
        elif command == "update_checkstatus":
            constructed_val=""
            if('In' in value):
                constructed_val="Check In\t\t"+str(datetime.now().strftime('%H:%M'))
            elif('Out' in value):
                constructed_val="Check Out\t\t"+str(datetime.now().strftime('%H:%M'))
            text_label.config(text=constructed_val)



    client_socket.close()


def title_text_check_visibility(state):
    global scan_label, title_label, text_label, root
    if state == True:
        scan_label.place(relx=0.75, rely=0.4, anchor="center")
        title_label.place(relx=0.75, rely=0.5, anchor="center")
        text_label.place(relx=0.75, rely=0.56, anchor="center")
        
        
        # Schedule user_check_visibility(False) to run after 10 seconds
        # root.after(10000, lambda: title_text_check_visibility(False))
    else:
        scan_label.place_forget()
        title_label.place_forget()
        text_label.place_forget()

def create_rounded_rectangle(canvas, x1, y1, x2, y2, r, **kwargs):
    """Create a rounded rectangle on a canvas."""
    # Top left corner
    canvas.create_arc(x1, y1, x1 + 2*r, y1 + 2*r, start=90, extent=90, **kwargs)
    # Top right corner
    canvas.create_arc(x2 - 2*r, y1, x2, y1 + 2*r, start=0, extent=90, **kwargs)
    # Bottom left corner
    canvas.create_arc(x1, y2 - 2*r, x1 + 2*r, y2, start=180, extent=90, **kwargs)
    # Bottom right corner
    canvas.create_arc(x2 - 2*r, y2 - 2*r, x2, y2, start=270, extent=90, **kwargs)
    # Top rectangle
    canvas.create_rectangle(x1 + r, y1, x2 - r, y1 + r, **kwargs)
    # Bottom rectangle
    canvas.create_rectangle(x1 + r, y2 - r, x2 - r, y2, **kwargs)
    # Left rectangle
    canvas.create_rectangle(x1, y1 + r, x1 + r, y2 - r, **kwargs)
    # Right rectangle
    canvas.create_rectangle(x2 - r, y1 + r, x2, y2 - r, **kwargs)
    # Center rectangle
    canvas.create_rectangle(x1 + r, y1 + r, x2 - r, y2 - r, **kwargs)


def wifi_connector():
    selected_network = network_selector.get()
    if selected_network:
        password = simpledialog.askstring("Password Entry", f"Enter password for {selected_network}:")
        if password:
            print(f'Network: {selected_network}, Password: {password}')
        else:
            print("Password entry cancelled.")
    else:
        print("No network selected.")

def connect():
    selected_network = network_selector.get()
    if selected_network:
        root.after(100, wifi_connector)  # Delay to allow the connect button to visually release before showing dialog
    else:
        print("Please select a network.")

def update_time():
    current_time = datetime.now().strftime('%H:%M:%S')
    time_label.config(text=current_time)
    current_date = datetime.now().strftime('%A, %d %B %Y')
    date_label.config(text=current_date)
    
    root.after(1000, update_time)

def center_window(root, width=850, height=450):
    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the position to center the window
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)

    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

root = tk.Tk()
# Remove window borders
# Maximize the window
# root.overrideredirect(True)

# try:
#     root.attributes('-fullscreen', True)
# except:
#     print("Error maximizing")
# root.focus_set()

def start_setup():
    global start_button, network_selector, connect_button
    # Your setup code here
    if device_connected:
        print("connected")
        start_button.place_forget()
        network_selector.place(relx=0.5, rely=0.6, anchor="center")
        connect_button.place(relx=0.5, rely=0.7, anchor="center")

root.attributes("-alpha", 0.9)
root.configure(bg="#C0CCDB")
root.title("Smart Fingerprint Scanner")
center_window(root)

# Place widgets on the canvas
user_count_label = ttk.Label(root, text="Users:0", style="Office.TLabel")
user_count_label.place(x=400,y=26)


wifi_icon = ImageTk.PhotoImage(Image.open(os.path.join("icons","wifi.png")).convert("RGBA").resize((24, 24)))
wifi_label = tk.Label(root, image=wifi_icon, borderwidth=0, highlightthickness=0)
wifi_label.place(x=40,y=26)
wifi_status = ttk.Label(root, text="WiFi: Connected", style="Office.TLabel")
wifi_status.place(x=70,y=26)




device_status = ttk.Label(root, text="Device: Connected", style="Office.TLabel")
device_status.place(x=600,y=26)
device_icon = ImageTk.PhotoImage(Image.open(os.path.join("icons","device.png")).convert("RGBA").resize((34, 34)))
device_label = tk.Label(root, image=device_icon, borderwidth=0, highlightthickness=0)
device_label.place(x=800,y=20)

time_label = ttk.Label(root, style="Time.TLabel")
time_label.place(x=30,y=400)

date_label = ttk.Label(root, style="Date.TLabel")
date_label.place(x=30,y=420)

logo = ImageTk.PhotoImage(Image.open(os.path.join("icons","sun.png")).convert("RGBA").resize((64, 64)))

logo_label = tk.Label(root, image=logo, borderwidth=0, highlightthickness=0)
logo_label.place(x=400,y=80)

office_center_b_label = ttk.Label(root, text="office center-b", style="OfficeCenterB.TLabel")
office_center_b_label.place(x=200,y=469)

location_icon = ImageTk.PhotoImage(Image.open(os.path.join("icons","device_not.png")).convert("RGBA").resize((24, 24)))
location_label = tk.Label(root, image=location_icon, borderwidth=0, highlightthickness=0)
# Calculate the x-coordinate for location_label
office_center_b_label_width = office_center_b_label.winfo_reqwidth()
location_icon_width = location_icon.width()
location_label_x = 200 - (office_center_b_label_width / 2) - 26 - (location_icon_width / 2)

#location_label_id=con1_canvas.create_window(location_label_x, 469, window=location_label)
location_label.place(x=location_label_x,y=469)


scan_icon = ImageTk.PhotoImage(Image.open(os.path.join("icons","moon.png")).convert("RGBA").resize((66, 66)))
scan_label = tk.Label(root, image=scan_icon, borderwidth=0, highlightthickness=0)
scan_label.place(relx=0.75, rely=0.5, anchor="center")

title_label = ttk.Label(root, text="Welcome", style="User.TLabel", justify="center", anchor="center")
title_label.place(relx=0.5, rely=0.4, anchor="center")

text_label = ttk.Label(root, text="Small Message", style="Text.TLabel", justify="center", anchor="center")
text_label.place(relx=0.5, rely=0.47, anchor="center")
# user_check_visibility(False)# hide initially
nfc_label_info = ttk.Label(root, text="Hold your phone near screen, please make\n sure your Phone's NFC is active", style="NFC.TLabel", justify="center", anchor="center")
nfc_label_info.place(relx=0.75, rely=0.9, anchor="center")

start_button = ttk.Button(root, text="Start Setup", command=start_setup , style='W.TButton')
start_button.place(relx=0.5, rely=0.55, anchor="center")


placeholder_text = "Available WiFi networks"
def on_combobox_click(event):
    # Clear the placeholder text when the combobox is clicked
    if network_selector.get() == placeholder_text:
        network_selector.set("")

def on_combobox_focusout(event):
    # Reset the placeholder text if the user didn't select a network
    if not network_selector.get():
        network_selector.set(placeholder_text)

# Create a ttk Combobox for network selection
network_selector = ttk.Combobox(root, values=networks)
network_selector.place(relx=0.5, rely=0.6, anchor="center")
network_selector.bind("<FocusIn>", on_combobox_click)
network_selector.bind("<FocusOut>", on_combobox_focusout)
network_selector.place_forget()
network_selector.set(placeholder_text)

# Create a button that triggers the connect function
connect_button = tk.Button(root, text="Connect", command=connect)
connect_button.place(relx=0.5, rely=0.65, anchor="center")
connect_button.place_forget()


# Styles
style = ttk.Style()
style.configure("Office.TLabel", foreground="black", background="#C0CCDB", font=("Roboto", 12))
style.configure("Time.TLabel", foreground="black", background="#C0CCDB", font=("Roboto", 12))
style.configure("Date.TLabel", foreground="black", background="#C0CCDB", font=("Roboto", 12))
style.configure("OfficeCenterB.TLabel", foreground="black", background="#C0CCDB", font=("Roboto", 12))
style.configure("Taim.TLabel", foreground="#9b9b9b", background="#C0CCDB", font=("Roboto", 32))
style.configure("NFC.TLabel", foreground="black", background="#C0CCDB", font=("Roboto", 12))
style.configure("User.TLabel", foreground="black", background="#C0CCDB", font=("Roboto", 24))
style.configure("Text.TLabel", foreground="black", background="#C0CCDB", font=("Roboto", 16))
style.configure('W.TButton', background='orange', width=30)



def close_window(event=None):
    global root
    root.destroy()

root.bind('<Escape>', close_window)

root.bind('q', close_window)
# Socket setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 9999))
server.listen(5)

# Start a thread to listen for incoming connections
def start_server():
    print("[SERVER] Waiting for connections...")
    while True:
        client_socket, addr = server.accept()
        print(f"[SERVER] Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.daemon = True  # Set the thread as a daemon thread
        client_handler.start()

# Start the server thread
server_thread = threading.Thread(target=start_server)
server_thread.daemon = True  # Set the thread as a daemon thread
server_thread.start()

try:
    update_time()
    root.mainloop()
except KeyboardInterrupt:
    root.destroy()  # Close the tkinter window
    exit()  # Exit the program