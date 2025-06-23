import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import subprocess
import json
import os

from neck_cervicalspine import create_sidebar_buttons

# === UNIVERSAL PATH SETUP ===
base_dir = os.path.expanduser(r"~\OneDrive\Desktop\project delhi")

# Paths
image_path = os.path.join(base_dir, "image", "anatomy.png")
therapy_script = os.path.join(base_dir, "PythonProject", "therapy.py")
temp_json_path = os.path.join(base_dir, "PythonProject", "temp_selection.json")

# === THERAPY DATA (shortened for brevity, include all parts here) ===
# === THERAPY DATA ===
therapy_data = {
    "ankle": {"acute": {"Power": 40, "Pulse Freq": 10000, "Time": 4, "Total Energy": 1500},
              "subacute": {"Power": 40, "Pulse Freq": 10000, "Time": 7, "Total Energy": 2400},
              "chronic": {"Power": 40, "Pulse Freq": 8000, "Time": 12, "Total Energy": 3500}},
    "knee": {"acute": {"Power": 50, "Pulse Freq": 7000, "Time": 3, "Total Energy": 1000},
             "subacute": {"Power": 50, "Pulse Freq": 7000, "Time": 6, "Total Energy": 1800},
             "chronic": {"Power": 60, "Pulse Freq": 5500, "Time": 12, "Total Energy": 3500}},
    "wrist": {"acute": {"Power": 45, "Pulse Freq": 6000, "Time": 3, "Total Energy": 750},
              "subacute": {"Power": 45, "Pulse Freq": 6000, "Time": 5, "Total Energy": 1200},
              "chronic": {"Power": 45, "Pulse Freq": 6000, "Time": 9, "Total Energy": 2100}},
    "foot": {"acute": {"Power": 40, "Pulse Freq": 10000, "Time": 4, "Total Energy": 1500},
             "subacute": {"Power": 40, "Pulse Freq": 10000, "Time": 7, "Total Energy": 2400},
             "chronic": {"Power": 40, "Pulse Freq": 6000, "Time": 6, "Total Energy": 1400}},
    "lumbar spine": {"acute": {"Power": 60, "Pulse Freq": 6500, "Time": 4, "Total Energy": 1500},
                     "subacute": {"Power": 60, "Pulse Freq": 6500, "Time": 7, "Total Energy": 2400},
                     "chronic": {"Power": 60, "Pulse Freq": 6000, "Time": 12, "Total Energy": 3500}},
    "neck": {"acute": {"Power": 40, "Pulse Freq": 8000, "Time": 5, "Total Energy": 1500},
             "subacute": {"Power": 35, "Pulse Freq": 10500, "Time": 7, "Total Energy": 2400},
             "chronic": {"Power": 35, "Pulse Freq": 10500, "Time": 11, "Total Energy": 3500}},
    "shoulder": {"acute": {"Power": 50, "Pulse Freq": 6500, "Time": 5, "Total Energy": 1500},
                 "subacute": {"Power": 50, "Pulse Freq": 6500, "Time": 8, "Total Energy": 2400},
                 "chronic": {"Power": 50, "Pulse Freq": 6500, "Time": 12, "Total Energy": 3500}},
    "elbow": {"acute": {"Power": 45, "Pulse Freq": 8000, "Time": 3, "Total Energy": 1000},
              "subacute": {"Power": 50, "Pulse Freq": 8000, "Time": 7, "Total Energy": 2400},
              "chronic": {"Power": 50, "Pulse Freq": 8000, "Time": 10, "Total Energy": 3500}},
    "tmj": {"acute": {"Power": 40, "Pulse Freq": 8000, "Time": 2, "Total Energy": 500},
            "subacute": {"Power": 40, "Pulse Freq": 8000, "Time": 3, "Total Energy": 900},
            "chronic": {"Power": 40, "Pulse Freq": 8000, "Time": 5, "Total Energy": 1400}},
    "hip": {"acute": {"Power": 50, "Pulse Freq": 8000, "Time": 4, "Total Energy": 1500},
            "subacute": {"Power": 50, "Pulse Freq": 8000, "Time": 7, "Total Energy": 2400},
            "chronic": {"Power": 60, "Pulse Freq": 6000, "Time": 11, "Total Energy": 3500}},
    "skin condition": {"acute": {"Power": 10, "Pulse Freq": 6000, "Time": 2, "Total Energy": 120},
                       "subacute": {"Power": 10, "Pulse Freq": 6000, "Time": 4, "Total Energy": 240},
                       "chronic": {"Power": 10, "Pulse Freq": 6000, "Time": 7, "Total Energy": 400}},
    "neuropathy": {"acute": {"Power": 40, "Pulse Freq": 6000, "Time": 2, "Total Energy": 900},
                   "subacute": {"Power": 40, "Pulse Freq": 6000, "Time": 4, "Total Energy": 1400},
                   "chronic": {"Power": 40, "Pulse Freq": 6000, "Time": 6, "Total Energy": 1800}},
    "muscle condition": {"acute": {"Power": 40, "Pulse Freq": 8000, "Time": 3, "Total Energy": 1000},
                         "subacute": {"Power": 40, "Pulse Freq": 8000, "Time": 6, "Total Energy": 1800},
                         "chronic": {"Power": 40, "Pulse Freq": 8000, "Time": 10, "Total Energy": 2800}}
}
# Load image size
temp_img = Image.open(image_path)
widthimg, heightimg = temp_img.size

# === CLICKABLE POINTS ===
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

RADIUS = 6
selected_circle = None
user_selections = {}
body_part_selected = None

# === MAIN WINDOW SETUP ===
root = tk.Tk()
root.title("Lumino Pro")
root.attributes('-fullscreen', True)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
app_width, app_height = int(screen_width * 0.9), int(screen_height * 0.9)
root.geometry(f"{app_width}x{app_height}")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# === RIGHT FRAME ===
right_frame = tk.Frame(root, bg="#2e2e2e", width=int(app_width * 0.35))
right_frame.grid(row=0, column=0, padx=5, pady=20, sticky="nsew")
right_frame.grid_propagate(False)

img = Image.open(image_path)
img_ratio = img.width / img.height
img_height_final = min(int(app_height * 0.8), int(app_width * 0.35 / img_ratio))
img_width_final = int(img_height_final * img_ratio)
if img_width_final > int(app_width * 0.35):
    img_width_final = int(app_width * 0.35)
    img_height_final = int(img_width_final / img_ratio)
img_resized = img.resize((img_width_final, img_height_final), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(img_resized)

canvas = tk.Canvas(right_frame, width=img_width_final, height=img_height_final,
                   bg="#2e2e2e", highlightthickness=0)
canvas.grid(row=0, column=0, sticky="nsew")
canvas.create_image(0, 0, anchor="nw", image=photo)

x_scale = img_width_final / widthimg
y_scale = img_height_final / heightimg

def on_point_click(label):
    global selected_circle, body_part_selected

    for item in canvas.find_withtag("clickable_point"):
        canvas.itemconfig(item, fill="red", outline="red")

    selected_tag = f"point_{label}"
    for item in canvas.find_withtag(selected_tag):
        canvas.itemconfig(item, fill="green", outline="green")
        selected_circle = item

    body_part_selected = label
    save_button.config(state="normal")
    for btn in input_buttons:
        btn.config(state="normal")

def on_enter():
    global user_selections

    if not body_part_selected:
        messagebox.showwarning("Warning", "Please select a body part first.")
        return

    user_selections = {headers[i]: selected_vars[i].get() for i in range(len(headers))}

    condition = user_selections["Condition"].lower()
    body_part = body_part_selected.lower()

    if body_part in therapy_data and condition in therapy_data[body_part]:
        filtered = therapy_data[body_part][condition]
    else:
        messagebox.showwarning("No Data", f"No data for condition: {user_selections['Condition']} in {body_part_selected}")
        return

    all_data = {
        "User Selections": user_selections,
        "Body Part": body_part_selected,
        "Therapy Data": filtered
    }

    try:
        with open(temp_json_path, "w") as f:
            json.dump(all_data, f, indent=2)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data:\n{e}")
        return

    try:
        subprocess.Popen(["python", therapy_script])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open therapy.py:\n{e}")

# Draw points
for x_orig, y_orig, label in points:
    x = x_orig * x_scale
    y = y_orig * y_scale
    tag = f"point_{label}"
    canvas.create_oval(x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS,
                       fill="red", outline="red", tags=("clickable_point", tag))
    canvas.create_text(x + RADIUS + 5, y, anchor="w", text=label,
                       fill="white", font=("Arial", 8, "bold"))
    canvas.tag_bind(tag, "<Button-1>", lambda event, lbl=label: on_point_click(lbl))

# === LEFT FRAME ===
left_frame = tk.Frame(root, bg="#2e2e2e")
left_frame.grid(row=0, column=1, padx=10, pady=20, sticky="nsew")
left_frame.grid_rowconfigure(0, weight=1)
left_frame.grid_columnconfigure(0, weight=1)

container = tk.Frame(left_frame, bg="#2e2e2e")
container.grid(row=0, column=0, sticky="nsew")
container.grid_columnconfigure(0, weight=1)

tk.Label(container, text="Lumino Pro", font=("Arial", 20, "bold"), fg="red", bg="#2e2e2e")\
    .grid(row=0, column=0, columnspan=6, pady=(0, 10))

headers = ["Condition", "Size", "Area", "Skin Tone"]
options = [["Acute", "Subacute", "Chronic"],
           ["Small", "Medium", "Large"],
           ["25cm2", "75cm2", "150cm2"],
           ["Light", "Tan", "Dark"]]

selected_vars = [tk.StringVar(value=opts[0]) for opts in options]
header_colors = ["#1E90FF", "#00CED1", "#32CD32", "#FF8C00"]
option_bg_colors = ["#B0C4DE", "#AFEEEE", "#90EE90", "#FFDAB9"]
input_buttons = []

grid_frame = tk.Frame(container, bg="#2e2e2e")
grid_frame.grid(row=1, column=0, pady=10)

for row_idx, header in enumerate(headers):
    tk.Label(grid_frame, text=header, font=("Arial", 10, "bold"), width=12,
             bg=header_colors[row_idx], fg="black", relief="ridge", padx=5, pady=5)\
        .grid(row=row_idx, column=0, padx=2, pady=2, sticky="w")

    for col_idx, option in enumerate(options[row_idx]):
        rb = tk.Radiobutton(grid_frame, text=option, variable=selected_vars[row_idx], value=option,
                            bg=option_bg_colors[row_idx], fg="black", indicatoron=0, width=12,
                            selectcolor="#FFD700", font=("Arial", 10, "bold"), relief="ridge")
        rb.grid(row=row_idx, column=col_idx + 1, padx=2, pady=2)
        rb.config(state="disabled")
        input_buttons.append(rb)

# SAVE button
save_button = tk.Button(container, text="START", font=("Arial", 12, "bold"),
                        bg="orange", fg="white", padx=20, pady=10, command=on_enter)
save_button.grid(row=2, column=0, pady=20)
save_button.config(state="disabled")

# === SIDEBAR ===
sidebar = tk.Frame(root, bg="gray20")
sidebar.grid(row=0, column=2, padx=10, pady=20, sticky="ns")
scale_factor = app_width / 1300
create_sidebar_buttons(sidebar, scale_factor, root)

# === START ===
root.mainloop()
