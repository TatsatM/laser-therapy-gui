🔬 Laser Therapy Machine - Raspberry Pi Based GUI Application
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
🧠 Features
🔐 Password-protected entry screen
🧍 Interactive anatomy-based body part selector
📝 Condition + Body Part + Skin tone + Size filters
📊 Dynamic therapy parameter display (Power, Energy, Frequency, etc.)
⏱️ Timer with Play/Pause and Stop for sessions
💾 Reads data from Excel and stores temp selection as JSON
📡 Socket integration for hardware communication
📱 Touchscreen-compatible full-screen layout
🖥️ Setup Instructions
🔧 Hardware Requirements
Raspberry Pi (preferably 4B)
TFT LCD Touchscreen (GPIO interface)
Laser diode module with voltage/frequency control
Power Supply Unit
Optional: Custom PCB for interfacing
🛠️ Software Installation
Install Required Python Packages

bash
Copy
Edit
sudo apt-get update
sudo apt-get install python3-tk python3-pil
pip3 install openpyxl
Autostart GUI on Boot
Add this to your Raspberry Pi's autostart:

bash
Copy
Edit
@sudo python3 /home/pi/Desktop/project-delhi/PythonProject/password.py
Enable SPI/GPIO
Enable GPIO/SPI from Raspberry Pi config:

bash
Copy
Edit
sudo raspi-config
🚀 Run the Application
On Raspberry Pi, from terminal:

bash
Copy
Edit
cd ~/Desktop/project-delhi/PythonProject
python3 password.py
🧪 Therapy Modes
Auto Mode: Guided navigation through condition and body part to display settings

Therapy Mode: Allows manual selection of parameters

Protocol Mode: Predefined treatment protocols

📡 Hardware Integration
Uses GPIO or socket communication to send therapy values (power, frequency, time) to the connected laser hardware.

Works with custom PCB or standard laser control modules.

⚠️ Safety Notice
Ensure appropriate laser safety measures are taken when operating the system. Only qualified personnel should use this for therapy sessions.

📚 References
Tkinter Documentation

Raspberry Pi GPIO Tutorials

Laser Therapy Clinical Guidelines

PIL (Pillow) for image support

Excel handling via openpyxl
