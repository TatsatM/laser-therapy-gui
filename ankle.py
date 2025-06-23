import tkinter as tk
from tkinter import messagebox
import os
import json
import subprocess
from neck_cervicalspine import load_and_resize_images, create_layout

# ======= EMBEDDED THERAPY DATA =======
therapy_data = {
    "Achilles tendinitis": {
        "BodyPart": "Ankle",
        "Condition": "Achilles tendinitis",
        "Power": 40,
        "Pulse Freq": 8000,
        "Time": 12,
        "Total Energy": 3500
    },
    "Ankle Sprain": {
        "BodyPart": "Ankle",
        "Condition": "Ankle Sprain",
        "Power": 40,
        "Pulse Freq": 10000,
        "Time": 10,
        "Total Energy": 3500
    }
}

# ======= PROJECT DIRECTORY PATH =======
PROJECT_DIR = os.path.expanduser(r"C:\Users\malvi\OneDrive\Desktop\project delhi\PythonProject")

def resource_path(relative_path):
    return os.path.join(PROJECT_DIR, relative_path)

def on_condition_selected(condition):
    try:
        if condition in therapy_data:
            therapy = therapy_data[condition]

            # === Structure JSON for therapy.py ===
            data_to_send = {
                "User Selections": {
                    "Condition": therapy["Condition"]
                },
                "Therapy Data": {
                    "Power": therapy["Power"],
                    "Pulse Freq": therapy["Pulse Freq"],
                    "Time": therapy["Time"],
                    "Total Energy": therapy["Total Energy"]
                },
                "Body Part": therapy["BodyPart"]
            }

            # === Save JSON ===
            temp_json_path = os.path.join(PROJECT_DIR, "temp_selection.json")
            with open(temp_json_path, "w") as f:
                json.dump(data_to_send, f)

            # === Launch therapy.py ===
            therapy_script = os.path.join(PROJECT_DIR, "therapy.py")
            subprocess.Popen(["python", therapy_script], cwd=PROJECT_DIR)
        else:
            messagebox.showwarning("Not Found", f"No therapy data for: {condition}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open therapy.py: {e}")

def main():
    root = tk.Tk()
    root.title("Lumino Pro - Ankle")
    root.attributes('-fullscreen', True)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    base_width, base_height = 1300, 750
    scale_factor = min(screen_width / base_width, screen_height / base_height)

    root.geometry(f"{int(base_width * scale_factor)}x{int(base_height * scale_factor)}")
    root.configure(bg="gray20")

    # Load images
    ankle_img_path = resource_path("image/bodyparts/ankle.png")
    anatomy_img_path = resource_path("image/anatomy.png")

    ankle_photo, anatomy_photo = load_and_resize_images(ankle_img_path, anatomy_img_path, scale_factor)

    # Use layout
    create_layout(
        root,
        anatomy_photo,
        ankle_photo,
        scale_factor,
        title="Lumino Pro",
        scroll_title="ankle",
        info_list=list(therapy_data.keys()),
        callback=on_condition_selected
    )

    root.mainloop()

if __name__ == "__main__":
    main()
