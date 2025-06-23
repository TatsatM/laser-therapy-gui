import tkinter as tk
from tkinter import messagebox
import os
import json
import subprocess
from neck_cervicalspine import load_and_resize_images, create_layout

# === Embedded therapy data for skin conditions ===
therapy_data = {
    "Burns": {"BodyPart": "Skin", "Condition": "Burns", "Power": 30, "Pulse Freq": 8500, "Time": 10, "Total Energy": 2900},
    "Bedsores/ Ulcer": {"BodyPart": "Skin", "Condition": "Bedsores/ Ulcer", "Power": 32, "Pulse Freq": 8700, "Time": 11, "Total Energy": 3100},
    "Wrinkles": {"BodyPart": "Skin", "Condition": "Wrinkles", "Power": 28, "Pulse Freq": 8000, "Time": 8, "Total Energy": 2500},
    "Stretch Marks": {"BodyPart": "Skin", "Condition": "Stretch Marks", "Power": 30, "Pulse Freq": 8300, "Time": 9, "Total Energy": 2700},
    "Skin Rejuvenation": {"BodyPart": "Skin", "Condition": "Skin Rejuvenation", "Power": 34, "Pulse Freq": 8800, "Time": 10, "Total Energy": 3000},
    "Acne vulgaris": {"BodyPart": "Skin", "Condition": "Acne vulgaris", "Power": 29, "Pulse Freq": 8200, "Time": 8, "Total Energy": 2400},
    "Herpes simplex": {"BodyPart": "Skin", "Condition": "Herpes simplex", "Power": 31, "Pulse Freq": 8600, "Time": 9, "Total Energy": 2600},
    "Wound healing": {"BodyPart": "Skin", "Condition": "Wound healing", "Power": 33, "Pulse Freq": 8900, "Time": 11, "Total Energy": 3150},
    "Toe Nail Fungus": {"BodyPart": "Skin", "Condition": "Toe Nail Fungus", "Power": 35, "Pulse Freq": 9000, "Time": 12, "Total Energy": 3300}
}

PROJECT_DIR = os.path.expanduser(r"C:\Users\malvi\OneDrive\Desktop\project delhi\PythonProject")

def resource_path(relative_path):
    return os.path.join(PROJECT_DIR, relative_path)

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
            with open(os.path.join(PROJECT_DIR, "temp_selection.json"), "w") as f:
                json.dump(data_to_send, f)
            subprocess.Popen(["python", os.path.join(PROJECT_DIR, "therapy.py")], cwd=PROJECT_DIR)
        else:
            messagebox.showwarning("Not Found", f"No therapy data for: {condition}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to launch therapy.py:\n{e}")

def main():
    root = tk.Tk()
    root.title("Lumino Pro - Skin")
    root.attributes('-fullscreen', True)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    base_width, base_height = 1300, 750
    scale_factor = min(screen_width / base_width, screen_height / base_height)

    root.geometry(f"{int(base_width * scale_factor)}x{int(base_height * scale_factor)}")
    root.configure(bg="gray20")

    # Universal paths to image files
    base_dir = os.path.join("C:", os.sep, "Users", "malvi", "OneDrive", "Desktop", "project delhi", "image")
    skin_path = os.path.join(base_dir, "bodyparts", "skin.png")
    anatomy_img_path = os.path.join(base_dir, "anatomy.png")

    skin_photo, anatomy_photo = load_and_resize_images(skin_path, anatomy_img_path, scale_factor)

    create_layout(
        root,
        anatomy_photo,
        skin_photo,
        scale_factor,
        title="Lumino Pro",
        scroll_title="Skin",
        info_list=list(therapy_data.keys()),
        callback=on_condition_selected
    )

    root.mainloop()

if __name__ == "__main__":
    main()
