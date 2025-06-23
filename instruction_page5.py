import tkinter as tk
import os
import sys
import subprocess

# === UNIVERSAL RELATIVE PATH SETUP ===

# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Use relative names for instruction pages
page_names = [
    "instruction_page1.py",
    "instruction_page2.py",
    "instruction_page3.py",
    "instruction_page4.py",
    "instruction_page5.py",
    "instruction_page6.py",
    "instruction_page7.py",
]

# Construct full paths dynamically
page_paths = [os.path.join(BASE_DIR, name) for name in page_names]

# Home page (e.g., password screen)
home_path = os.path.join(BASE_DIR, "new_passwordscreen.py")

# === UNIVERSAL NAVIGATION FUNCTION ===

def navigate(current_file, direction):
    """
    Navigate to the next, previous, or home screen based on direction.

    :param current_file: str - Full path to the current file.
    :param direction: str - 'next', 'back', or 'home'
    """
    try:
        current_index = page_paths.index(os.path.abspath(current_file))

        # Determine next path
        if direction == "next" and current_index < len(page_paths) - 1:
            next_path = page_paths[current_index + 1]
        elif direction == "back" and current_index > 0:
            next_path = page_paths[current_index - 1]
        elif direction == "home":
            next_path = home_path
        else:
            return  # Out of range or invalid direction

        # Open the target script and close the current one
        subprocess.Popen([sys.executable, next_path])
        sys.exit()

    except Exception as e:
        print(f"Navigation Error: {e}")

# === SIDEBAR WITH NAVIGATION BUTTONS ===

def create_sidebar_buttons(sidebar, current_file, scale_factor=1.0):
    """
    Create and pack Home, Back, and Next navigation buttons in the sidebar.

    :param sidebar: tk.Frame - Sidebar frame
    :param current_file: str - Current file path
    :param scale_factor: float - To scale UI on different screen sizes
    """
    buttons = [
        ("🏠 Home", lambda: navigate(current_file, "home")),
        ("🔙 Back", lambda: navigate(current_file, "back")),
        ("➡️ Next", lambda: navigate(current_file, "next")),
    ]

    for text, cmd in buttons:
        tk.Button(
            sidebar, text=text,
            font=("Segoe UI", int(16 * scale_factor), "bold"),
            bg="#2a5d77", fg="white",
            activebackground="#378ba4", activeforeground="white",
            width=14, height=2,
            command=cmd
        ).pack(pady=int(10 * scale_factor), padx=5)

# === EXAMPLE: BIOLOGICAL EFFECTS GUI PAGE ===

def draw_biological_effects_gui():
    """
    Creates a full-screen GUI showing biological effects of light therapy.
    Includes a sidebar for navigation.
    """
    current_file = os.path.abspath(__file__)
    root = tk.Tk()
    root.title("Photo Bio-Modulation Therapy - Biological Effects")
    root.configure(bg="#2f2f2f")

    # Get screen size and scale layout
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width * 0.95)
    window_height = int(screen_height * 0.9)
    root.geometry(f"{window_width}x{window_height}")

    # === MAIN CONTENT AREA ===
    content_frame = tk.Frame(root, bg="#2f2f2f")
    content_frame.pack(side="left", fill="both", expand=True, padx=40, pady=20)

    # Header
    tk.Label(content_frame, text="Lumino Pro", font=("Helvetica", 20, "bold"),
             fg="red", bg="#2f2f2f").pack(anchor="nw")

    tk.Label(content_frame, text="Photo Bio-Modulation Therapy",
             font=("Helvetica", 30, "bold"), fg="#ff4d4d", bg="#2f2f2f").pack(anchor="nw", pady=(0, 20))

    tk.Label(content_frame, text="Biological Effects",
             font=("Helvetica", 20, "bold", "underline"),
             fg="yellow", bg="#2f2f2f", anchor="w").pack(anchor="w", pady=(10, 20))

    # List of biological effects
    effects = [
        "Anti-Inflammation",
        "Anti-Pain (Analgesic)",
        "Accelerated Tissue Repair and Cell Growth",
        "Improved Vascular Activity",
        "Increased Metabolic Activity",
        "Trigger Points and Acupuncture Points",
        "Reduced Fibrous Tissue Formation",
        "Improved Nerve Function",
        "Immunoregulation",
        "Faster Wound Healing"
    ]

    for effect in effects:
        tk.Label(content_frame, text=effect, font=("Helvetica", 18, "bold"),
                 fg="white", bg="#2f2f2f", anchor="w").pack(anchor="w", pady=2)

    # === SIDEBAR ===
    sidebar = tk.Frame(root, bg="#1c1c1c", width=200)
    sidebar.pack(side="right", fill="y")

    scale_factor = window_width / 1300  # Scaling based on base width
    create_sidebar_buttons(sidebar, current_file, scale_factor=scale_factor)

    root.mainloop()

# === RUN MAIN ===
if __name__ == "__main__":
    draw_biological_effects_gui()
