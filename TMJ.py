import tkinter as tk
from tkinter import messagebox
import os
import json
import subprocess
from neck_cervicalspine import load_and_resize_images, create_layout

# === Therapy data for TMJ ===
therapy_data = {
    "TMDs": {
        "BodyPart": "TMJ",
        "Condition": "TMDs",
        "Power": 36,
        "Pulse Freq": 8700,
        "Time": 11,
        "Total Energy": 3100
    }
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
    root.title("Lumino Pro - TMJ")
    root.attributes('-fullscreen', True)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    base_width, base_height = 1300, 750
    scale_factor = min(screen_width / base_width, screen_height / base_height)

    root.geometry(f"{int(base_width * scale_factor)}x{int(base_height * scale_factor)}")
    root.configure(bg="gray20")

    base_image_dir = os.path.join("C:", os.sep, "Users", "malvi", "OneDrive", "Desktop", "project delhi", "image")
    tmj_path = os.path.join(base_image_dir, "bodyparts", "TMJ.png")
    anatomy_img_path = os.path.join(base_image_dir, "anatomy.png")

    tmj_photo, anatomy_photo = load_and_resize_images(tmj_path, anatomy_img_path, scale_factor)

    create_layout(
        root,
        anatomy_photo,
        tmj_photo,
        scale_factor,
        title="Lumino Pro",
        scroll_title="TMJ",
        info_list=list(therapy_data.keys()),
        callback=on_condition_selected
    )

    root.mainloop()

if __name__ == "__main__":
    main()
