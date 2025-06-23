import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import sys
import configparser
from pathlib import Path

PASSWORD = "1234"

class PasswordApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ray of Hope")
        self.state('zoomed')
        self.configure(bg="#2E3440")

        # Style setup
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Arial', 16, 'bold'), foreground='#ECEFF4',
                             background='#4C566A', borderwidth=0)
        self.style.map('TButton', background=[('active', '#5E81AC')])
        self.style.configure('TEntry', font=('Arial', 26), fieldbackground='#D8DEE9', foreground='#2E3440')

        self.display_var = tk.StringVar()
        self.attempts_left = 3

        # Fixed universal path to your project
        self.base_dir = Path(r"C:\Users\malvi\OneDrive\Desktop\project delhi\PythonProject")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Ray of Hope", font=("Arial", 32, "bold"), fg="#88C0D0", bg="#2E3440").place(
            relx=0.18, rely=1.0, x=0, y=0, anchor=tk.SE)
        tk.Label(self, text="Lumino Pro", font=("Arial", 20, "bold"), fg="#EBCB8B", bg="#2E3440").place(
            relx=0.95, rely=0.05, anchor="e")

        keypad_frame = tk.Frame(self, bg="#2E3440")
        keypad_frame.place(relx=0.5, rely=0.45, anchor="center")

        display = ttk.Entry(keypad_frame, textvariable=self.display_var, font=("Arial", 26), width=18, show='*')
        display.grid(row=0, column=0, columnspan=3, pady=10, ipady=8)
        display.focus_set()
        display.bind("<Return>", self.handle_return_key)

        buttons = [
            ('1', 1, 0), ('2', 1, 1), ('3', 1, 2),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2),
            ('Clear', 4, 0), ('0', 4, 1), ('Enter', 4, 2)
        ]
        for (text, row, col) in buttons:
            if text == "Clear":
                cmd = self.clear_display
            elif text == "Enter":
                cmd = self.check_password
            else:
                cmd = lambda val=text: self.append_digit(val)
            ttk.Button(keypad_frame, text=text, command=cmd, width=8).grid(
                row=row, column=col, padx=5, pady=5, ipady=10
            )

        ttk.Button(self, text="Instructions", command=self.show_instructions, width=15).place(
            relx=0.95, rely=0.8, anchor="e")
        ttk.Button(self, text="Settings", command=self.open_setting_page, width=15).place(
            relx=0.95, rely=0.88, anchor="e")

    def handle_return_key(self, event):
        self.check_password()

    def append_digit(self, digit):
        current = self.display_var.get()
        if len(current) < 8:
            self.display_var.set(current + digit)

    def clear_display(self):
        self.display_var.set("")

    def check_password(self):
        if self.display_var.get() == PASSWORD:
            self.attempts_left = 3
            self.clear_display()

            try:
                config_path = self.base_dir / "config.ini"
                if not config_path.exists():
                    raise FileNotFoundError(f"Missing config.ini at:\n{config_path}")

                config = configparser.ConfigParser()
                config.read(config_path)

                selected_mode = config.get('DEFAULT', 'selected_mode', fallback='automode.py')
                selected_mode = Path(selected_mode).name  # Remove any folders if present
                target_script = self.base_dir / selected_mode

                if not target_script.exists():
                    raise FileNotFoundError(f"Script not found:\n{target_script}")

                subprocess.Popen([sys.executable, str(target_script)])
                self.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to launch the main script:\n{e}")
        else:
            self.attempts_left -= 1
            if self.attempts_left > 0:
                messagebox.showwarning("Access Denied", f"Incorrect password. {self.attempts_left} attempts left.")
            else:
                messagebox.showerror("Machine Locked", "Machine Locked! Too many failed attempts.")
                self.after(5000, self.destroy)
            self.clear_display()

    def show_instructions(self):
        try:
            script_path = self.base_dir / "instruction_page1.py"
            if not script_path.exists():
                raise FileNotFoundError("Instructions page missing.")
            subprocess.Popen([sys.executable, str(script_path)])
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open instructions:\n{e}")

    def open_setting_page(self):
        try:
            script_path = self.base_dir / "setting_page.py"
            if not script_path.exists():
                raise FileNotFoundError("Settings page missing.")
            subprocess.Popen([sys.executable, str(script_path)])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open settings:\n{e}")

if __name__ == "__main__":
    app = PasswordApp()
    app.mainloop()
