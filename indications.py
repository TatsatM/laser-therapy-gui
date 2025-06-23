import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Dummy sidebar function (replace with your own from neck_cervicalspine.py if you have it)
def create_sidebar_buttons(sidebar, scale_factor, root=None):
    sidebar_buttons = ["🔄 Auto", "📜 Protocol", "🏃 Therapy", "🏠 Home", "🔙 Back"]

    def on_button_click(name):
        print(f"{name} clicked")

    for btn_text in sidebar_buttons:
        btn = tk.Button(
            sidebar,
            text=btn_text,
            font=("Segoe UI", int(16 * scale_factor), "bold"),
            bg="#2a5d77",
            fg="white",
            activebackground="#378ba4",
            activeforeground="white",
            width=14,
            height=2,
            command=lambda name=btn_text: on_button_click(name)
        )
        btn.pack(pady=int(10 * scale_factor), padx=5)

def create_layout(root, anatomy_photo, scale_factor, title="Lumino Pro", scroll_title="Shoulder", info_list=None):
    if info_list is None:
        info_list = ["Frozen shoulder", "Swimmer's shoulder"]

    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.attributes('-fullscreen', True)

    # Title
    title_label = tk.Label(root, text=title, font=("Arial", int(24 * scale_factor), "bold"), fg="red", bg="gray20")
    title_label.grid(row=0, column=0, columnspan=3, sticky="w", padx=20, pady=(10, 0))

    # Anatomy Image (Left)
    anatomy_label = tk.Label(root, image=anatomy_photo, bg="gray20")
    anatomy_label.grid(row=1, column=0, rowspan=3, padx=10, pady=10, sticky="n")
    anatomy_label.image = anatomy_photo

    # Center Content Frame
    middle_frame = tk.Frame(root, bg="gray20")
    middle_frame.grid(row=1, column=1, sticky="n")

    # Scroll Title
    scroll_title_label = tk.Label(
        middle_frame,
        text=scroll_title,
        font=("Helvetica", int(20 * scale_factor), "bold"),
        fg="yellow",
        bg="gray25"
    )
    scroll_title_label.pack(fill="x", padx=10, pady=(10, 0))

    # Scrollable Area
    scroll_canvas = tk.Canvas(
        middle_frame,
        height=int(400 * scale_factor),
        width=int(400 * scale_factor),
        bg="gray25",
        highlightthickness=0
    )
    scroll_canvas.pack(padx=10, pady=(0, 20), fill="x")

    scrollbar = ttk.Scrollbar(middle_frame, orient="vertical", command=scroll_canvas.yview)
    scrollbar.pack(side="right", fill="y")

    text_frame = tk.Frame(scroll_canvas, bg="gray25")
    scroll_canvas.create_window((0, 0), window=text_frame, anchor="nw")
    scroll_canvas.configure(yscrollcommand=scrollbar.set)

    def update_scroll(event):
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
    text_frame.bind("<Configure>", update_scroll)

    def on_item_click(item_name):
        print(f"{item_name} clicked!")

    for item in info_list:
        btn = tk.Button(
            text_frame,
            text=item,
            font=("Helvetica", int(16 * scale_factor)),
            fg="white",
            bg="gray40",
            activebackground="gray60",
            width=25,
            command=lambda i=item: on_item_click(i)
        )
        btn.pack(pady=5)

    # Sidebar
    sidebar = tk.Frame(root, bg="gray20")
    sidebar.grid(row=1, column=2, padx=10, pady=10, sticky="ne")
    create_sidebar_buttons(sidebar, scale_factor, root)

def main():
    root = tk.Tk()
    root.title("Lumino Pro - Shoulder")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    base_width, base_height = 1300, 700
    scale_factor = min(screen_width / base_width, screen_height / base_height)

    root.geometry(f"{int(base_width * scale_factor)}x{int(base_height * scale_factor)}")
    root.configure(bg="gray20")

    # Replace this with your actual image path!
    anatomy_img_path = r"C:\Users\malvi\OneDrive\Desktop\project delhi\image\anatomy.png"
    try:
        anatomy_img = Image.open(anatomy_img_path).resize((int(400 * scale_factor), int(500 * scale_factor)))
        anatomy_photo = ImageTk.PhotoImage(anatomy_img)
    except Exception as e:
        # If image not found, use a blank image
        anatomy_photo = ImageTk.PhotoImage(Image.new("RGB", (int(400 * scale_factor), int(500 * scale_factor)), "gray"))

    create_layout(
        root,
        anatomy_photo,
        scale_factor,
        title="Lumino Pro",
        scroll_title="Indications",
        info_list=[
            "Neck - Cervical Spine", "Shoulder", "Elbow", "Wrist",
            "Low Back – Lumbar Spine", "Hamstring – Muscular Conditions",
            "Ankle", "TMJ", "Hip", "Knee", "Foot", "Neuropathy", "Skin"
        ]
    )

    root.mainloop()

if __name__ == "__main__":
    main()
