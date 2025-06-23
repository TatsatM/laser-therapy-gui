import tkinter as tk
from tkinter import messagebox
import os
import json
import subprocess
from neck_cervicalspine import load_and_resize_images, create_layout

therapy_data = {
    "Degenerative Disc": {"BodyPart": "Lumbar Spine", "Condition": "Degenerative Disc", "Power": 40, "Pulse Freq": 9000, "Time": 12, "Total Energy": 3600},
    "Herniated Discs": {"BodyPart": "Lumbar Spine", "Condition": "Herniated Discs", "Power": 42, "Pulse Freq": 9500, "Time": 14, "Total Energy": 3900},
    "Spondylolisthesis": {"BodyPart": "Lumbar Spine", "Condition": "Spondylolisthesis", "Power": 38, "Pulse Freq": 9300, "Time": 13, "Total Energy": 3700},
    "Spinal Stenosis": {"BodyPart": "Lumbar Spine", "Condition": "Spinal Stenosis", "Power": 35, "Pulse Freq": 9100, "Time": 11, "Total Energy": 3400},
    "Sciatica": {"BodyPart": "Lumbar Spine", "Condition": "Sciatica", "Power": 36, "Pulse Freq": 9400, "Time": 12, "Total Energy": 3550},
    "Sacroiliitis": {"BodyPart": "Lumbar Spine", "Condition": "Sacroiliitis", "Power": 37, "Pulse Freq": 8800, "Time": 10, "Total Energy": 3300},
    "Piriformis syndrome": {"BodyPart": "Lumbar Spine", "Condition": "Piriformis syndrome", "Power": 34, "Pulse Freq": 8600, "Time": 9, "Total Energy": 3150}
}

UNIVERSAL_BASE_DIR = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop", "project delhi")
PROJECT_DIR = os.path.join(UNIVERSAL_BASE_DIR, "PythonProject")

print(f"DEBUG PATH: UNIVERSAL_BASE_DIR: {UNIVERSAL_BASE_DIR}")
print(f"DEBUG PATH: PROJECT_DIR: {PROJECT_DIR}")
print(f"DEBUG PATH: temp_json_path (where applicable): {os.path.join(PROJECT_DIR, 'temp_selection.json')}")

def resource_path(relative_path):
    return os.path.join(PROJECT_DIR, relative_path)

def on_condition_selected(condition):
    try:
        if condition in therapy_data:
            therapy = therapy_data[condition]
            data_to_send = {
                "User Selections": {"Condition": therapy["Condition"]},
                "Therapy Data": {k: therapy[k] for k in ["Power", "Pulse Freq", "Time", "Total Energy"]},
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
    root.title("Lumino Pro - Lumbar Spine")
    root.attributes('-fullscreen', True)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    scale_factor = min(screen_width / 1300, screen_height / 750)
    root.geometry(f"{int(1300 * scale_factor)}x{int(750 * scale_factor)}")
    root.configure(bg="gray20")

    lumbar_img_path = resource_path("image/bodyparts/Lumbar_Spine.png")
    anatomy_img_path = resource_path("image/anatomy.png")
    lumbar_photo, anatomy_photo = load_and_resize_images(lumbar_img_path, anatomy_img_path, scale_factor)

    create_layout(
        root,
        anatomy_photo,
        lumbar_photo,
        scale_factor,
        title="Lumino Pro",
        scroll_title="Lumbar Spine",
        info_list=list(therapy_data.keys()),
        callback=on_condition_selected
    )

    root.mainloop()

if __name__ == "__main__":
    main()
