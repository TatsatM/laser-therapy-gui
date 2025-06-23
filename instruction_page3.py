import tkinter as tk
import os
import sys
import subprocess

# Automatically detect the current directory to make paths universal
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the order of instruction pages using relative paths
page_paths = [
    os.path.join(BASE_DIR, "instruction_page1.py"),
    os.path.join(BASE_DIR, "instruction_page2.py"),
    os.path.join(BASE_DIR, "instruction_page3.py"),
    os.path.join(BASE_DIR, "instruction_page4.py"),
    os.path.join(BASE_DIR, "instruction_page5.py"),
    os.path.join(BASE_DIR, "instruction_page6.py"),
    os.path.join(BASE_DIR, "instruction_page7.py"),
]

# Define the path to the home screen (password screen)
home_path = os.path.join(BASE_DIR, "new_passwordscreen.py")

# Function to navigate between pages (Next, Back, Home)
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
            return
        subprocess.Popen(["python", next_path])  # Launch next page
        sys.exit()  # Exit current window
    except Exception as e:
        print(f"Navigation error: {e}")

# Function to create sidebar navigation buttons
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

# Main GUI function
def draw_photo_biomodulation_gui():
    current_file = os.path.abspath(__file__)
    root = tk.Tk()
    root.title("Photo Bio-Modulation Therapy")

    # Scale window to 95% of screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width * 0.95)
    window_height = int(screen_height * 0.9)
    root.geometry(f"{window_width}x{window_height}")
    root.configure(bg="#2f2f2f")

    # Main frame for content
    main_frame = tk.Frame(root, bg="#2f2f2f")
    main_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Header with title and branding
    header_frame = tk.Frame(main_frame, bg="#2f2f2f")
    header_frame.pack(pady=(10, 0), fill="x")

    # Branding label
    tk.Label(header_frame, text="Lumino Pro", font=("Helvetica", 20, "bold"),
             fg="red", bg="#2f2f2f").pack(side="left", padx=20)

    # Main title label
    tk.Label(header_frame, text="Photo Bio-Modulation Therapy",
             font=("Helvetica", 30, "bold"), fg="#ff4d4d", bg="#2f2f2f").pack(side="left", padx=100)

    # Description of the therapy
    description = (
        "Chromophore is the light-absorbing part of a molecule and is responsible for its colour.\n"
        "Specific chromophores absorb specific wavelengths of laser radiation.\n"
        "The primary chromophores in tissue are seen in Water, Oxy-hemoglobin,\n"
        "Mitochondrial Cytochrome C and Melanin."
    )
    tk.Label(main_frame, text=description, font=("Helvetica", 20), fg="white", bg="#2f2f2f",
             justify="center", wraplength=window_width - 200).pack(pady=(30, 10))

    # Table showing wavelength vs. chromophore absorption
    table_frame = tk.Frame(main_frame, bg="#2f2f2f")
    table_frame.pack(expand=True, fill="both", pady=10)

    wavelengths = ["638nm", "808nm", "980nm", "1064nm"]
    chromophores = ["Melanin", "Mitochondrial\nCytochrome C", "Oxy-\nHemoglobin", "Water"]
    placeholders = ["[Melanin]", "[Mitochondria]", "[Hemoglobin]", "[Water]"]
    colors = ["#ffa07a", "#ffd700", "#ff8c00", "#ffa500"]

    # Configure grid rows and columns
    for i in range(4):
        table_frame.columnconfigure(i, weight=1)
    for i in range(3):
        table_frame.rowconfigure(i, weight=1)

    # Populate the table
    for i in range(4):
        tk.Label(table_frame, text=wavelengths[i], font=("Helvetica", 18, "bold"),
                 bg=colors[i], fg="black", relief="ridge").grid(row=0, column=i, sticky="nsew", padx=4, pady=4)
        tk.Label(table_frame, text=chromophores[i], font=("Helvetica", 15, "bold"),
                 bg=colors[i], fg="black", relief="ridge", justify="center").grid(row=1, column=i, sticky="nsew", padx=4, pady=4)
        tk.Label(table_frame, text=placeholders[i], font=("Helvetica", 14),
                 bg=colors[i], fg="black", relief="ridge").grid(row=2, column=i, sticky="nsew", padx=4, pady=4)

    # Sidebar for navigation
    sidebar = tk.Frame(root, bg="#1c1c1c", width=200)
    sidebar.pack(side="right", fill="y")

    # Add navigation buttons
    create_sidebar_buttons(sidebar, current_file, scale_factor=window_width / 1300)

    # Run the GUI loop
    root.mainloop()

# Entry point
if __name__ == "__main__":
    draw_photo_biomodulation_gui()
