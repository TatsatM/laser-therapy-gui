import tkinter as tk
from tkinter import messagebox
import os
import json
import subprocess
from neck_cervicalspine import load_and_resize_images, create_layout

# === Embedded therapy data for wrist conditions ===
therapy_data = {
    "De Quervain's Tenosynovitis": {
        "BodyPart": "Wrist",
        "Condition": "De Quervain's Tenosynovitis",
        "Power": 35,
        "Pulse Freq": 8700,
        "Time": 10,
        "Total Energy": 3000
    },
    "Tendinitis of wrist": {
        "BodyPart": "Wrist",
        "Condition": "Tendinitis of wrist",
        "Power": 34,
        "Pulse Freq": 8600,
        "Time": 9,
        "Total Energy": 2900
    },
    "Carpal tunnel syndrome (CTS)": {
        "BodyPart": "Wrist",
        "Condition": "Carpal tunnel syndrome (CTS)",
        "Power": 36,
        "Pulse Freq": 9000,
        "Time": 11,
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
    root.title("Lumino Pro - Wrist")
    root.attributes('-fullscreen', True)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    base_width, base_height = 1300, 750
    scale_factor = min(screen_width / base_width, screen_height / base_height)

    root.geometry(f"{int(base_width * scale_factor)}x{int(base_height * scale_factor)}")
    root.configure(bg="gray20")

    base_dir = os.path.join("C:", os.sep, "Users", "malvi", "OneDrive", "Desktop", "project delhi", "image")
    wrist_path = os.path.join(base_dir, "bodyparts", "wrist.png")
    anatomy_img_path = os.path.join(base_dir, "anatomy.png")

    wrist_photo, anatomy_photo = load_and_resize_images(wrist_path, anatomy_img_path, scale_factor)

    create_layout(
        root,
        anatomy_photo,
        wrist_photo,
        scale_factor,
        title="Lumino Pro",
        scroll_title="Wrist",
        info_list=list(therapy_data.keys()),
        callback=on_condition_selected
    )

    root.mainloop()

if __name__ == "__main__":
    main()
