import tkinter as tk
from tkinter import ttk

class LoginWindow(tk.Toplevel):
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.title("Login")
        self.geometry("300x150")
        self.parent = parent
        self.on_login_success = on_login_success

        self.username_label = ttk.Label(self, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.password_label = ttk.Label(self, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.login_button = ttk.Button(self, text="Login", command=self.attempt_login)
        self.login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.grid_columnconfigure(1, weight=1)

    def attempt_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Basic hardcoded authentication
        if username == "staff" and password == "password":
            self.on_login_success()
            self.destroy()
        else:
            ttk.Label(self, text="Login failed. Please try again.", foreground="red").grid(row=3, column=0, columnspan=2, pady=5)