import tkinter as tk
import subprocess
import sys
import os

# ----- Universal Path Setup -----
# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# List of all instruction page scripts (update this list as needed)
PAGE_PATHS = [
    os.path.join(BASE_DIR, "instruction_page1.py"),
    os.path.join(BASE_DIR, "instruction_page2.py"),
    os.path.join(BASE_DIR, "instruction_page3.py"),
    os.path.join(BASE_DIR, "instruction_page4.py"),
    os.path.join(BASE_DIR, "instruction_page5.py"),
    os.path.join(BASE_DIR, "instruction_page6.py"),
    os.path.join(BASE_DIR, "instruction_page7.py")
]

# Path to the home screen script (password screen)
HOME_PAGE = os.path.join(BASE_DIR, "new_passwordscreen.py")

# ----- Navigation Handler -----
def navigate(action, current_file):
    """Handles navigation between pages."""
    try:
        current_file = os.path.abspath(current_file)

        if action == "Home":
            # Go to home page
            subprocess.Popen([sys.executable, HOME_PAGE])
        else:
            # Find the current index
            index = PAGE_PATHS.index(current_file)

            # Navigate to next page if it exists
            if action == "Next" and index < len(PAGE_PATHS) - 1:
                subprocess.Popen([sys.executable, PAGE_PATHS[index + 1]])

            # Navigate to previous page if it exists
            elif action == "Back" and index > 0:
                subprocess.Popen([sys.executable, PAGE_PATHS[index - 1]])

        sys.exit()  # Close current window
    except Exception as e:
        print(f"Navigation Error: {e}")

# ----- Sidebar Creation -----
def create_sidebar_buttons(sidebar, scale_factor=1.0, root=None, current_file=None):
    """Adds Home, Back, Next buttons in the sidebar."""
    sidebar_buttons = [
        ("🏠 Home", "Home"),
        ("🔙 Back", "Back"),
        ("➡️ Next", "Next")
    ]

    for btn_text, action in sidebar_buttons:
        btn = tk.Button(
            sidebar,
            text=btn_text,
            font=("Segoe UI", int(16 * scale_factor), "bold"),
            bg="#2a5d77",
            fg="white",
            activebackground="#378ba4",
            activeforeground="white",
            width=14,
            height=2,
            command=lambda a=action: navigate(a, current_file)
        )
        btn.pack(pady=int(10 * scale_factor), padx=5)

# ----- Add L.A.S.E.R. Colored Acronym -----
def add_colored_acronym(parent):
    rows = [
        ('L', 'ight', 'red'),
        ('A', 'mplification by', 'orange'),
        ('S', 'timulated', '#B89313'),
        ('E', 'mission of', 'green'),
        ('R', 'adiation', 'blue')
    ]

    for i, (letter, rest, color) in enumerate(rows):
        row_frame = tk.Frame(parent, bg="gray")
        row_frame.grid(row=i, column=0, sticky="w")

        # First colored letter
        tk.Label(row_frame, text=letter, fg=color, bg="white", font=("Arial", 22, "bold")).pack(side="left")
        # Rest of the text
        tk.Label(row_frame, text=rest, fg="black", bg="white", font=("Arial", 22, "bold")).pack(side="left")

# ----- Main Page Class -----
class LaserClassificationPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lumino Pro - Laser Classification")
        self.attributes("-fullscreen", True)  # Fullscreen mode
        self.configure(bg="white")

        # ---- Main Frame (Content) ----
        main_frame = tk.Frame(self, bg="white")
        main_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=20, pady=10)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ---- Title Section ----
        title_frame = tk.Frame(main_frame, bg="white")
        title_frame.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        tk.Label(
            title_frame, text="Lumino Pro", font=("Arial", 24, "bold"),
            fg="#ff1a53", bg="white"
        ).pack(anchor="w")

        # Orange glow bar under title
        glow = tk.Canvas(title_frame, width=140, height=15, bg="white", highlightthickness=0)
        glow.pack(anchor="w", pady=(0, 10))
        glow.create_oval(0, 2, 140, 13, fill="#ff7f2a", outline="")

        # ---- Left: Acronym ----
        laser_frame = tk.Frame(main_frame, bg="white")
        laser_frame.grid(row=1, column=0, sticky="nw")
        add_colored_acronym(laser_frame)

        # ---- Right: Table Info ----
        table_frame = tk.Frame(main_frame, bg="white", bd=0)
        table_frame.grid(row=1, column=1, sticky="nw", padx=(60, 0))

        # Section Title
        tk.Label(
            table_frame, text="Laser Classification", font=("Arial", 26, "bold"),
            fg="#ff7f2a", bg="white"
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 18))

        # Subtitle
        tk.Label(
            table_frame, text="Laser Eye injury hazard classification\nBased on Power* (Watts)",
            font=("Arial", 13, "bold"), fg="orange", bg="white"
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # Table rows
        rows = [
            ("Class 2", "0-1 milliWatt\nNo risk"),
            ("Class 3A", "1–5 milliWatt\nLow risk"),
            ("Class 3B", "5-500 milliWatt\nMedium to High Risk"),
            ("Class 4", ">500 milliWatt\nHigh to Severe Risk")
        ]

        for i, (cls, desc) in enumerate(rows):
            bg_color = "#cfd8dc" if i % 2 == 0 else "#e0e0e0"

            tk.Label(
                table_frame, text=cls, font=("Arial", 14, "bold"),
                bg=bg_color, width=12, anchor="w"
            ).grid(row=2 + i, column=0, sticky="w", padx=(0, 5), pady=2)

            tk.Label(
                table_frame, text=desc, font=("Arial", 14),
                bg=bg_color, width=28, anchor="w"
            ).grid(row=2 + i, column=1, sticky="w", pady=2)

        # Additional Notes
        tk.Label(
            table_frame,
            text="Class IIIa Power 1-5mW\nClass IIIB Power up to 500 mW\nClass IV Power higher than 500 mW\n(500 mW = 0.5W)",
            font=("Arial", 13, "bold"), fg="black", bg="white", justify="left"
        ).grid(row=6, column=0, columnspan=2, sticky="w", pady=(20, 0))

        # ---- Sidebar ----
        sidebar = tk.Frame(self, bg="#222")
        sidebar.grid(row=0, column=1, rowspan=2, sticky="ns", padx=(15, 0))

        # Add navigation buttons to sidebar
        create_sidebar_buttons(sidebar, scale_factor=1.0, current_file=__file__)

# ----- Run the App -----
if __name__ == "__main__":
    app = LaserClassificationPage()
    app.mainloop()
