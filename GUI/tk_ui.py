import tkinter as tk
from tkinter import ttk
from datetime import datetime
from PIL import Image, ImageTk
from tkinter import simpledialog
import os
import time
import socket
import threading
import sys
import re

def restart_program():
    """Restarts the current program."""
    python = sys.executable
    os.execl(python, python, *sys.argv)

client_socket=0

device_connected=1
wifi_connected=0
start_setup_process=0
placeholder_text = "Available WiFi networks" #for combobox
paired_users_count=0
available_users_count=0
# Array of network names
networks=[] #get from esp32
teammates_list=["User 1", "User 2", "User 3"] #get from backend
# Function to handle client connections
def handle_client(client_socket):
    global networks, start_setup_process,device_connected,wifi_connected,wifi_status, title_label,text_label, nfc_icon, wifi_icon, wifi_label, success_error_label, success_error_icon, title_label,text_label, device_icon, network_selector
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break

        # Split the received data
        # print(data)
        command, value = data.split(':')
        

        if command == "update_user_count":
            user_count_label.config(text="Users: " + str(value))
        elif command == "update_title":
            title_label.config(text=value)
        elif command == "update_networks_list":
            networks=value.split(";")
            network_selector.config(values=networks)
            # print(networks)
        elif command == "update_text":
            text_label.config(text=value)


        elif command == "update_nfc_icon":
            nfc_icon = ImageTk.PhotoImage(Image.open(os.path.join("icons",value)).convert("RGBA").resize((34, 34)))
            nfc_label.config(image=nfc_icon)
        
        elif command == "update_warning":
            success_error_icon = ImageTk.PhotoImage(Image.open(os.path.join("icons","warning.png")).convert("RGBA").resize((66, 66)))
            success_error_label.config(image=success_error_icon)
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
                if(start_setup_process==1):
                    WiFiConnectionState(0)
            else:
                wifi_icon = ImageTk.PhotoImage(Image.open(os.path.join("icons","wifi.png")).convert("RGBA").resize((24, 24)))
                wifi_label.config(image=wifi_icon)
                wifi_status.config(text="WiFi: Connected")
                wifi_connected=1
                if(start_setup_process==1):
                    WiFiConnectionState(1)
                

                

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

def WiFiConnectionState(state):
    global success_error_icon, success_error_icon, title_label, text_label,start_button, network_selector, connect_button, action_button
    if(state==1):
        success_error_label.place(relx=0.6, rely=0.5, anchor="center")
        title_label.place(relx=0.5, rely=0.4, anchor="center")
        text_label.place(relx=0.5, rely=0.47, anchor="center")
        
        title_label.config(text="WiFi Connected!")
        text_label.config(text="WiFi Connection Successful!")
        success_error_icon = ImageTk.PhotoImage(Image.open(os.path.join("icons","success.png")).convert("RGBA").resize((64, 64)))
        success_error_label.config(image=success_error_icon)
        success_error_label.place(relx=0.5, rely=0.67, anchor="center")
        connect_button.place_forget()
        network_selector.place_forget()
        action_button.place(relx=0.5, rely=0.85, anchor="center")
        action_button.config(text="Next", command=email_handler)
    elif(state==0):
        success_error_label.place(relx=0.6, rely=0.5, anchor="center")
        title_label.place(relx=0.5, rely=0.4, anchor="center")
        text_label.place(relx=0.5, rely=0.47, anchor="center")
        
        title_label.config(text="WiFi Not Connected")
        text_label.config(text="WiFi Connection failed!")
        success_error_icon = ImageTk.PhotoImage(Image.open(os.path.join("icons","error.png")).convert("RGBA").resize((64, 64)))
        success_error_label.config(image=success_error_icon)
        success_error_label.place(relx=0.5, rely=0.67, anchor="center")
        connect_button.place_forget()
        network_selector.place_forget()
        action_button.place(relx=0.5, rely=0.85, anchor="center")
        action_button.config(text="Retry", command=restart_program)

def title_text_check_visibility(state):
    global success_error_label, title_label, text_label, root
    if state == True:
        success_error_label.place(relx=0.75, rely=0.4, anchor="center")
        title_label.place(relx=0.75, rely=0.5, anchor="center")
        text_label.place(relx=0.75, rely=0.56, anchor="center")
        
        
        # Schedule user_check_visibility(False) to run after 10 seconds
        # root.after(10000, lambda: title_text_check_visibility(False))
    else:
        success_error_label.place_forget()
        title_label.place_forget()
        text_label.place_forget()


def is_valid_email(char, value):
    """Validate if the input is a valid email address."""
    # A basic regex pattern to validate an email address
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.match(pattern, value) or value == "":
        return True
    else:
        return False


def add_another_user():
    print("add new")
def scan_done():
    global success_error_icon, success_error_icon, title_label, text_label,start_button, network_selector, connect_button, action_button, email_entry
    global user_selector, paired_users_count, user_image_icon, user_image_label
    
    title_label.place_forget()
    text_label.place(relx=0.5, rely=0.4, anchor="center")
    text_label.config(text="Successfuly Paired Teammate")
    
    action_button.config(text="Add another", command=add_another_user)
    success_error_icon = ImageTk.PhotoImage(Image.open(os.path.join("icons","success.png")).convert("RGBA").resize((64, 64)))
    success_error_label.config(image=success_error_icon)
    success_error_label.place(relx=0.8, rely=0.5, anchor="center")
    user_count_label.config(text="Users: 26")
    paired_users.config(text="Paired-Users: 0")
    paired_user_info.place(relx=0.5, rely=0.55, anchor="center")
    paired_users_count=paired_users_count+1
    if(paired_users_count>=26):
        paired_users_count=0
    paired_users.config(text="Paired-Users: "+str(paired_users_count))
    paried_user_text="Name: "+user_selector.get()+"\nEmployee#: "+str(paired_users_count)
    paired_user_info.config(text=paried_user_text)

    user_image_icon = ImageTk.PhotoImage(Image.open(os.path.join("icons","user.png")).convert("RGBA").resize((64, 64)))
    user_image_label.config(image=user_image_icon)
    user_image_label.place(relx=0.2, rely=0.5, anchor="center")
    


def scan_second():
    global success_error_icon, success_error_icon, title_label, text_label,start_button, network_selector, connect_button, action_button,placeholder_text,user_selector
    global user_selector, paired_users_count
    print("scan fingerprint")
    title_label.config(text="Scanning")
    text_label.config(text="Please put "+user_selector.get()+ " finger AGAIN \non the scanner.")
    text_label.place(relx=0.5, rely=0.5, anchor="center")
    user_selector.place_forget()
    action_button.config(text="Complete pairing", command=scan_done)
    


def scan_first():
    global success_error_icon, success_error_icon, title_label, text_label,start_button, network_selector, connect_button, action_button,placeholder_text,user_selector
    global user_selector, paired_users_count
    print("scan fingerprint")
    title_label.config(text="Scanning")
    text_label.config(text="Please put "+user_selector.get()+ " finger \non the scanner.")
    text_label.place(relx=0.5, rely=0.5, anchor="center")
    user_selector.place_forget()
    action_button.config(text="Next", command=scan_second)

def pair_now():
    global user_selector, paired_users_count
    print("pair command sent to esp32")
    
    action_button.config(text="Pair Next User")
    selected_teammate = user_selector.get()
    action_button.config(text="Scan Fingerprint", command=scan_first)
    print(selected_teammate)
    
def pair_users():
    print("pairing")
    global success_error_icon, success_error_icon, title_label, text_label,start_button, network_selector, connect_button, action_button,placeholder_text,user_selector
    title_label.config(text="Please pair your teammate")
    title_label.place(relx=0.5, rely=0.4, anchor="center")
    action_button.config(text="Pair", command=pair_now)
    user_selector.place(relx=0.5, rely=0.6, anchor="center")
    success_error_label.place_forget()
    placeholder_text="Select teammates"
    selected_teammate = user_selector.get()
    print(selected_teammate)


def get_email_data():
    global success_error_icon, success_error_icon, title_label, text_label,start_button, network_selector, connect_button, action_button, email_entry
    """Retrieve the email address from the Entry widget."""
    email = email_entry.get()
    print(email)
    title_label.config(text="Successful connection to Orgid")
    email_entry.place_forget()
    title_label.place(relx=0.5, rely=0.4, anchor="center")
    action_button.config(text="Pair User", command=pair_users)
    success_error_icon = ImageTk.PhotoImage(Image.open(os.path.join("icons","success.png")).convert("RGBA").resize((64, 64)))
    success_error_label.config(image=success_error_icon)
    success_error_label.place(relx=0.5, rely=0.67, anchor="center")
    user_count_label.config(text="Users: 26")
    paired_users.config(text="Paired-Users: 0")
    
    


def email_handler():
    global success_error_icon, success_error_icon, title_label, text_label,start_button, network_selector, connect_button, action_button
    success_error_label.place_forget()
    text_label.place_forget()
    title_label.config(text="Send your admin email")
    title_label.place(relx=0.5, rely=0.4, anchor="center")
    action_button.config(text="Next", command=get_email_data)
    email_entry.place(relx=0.5, rely=0.6, anchor="center")

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
    global client_socket
    selected_network = network_selector.get()
    if selected_network:
        password = simpledialog.askstring("Password Entry", f"Enter password for {selected_network}:")
        if password:
            network_string="network;"+selected_network+";"+password
            client_socket.send(network_string.encode('utf-8'))
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
    global start_button, network_selector, connect_button, client_socket, wifi_connected, title_label, text_label,success_error_label
    global start_setup_process
    start_setup_process=1
    # Your setup code here
    if device_connected:
        client_socket.send("get_wifi".encode('utf-8'))
        # print("connected")
        if(wifi_connected==1):
            start_button.place_forget()
            WiFiConnectionState(1)
        else:
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


success_error_icon = ImageTk.PhotoImage(Image.open(os.path.join("icons","success.png")).convert("RGBA").resize((66, 66)))
success_error_label = tk.Label(root, image=success_error_icon, borderwidth=0, highlightthickness=0)
success_error_label.place(relx=0.6, rely=0.5, anchor="center")
success_error_label.place_forget()

user_image_icon = ImageTk.PhotoImage(Image.open(os.path.join("icons","moon.png")).convert("RGBA").resize((66, 66)))
user_image_label = tk.Label(root, image=user_image_icon, borderwidth=0, highlightthickness=0)
user_image_label.place(relx=0.6, rely=0.5, anchor="center")
user_image_label.place_forget()


title_label = ttk.Label(root, text="Welcome", style="User.TLabel", justify="center", anchor="center")
title_label.place(relx=0.5, rely=0.4, anchor="center")

text_label = ttk.Label(root, text="Small Message", style="Text.TLabel", justify="center", anchor="center")
text_label.place(relx=0.5, rely=0.47, anchor="center")

paired_user_info = ttk.Label(root, text="", style="Text.TLabel", justify="center", anchor="center")
paired_user_info.place(relx=0.5, rely=0.55, anchor="center")
paired_user_info.place_forget()
# user_check_visibility(False)# hide initially
paired_users = ttk.Label(root, text="Paired Users: 0", style="NFC.TLabel", justify="center", anchor="center")
paired_users.place(relx=0.75, rely=0.9, anchor="center")

start_button = ttk.Button(root, text="Start Setup", command=start_setup , style='W.TButton')
start_button.place(relx=0.5, rely=0.55, anchor="center")



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

user_selector = ttk.Combobox(root, values=teammates_list)
user_selector.place(relx=0.5, rely=0.6, anchor="center")
user_selector.bind("<FocusIn>", on_combobox_click)
user_selector.bind("<FocusOut>", on_combobox_focusout)
user_selector.place_forget()
user_selector.set("Select teammate")

# validate_cmd = root.register(is_valid_email)
email_entry = ttk.Entry(root)
email_entry.place(relx=0.5, rely=0.6, anchor="center", width=100, height=10)
email_entry.place_forget()

# Create a button that triggers the connect function
connect_button = ttk.Button(root, text="Connect", command=connect, style='W.TButton')
connect_button.place(relx=0.5, rely=0.65, anchor="center")
connect_button.place_forget()

# Create a button that triggers the action functions
action_button = ttk.Button(root, text="Retry", command=restart_program, style='W.TButton')
action_button.place(relx=0.5, rely=0.85, anchor="center")
action_button.place_forget()


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
    global client_socket
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