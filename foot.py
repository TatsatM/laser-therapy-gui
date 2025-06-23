import tkinter as tk
from tkinter import messagebox
import os
import json
import subprocess
from neck_cervicalspine import load_and_resize_images, create_layout

therapy_data = {
    "Plantar fasciitis": {
        "BodyPart": "Foot",
        "Condition": "Plantar fasciitis",
        "Power": 35,
        "Pulse Freq": 9000,
        "Time": 10,
        "Total Energy": 3000
    },
    "Morton's neuroma": {
        "BodyPart": "Foot",
        "Condition": "Morton's neuroma",
        "Power": 30,
        "Pulse Freq": 8500,
        "Time": 12,
        "Total Energy": 3200
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
    root.title("Lumino Pro - Foot")
    root.attributes('-fullscreen', True)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    scale_factor = min(screen_width / 1300, screen_height / 750)
    root.geometry(f"{int(1300 * scale_factor)}x{int(750 * scale_factor)}")
    root.configure(bg="gray20")
    foot_img_path = resource_path("image/bodyparts/foot.png")
    anatomy_img_path = resource_path("image/anatomy.png")
    foot_photo, anatomy_photo = load_and_resize_images(foot_img_path, anatomy_img_path, scale_factor)
    create_layout(root, anatomy_photo, foot_photo, scale_factor, title="Lumino Pro", scroll_title="Foot", info_list=list(therapy_data.keys()), callback=on_condition_selected)
    root.mainloop()

if __name__ == "__main__":
    main()
