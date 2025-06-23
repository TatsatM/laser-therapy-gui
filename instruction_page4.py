import tkinter as tk
import os
import sys
import subprocess

# Define relative paths instead of hardcoding absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Sequence of instruction page scripts
page_paths = [
    os.path.join(BASE_DIR, f"instruction_page{i}.py") for i in range(1, 8)
]

# Path to home screen script
home_path = os.path.join(BASE_DIR, "new_passwordscreen.py")

def navigate(current_file, direction):
    """
    Navigates to the next, previous, or home script.
    """
    try:
        current_index = page_paths.index(os.path.abspath(current_file))
        if direction == "next" and current_index < len(page_paths) - 1:
            next_path = page_paths[current_index + 1]
        elif direction == "back" and current_index > 0:
            next_path = page_paths[current_index - 1]
        elif direction == "home":
            next_path = home_path
        else:
            return  # Invalid direction or edge of list
        subprocess.Popen(["python", next_path])  # Launch next script
        sys.exit()  # Exit current script
    except Exception as e:
        print(f"Navigation error: {e}")

def create_sidebar_buttons(sidebar, current_file, scale_factor=1.0):
    """
    Creates navigation buttons on the sidebar.
    """
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

def draw_bio_modulation_gui():
    """
    Main GUI rendering function.
    """
    current_file = os.path.abspath(__file__)
    root = tk.Tk()
    root.title("Photo Bio-Modulation Therapy")
    root.configure(bg="#2f2f2f")

    # Fullscreen scaling
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width * 0.95)
    window_height = int(screen_height * 0.9)
    root.geometry(f"{window_width}x{window_height}")

    # Main content area
    content_frame = tk.Frame(root, bg="#2f2f2f")
    content_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    # Header Section
    header_frame = tk.Frame(content_frame, bg="#2f2f2f")
    header_frame.pack(fill="x", pady=(10, 0))

    tk.Label(header_frame, text="Lumino Pro", font=("Helvetica", 20, "bold"),
             fg="red", bg="#2f2f2f").pack(side="left", padx=20)

    tk.Label(header_frame, text="Photo Bio-Modulation Therapy",
             font=("Helvetica", 30, "bold"), fg="#ff4d4d", bg="#2f2f2f").pack(side="left", padx=100)

    # Left content box with primary description
    left_frame = tk.Frame(content_frame, bg="#5c0d0d", bd=2, relief="ridge")
    left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    tk.Label(left_frame,
             text="Light enters Cell's Mitochondria and is\nabsorbed by Chromophores, including\nthe Protein Cytochrome C Oxidase.",
             font=("Helvetica", 20, "bold"), fg="white", bg="#5c0d0d", justify="center", wraplength=400
             ).pack(expand=True)

    # Right content box with effects
    right_frame = tk.Frame(content_frame, bg="#2f2f2f")
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # Box: ATP
    atp_box = tk.Label(right_frame,
                       text="🧬 Adenosine Triphosphate\nIncrease in ATP increases cell's\nability to fight infection &\naccelerates healing process.",
                       font=("Helvetica", 14, "bold"), fg="black", bg="#66ffff", bd=4, relief="ridge",
                       padx=10, pady=10, wraplength=300, justify="center")
    atp_box.pack(pady=10, fill="x")

    # Box: Reactive Oxygen Species (ROS)
    ros_box = tk.Label(right_frame,
                       text="Reactive Oxygen Species\nModulation of ROS activates\ntranscription factors positively\nimpacting cellular repair & healing.",
                       font=("Helvetica", 14, "bold"), fg="white", bg="#ff66cc", bd=4, relief="ridge",
                       padx=10, pady=10, wraplength=300, justify="center")
    ros_box.pack(pady=10, fill="x")

    # Box: Nitric Oxide
    no_box = tk.Label(right_frame,
                      text="Nitric Oxide release, a potent\nvasodilator, increases circulation,\ndecreases inflammation and enhances the\ntransport of oxygen and immune cells through tissue.",
                      font=("Helvetica", 14), fg="black", bg="#ffe599", bd=4, relief="ridge",
                      padx=10, pady=10, wraplength=300, justify="center")
    no_box.pack(pady=10, fill="x")

    # Sidebar for navigation
    sidebar = tk.Frame(root, bg="#1c1c1c", width=200)
    sidebar.pack(side="right", fill="y")

    scale_factor = window_width / 1300
    create_sidebar_buttons(sidebar, current_file, scale_factor=scale_factor)

    root.mainloop()

if __name__ == "__main__":
    draw_bio_modulation_gui()
