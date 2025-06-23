import tkinter as tk
import os
import sys
import subprocess

# === Universal Path Configuration ===

# Root directory for all scripts
BASE_DIR = os.path.join("C:", os.sep, "Users", "malvi", "OneDrive", "Desktop", "project delhi", "PythonProject")

# Instruction pages list
page_paths = [
    os.path.join(BASE_DIR, f"instruction_page{i}.py") for i in range(1, 8)
]

# Home screen path
home_path = os.path.join(BASE_DIR, "new_passwordscreen.py")


# === Navigation Function ===

def navigate(current_file, direction):
    """
    Handle page navigation: next, back, and home.
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
            return  # Invalid direction or edge page reached

        # Open target script and close current one
        subprocess.Popen(["python", next_path])
        sys.exit()
    except Exception as e:
        print(f"Navigation error: {e}")


# === Sidebar Buttons Creator ===

def create_sidebar_buttons(sidebar, current_file, scale_factor=1.0):
    """
    Create sidebar with navigation buttons (Back, Next).
    """
    buttons = [
        ("🏠 Home", lambda: navigate(current_file, "home")),
        ("🔙 Back", lambda: navigate(current_file, "back")),
        ("➡️ Next", lambda: navigate(current_file, "next")),
    ]
    for text, cmd in buttons:
        btn = tk.Button(
            sidebar,
            text=text,
            font=("Segoe UI", int(16 * scale_factor), "bold"),
            bg="#2a5d77",
            fg="white",
            activebackground="#378ba4",
            activeforeground="white",
            width=14,
            height=2,
            command=cmd
        )
        btn.pack(pady=int(10 * scale_factor), padx=5)


# === Main GUI Window ===

def draw_indications_gui():
    """
    GUI showing therapy indications with navigation and styling.
    """
    current_file = os.path.abspath(__file__)
    root = tk.Tk()
    root.title("Photo Bio-Modulation Therapy - Indications")
    root.configure(bg="#2f2f2f")

    # Adjust window to full screen size
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width * 0.95)
    window_height = int(screen_height * 0.9)
    root.geometry(f"{window_width}x{window_height}")

    # Header frame with title
    header_frame = tk.Frame(root, bg="#2f2f2f")
    header_frame.pack(fill="x", pady=(10, 0))

    tk.Label(header_frame, text="Lumino Pro", font=("Helvetica", 20, "bold"),
             fg="red", bg="#2f2f2f").pack(side="left", padx=20)

    tk.Label(root, text="Indications", font=("Helvetica", 22, "bold", "underline"),
             fg="yellow", bg="#2f2f2f", anchor="w").pack(anchor="w", padx=40, pady=(10, 10))

    # Content container
    main_frame = tk.Frame(root, bg="#2f2f2f")
    main_frame.pack(fill="both", expand=True, padx=40, pady=10)

    # Indication data frames
    content_frame = tk.Frame(main_frame, bg="#2f2f2f")
    content_frame.pack(side="left", fill="both", expand=True)

    # Left and Right lists of indications
    left_list = [
        "Achilles tendinitis", "Ankle Sprain", "Arthritis", "Bursitis",
        "Carpal tunnel syndrome (CTS)", "De Quervain's tenosynovitis",
        "Degenerative Disc disease", "Diabetic neuropathy", "Discs Herniation",
        "Facet Joint Syndrome", "Frozen shoulder", "Golfer’s elbow",
        "Greater trochanteric pain syndrome", "Iliotibial band syndrome",
        "Jumper’s knee", "Knee osteoarthritis", "Meniscus tear", "Morton's neuroma",
        "Muscle spasms", "Pes Anserine Bursitis", "Plantar fasciitis",
        "Piriformis syndrome", "Runner’s knee"
    ]

    right_list = [
        "Sacroiliac Neuralgia", "Sciatica", "Spinal Stenosis", "Cervical Spondyloarthrosis",
        "Spondylolisthesis", "Cervical Spondylosis", "Sprains", "Strains",
        "Swimmer’s shoulder", "Temporomandibular disorders", "Wrist tendinitis",
        "Tennis elbow", "Skin -", "    Burns", "    Bedsores / Ulcers", "    Wrinkles",
        "    Stretch Marks", "    Skin Rejuvenation", "    Acne vulgaris",
        "    Herpes simplex", "    Wound healing", "    Toenail fungus"
    ]

    # Display left column
    left_frame = tk.Frame(content_frame, bg="#2f2f2f")
    left_frame.pack(side="left", fill="both", expand=True)

    for item in left_list:
        tk.Label(left_frame, text="• " + item, font=("Helvetica", 14, "bold"),
                 fg="white", bg="#2f2f2f", anchor="w").pack(anchor="w", pady=1)

    # Display right column
    right_frame = tk.Frame(content_frame, bg="#2f2f2f")
    right_frame.pack(side="left", fill="both", expand=True, padx=(50, 0))

    for item in right_list:
        tk.Label(right_frame, text="• " + item, font=("Helvetica", 14, "bold"),
                 fg="white", bg="#2f2f2f", anchor="w").pack(anchor="w", pady=1)

    # Sidebar for nav buttons
    sidebar = tk.Frame(main_frame, bg="#1c1c1c", width=200)
    sidebar.pack(side="right", fill="y", padx=(30, 0))

    scale_factor = window_width / 1300
    create_sidebar_buttons(sidebar, current_file, scale_factor=scale_factor)

    # Bottom navigation row
    nav_frame = tk.Frame(root, bg="#2f2f2f")
    nav_frame.pack(fill="x", pady=(20, 10))

    for text, direction in [("Home", "home"), ("Back", "back"), ("Next", "next")]:
        tk.Button(nav_frame, text=text, font=("Helvetica", 14, "bold"),
                  width=12, height=1, bg="#ff4d4d", fg="white",
                  command=lambda d=direction: navigate(current_file, d)).pack(side="left", padx=40)

    root.mainloop()


# Entry point
if __name__ == "__main__":
    draw_indications_gui()
