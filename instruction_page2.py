import tkinter as tk
import os
import sys
import subprocess
from PIL import Image, ImageTk  # For displaying anatomy image

# --- Universal Path Setup ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Current script directory

# Paths to navigation pages (relative to BASE_DIR)
page_files = [
    "instruction_page1.py",
    "instruction_page2.py",
    "instruction_page3.py",
    "instruction_page4.py",
    "instruction_page5.py",
    "instruction_page6.py",
    "instruction_page7.py",
]

page_paths = [os.path.join(BASE_DIR, file) for file in page_files]
home_path = os.path.join(BASE_DIR, "new_passwordscreen.py")

# --- Navigation Logic ---
def navigate(current_file, direction):
    try:
        current_index = page_paths.index(os.path.abspath(current_file))
        if direction == "next" and current_index < len(page_paths) - 1:
            next_path = page_paths[current_index + 1]
        elif direction == "back" and current_index > 0:
            next_path = page_paths[current_index - 1]
        elif direction == "home":
            next_path = home_path
        else:
            return  # Invalid direction or out of range

        subprocess.Popen([sys.executable, next_path])
        sys.exit()
    except Exception as e:
        print(f"Navigation error: {e}")

# --- Sidebar Button Creation ---
def create_sidebar_buttons(sidebar, current_file, scale_factor=1.0):
    buttons = [
        ("🏠 Home", lambda: navigate(current_file, "home")),
        ("🔙 Back", lambda: navigate(current_file, "back")),
        ("➡️ Next", lambda: navigate(current_file, "next")),
    ]
    for text, cmd in buttons:
        btn = tk.Button(
            sidebar, text=text, font=("Segoe UI", int(16 * scale_factor), "bold"),
            bg="#2a5d77", fg="white", activebackground="#378ba4",
            activeforeground="white", width=14, height=2, command=cmd
        )
        btn.pack(pady=int(10 * scale_factor), padx=5)

# --- Main GUI Layout ---
def design_gui():
    current_file = os.path.abspath(__file__)
    root = tk.Tk()
    root.title("Lumino Pro - Power Calculation")
    root.attributes('-fullscreen', True)

    # Dynamic scaling
    base_width, base_height = 1000, 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    scale_factor = min(screen_width / base_width, screen_height / base_height)
    window_width = int(base_width * scale_factor)
    window_height = int(base_height * scale_factor)
    root.geometry(f"{window_width}x{window_height}")
    root.configure(bg="#2f2f2f")

    # Sidebar
    sidebar_width = int(180 * scale_factor)
    sidebar = tk.Frame(root, bg="#222", width=sidebar_width)
    sidebar.place(x=window_width - sidebar_width, y=0, height=window_height)
    create_sidebar_buttons(sidebar, current_file, scale_factor)

    # Title
    title = tk.Label(
        root, text="Power Calculation", font=("Helvetica", int(26 * scale_factor), "bold"),
        fg="#ff4d4d", bg="#2f2f2f"
    )
    title.place(x=int(400 * scale_factor), y=int(10 * scale_factor))

    # Laser Acronym Box
    laser_box = tk.Frame(root, bg="#ff5500", width=int(320 * scale_factor), height=int(230 * scale_factor))
    laser_box.place(x=int(20 * scale_factor), y=int(60 * scale_factor))
    laser_texts = [("L", "ight"), ("A", "mplification by"), ("S", "timulated"),
                   ("E", "mission of"), ("R", "adiation")]
    for i, (letter, text) in enumerate(laser_texts):
        tk.Label(
            laser_box, text=letter, font=("Helvetica", int(16 * scale_factor), "bold"),
            fg="yellow", bg="#ff5500"
        ).place(x=int(10 * scale_factor), y=int(10 * scale_factor + i * 40 * scale_factor))
        tk.Label(
            laser_box, text=text, font=("Helvetica", int(14 * scale_factor)),
            fg="white", bg="#ff5500"
        ).place(x=int(40 * scale_factor), y=int(10 * scale_factor + i * 40 * scale_factor))

    # Power Calculation Formulas
    eq_frame = tk.Frame(root, bg="#2f2f2f")
    eq_frame.place(x=int(380 * scale_factor), y=int(60 * scale_factor))
    energy_eqs = [
        "Energy = Power x Time", "Joules = Watt x Sec", "",
        "1 J = 1mW x 1000 Sec", "1 J = 10mW x 100 Sec", "1 J = 100mW x 10 Sec",
        "1 J = 1000mW x 1 Sec", "", "To deliver high energy", "quickly, we need high power"
    ]
    for line in energy_eqs:
        tk.Label(
            eq_frame, text=line, font=("Helvetica", int(12 * scale_factor)), fg="white", bg="#2f2f2f"
        ).pack(anchor="w")

    # Pulse Calculation Explanation
    calc_frame = tk.Frame(root, bg="#1a1a1a", width=int(500 * scale_factor), height=int(150 * scale_factor))
    calc_frame.place(x=int(100 * scale_factor), y=int(310 * scale_factor))
    calc_texts = [
        "Pulse Mode Average Power = P³", "P³ = Power x Pulse Width x Pulse Freq", "",
        "P = 50mW x 200 nSec x 2000Hz   = 20mW",
        "P = 50mW x 200 nSec x 10,000Hz = 100mW",
        "Diode Power same - 50mW but", "Average Power increased by frequency."
    ]
    for i, line in enumerate(calc_texts):
        tk.Label(
            calc_frame, text=line, font=("Helvetica", int(12 * scale_factor)),
            fg="white", bg="#1a1a1a"
        ).place(x=int(10 * scale_factor), y=int(5 * scale_factor + i * 20 * scale_factor))

    # Anatomy Image (Optional)
    image_path = os.path.join(BASE_DIR, "image", "anatomy.png")
    try:
        temp_img = Image.open(image_path)
        temp_img = temp_img.resize((int(220 * scale_factor), int(250 * scale_factor)))
        photo = ImageTk.PhotoImage(temp_img)
        image_label = tk.Label(root, image=photo, bg="#2f2f2f")
        image_label.image = photo  # Keep a reference
        image_label.place(x=int(650 * scale_factor), y=int(310 * scale_factor))
    except FileNotFoundError:
        print(f"Image not found at {image_path}")

    root.mainloop()

# --- Entry Point ---
if __name__ == "__main__":
    design_gui()
