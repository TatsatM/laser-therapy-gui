import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import subprocess
import os
import sys
import configparser
import socket
import json

# Dummy sidebar fallback - This ensures the code runs even if neck_cervicalspine is not available
try:
    from neck_cervicalspine import create_sidebar_buttons
except ImportError:
    def create_sidebar_buttons(frame, scale_factor, root=None):
        tk.Label(frame, text="Sidebar", bg="gray20", fg="white", font=("Arial", int(14 * scale_factor))).pack(padx=10,
                                                                                                              pady=10)
        # Add a dummy button for demonstration
        ttk.Button(frame, text="Dummy Button",
                   command=lambda: messagebox.showinfo("Sidebar", "Dummy button clicked!")).pack(pady=5)

# Define the path for the monitor application (adjust if your therapy.py is elsewhere)
MONITOR_APP_PATH = os.path.join(os.path.dirname(__file__), 'therapy.py')


class LaserTherapyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Lumino Pro Laser Therapy")
        self.root.attributes('-fullscreen', True)  # Starts in fullscreen mode
        self.is_running = False
        self.therapy_start_time = 0
        self.therapy_end_time = 0  # To store when therapy should end

        # Shared variables for wavelengths, master power, and mode
        self.wavelengths = {
            "808nm": {"enabled": tk.BooleanVar(value=True), "power": tk.IntVar(value=0)},
            "980nm": {"enabled": tk.BooleanVar(value=True), "power": tk.IntVar(value=0)},
            "1064nm": {"enabled": tk.BooleanVar(value=True), "power": tk.IntVar(value=0)},
        }
        self.master_power = tk.IntVar(value=0)
        self.previous_master_power = 0
        self.mode = tk.StringVar(value="CW")
        self.pulse_type = tk.StringVar(value="Frequency")
        self.pulse_duration = tk.DoubleVar(value=0.01)
        self.frequency = tk.IntVar(value=1)

        # Variables for Power, Energy, Time (P=E/T) calculation section
        self.set_power = tk.DoubleVar(value=0.0)
        self.set_energy = tk.DoubleVar(value=0.0)
        self.set_time = tk.DoubleVar(value=0.0)

        self.active_pes_input = tk.StringVar(value="")
        self.last_target_was_energy = tk.BooleanVar(value=False)

        self.delivery_mode = tk.StringVar(value="")
        self.hand_probe_var = tk.BooleanVar(value=False)
        self.foot_switch_var = tk.BooleanVar(value=False)

        self.master_power_display_var = tk.StringVar(value="0 W")
        self.wavelength_power_display_vars = {
            "808nm": tk.StringVar(value="0 %"),
            "980nm": tk.StringVar(value="0 %"),
            "1064nm": tk.StringVar(value="0 %"),
        }

        self.status = tk.StringVar(value="Ready")
        self.power_spinboxes = {}
        self.power_display_sliders = {}

        self.master_spinbox = None
        self.master_display_slider = None

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 16))
        self.style.configure("TLabel", font=("Arial", 16))
        self.style.configure("TCheckbutton", font=("Arial", 16))
        self.style.configure("TRadiobutton", font=("Arial", 16))
        self.style.configure("TEntry", font=("Arial", 16))
        self.style.configure("Readonly.TEntry", fieldbackground="lightgray", foreground="black")
        self.style.configure("TSpinbox", font=("Arial", 16))

        self.style.configure("Violet.Vertical.TScale", troughcolor="violet", sliderrelief="raised")
        self.style.configure("Orange.Vertical.TScale", troughcolor="orange", sliderrelief="raised")
        self.style.configure("Yellow.Vertical.TScale", troughcolor="yellow", sliderrelief="raised")
        self.style.configure("Blue.Vertical.TScale", troughcolor="blue", sliderrelief="raised")
        self.style.configure("Disabled.Vertical.TScale", troughcolor="gray", sliderrelief="flat")

        self.sidebar_frame = None
        self.main_frame = None

        self.build_main_ui()

        self.monitor_socket = None
        self.monitor_process = None

    def connect_to_monitor(self):
        """Attempts to establish a socket connection to the monitor application."""
        max_attempts = 20
        for i in range(max_attempts):
            try:
                self.monitor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.monitor_socket.connect(('localhost', 65432))
                print("Connected to monitor application.")
                return True
            except ConnectionRefusedError:
                print(f"Connection attempt {i + 1} failed. Retrying...")
                time.sleep(0.2)
            except Exception as e:
                print(f"An error occurred while connecting: {e}")
                self.monitor_socket = None
                return False
        messagebox.showerror("Connection Error",
                             "Could not connect to the monitoring application after multiple attempts. Please ensure it's running or try again.")
        self.monitor_socket = None
        return False

    def send_data_to_monitor(self, data):
        """Sends JSON-encoded data to the connected monitor application."""
        if self.monitor_socket:
            try:
                self.monitor_socket.sendall(json.dumps(data).encode('utf-8'))
            except Exception as e:
                print(f"Error sending data to monitor: {e}")
                self.monitor_socket = None

    def build_main_ui(self):
        """Builds the main user interface layout."""
        if self.main_frame:
            self.main_frame.destroy()
        if self.sidebar_frame:
            self.sidebar_frame.destroy()

        self.container = tk.Frame(self.root, bg="gray10")
        self.container.pack(fill="both", expand=True)
        self.container.columnconfigure(0, weight=3)
        self.container.columnconfigure(1, weight=1)

        self.main_frame = ttk.Frame(self.container, padding=20)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.container.rowconfigure(0, weight=1)

        self.sidebar_frame = tk.Frame(self.container, bg="gray20")
        self.sidebar_frame.grid(row=0, column=1, sticky="nswe", padx=10, pady=20)

        screen_width = self.root.winfo_screenwidth()
        base_width = 1300
        scale_factor = screen_width / base_width
        create_sidebar_buttons(self.sidebar_frame, scale_factor, self.root)

        self.create_widgets()
        self.update_all()

    def create_widgets(self):
        """Creates and arranges all GUI widgets within the main frame."""
        frame = self.main_frame
        for i in range(3):
            frame.columnconfigure(i, weight=1)
        for i in range(4):
            frame.rowconfigure(i, weight=1)

        self.frame_power = ttk.LabelFrame(frame, text="Step 2: Set Power", padding=(10, 5))
        self.frame_power.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        for i in range(4):
            self.frame_power.columnconfigure(i, weight=1)

        self.frame_power.rowconfigure(1, weight=1)
        self.frame_power.rowconfigure(2, weight=0)

        master_col = 0
        ttk.Label(self.frame_power, text="Master (W)").grid(row=0, column=master_col, sticky="s", pady=(0, 5))

        master_display_slider = ttk.Scale(self.frame_power, from_=30, to=0, orient="vertical",
                                          variable=self.master_power, state="disabled", length=200,
                                          style="Violet.Vertical.TScale")
        master_display_slider.grid(row=1, column=master_col, padx=5, pady=5, sticky="ns")
        self.master_display_slider = master_display_slider

        master_spinbox = ttk.Spinbox(self.frame_power, from_=0, to=30, increment=1, textvariable=self.master_power,
                                     command=self.on_master_power_change, width=5)
        master_spinbox.grid(row=2, column=master_col, padx=5, pady=5)
        self.master_spinbox = master_spinbox
        master_spinbox.bind("<ButtonRelease-1>", lambda e: self.on_master_power_change())
        master_spinbox.bind("<Return>", lambda e: self.on_master_power_change())
        master_spinbox.bind("<FocusOut>", lambda e: self.on_master_power_change())

        col_offset = 1
        slider_styles = {"808nm": "Orange.Vertical.TScale", "980nm": "Yellow.Vertical.TScale",
                         "1064nm": "Blue.Vertical.TScale"}
        for wl, vals in self.wavelengths.items():
            ttk.Label(self.frame_power, text=f"{wl} (%)").grid(row=0, column=col_offset, sticky="s", pady=(0, 5))

            display_slider = ttk.Scale(self.frame_power, from_=100, to=0, orient="vertical",
                                       variable=vals["power"], state="disabled", length=200,
                                       style=slider_styles[wl])
            display_slider.grid(row=1, column=col_offset, padx=5, pady=5, sticky="ns")
            self.power_display_sliders[wl] = display_slider

            spinbox = ttk.Spinbox(self.frame_power, from_=0, to=100, increment=1, textvariable=vals["power"],
                                  command=lambda w=wl: self.on_individual_power_change(w), width=5)
            spinbox.grid(row=2, column=col_offset, padx=5, pady=5)
            self.power_spinboxes[wl] = spinbox
            spinbox.bind("<ButtonRelease-1>", lambda e, w=wl: self.on_individual_power_change(w))
            spinbox.bind("<Return>", lambda e, w=wl: self.on_individual_power_change(w))
            spinbox.bind("<FocusOut>", lambda e, w=wl: self.on_individual_power_change(w))

            col_offset += 1

        self.frame_mode = ttk.LabelFrame(frame, text="Step 3: Select Mode", padding=(10, 5))
        self.frame_mode.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        self.frame_mode.columnconfigure(0, weight=1)
        ttk.Radiobutton(self.frame_mode, text="CW (Continuous Wave)", variable=self.mode, value="CW",
                        command=self.update_all).grid(row=0, column=0, sticky="w", pady=2)
        ttk.Radiobutton(self.frame_mode, text="Pulse", variable=self.mode, value="Pulse", command=self.update_all).grid(
            row=1, column=0, sticky="w", pady=2)

        self.frame_pulse = ttk.LabelFrame(self.frame_mode, text="Pulse Settings", padding=(10, 5))
        self.frame_pulse.grid(row=2, column=0, pady=10, sticky="ew")
        self.frame_pulse.columnconfigure(1, weight=1)

        ttk.Radiobutton(self.frame_pulse, text="Single Pulse", variable=self.pulse_type, value="Single",
                        command=self.update_all).grid(row=0, column=0, sticky="w", pady=2)
        ttk.Radiobutton(self.frame_pulse, text="Frequency (Hz)", variable=self.pulse_type, value="Frequency",
                        command=self.update_all).grid(row=1, column=0, sticky="w", pady=2)

        ttk.Label(self.frame_pulse, text="Pulse Duration (s):").grid(row=2, column=0, sticky="w", pady=2)
        self.entry_pulse_duration = ttk.Entry(self.frame_pulse, textvariable=self.pulse_duration, width=10)
        self.entry_pulse_duration.grid(row=2, column=1, padx=5, sticky="ew", pady=2)
        self.entry_pulse_duration.bind("<FocusOut>", lambda e: self.update_all())
        self.entry_pulse_duration.bind("<Return>", lambda e: self.update_all())

        ttk.Label(self.frame_pulse, text="Frequency (Hz):").grid(row=3, column=0, sticky="w", pady=2)
        self.entry_freq = ttk.Entry(self.frame_pulse, textvariable=self.frequency, width=10)
        self.entry_freq.grid(row=3, column=1, padx=5, sticky="ew", pady=2)
        self.entry_freq.bind("<FocusOut>", lambda e: self.update_all())
        self.entry_freq.bind("<Return>", lambda e: self.update_all())

        self.frame_wl = ttk.LabelFrame(frame, text="Step 1: Choose Wavelength(s)", padding=(10, 5))
        self.frame_wl.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.frame_wl.columnconfigure(0, weight=1)
        self.frame_wl.columnconfigure(1, weight=1)
        targets = ['Mitochondrial Cytochrome C', 'Oxy-hemoglobin', 'Water']
        for i, (wl, vals) in enumerate(self.wavelengths.items()):
            ttk.Checkbutton(self.frame_wl, text=wl, variable=vals["enabled"], command=self.update_all).grid(row=i,
                                                                                                            column=0,
                                                                                                            sticky="w",
                                                                                                            pady=2)
            ttk.Label(self.frame_wl, text=f"Target: {targets[i]}").grid(row=i, column=1, sticky="w", pady=2)

        self.frame_pes_calc = ttk.LabelFrame(frame, text="Step 4: Set Parameters (P=E/T)", padding=(10, 5))
        self.frame_pes_calc.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.frame_pes_calc.columnconfigure(0, weight=1)
        self.frame_pes_calc.columnconfigure(1, weight=1)

        ttk.Label(self.frame_pes_calc, text="Power (W):").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_set_power = ttk.Entry(self.frame_pes_calc, textvariable=self.set_power, width=12, state="readonly",
                                         style="Readonly.TEntry")
        self.entry_set_power.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(self.frame_pes_calc, text="Energy (J):").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_set_energy = ttk.Entry(self.frame_pes_calc, textvariable=self.set_energy, width=12)
        self.entry_set_energy.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        self.entry_set_energy.bind("<FocusIn>", lambda e: self.set_active_input_pes("energy"))
        self.entry_set_energy.bind("<FocusOut>", lambda e: self.calculate_pes())
        self.entry_set_energy.bind("<Return>", lambda e: self.calculate_pes())

        ttk.Label(self.frame_pes_calc, text="Time (Min):").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_set_time = ttk.Entry(self.frame_pes_calc, textvariable=self.set_time, width=12)
        self.entry_set_time.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        self.entry_set_time.bind("<FocusIn>", lambda e: self.set_active_input_pes("time"))
        self.entry_set_time.bind("<FocusOut>", lambda e: self.calculate_pes())
        self.entry_set_time.bind("<Return>", lambda e: self.calculate_pes())

        self.frame_current_readings = ttk.LabelFrame(frame, text="Current Setup Readings", padding=(10, 5))
        self.frame_current_readings.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)
        self.frame_current_readings.columnconfigure(0, weight=1)
        self.frame_current_readings.columnconfigure(1, weight=1)

        self.lbl_mode = ttk.Label(self.frame_current_readings, text="");
        self.lbl_mode.grid(row=0, column=0, sticky="w", columnspan=2, pady=2)
        self.lbl_peak_power = ttk.Label(self.frame_current_readings, text="");
        self.lbl_peak_power.grid(row=1, column=0, sticky="w", columnspan=2, pady=2)
        self.lbl_average_power = ttk.Label(self.frame_current_readings, text="");
        self.lbl_average_power.grid(row=2, column=0, columnspan=2, sticky="w", pady=2)
        self.lbl_pulse_info = ttk.Label(self.frame_current_readings, text="");
        self.lbl_pulse_info.grid(row=3, column=0, columnspan=2, sticky="w", pady=2)

        self.frame_delivery = ttk.LabelFrame(frame, text="Step 5: Choose Delivery Mode", padding=(10, 5))
        self.frame_delivery.grid(row=2, column=2, sticky="nsew", padx=10, pady=10)
        self.frame_delivery.columnconfigure(0, weight=1)

        self.rb_hand_probe = ttk.Radiobutton(self.frame_delivery, text="Hand Probe", variable=self.delivery_mode,
                                             value="Hand Probe", command=self.update_all)
        self.rb_hand_probe.grid(row=0, column=0, sticky="w", pady=2)
        self.rb_foot_switch = ttk.Radiobutton(self.frame_delivery, text="Foot Switch", variable=self.delivery_mode,
                                              value="Foot Switch", command=self.update_all)
        self.rb_foot_switch.grid(row=1, column=0, sticky="w", pady=2)

        frame_therapy = ttk.LabelFrame(frame, text="Step 6: Therapy Control", padding=(10, 5))
        frame_therapy.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
        frame_therapy.columnconfigure(0, weight=1)
        frame_therapy.columnconfigure(1, weight=1)
        frame_therapy.columnconfigure(2, weight=1)

        self.btn_start = ttk.Button(frame_therapy, text="Start Therapy", command=self.start_therapy)
        self.btn_start.grid(row=0, column=0, padx=10, pady=5)
        self.btn_stop = ttk.Button(frame_therapy, text="Stop Therapy", command=self.stop_therapy, state="disabled")
        self.btn_stop.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(frame_therapy, text="Status:").grid(row=1, column=0, sticky="e", pady=5)
        ttk.Label(frame_therapy, textvariable=self.status, foreground="blue", font=("Arial", 16, "bold")).grid(row=1,
                                                                                                               column=1,
                                                                                                               sticky="w",
                                                                                                               pady=5)

    def on_master_power_change(self):
        """
        Handles changes to the master power. Scales individual wavelength powers proportionally.
        """
        try:
            current_master_power = self.master_power.get()
            if current_master_power < 0:
                current_master_power = 0
                self.master_power.set(0)
        except tk.TclError:
            self.master_power.set(self.previous_master_power)
            messagebox.showwarning("Input Error", "Invalid input for Master Power. Please enter a number.")
            return

        if self.previous_master_power == 0:
            if current_master_power > 0:
                for wl, vals in self.wavelengths.items():
                    if vals["enabled"].get():
                        vals["power"].set(100)
            elif current_master_power == 0:
                for wl, vals in self.wavelengths.items():
                    vals["power"].set(0)
        else:
            scale_factor = current_master_power / self.previous_master_power
            for wl, vals in self.wavelengths.items():
                if vals["enabled"].get():
                    current_individual_power = vals["power"].get()
                    new_individual_power = int(round(current_individual_power * scale_factor))
                    vals["power"].set(max(0, min(100, new_individual_power)))

        self.previous_master_power = current_master_power
        self.update_all()

    def on_individual_power_change(self, wavelength):
        """
        Handles changes to individual wavelength power.
        If master power is 0, setting individual power should not be allowed.
        """
        try:
            current_individual_power_percent = self.wavelengths[wavelength]["power"].get()
        except tk.TclError:
            self.wavelengths[wavelength]["power"].set(0)
            messagebox.showwarning("Input Error", f"Invalid input for {wavelength} Power. Please enter a number.")
            self.update_all()
            return

        master_power_val = self.master_power.get()

        if master_power_val == 0 and current_individual_power_percent > 0:
            self.wavelengths[wavelength]["power"].set(0)
            messagebox.showwarning("Power Setting",
                                   "Individual wavelength power cannot be set if Master Power is 0 W. Set Master Power first.")
        self.update_all()

    def update_power_display_vars(self):
        """Updates the StringVar for power display labels to include units."""
        self.master_power_display_var.set(f"{self.master_power.get()} W")
        for wl, vals in self.wavelengths.items():
            self.wavelength_power_display_vars[wl].set(f"{vals['power'].get()} %")

    def set_active_input_pes(self, input_name):
        """Sets which of the P,E,T inputs was most recently focused."""
        self.active_pes_input.set(input_name)
        if input_name == "energy":
            self.last_target_was_energy.set(True)
        elif input_name == "time":
            self.last_target_was_energy.set(False)

    def calculate_pes(self):
        """
        Calculates Energy or Time based on user input and the machine's current average power.
        The 'Power (W)' entry always displays the machine's average power.
        Prioritizes the input field that was most recently interacted with.
        """
        current_active_input = self.active_pes_input.get()
        machine_avg_power = self.get_average_power()

        try:
            e_val_str = self.set_energy.get()
            t_min_str = self.set_time.get()

            e_val = float(e_val_str) if e_val_str else 0.0
            t_min = float(t_min_str) if t_min_str else 0.0
            t_sec = t_min * 60

            if current_active_input == "energy":
                if e_val >= 0 and machine_avg_power > 0:
                    calculated_t_sec = e_val / machine_avg_power
                    self.set_time.set(round(calculated_t_sec / 60, 2))
                else:
                    self.set_time.set(0.0)
                self.last_target_was_energy.set(True)

            elif current_active_input == "time":
                if t_sec >= 0:
                    calculated_e = machine_avg_power * t_sec
                    self.set_energy.set(round(calculated_e, 2))
                else:
                    self.set_energy.set(0.0)
                self.last_target_was_energy.set(False)

            else:
                if self.last_target_was_energy.get():
                    if e_val > 0 and machine_avg_power > 0:
                        calculated_t_sec = e_val / machine_avg_power
                        self.set_time.set(round(calculated_t_sec / 60, 2))
                    else:
                        self.set_time.set(0.0)
                else:
                    if t_sec > 0:
                        calculated_e = machine_avg_power * t_sec
                        self.set_energy.set(round(calculated_e, 2))
                    else:
                        self.set_energy.set(0.0)

            self.active_pes_input.set("")

        except (ValueError, tk.TclError) as e:
            print(f"Calculation input error: {e}")
            messagebox.showwarning("Input Error", "Please enter valid numbers for Energy or Time.")
            if current_active_input == "energy":
                self.set_energy.set(0.0)
                self.set_time.set(0.0)
            elif current_active_input == "time":
                self.set_time.set(0.0)
                self.set_energy.set(0.0)
            self.active_pes_input.set("")
        finally:
            self.set_power.set(round(machine_avg_power, 2))
            self.update_readings()

    def update_all(self, event=None):
        """Called whenever a relevant setting changes to update UI and perform calculations."""
        self.update_power_spinboxes_and_sliders_state()
        self.update_pulse_settings_state()
        self.update_power_display_vars()
        if self.active_pes_input.get() == "":
            self.calculate_pes()
        self.check_start_button_state()

    def update_power_spinboxes_and_sliders_state(self):
        """Enables/disables individual wavelength power spinboxes AND their display sliders based on their enabled state."""
        any_wavelength_enabled = False
        for wl, vals in self.wavelengths.items():
            state = "normal" if vals["enabled"].get() else "disabled"
            if vals["enabled"].get():
                any_wavelength_enabled = True

            self.power_spinboxes[wl].config(state=state)

            if state == "disabled":
                self.power_display_sliders[wl].config(state=state, style="Disabled.Vertical.TScale")
            else:
                slider_styles = {"808nm": "Orange.Vertical.TScale", "980nm": "Yellow.Vertical.TScale",
                                 "1064nm": "Blue.Vertical.TScale"}
                self.power_display_sliders[wl].config(state=state, style=slider_styles[wl])

            if not vals["enabled"].get():
                vals["power"].set(0)

        master_state = "normal" if any_wavelength_enabled else "disabled"
        if self.master_spinbox:
            self.master_spinbox.config(state=master_state)
        if self.master_display_slider:
            self.master_display_slider.config(state=master_state)

        if not any_wavelength_enabled:
            self.master_power.set(0)

    def update_pulse_settings_state(self):
        """Shows/hides pulse settings and enables/disables entries based on mode and pulse type."""
        if self.mode.get() == "CW":
            self.frame_pulse.grid_remove()
            self.pulse_duration.set(0.01)
            self.frequency.set(1)
        else:
            self.frame_pulse.grid()
            self.entry_pulse_duration.config(state="normal")
            self.entry_freq.config(state="normal" if self.pulse_type.get() == "Frequency" else "disabled")
            if self.pulse_type.get() == "Single":
                self.frequency.set(0)

    def update_readings(self):
        """Updates the 'Current Setup Readings' display labels."""
        P = self.master_power.get()
        E = 0.0
        T_sec = 0.0

        self.lbl_peak_power.config(text=f"Peak Power: {P} W")

        avg_power = self.get_average_power()
        self.lbl_average_power.config(text=f"Average Power: {avg_power:.2f} W")
        self.set_power.set(round(avg_power, 2))

        mode_text = f"Mode: {self.mode.get()}"
        self.lbl_mode.config(text=mode_text)

        pulse_info_text = ""
        if self.mode.get() == "Pulse":
            pulse_duration = self.pulse_duration.get()
            pulse_type = self.pulse_type.get()
            if pulse_type == "Single":
                pulse_info_text = f"Pulse Type: Single, Duration: {pulse_duration:.2f} s"
            elif pulse_type == "Frequency":
                frequency = self.frequency.get()
                pulse_info_text = f"Pulse Type: Frequency, Freq: {frequency} Hz, Duration: {pulse_duration:.2f} s"
        self.lbl_pulse_info.config(text=pulse_info_text)

    def get_total_power_percentage(self):
        """Calculates the sum of enabled wavelength power percentages."""
        total_percent = 0
        for wl, vals in self.wavelengths.items():
            if vals["enabled"].get():
                total_percent += vals["power"].get()
        return total_percent

    def get_average_power(self):
        """
        Calculates the average power of the laser output based on master power,
        wavelength percentages, mode, pulse duration, and frequency.
        """
        master_power_watts = self.master_power.get()
        total_wavelength_percentage = self.get_total_power_percentage()

        if master_power_watts == 0 or total_wavelength_percentage == 0:
            return 0.0

        normalized_total_percent = min(100, total_wavelength_percentage) / 100.0
        effective_peak_power = master_power_watts * normalized_total_percent

        if self.mode.get() == "CW":
            return effective_peak_power

        elif self.mode.get() == "Pulse":
            try:
                pulse_duration = float(self.pulse_duration.get())
            except ValueError:
                pulse_duration = 0.01
                self.pulse_duration.set(0.01)

            if self.pulse_type.get() == "Single":
                return effective_peak_power

            elif self.pulse_type.get() == "Frequency":
                try:
                    frequency = float(self.frequency.get())
                except ValueError:
                    frequency = 1
                    self.frequency.set(1)

                if frequency <= 0 or pulse_duration <= 0:
                    return 0.0

                duty_cycle = pulse_duration * frequency
                if duty_cycle > 1.0:
                    return effective_peak_power

                return effective_peak_power * duty_cycle
        return 0.0

    def check_start_button_state(self):
        """Enables/disables the Start button based on conditions."""
        master_power_ok = self.master_power.get() > 0

        wavelength_power_ok = False
        for wl, vals in self.wavelengths.items():
            if vals["enabled"].get() and vals["power"].get() > 0:
                wavelength_power_ok = True
                break

        pulse_settings_ok = True
        if self.mode.get() == "Pulse":
            try:
                if self.pulse_duration.get() <= 0:
                    pulse_settings_ok = False
                if self.pulse_type.get() == "Frequency" and self.frequency.get() <= 0:
                    pulse_settings_ok = False
            except (tk.TclError, ValueError):
                pulse_settings_ok = False

        pes_set_ok = (self.set_energy.get() > 0 or self.set_time.get() > 0)

        avg_power_ok_for_energy_target = True
        if self.set_energy.get() > 0 and self.get_average_power() == 0:
            avg_power_ok_for_energy_target = False

        delivery_mode_selected = self.delivery_mode.get() in ["Hand Probe", "Foot Switch"]

        if master_power_ok and wavelength_power_ok and pulse_settings_ok and pes_set_ok and avg_power_ok_for_energy_target and delivery_mode_selected and not self.is_running:
            self.btn_start.config(state="normal")
        else:
            self.btn_start.config(state="disabled")

    def start_therapy(self):
        """Starts the laser therapy session."""
        if self.is_running:
            messagebox.showwarning("Therapy Status", "Therapy is already running.")
            return

        if self.master_power.get() <= 0:
            messagebox.showwarning("Validation Error", "Master Power must be greater than 0.")
            return

        any_wl_enabled_and_powered = False
        for wl, vals in self.wavelengths.items():
            if vals["enabled"].get() and vals["power"].get() > 0:
                any_wl_enabled_and_powered = True
                break
        if not any_wl_enabled_and_powered:
            messagebox.showwarning("Validation Error",
                                   "At least one enabled wavelength must have power greater than 0%.")
            return

        if self.mode.get() == "Pulse":
            try:
                if self.pulse_duration.get() <= 0:
                    messagebox.showwarning("Validation Error", "Pulse Duration must be greater than 0 in Pulse mode.")
                    return
                if self.pulse_type.get() == "Frequency" and self.frequency.get() <= 0:
                    messagebox.showwarning("Validation Error", "Frequency must be greater than 0 in Frequency mode.")
                    return
            except (tk.TclError, ValueError):
                messagebox.showwarning("Input Error", "Please enter valid numbers for Pulse Duration and Frequency.")
                return

        if self.delivery_mode.get() not in ["Hand Probe", "Foot Switch"]:
            messagebox.showwarning("Validation Error",
                                   "Please select either 'Hand Probe' or 'Foot Switch' for delivery.")
            return

        target_energy = self.set_energy.get()
        target_time_min = self.set_time.get()
        target_time_sec = target_time_min * 60

        actual_therapy_duration_sec = 0
        avg_power = self.get_average_power()

        if target_energy > 0 and (target_time_min == 0 or self.last_target_was_energy.get()):
            if avg_power > 0:
                actual_therapy_duration_sec = target_energy / avg_power
                self.set_time.set(round(actual_therapy_duration_sec / 60, 2))
                messagebox.showinfo("Therapy Calculation",
                                    f"Therapy will run for {actual_therapy_duration_sec:.2f} seconds to deliver {target_energy:.2f} Joules.")
            else:
                messagebox.showwarning("Validation Error",
                                       "Average power is 0. Cannot deliver target energy. Adjust power settings.")
                return
        elif target_time_min > 0 and (target_energy == 0 or not self.last_target_was_energy.get()):
            actual_therapy_duration_sec = target_time_sec
            calculated_e = avg_power * actual_therapy_duration_sec
            self.set_energy.set(round(calculated_e, 2))
            messagebox.showinfo("Therapy Calculation",
                                f"Therapy will run for {actual_therapy_duration_sec:.2f} seconds ({target_time_min:.2f} minutes).")
        else:
            messagebox.showwarning("Validation Error", "Please set a valid target Energy or Time for the therapy.")
            return

        if actual_therapy_duration_sec <= 0:
            messagebox.showwarning("Validation Error",
                                   "Calculated therapy duration is zero or negative. Adjust settings.")
            return

        self.is_running = True
        self.btn_start.config(state="disabled")
        self.btn_stop.config(state="normal")
        self.status.set("Running...")
        self.therapy_start_time = time.time()
        self.therapy_end_time = self.therapy_start_time + actual_therapy_duration_sec

        self.therapy_thread = threading.Thread(target=self.run_therapy_session,
                                               args=(actual_therapy_duration_sec,))
        self.therapy_thread.daemon = True
        self.therapy_thread.start()

        if self.monitor_process is None or self.monitor_process.poll() is not None:
            try:
                self.monitor_process = subprocess.Popen([sys.executable, MONITOR_APP_PATH])
                print(f"Started monitor application: {MONITOR_APP_PATH}")
                time.sleep(1)
                if not self.connect_to_monitor():
                    self.stop_therapy()
                    return
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start monitor application: {e}")
                self.stop_therapy()
                return

        # Send initial therapy parameters with the 'start_therapy' command
        self.send_therapy_parameters_to_monitor(command_type="start_therapy")

        self.monitor_progress()

    def stop_therapy(self):
        """Stops the laser therapy session."""
        if not self.is_running:
            self.status.set("Stopped")
            self.btn_start.config(state="normal")
            self.btn_stop.config(state="disabled")
            if self.monitor_socket:
                try:
                    self.send_data_to_monitor({"command": "stop_therapy"})
                    self.monitor_socket.close()
                except Exception as e:
                    print(f"Error during stop_therapy socket close: {e}")
                finally:
                    self.monitor_socket = None
                    print("Disconnected from monitor application (forced stop).")
            if self.monitor_process and self.monitor_process.poll() is None:
                print("Terminating monitor application (forced stop).")
                try:
                    self.monitor_process.terminate()
                    self.monitor_process.wait(timeout=2)
                    if self.monitor_process.poll() is None:
                        self.monitor_process.kill()
                except Exception as e:
                    print(f"Error terminating monitor process: {e}")
                finally:
                    self.monitor_process = None
            return

        self.is_running = False
        self.status.set("Stopped")
        self.btn_start.config(state="normal")
        self.btn_stop.config(state="disabled")

        if self.monitor_socket:
            self.send_data_to_monitor({"command": "stop_therapy"})
            try:
                self.monitor_socket.close()
            except Exception as e:
                print(f"Error closing socket during stop_therapy: {e}")
            self.monitor_socket = None
            print("Disconnected from monitor application.")

        if self.monitor_process and self.monitor_process.poll() is None:
            print("Terminating monitor application.")
            try:
                self.monitor_process.terminate()
                self.monitor_process.wait(timeout=5)
                if self.monitor_process.poll() is None:
                    self.monitor_process.kill()
            except Exception as e:
                print(f"Error terminating monitor process during stop: {e}")
            finally:
                self.monitor_process = None

    def run_therapy_session(self, duration_sec):
        """
        Simulates the therapy session, updating elapsed time and checking for completion.
        This runs in a separate thread.
        """
        start_time = time.time()
        while self.is_running and (time.time() - start_time) < duration_sec:
            time.sleep(0.1)

        if self.is_running:
            self.root.after(100, self.complete_therapy)

    def complete_therapy(self):
        """Handles therapy completion."""
        self.is_running = False
        self.status.set("Completed")
        self.btn_start.config(state="normal")
        self.btn_stop.config(state="disabled")
        messagebox.showinfo("Therapy Status", "Therapy session completed!")

        if self.monitor_socket:
            self.send_data_to_monitor({"command": "therapy_completed"})
            try:
                self.monitor_socket.close()
            except Exception as e:
                print(f"Error closing socket during therapy_completed: {e}")
            self.monitor_socket = None
            print("Disconnected from monitor application (therapy completed).")

        if self.monitor_process and self.monitor_process.poll() is None:
            print("Terminating monitor application after completion.")
            try:
                self.monitor_process.terminate()
                self.monitor_process.wait(timeout=5)
                if self.monitor_process.poll() is None:
                    self.monitor_process.kill()
            except Exception as e:
                print(f"Error terminating monitor process after completion: {e}")
            finally:
                self.monitor_process = None

    def send_therapy_parameters_to_monitor(self, command_type="update_parameters"):
        """Collects current therapy parameters and sends them to the monitor."""
        parameters = {
            "master_power": self.master_power.get(),
            "wavelengths": {wl: {"enabled": vals["enabled"].get(), "power_percent": vals["power"].get()}
                            for wl, vals in self.wavelengths.items()},
            "mode": self.mode.get(),
            "pulse_type": self.pulse_type.get(),
            "pulse_duration": self.pulse_duration.get(),
            "frequency": self.frequency.get(),
            "set_power": self.set_power.get(),
            "set_energy": self.set_energy.get(),
            "set_time_min": self.set_time.get(),
            "therapy_end_time": self.therapy_end_time,
            "command": command_type,
            "delivery_mode": self.delivery_mode.get()
        }
        self.send_data_to_monitor(parameters)

    def monitor_progress(self):
        """
        Continuously sends updated parameters to the monitor and updates the GUI
        with remaining time if therapy is running.
        """
        if self.is_running:
            self.send_therapy_parameters_to_monitor()

            current_time = time.time()
            remaining_time_sec = self.therapy_end_time - current_time
            if remaining_time_sec < 0:
                remaining_time_sec = 0

            if remaining_time_sec <= 0 and self.therapy_end_time > 0:
                self.root.after(10, self.complete_therapy)
                return

            if self.therapy_end_time > 0 and self.is_running:
                self.status.set(f"Running... Time Left: {remaining_time_sec:.1f} s")

            self.root.after(1000, self.monitor_progress)

        elif not self.is_running and self.status.get().startswith("Running"):
            self.status.set("Stopped" if self.status.get() != "Completed" else "Completed")

    def on_closing(self):
        """Handles closing the GUI window."""
        if self.is_running:
            if messagebox.askyesno("Exit", "Therapy is currently running. Do you want to stop and exit?"):
                self.stop_therapy()
                self.root.destroy()
        else:
            self.stop_therapy()
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = LaserTherapyGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()