This project is a Tkinter-based GUI application designed to run on a Raspberry Pi connected to a TFT touchscreen. It serves as the main control interface for a Laser Therapy Machine, allowing users to select therapy modes, conditions, body parts, and view treatment parameters like power, frequency, and energy.

📁 Project Structure
bash
Copy
Edit
project-delhi/
│
├── PythonProject/
│   ├── auto.py                # Auto mode logic & UI
│   ├── therapy.py             # Final therapy session page with data and timer
│   ├── password.py            # Login/password page
│   ├── sidebar.py             # Sidebar for navigation
│   ├── temp_selection.json    # Stores user selections
│   ├── dataset.xlsx           # Therapy data (conditions, body parts, settings)
│   └── body_parts/
│       ├── ankle.py
│       ├── knee.py
│       └── ...                # Other body parts
│
├── images/                    # Body part and logo images
├── tft_boot/                  # Setup to autostart GUI on boot
└── README.md



Overview
This project is a Laser Therapy Device Control System designed for physiotherapy applications. The software features a user-friendly GUI for configuring laser parameters, selecting treatment protocols, and interfacing with hardware. It demonstrates advanced skills in Python, GUI development, modular programming, and hardware integration.

Features
Python Tkinter GUI
Built a multi-page, intuitive interface using Tkinter, supporting real-time parameter adjustment and therapy monitoring.

Modular, Reusable Code
Structured the application for maximum code reuse and maintainability, with clear separation of logic and UI components.

Hardware Integration
Enabled communication with Raspberry Pi for direct control of laser hardware.

Dynamic Protocol Management
Supports loading and updating therapy protocols via external JSON files.

Responsive Layout
Designed for usability across various screen sizes, including auto-scaling features.

Real-Time Data Display
Provides live updates of device status and therapy progress.

Security Features
Includes password-protected access for engineering and settings modes.

Software Skills Highlighted
Python Programming: Advanced use of Python for GUI, hardware I/O, and data management.

Tkinter GUI Development: Multi-frame layouts, custom widgets, image integration, and event-driven design.

File Handling & Data Integration: Dynamic protocol loading using JSON and image files.

Device Automation: Automated app startup and device communication on Raspberry Pi and Windows.

Problem Solving: Addressed real-world engineering challenges such as responsive design, live status updates, and secure access.

Getting Started

Tkinter

Pillow (PIL)

Raspberry Pi (for hardware integration)

JSON protocol files

Installation

bash
pip install pillow
Running the App

bash
python main.py
Customizing Protocols

Add your protocol JSON files to the /protocols directory.
