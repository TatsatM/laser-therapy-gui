import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import subprocess
import os
import sys
import json

# === Paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

# === Therapy data for cervical spine ===
therapy_data = {
    "Spondylosis": {
        "BodyPart": "Cervical Spine",
        "Condition": "Spondylosis",
        "Power": 36,
        "Pulse Freq": 8800,
        "Time": 12,
        "Total Energy": 3400
    },
    "Spondylo-arthrosis": {
        "BodyPart": "Cervical Spine",
        "Condition": "Spondylo-arthrosis",
        "Power": 35,
        "Pulse Freq": 8500,
        "Time": 11,
        "Total Energy": 3250
    },
    "Spondylitis": {
        "BodyPart": "Cervical Spine",
        "Condition": "Spondylitis",
        "Power": 34,
        "Pulse Freq": 8700,
        "Time": 10,
        "Total Energy": 3100
    }
}

def on_condition_selected(condition):
    try:
        if condition in therapy_data:
            therapy = therapy_data[condition]
            data_to_send = {
                "User Selections": {"Condition": therapy["Condition"]},
                "Therapy Data": {
                    "Power": therapy["Power"],
                    "Pulse Freq": therapy["Pulse Freq"],
                    "Time": therapy["Time"],
                    "Total Energy": therapy["Total Energy"]
                },
                "Body Part": therapy["BodyPart"]
            }
            json_path = os.path.join(PROJECT_DIR, "PythonProject", "temp_selection.json")
            with open(json_path, "w") as f:
                json.dump(data_to_send, f)
            subprocess.Popen(["python", os.path.join(PROJECT_DIR, "PythonProject", "therapy.py")], cwd=os.path.join(PROJECT_DIR, "PythonProject"))
        else:
            messagebox.showwarning("Not Found", f"No therapy data for: {condition}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to launch therapy.py:\n{e}")

def load_and_resize_images(bodypart_img_name, anatomy_img_name, scale_factor):
    project_delhi_dir = os.path.dirname(BASE_DIR)
    bodypart_img_path = os.path.join(project_delhi_dir, "image", bodypart_img_name)
    anatomy_img_path = os.path.join(project_delhi_dir, "image", anatomy_img_name)

    # Resize body part image
    target_bodypart_width = int(450 * scale_factor)
    target_bodypart_height = int(400 * scale_factor)

    try:
        bodypart_img = Image.open(bodypart_img_path)
        original_width, original_height = bodypart_img.size
        ratio = min(target_bodypart_width / original_width, target_bodypart_height / original_height)
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        bodypart_img = bodypart_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        bodypart_photo = ImageTk.PhotoImage(bodypart_img)
    except Exception as e:
        messagebox.showerror("Image Error", f"Body part image error:\n{e}")
        bodypart_photo = ImageTk.PhotoImage(Image.new("RGB", (target_bodypart_width, target_bodypart_height), "gray"))

    # Resize anatomy image
    target_anatomy_width = int(530 * scale_factor)
    target_anatomy_height = int(700 * scale_factor)

    try:
        anatomy_img = Image.open(anatomy_img_path)
        original_width, original_height = anatomy_img.size
        ratio = min(target_anatomy_width / original_width, target_anatomy_height / original_height)
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        anatomy_img = anatomy_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        anatomy_photo = ImageTk.PhotoImage(anatomy_img)
    except Exception as e:
        messagebox.showerror("Image Error", f"Anatomy image error:\n{e}")
        anatomy_photo = ImageTk.PhotoImage(Image.new("RGB", (target_anatomy_width, target_anatomy_height), "gray"))

    return bodypart_photo, anatomy_photo

def create_sidebar_buttons(sidebar, scale_factor, root):
    sidebar_buttons = ["🔄 Auto", "📜 Protocol", "🏃 Therapy", "🏠 Home", "🔙 Back"]

    def on_button_click(name):
        script_paths = {
            "🔄 Auto": os.path.join(BASE_DIR, "automode.py"),
            "📜 Protocol": os.path.join(BASE_DIR, "protocol1.py"),
            "🏃 Therapy": os.path.join(BASE_DIR, "therapyq.py"),
            "🏠 Home": os.path.join(BASE_DIR, "new_passwordscreen.py")
        }
        if name == "🔙 Back":
            root.destroy()
        elif name in script_paths and os.path.exists(script_paths[name]):
            subprocess.Popen([sys.executable, script_paths[name]])
            root.destroy()

    for btn_text in sidebar_buttons:
        canvas = tk.Canvas(sidebar, width=int(160*scale_factor), height=int(100*scale_factor), bg="gray20", highlightthickness=0)
        canvas.pack(pady=int(10 * scale_factor))
        rect = canvas.create_rectangle(0, 0, int(160*scale_factor), int(100*scale_factor), fill="#2a5d77", outline="")
        text_id = canvas.create_text(int(80*scale_factor), int(50*scale_factor), text=btn_text, font=("Segoe UI", int(16*scale_factor), "bold"), fill="white")
        for item in [rect, text_id]:
            canvas.tag_bind(item, "<Enter>", lambda e, c=canvas, r=rect: c.itemconfig(r, fill="#378ba4"))
            canvas.tag_bind(item, "<Leave>", lambda e, c=canvas, r=rect: c.itemconfig(r, fill="#2a5d77"))
            canvas.tag_bind(item, "<Button-1>", lambda e, name=btn_text: on_button_click(name))

def create_layout(root, anatomy_photo, bodypart_photo, scale_factor,
                  title="Lumino Pro", scroll_title="Cervical Spine", info_list=None, callback=None):
    if info_list is None:
        info_list = list(therapy_data.keys())

    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(1, weight=1)

    tk.Label(root, text=title, font=("Arial", int(28*scale_factor), "bold"), fg="red", bg="gray20").grid(row=0, column=0, columnspan=3, sticky="w", padx=20, pady=(10, 0))

    # Anatomy Image
    anatomy_label = tk.Label(root, image=anatomy_photo, bg="gray20")
    anatomy_label.grid(row=1, column=0, rowspan=3, padx=10, pady=(10, 0), sticky="n")

    # Platform Canvas under anatomy image
    platform_canvas = tk.Canvas(root, width=int(530 * scale_factor), height=int(40 * scale_factor), bg="#1e1e1e", highlightthickness=0)
    platform_canvas.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="n")
    platform_canvas.create_rectangle(
        0, 0,
        int(530 * scale_factor),
        int(40 * scale_factor),
        fill="#3c3c3c",
        outline="#2a2a2a"
    )

    # Middle frame
    middle_frame = tk.Frame(root, bg="gray20")
    middle_frame.grid(row=1, column=1, sticky="n")

    tk.Label(middle_frame, image=bodypart_photo, bg="gray20").pack(pady=10)
    tk.Label(middle_frame, text=scroll_title, font=("Helvetica", int(22*scale_factor), "bold"), fg="yellow", bg="gray25").pack(fill="x", padx=10, pady=(10, 0))

    scroll_canvas = tk.Canvas(middle_frame, height=int(250*scale_factor), width=int(420*scale_factor), bg="gray25", highlightthickness=0)
    scroll_canvas.pack(padx=10, pady=(0, 20), fill="x")
    scrollbar = ttk.Scrollbar(middle_frame, orient="vertical", command=scroll_canvas.yview)
    scrollbar.place(in_=scroll_canvas, relx=1.0, rely=0, relheight=1.0, anchor="ne")
    text_frame = tk.Frame(scroll_canvas, bg="gray25")
    scroll_canvas.create_window((scroll_canvas.winfo_width() / 2, 0), window=text_frame, anchor="n", tags="text_frame_window")
    scroll_canvas.configure(yscrollcommand=scrollbar.set)

    def update_scroll_region(event):
        scroll_canvas.update_idletasks()
        scroll_canvas.itemconfig("text_frame_window", width=scroll_canvas.winfo_width())
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

    scroll_canvas.bind("<Configure>", update_scroll_region)
    text_frame.bind("<Configure>", update_scroll_region)

    for item in info_list:
        btn = tk.Button(text_frame, text=item, font=("Segoe UI", int(18*scale_factor), "bold"), fg="white", bg="#284b63",
                        activebackground="#3b6a8d", activeforeground="white", width=28, relief="flat", bd=0,
                        cursor="hand2", padx=10, pady=10, command=lambda i=item: callback(i) if callback else print(f"{i} clicked!"))
        btn.pack(pady=8, padx=12)
        btn.bind("<Enter>", lambda e: e.widget.config(bg="#3b6a8d"))
        btn.bind("<Leave>", lambda e: e.widget.config(bg="#284b63"))

    # Sidebar
    sidebar = tk.Frame(root, bg="gray20")
    sidebar.grid(row=1, column=2, padx=10, pady=10, sticky="ne")
    create_sidebar_buttons(sidebar, scale_factor, root)

def main():
    root = tk.Tk()
    root.title("Lumino Pro - Cervical Spine")
    root.attributes('-fullscreen', True)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    scale_factor = min(screen_width / 1300, screen_height / 750)

    root.geometry(f"{int(1300 * scale_factor)}x{int(750 * scale_factor)}")
    root.configure(bg="gray20")

    neck_img_name = r"bodyparts\Neck.png"
    anatomy_img_name = r"anatomy.png"

    neck_photo, anatomy_photo = load_and_resize_images(neck_img_name, anatomy_img_name, scale_factor)

    create_layout(
        root,
        anatomy_photo,
        neck_photo,
        scale_factor,
        title="Lumino Pro",
        scroll_title="Cervical Spine",
        info_list=list(therapy_data.keys()),
        callback=on_condition_selected
    )

    root.mainloop()

if __name__ == "__main__":
    main()
