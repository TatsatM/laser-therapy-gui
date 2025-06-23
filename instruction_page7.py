import tkinter as tk
import subprocess
import sys
import os

# === Get the base folder (i.e., current project directory) ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# === Use universal relative paths from BASE_DIR ===
page_paths = [
    os.path.join(BASE_DIR, "instruction_page5.py"),
    os.path.join(BASE_DIR, "instruction_page6.py"),  # This file
    os.path.join(BASE_DIR, "instruction_page7.py"),
]

home_path = os.path.join(BASE_DIR, "new_passwordscreen.py")

def navigate(current_file, direction):
    """
    Navigate to the next, previous, or home page based on direction.
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
            return

        subprocess.Popen(["python", next_path])
        sys.exit()

    except Exception as e:
        print(f"Navigation error: {e}")

def create_sidebar_buttons(sidebar, current_file, scale_factor=1.0):
    """
    Creates navigation buttons in the sidebar.
    """
    buttons = [
        ("🏠 Home", lambda: navigate(current_file, "home")),
        ("🔙 Back", lambda: navigate(current_file, "back")),
        ("➡️ Next", lambda: navigate(current_file, "next")),
    ]

    for text, cmd in buttons:
        btn = tk.Button(
            sidebar, text=text,
            font=("Segoe UI", int(16 * scale_factor), "bold"),
            bg="#2a5d77", fg="white",
            activebackground="#378ba4", activeforeground="white",
            width=14, height=2, command=cmd
        )
        btn.pack(pady=int(10 * scale_factor), padx=5)

def create_contraindications_window():
    """
    Launches the Contraindications page window.
    """
    current_file = os.path.abspath(__file__)

    root = tk.Tk()
    root.title("Contraindications")
    root.configure(bg="#2f2f2f")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width * 0.95)
    window_height = int(screen_height * 0.9)
    root.geometry(f"{window_width}x{window_height}")

    sidebar = tk.Frame(root, bg="#222222")
    sidebar.pack(side="right", fill="y", padx=(15, 0), pady=10)
    create_sidebar_buttons(sidebar, current_file, scale_factor=window_width / 1300)

    title_label = tk.Label(root, text="Contraindications", font=("Arial", 36, "bold"),
                           fg="white", bg="#2f2f2f")
    title_label.pack(pady=(30, 10), anchor="nw", padx=40)

    contraindications_text = (
        "• Fresh haematomas\n"
        "• Malignant, semi-malignant and benign tumours\n"
        "• Treatments in area surrounding eye\n"
        "• Carotid Triangle\n"
        "• Pregnancy in the region of the abdomen and lower back during menstruation\n"
        "• Particular caution is required when administering treatment\n"
        "  near the ear, nose, mucous membranes and blood vessels.\n"
        "  Direct radiation must be avoided."
    )

    contraindications_label = tk.Label(
        root,
        text=contraindications_text,
        font=("Arial", 16),
        fg="white",
        bg="#2f2f2f",
        justify="left",
        wraplength=800
    )
    contraindications_label.pack(padx=40, anchor="nw")

    nav_frame = tk.Frame(root, bg="#2f2f2f")
    nav_frame.pack(fill="x", pady=(20, 10))

    tk.Button(nav_frame, text="Home", font=("Helvetica", 14, "bold"),
              width=12, height=1, bg="#ff4d4d", fg="white",
              command=lambda: navigate(current_file, "home")).pack(side="left", padx=40)

    tk.Button(nav_frame, text="Back", font=("Helvetica", 14, "bold"),
              width=12, height=1, bg="#ff4d4d", fg="white",
              command=lambda: navigate(current_file, "back")).pack(side="left", padx=40)

    tk.Button(nav_frame, text="Next", font=("Helvetica", 14, "bold"),
              width=12, height=1, bg="#ff4d4d", fg="white",
              command=lambda: navigate(current_file, "next")).pack(side="left", padx=40)

    root.mainloop()

if __name__ == "__main__":
    create_contraindications_window()
