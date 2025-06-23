import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import configparser
import os

# --------- Sidebar Button Logic ---------
def create_sidebar_buttons(sidebar, scale_factor, root):
    sidebar_buttons = ["🔄 Auto", "📜 Protocol", "🏃 Therapy", "🔙 Back"]

    # Sidebar title
    title_label = tk.Label(sidebar, text="Select the Mode from Here", font=("Arial", 14, "bold"),
                           bg="gray20", fg="white", pady=15)
    title_label.pack()

    def on_hover(event, canvas, rect, text_id):
        canvas.itemconfig(rect, fill="#378ba4")

    def on_leave(event, canvas, rect, text_id):
        canvas.itemconfig(rect, fill="#2a5d77")

    def on_button_click(name):
        # Universal script paths (relative to this file)
        base_path = os.path.join(os.getcwd(), "PythonProject")
        script_paths = {
            "🔄 Auto": os.path.join(base_path, "automode.py"),
            "📜 Protocol": os.path.join(base_path, "protocol1.py"),
            "🏃 Therapy": os.path.join(base_path, "therapyq.py")
        }

        if name == "🔙 Back":
            root.destroy()
        elif name in script_paths:
            config = configparser.ConfigParser()
            config['DEFAULT'] = {'selected_mode': script_paths[name]}
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            messagebox.showinfo("Mode Selected", f"{name} mode selected!\nEnter password to continue.")

    canvas_width = int(160 * scale_factor)
    canvas_height = int(100 * scale_factor)

    for btn_text in sidebar_buttons:
        canvas = tk.Canvas(sidebar, width=canvas_width, height=canvas_height, bg="gray20", highlightthickness=0)
        canvas.pack(pady=int(10 * scale_factor))

        rect = canvas.create_rectangle(0, 0, canvas_width, canvas_height, fill="#2a5d77", outline="")
        text_id = canvas.create_text(canvas_width // 2, canvas_height // 2,
                                     text=btn_text,
                                     font=("Segoe UI", int(16 * scale_factor), "bold"),
                                     fill="white")

        # Hover and click bindings
        canvas.tag_bind(rect, "<Enter>", lambda e, c=canvas, r=rect, t=text_id: on_hover(e, c, r, t))
        canvas.tag_bind(text_id, "<Enter>", lambda e, c=canvas, r=rect, t=text_id: on_hover(e, c, r, t))
        canvas.tag_bind(rect, "<Leave>", lambda e, c=canvas, r=rect, t=text_id: on_leave(e, c, r, t))
        canvas.tag_bind(text_id, "<Leave>", lambda e, c=canvas, r=rect, t=text_id: on_leave(e, c, r, t))
        canvas.tag_bind(rect, "<Button-1>", lambda e, name=btn_text: on_button_click(name))
        canvas.tag_bind(text_id, "<Button-1>", lambda e, name=btn_text: on_button_click(name))

# --------- Save Settings ---------
def save_settings():
    volume = volume_slider.get()
    brightness = brightness_slider.get()
    messagebox.showinfo("Settings Saved", f"Volume: {volume:.1f}\nBrightness: {brightness:.1f}")

# --------- Engineering Password Entry ---------
def show_engineering_popup():
    password_win = tk.Toplevel(root)
    password_win.title("Enter Password")
    password_win.geometry("300x260")
    password_win.resizable(False, False)
    password_win.grab_set()

    tk.Label(password_win, text="Enter Engineering Password:", font=("Arial", 11)).pack(pady=(15, 5))
    pw_entry = tk.Entry(password_win, show="*", font=("Arial", 12), justify="center")
    pw_entry.pack(pady=3)
    pw_entry.focus_set()

    def insert_digit(digit): pw_entry.insert(tk.END, digit)
    def clear_entry(): pw_entry.delete(0, tk.END)
    def backspace():
        current = pw_entry.get()
        pw_entry.delete(0, tk.END)
        pw_entry.insert(0, current[:-1])

    def check_password(event=None):
        if pw_entry.get() == "9761":
            password_win.destroy()
            open_engineering_mode()
        else:
            messagebox.showerror("Error", "Incorrect password")
            clear_entry()

    keypad_frame = tk.Frame(password_win)
    keypad_frame.pack(pady=5)
    buttons = [
        ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
        ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
        ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
        ('Clear', 3, 0), ('0', 3, 1), ('⌫', 3, 2)
    ]
    for (text, row, col) in buttons:
        cmd = clear_entry if text == 'Clear' else backspace if text == '⌫' else lambda t=text: insert_digit(t)
        tk.Button(keypad_frame, text=text, width=5, height=2, command=cmd).grid(row=row, column=col, padx=2, pady=2)

    ttk.Button(password_win, text="Submit", command=check_password).pack(pady=10)
    password_win.bind("<Return>", check_password)

# --------- Engineering Mode Data ---------
def open_engineering_mode():
    eng_win = tk.Toplevel(root)
    eng_win.title("Engineering Mode")
    eng_win.geometry("270x150")
    eng_win.configure(bg="#333333")
    eng_win.resizable(False, False)
    eng_win.grab_set()

    voltage_var = tk.StringVar()
    current_var = tk.StringVar()
    temp_var = tk.StringVar()

    tk.Label(eng_win, text="Engineering Mode", font=("Arial", 13, "bold"),
             fg="white", bg="#333333").pack(pady=(10, 8))
    tk.Label(eng_win, textvariable=voltage_var, font=("Arial", 12), fg="cyan", bg="#333333").pack(anchor="w", padx=20)
    tk.Label(eng_win, textvariable=current_var, font=("Arial", 12), fg="orange", bg="#333333").pack(anchor="w", padx=20)
    tk.Label(eng_win, textvariable=temp_var, font=("Arial", 12), fg="lightgreen", bg="#333333").pack(anchor="w", padx=20)

    def update_engineering_data_popup():
        voltage_var.set("Voltage: 220V")
        current_var.set("Current: 0.8A")
        temp_var.set("Temperature: 42°C")
        eng_win.after(2000, update_engineering_data_popup)

    update_engineering_data_popup()

# --------- Main Window ---------
root = tk.Tk()
root.title("Lumino Pro")
root.configure(bg="#2e2e2e")
root.attributes('-fullscreen', True)

# Sidebar Frame (Right Side)
sidebar_frame = tk.Frame(root, bg="gray20")
sidebar_frame.pack(side="right", fill="y", padx=(0, 0), pady=0)
create_sidebar_buttons(sidebar_frame, scale_factor=1.0, root=root)

# Header
header = tk.Label(root, text="Lumino Pro", font=("Arial", 28, "bold"),
                  fg="#ff4dff", bg="#2e2e2e")
header.place(x=20, y=20)

# Control Frame
control_frame = tk.Frame(root, bg="#2e2e2e")
control_frame.place(relx=0.35, rely=0.5, anchor="w")

# Volume Slider
tk.Label(control_frame, text="Volume", font=("Arial", 14, "bold"),
         fg="white", bg="#2e2e2e").grid(row=0, column=0, padx=40)
volume_slider = ttk.Scale(control_frame, from_=100, to=0, orient="vertical", length=150)
volume_slider.set(50)
volume_slider.grid(row=1, column=0, padx=40)

# Brightness Slider
tk.Label(control_frame, text="Brightness", font=("Arial", 14, "bold"),
         fg="white", bg="#2e2e2e").grid(row=0, column=1, padx=40)
brightness_slider = ttk.Scale(control_frame, from_=100, to=0, orient="vertical", length=150)
brightness_slider.set(75)
brightness_slider.grid(row=1, column=1, padx=40)

# Save Button
save_btn = tk.Button(control_frame, text="💾 Save Settings", command=save_settings,
                     font=("Arial", 12), bg="#4CAF50", fg="white", width=18)
save_btn.grid(row=2, column=0, columnspan=2, pady=15)

# Settings Icon (Bottom Left)
tk.Label(root, text="⚙️", font=("Arial", 90), bg="#2e2e2e", fg="#ff5733").place(relx=0.05, rely=0.7)

# Engineering Mode Icon (Top Left)
eng_icon_btn = tk.Button(root, text="🛠️", font=("Arial", 30), bg="#2e2e2e", fg="#ff5733",
                         bd=0, activebackground="#2e2e2e", activeforeground="#ff5733",
                         command=show_engineering_popup)
eng_icon_btn.place(relx=0.05, rely=0.25)

root.mainloop()
