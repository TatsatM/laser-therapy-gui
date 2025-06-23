import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pathlib import Path
import subprocess
import sys

# -------------------- CONFIG --------------------

# Base project path
BASE_DIR = Path(__file__).resolve().parent.parent  # One level up from this script (e.g., PythonProject)

# Paths
IMG_PATH = BASE_DIR / "image" / "anatomy.png"
SEARCH_PAGE_SCRIPT = BASE_DIR / "PythonProject" / "search_page.py"

# List of (x, y, label) for clickable points (calculated below image load)
points = []

# Script mapping (relative and dynamic)
SCRIPT_MAP = {
    "Neck": BASE_DIR / "PythonProject" / "neck_cervicalspine.py",
    "Shoulder": BASE_DIR / "PythonProject" / "shoulder.py",
    "Elbow": BASE_DIR / "PythonProject" / "Elbow.py",
    "Wrist": BASE_DIR / "PythonProject" / "Wrist.py",
    "Lumbar Spine": BASE_DIR / "PythonProject" / "lumberspine.py",
    "Muscle Condition": BASE_DIR / "PythonProject" / "muscle_condition.py",
    "Ankle": BASE_DIR / "PythonProject" / "ankle.py",
    "TMJ": BASE_DIR / "PythonProject" / "TMJ.py",
    "Hip": BASE_DIR / "PythonProject" / "Hip.py",
    "Knee": BASE_DIR / "PythonProject" / "knee.py",
    "Foot": BASE_DIR / "PythonProject" / "foot.py",
    "Neuropathy": BASE_DIR / "PythonProject" / "neuropathy.py",
    "Skin Condition": BASE_DIR / "PythonProject" / "skin.py",
}

# -------------------- GUI CLASS --------------------

class AnatomyImageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Anatomy Image with Points")

        # Load image
        img = Image.open(IMG_PATH)
        widthimg, heightimg = img.size
        self.photo = ImageTk.PhotoImage(img)

        global points
        points = [
            (widthimg / 3.3, heightimg / 6.9, "TMJ"),
            (widthimg / 2.63, heightimg / 4, "Shoulder"),
            (widthimg / 6.4, heightimg / 2.5, "Elbow"),
            (widthimg / 3, heightimg / 2.1, "Hip"),
            (widthimg / 7.5, heightimg / 1.8, "Wrist"),
            (widthimg / 4.2, heightimg / 1.38, "Knee"),
            (widthimg / 3.4, heightimg / 1.065, "Foot"),
            (widthimg / 1.41, heightimg / 6.8, "Neck"),
            (widthimg / 1.465, heightimg / 1.075, "Ankle"),
            (widthimg / 1.395, heightimg / 2.3, "Lumbar Spine"),
            (widthimg / 1.350, heightimg / 1.055, "Neuropathy"),
            (widthimg / 1.25, heightimg / 2.8, "Skin Condition"),
            (widthimg / 1.50, heightimg / 1.5, "Muscle Condition")
        ]

        # Grid setup
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0)

        # Layout: Main + Sidebar
        main_frame = tk.Frame(self.root, bg="gray20")
        main_frame.grid(row=0, column=0, sticky="nsew")

        from neck_cervicalspine import create_sidebar_buttons
        sidebar = tk.Frame(self.root, bg="gray20")
        sidebar.grid(row=0, column=1, sticky="ns", padx=10, pady=10)
        create_sidebar_buttons(sidebar, 1.0, self.root)

        # Canvas for image + labels
        canvas_frame = tk.Frame(main_frame, bg="gray20")
        canvas_frame.pack(padx=10, pady=10)

        self.canvas = tk.Canvas(canvas_frame, width=widthimg, height=heightimg)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        # Draw interactive points
        RADIUS = 6
        for x, y, label in points:
            self.canvas.create_oval(x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS, fill="red")
            self.canvas.create_text(x + RADIUS + 15, y,
                                    text=label, anchor=tk.W, fill="black",
                                    font=("Segoe UI", 10, "bold"))
        self.canvas.bind("<Button-1>", self.on_click)

        # Big "List" button
        tk.Button(
            main_frame,
            text="📝 List",
            font=("Segoe UI", 28, "bold"),
            bg="#378ba4",
            fg="black",
            activebackground="#2a5d77",
            width=8,
            height=2,
            relief="raised",
            cursor="hand2",
            command=self.launch_search_page
        ).pack(pady=30)

    def launch_search_page(self):
        if SEARCH_PAGE_SCRIPT.exists():
            try:
                subprocess.Popen([sys.executable, str(SEARCH_PAGE_SCRIPT)])
            except Exception as e:
                messagebox.showerror("Launch Error", f"Could not launch search page:\n{e}")
        else:
            messagebox.showwarning("Script Not Found", f"Search page script not found:\n{SEARCH_PAGE_SCRIPT}")

    def on_click(self, event):
        RADIUS = 6
        for x, y, label in points:
            if (event.x - x) ** 2 + (event.y - y) ** 2 <= RADIUS ** 2:
                script_path = SCRIPT_MAP.get(label)
                if script_path and script_path.exists():
                    try:
                        subprocess.Popen([sys.executable, str(script_path)])
                    except Exception as e:
                        messagebox.showerror("Launch Error", f"Could not launch script for {label}:\n{e}")
                elif label == "Neuropathy":
                    messagebox.showinfo("Information", f"Script for '{label}' is not yet configured.")
                else:
                    messagebox.showwarning("Script Not Found", f"No script mapped for: {label}")
                break

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x800")
    app = AnatomyImageGUI(root)
    root.mainloop()
