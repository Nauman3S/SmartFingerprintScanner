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


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Assuming you have defined these styles elsewhere
        self.user_count_label = ttk.Label(
            self, text="Users:0", style="Office.TLabel")
        self.user_count_label.place(x=400, y=26)

        self.wifi_icon = ImageTk.PhotoImage(Image.open(os.path.join(
            "icons", "wifi.png")).convert("RGBA").resize((24, 24)))
        self.wifi_label = tk.Label(
            self, image=self.wifi_icon, borderwidth=0, highlightthickness=0)
        self.wifi_label.place(x=40, y=26)
        self.wifi_status = ttk.Label(
            self, text="WiFi: Connected", style="Office.TLabel")
        self.wifi_status.place(x=70, y=26)

        self.device_status = ttk.Label(
            self, text="Device: Connected", style="Office.TLabel")
        self.device_status.place(x=600, y=26)
        self.device_icon = ImageTk.PhotoImage(Image.open(os.path.join(
            "icons", "device.png")).convert("RGBA").resize((34, 34)))
        self.device_label = tk.Label(
            self, image=self.device_icon, borderwidth=0, highlightthickness=0)
        self.device_label.place(x=800, y=20)
        self.paired_users = ttk.Label(
            self, text="Paired Users: 0", style="NFC.TLabel", justify="center", anchor="center")
        self.paired_users.place(x=750, rely=0.9, anchor="center")

        self.users_pending = ttk.Label(
            self, text="Users: Pending", style="NFC.TLabel", justify="center", anchor="center")
        self.users_pending.place(x=70, rely=0.9, anchor="center")

        # Styles
        self.style = ttk.Style()
        self.style.configure("Office.TLabel", foreground="black",
                             background="#C0CCDB", font=("Roboto", 12))
        self.style.configure("Time.TLabel", foreground="black",
                             background="#C0CCDB", font=("Roboto", 12))
        self.style.configure("Date.TLabel", foreground="black",
                             background="#C0CCDB", font=("Roboto", 12))
        self.style.configure("OfficeCenterB.TLabel", foreground="black",
                             background="#C0CCDB", font=("Roboto", 12))
        self.style.configure("Taim.TLabel", foreground="#9b9b9b",
                             background="#C0CCDB", font=("Roboto", 32))
        self.style.configure("NFC.TLabel", foreground="black",
                             background="#C0CCDB", font=("Roboto", 12))
        self.style.configure("User.TLabel", foreground="black",
                             background="#C0CCDB", font=("Roboto", 24))
        self.style.configure("Text.TLabel", foreground="black",
                             background="#C0CCDB", font=("Roboto", 16))
        self.style.configure('W.TButton', background='orange', width=30)
        self.style.configure('WHome.TButton', background='orange', width=10)

        # global vars
        self.selected_network_value = ""
        self.selected_teammate_value = ""

        self.frames = {}
        for F in (StartPage, SelectWiFiPage, WiFiPasswordPage, WiFiStatePage, AdminEmailPage, AdminStatePage, TeammateSelectionPage, FirstFingerScanPage, SecondFingerScanPage, PairStatePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
        self.attributes("-alpha", 0.9)

        self.title("Smart Fingerprint Scanner")
        self.center_window(self)

    def center_window(self, root, width=850, height=450):
        # Get screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Calculate the position to center the window
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        root.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()
        if hasattr(frame, "on_show_frame"):
            frame.on_show_frame()


class BaseFrame(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#C0CCDB")


class StartPage(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        # label = tk.Label(self, text="This is the start page")
        # label.pack(pady=10, padx=10)
        self.logo = ImageTk.PhotoImage(Image.open(os.path.join(
            "icons", "sun.png")).convert("RGBA").resize((64, 64)))

        self.logo_label = tk.Label(
            self, image=self.logo, borderwidth=0, highlightthickness=0)
        self.logo_label.place(x=400, y=80)
        self.title_label = ttk.Label(
            self, text="Welcome", style="User.TLabel", justify="center", anchor="center")
        self.title_label.place(relx=0.5, rely=0.4, anchor="center")

        self.text_label = ttk.Label(
            self, text="Small Message", style="Text.TLabel", justify="center", anchor="center")
        self.text_label.place(relx=0.5, rely=0.47, anchor="center")

        self.start_button = ttk.Button(self, text="Start Setup", command=lambda: controller.show_frame(
            SelectWiFiPage), style='W.TButton')
        self.start_button.place(relx=0.5, rely=0.55, anchor="center")


class SelectWiFiPage(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.placeholder_text = "Available WiFi networks"  # for combobox
        self.networks = []  # get from esp32
        self.title_label = ttk.Label(
            self, text="Select A WiFi Network", style="User.TLabel", justify="center", anchor="center")
        self.title_label.place(relx=0.5, rely=0.3, anchor="center")
        self.text_label = ttk.Label(
            self, text="From the list below", style="Text.TLabel", justify="center", anchor="center")
        self.text_label.place(relx=0.5, rely=0.45, anchor="center")
        # Create a ttk Combobox for network selection
        self.network_selector = ttk.Combobox(self, values=self.networks)
        self.network_selector.place(relx=0.5, rely=0.6, anchor="center")
        self.network_selector.bind("<FocusIn>", self.on_combobox_click)
        self.network_selector.bind("<FocusOut>", self.on_combobox_focusout)
        self.network_selector.set(self.placeholder_text)

        self.wifi_connect = ttk.Button(
            self, text="Connect", command=self.connect_ssid, style='W.TButton')
        self.wifi_connect.place(relx=0.5, rely=0.8, anchor="center")

        self.home_button = ttk.Button(self, text="Home", command=lambda: controller.show_frame(
            StartPage), style='WHome.TButton')
        self.home_button.place(x=40, rely=0.8)

    def connect_ssid(self):
        self.selected_network_value = self.network_selector.get()

        if (self.selected_network_value != "" and self.selected_network_value != self.placeholder_text):
            self.controller.selected_network_value = self.selected_network_value
            print(self.selected_network_value)
            print(self.controller.selected_network_value)

            self.controller.show_frame(WiFiPasswordPage)
        else:
            self.text_label.config(text="Nothing selected!", foreground="red")

    def on_combobox_click(self, event):
        # Clear the placeholder text when the combobox is clicked
        if self.network_selector.get() == self.placeholder_text:
            self.network_selector.set("")

    def on_combobox_focusout(self, event):
        # Reset the placeholder text if the user didn't select a network
        if not self.network_selector.get():
            self.network_selector.set(self.placeholder_text)


class WiFiPasswordPage(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.home_button = ttk.Button(
            self, text="<-Back", command=lambda: controller.show_frame(SelectWiFiPage), style='WHome.TButton')
        self.home_button.place(x=40, rely=0.8)

    def on_show_frame(self):
        print(
            f"Accessing selected_network in WiFiPasswordPage: {self.controller.selected_network_value}")
        self.title_label = ttk.Label(
            self, text=f"Enter WiFi Password for {self.controller.selected_network_value}", style="User.TLabel", justify="center", anchor="center")
        self.title_label.place(relx=0.5, rely=0.3, anchor="center")
        self.text_label = ttk.Label(
            self, text="", style="Text.TLabel", justify="center", anchor="center")
        self.text_label.place(relx=0.5, rely=0.45, anchor="center")
        print(self.controller.selected_network_value)
        self.wifi_password = ttk.Entry(self)
        self.wifi_password.place(
            relx=0.5, rely=0.6, anchor="center", width=300, height=40)

        self.wifi_connect = ttk.Button(
            self, text="Connect", command=self.connect_to_wifi, style='W.TButton')
        self.wifi_connect.place(relx=0.5, rely=0.8, anchor="center")

    def connect_to_wifi(self):
        self.text_label = ttk.Label(
            self, text="Please wait...", style="Text.TLabel", justify="center", anchor="center")
        self.text_label.config(foreground="green")
        self.text_label.place(relx=0.5, rely=0.45, anchor="center")
        self.controller.show_frame(WiFiStatePage)


class WiFiStatePage(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.home_button = ttk.Button(
            self, text="<-Back", command=lambda: controller.show_frame(SelectWiFiPage), style='WHome.TButton')
        self.home_button.place(x=40, rely=0.8)

    def on_show_frame(self):
        self.title_label = ttk.Label(
            self, text=f"Successful WiFi Connection to {self.controller.selected_network_value}", style="User.TLabel", justify="center", anchor="center")
        self.title_label.place(relx=0.5, rely=0.3, anchor="center")
        self.text_label = ttk.Label(
            self, text="WiFi Connected", style="Text.TLabel", justify="center", anchor="center")
        self.text_label.place(relx=0.5, rely=0.45, anchor="center")
        print(self.controller.selected_network_value)

        self.logo = ImageTk.PhotoImage(Image.open(os.path.join(
            "icons", "success.png")).convert("RGBA").resize((64, 64)))

        self.logo_label = tk.Label(
            self, image=self.logo, borderwidth=0, highlightthickness=0)
        self.logo_label.place(x=400, y=250)

        self.wifi_connect = ttk.Button(
            self, text="Next", command=self.to_admin_email, style='W.TButton')
        self.wifi_connect.place(relx=0.5, rely=0.8, anchor="center")

    def to_admin_email(self):
        print("admin email")
        self.controller.show_frame(AdminEmailPage)


class AdminEmailPage(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.home_button = ttk.Button(
            self, text="<-Back", command=lambda: controller.show_frame(SelectWiFiPage), style='WHome.TButton')
        self.home_button.place(x=40, rely=0.8)

    def on_show_frame(self):
        self.title_label = ttk.Label(
            self, text="Send your admin email", style="User.TLabel", justify="center", anchor="center")
        self.title_label.place(relx=0.5, rely=0.3, anchor="center")
        self.text_label = ttk.Label(
            self, text="Email Address:", style="Text.TLabel", justify="center", anchor="center")
        self.text_label.place(relx=0.5, rely=0.45, anchor="center")
        self.admin_email = ttk.Entry(self)
        self.admin_email.place(
            relx=0.5, rely=0.6, anchor="center", width=300, height=40)

        self.admin_connect = ttk.Button(
            self, text="Next", command=self.connect_to_admin, style='W.TButton')
        self.admin_connect.place(relx=0.5, rely=0.8, anchor="center")

    def connect_to_admin(self):
        self.text_label = ttk.Label(
            self, text="Please wait...", style="Text.TLabel", justify="center", anchor="center")
        self.text_label.config(foreground="green")
        self.text_label.place(relx=0.5, rely=0.45, anchor="center")
        self.controller.show_frame(AdminStatePage)


class AdminStatePage(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.home_button = ttk.Button(
            self, text="<-Back", command=lambda: controller.show_frame(SelectWiFiPage), style='WHome.TButton')
        self.home_button.place(x=40, rely=0.8)

    def on_show_frame(self):
        self.title_label = ttk.Label(self, text="Successful Connection to Orgid",
                                     style="User.TLabel", justify="center", anchor="center")
        self.title_label.place(relx=0.5, rely=0.3, anchor="center")
        self.text_label = ttk.Label(
            self, text="Connected", style="Text.TLabel", justify="center", anchor="center")
        self.text_label.place(relx=0.5, rely=0.45, anchor="center")

        self.logo = ImageTk.PhotoImage(Image.open(os.path.join(
            "icons", "success.png")).convert("RGBA").resize((64, 64)))
        self.logo_label = tk.Label(
            self, image=self.logo, borderwidth=0, highlightthickness=0)
        self.logo_label.place(x=400, y=250)

        self.wifi_connect = ttk.Button(
            self, text="Next", command=self.to_teammate_selection, style='W.TButton')
        self.wifi_connect.place(relx=0.5, rely=0.8, anchor="center")

    def to_teammate_selection(self):
        print("admin email")
        self.controller.show_frame(TeammateSelectionPage)


class TeammateSelectionPage(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.teammates_list = ['User 1', 'User 2', 'User 3']
        self.home_button = ttk.Button(
            self, text="<-Back", command=lambda: controller.show_frame(SelectWiFiPage), style='WHome.TButton')
        self.home_button.place(x=40, rely=0.8)

    def on_show_frame(self):
        self.title_label = ttk.Label(self, text="Please pair your first teammate",
                                     style="User.TLabel", justify="center", anchor="center")
        self.title_label.place(relx=0.5, rely=0.3, anchor="center")
        self.text_label = ttk.Label(
            self, text="Teammates List:", style="Text.TLabel", justify="center", anchor="center")
        self.text_label.place(relx=0.5, rely=0.45, anchor="center")
        self.admin_email = ttk.Entry(self)

        self.user_selector = ttk.Combobox(self, values=self.teammates_list)
        self.user_selector.place(
            relx=0.5, rely=0.6, anchor="center", width=300, height=40)

        self.admin_connect = ttk.Button(
            self, text="Next", command=self.to_scan_fingers_page, style='W.TButton')
        self.admin_connect.place(relx=0.5, rely=0.8, anchor="center")

    def to_scan_fingers_page(self):
        self.selected_teammate_value = self.user_selector.get()
        if (self.selected_teammate_value != ""):
            self.controller.selected_teammate_value = self.selected_teammate_value
            print(self.selected_teammate_value)
            print(self.controller.selected_teammate_value)

            self.controller.show_frame(FirstFingerScanPage)
        else:
            self.text_label.config(text="Nothing selected!", foreground="red")
            self.text_label.place(relx=0.5, rely=0.45, anchor="center")


class FirstFingerScanPage(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.home_button = ttk.Button(
            self, text="<-Back", command=lambda: controller.show_frame(SelectWiFiPage), style='WHome.TButton')
        self.home_button.place(x=40, rely=0.8)

    def on_show_frame(self):
        print(
            f"Accessing selected_teammates: {self.controller.selected_teammate_value}")

        self.title_label = ttk.Label(
            self, text=f"Please put finger of {self.controller.selected_teammate_value} on the scanner", style="User.TLabel", justify="center", anchor="center")
        self.title_label.place(relx=0.5, rely=0.3, anchor="center")
        self.text_label = ttk.Label(
            self, text="Scanning", style="Text.TLabel", justify="center", anchor="center")
        self.text_label.place(relx=0.5, rely=0.45, anchor="center")
        self.admin_email = ttk.Entry(self)

        self.admin_connect = ttk.Button(
            self, text="Next", command=self.scan_first_finger, style='W.TButton')
        self.admin_connect.place(relx=0.5, rely=0.8, anchor="center")

    def scan_first_finger(self):
        self.text_label.place(relx=0.5, rely=0.45, anchor="center")
        self.controller.show_frame(SecondFingerScanPage)


class SecondFingerScanPage(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.home_button = ttk.Button(
            self, text="<-Back", command=lambda: controller.show_frame(SelectWiFiPage), style='WHome.TButton')
        self.home_button.place(x=40, rely=0.8)

    def on_show_frame(self):
        self.title_label = ttk.Label(
            self, text=f"Please put finger of {self.controller.selected_teammate_value} AGAIN on the scanner", style="User.TLabel", justify="center", anchor="center")
        self.title_label.place(relx=0.5, rely=0.3, anchor="center")
        self.text_label = ttk.Label(
            self, text="Scanning", style="Text.TLabel", justify="center", anchor="center")
        self.text_label.place(relx=0.5, rely=0.45, anchor="center")
        self.admin_email = ttk.Entry(self)

        self.admin_connect = ttk.Button(
            self, text="Next", command=self.scan_second_finger, style='W.TButton')
        self.admin_connect.place(relx=0.5, rely=0.8, anchor="center")

    def scan_second_finger(self):
        self.text_label.place(relx=0.5, rely=0.45, anchor="center")
        self.controller.show_frame(PairStatePage)


class PairStatePage(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.home_button = ttk.Button(
            self, text="<-Back", command=lambda: controller.show_frame(SelectWiFiPage), style='WHome.TButton')
        self.home_button.place(x=40, rely=0.8)

    def on_show_frame(self):
        self.title_label = ttk.Label(
            self, text=f"Successful {self.controller.selected_teammate_value} Paired", style="User.TLabel", justify="center", anchor="center")
        self.title_label.place(relx=0.5, rely=0.3, anchor="center")

        self.user_picture = ImageTk.PhotoImage(Image.open(
            os.path.join("icons", "user.png")).convert("RGBA").resize((64, 64)))
        self.user_picture_label = tk.Label(
            self, image=self.user_picture, borderwidth=0, highlightthickness=0)
        self.user_picture_label.place(x=120, y=165)

        self.text_label = ttk.Label(
            self, text="Name\nLastName\nEmployee#", style="Text.TLabel", justify="center", anchor="center")
        self.text_label.place(relx=0.5, rely=0.5, anchor="center")
        self.admin_email = ttk.Entry(self)

        self.logo = ImageTk.PhotoImage(Image.open(os.path.join(
            "icons", "success.png")).convert("RGBA").resize((64, 64)))
        self.logo_label = tk.Label(
            self, image=self.logo, borderwidth=0, highlightthickness=0)
        self.logo_label.place(x=670, y=165)

        self.start_page_btn = ttk.Button(
            self, text="Finish", command=self.to_home_page, style='W.TButton')
        self.start_page_btn.place(relx=0.7, rely=0.8, anchor="center")

        self.add_other_player = ttk.Button(
            self, text="Add another", command=self.add_other_player, style='W.TButton')
        self.add_other_player.place(relx=0.3, rely=0.8, anchor="center")

    def to_home_page(self):
        self.text_label.place(relx=0.5, rely=0.45, anchor="center")
        self.controller.show_frame(StartPage)

    def add_other_player(self):
        self.text_label.place(relx=0.5, rely=0.45, anchor="center")
        self.controller.show_frame(TeammateSelectionPage)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
