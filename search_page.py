import tkinter as tk
from tkinter import messagebox
from neck_cervicalspine import create_sidebar_buttons
import subprocess
import sys

# List of conditions
ISSUES = sorted([
    "Spondylosis", "Spondylo-arthrosis", "Spondylitis", "Frozen shoulder", "Swimmer's shoulder",
    "Golfer's elbow", "Tennis elbow", "De Quervain's Tenosynovitis", "Tendinitis of wrist", "Carpal tunnel syndrome (CTS)",
    "Degenerative Disc", "Herniated Discs", "Spondylolisthesis", "Spinal Stenosis", "Sciatica", "Sacroiliitis",
    "Piriformis syndrome", "Muscle Spasm", "Strains", "Sprains", "Achilles tendinitis", "Ankle Sprain",
    "TMDs", "GTPS", "ITBS", "Knee OA", "Runner's knee", "Jumper's knee", "Meniscus tear",
    "Pes Anserine Bursitis", "Plantar fasciitis", "Morton's neuroma", "Diabetic neuropathy", "Burns",
    "Bedsores/ Ulcer", "Wrinkles", "Stretch Marks", "Skin Rejuvenation", "Acne vulgaris", "Herpes simplex",
    "Wound healing", "Toe Nail Fungus"
])

# Map conditions to body-part scripts
CONDITION_TO_SCRIPT = {
    "Frozen shoulder": "shoulder.py",
    "Swimmer's shoulder": "shoulder.py",
    "Tennis elbow": "elbow.py",
    "Golfer's elbow": "elbow.py",
    "De Quervain's Tenosynovitis": "wrist.py",
    "Tendinitis of wrist": "wrist.py",
    "Carpal tunnel syndrome (CTS)": "wrist.py",
    "Achilles tendinitis": "ankle.py",
    "Ankle Sprain": "ankle.py",
    "TMDs": "tmj.py",
    "Burns": "skin.py",
    "Bedsores/ Ulcer": "skin.py",
    "Wrinkles": "skin.py",
    "Stretch Marks": "skin.py",
    "Skin Rejuvenation": "skin.py",
    "Acne vulgaris": "skin.py",
    "Herpes simplex": "skin.py",
    "Wound healing": "skin.py",
    "Toe Nail Fungus": "skin.py"
    # Add remaining mappings as needed
}

class SearchPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Search Issues")
        self.geometry("1000x750")

        self.filtered_issues = list(ISSUES)

        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        content_frame = tk.Frame(main_frame)
        content_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        sidebar = tk.Frame(main_frame, bg="gray20")
        sidebar.grid(row=0, column=1, sticky="ns", padx=10, pady=10)

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=0)
        main_frame.rowconfigure(0, weight=1)

        tk.Label(content_frame, text="Search and Select an Issue:", font=("Arial", 14)).pack(pady=10)

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.update_list)

        self.search_entry = tk.Entry(content_frame, textvariable=self.search_var, font=("Arial", 12), width=120)
        self.search_entry.pack(pady=5, ipady=10)
        self.search_entry.bind("<Return>", self.enter_key_pressed)

        list_frame = tk.Frame(content_frame)
        list_frame.pack(pady=10)

        self.scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(list_frame, selectmode=tk.BROWSE, height=12, width=60, yscrollcommand=self.scrollbar.set, font=("Arial", 11))
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for issue in self.filtered_issues:
            self.listbox.insert(tk.END, issue)

        self.listbox.bind("<<ListboxSelect>>", self.on_selection)

        self.selected_var = tk.StringVar()
        self.selected_label = tk.Label(content_frame, textvariable=self.selected_var, wraplength=700, font=("Arial", 11), fg="blue")
        self.selected_label.pack(pady=10)

        self.create_virtual_keyboard(content_frame)
        create_sidebar_buttons(sidebar, scale_factor=1, root=self)

    def update_list(self, *args):
        search_term = self.search_var.get().lower()
        self.filtered_issues = [issue for issue in ISSUES if search_term in issue.lower()]
        self.listbox.delete(0, tk.END)
        for issue in self.filtered_issues:
            self.listbox.insert(tk.END, issue)

    def on_selection(self, event):
        selection = self.listbox.curselection()
        if selection:
            selected_issue = self.filtered_issues[selection[0]]
            self.selected_var.set(f"Selected: {selected_issue}")
        else:
            self.selected_var.set("")

    def create_virtual_keyboard(self, parent):
        keyboard_frame = tk.Frame(parent)
        keyboard_frame.pack(pady=10)

        keys = [
            list("QWERTYUIOP"),
            list("ASDFGHJKL"),
            list("ZXCVBNM"),
            ["Enter", "Space", "Clear"]
        ]

        for row in keys:
            row_frame = tk.Frame(keyboard_frame)
            row_frame.pack()
            for key in row:
                width = 6
                height = 3
                if key == "Enter":
                    width = 12
                elif key in ["Space", "Clear"]:
                    width = 10
                btn = tk.Button(row_frame, text=key, width=width, height=height, command=lambda k=key: self.on_key_press(k))
                btn.pack(side=tk.LEFT, padx=2, pady=2)

    def on_key_press(self, key):
        current = self.search_var.get()
        if key == "Backspace":
            self.search_var.set(current[:-1])
        elif key == "Space":
            if current:  # only add space if not empty
                self.search_var.set(current + " ")
        elif key == "Clear":
            self.search_var.set("")
        elif key == "Enter":
            self.enter_key_pressed()
        else:
            self.search_var.set(current + key)

    def enter_key_pressed(self, event=None):
        input_text = self.search_var.get().strip().lower()
        match = None
        for issue in ISSUES:
            if input_text in issue.lower():
                match = issue
                break

        if match:
            self.selected_var.set(f"Selected: {match}")
            script_name = CONDITION_TO_SCRIPT.get(match)
            if script_name:
                try:
                    subprocess.Popen([sys.executable, script_name])
                except Exception as e:
                    messagebox.showerror("Error", f"Cannot open {script_name}\n{e}")
            else:
                messagebox.showwarning("Not Found", f"No script found for '{match}'")
        else:
            messagebox.showinfo("No Match", "No matching issue found. Please check spelling or try again.")


if __name__ == "__main__":
    app = SearchPage()
    app.mainloop()
