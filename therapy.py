import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import sys
import json
import time
import threading
import socket
import configparser
import traceback # Import traceback for detailed error logging

# --- Universal Path Setup (as in automode.py for consistency) ---
# Ensure this path is correct and accessible.
# Using r"..." for raw string to avoid issues with backslashes.
# os.path.expanduser handles the '~' correctly across OS.
base_dir = os.path.expanduser(r"~\OneDrive\Desktop\project delhi")
temp_json_path = os.path.join(base_dir, "PythonProject", "temp_selection.json")
PASSWORD_SCREEN_PATH = os.path.join(base_dir, "PythonProject", "new_passwordscreen.py")

# Add a variable for elapsed time for proper pause/resume
# This needs to be part of the class, so initialize it in __init__
class LuminoProApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lumino Pro")
        self.attributes('-fullscreen', True)
        self.configure(bg="#2b2b2b")

        # Variables for displayed values
        self.joule_var = tk.StringVar(value="0")
        self.power_var = tk.StringVar(value="0")
        self.freq_var = tk.StringVar(value="0")
        self.time_var = tk.StringVar(value="00.00")
        self.delivered_j_var = tk.StringVar(value="0000")
        self.delivery_mode_var = tk.StringVar(value="N/A")

        # Variables to store the last received values from LaserTherapyGUI.py
        self._last_received_target_joule = 0
        self._last_received_avg_power = 0.0
        self._last_received_freq = 0
        self._last_received_target_time_seconds = 0.0
        self._last_received_delivery_mode = "N/A"

        # NEW: Variables for live therapy tracking
        self.therapy_start_timestamp = 0
        self.therapy_end_timestamp = 0
        self.total_therapy_duration_sec = 0
        self.elapsed_time_at_pause = 0.0 # Crucial for accurate pause/resume

        # List to hold references to labels/buttons that need dynamic font updates
        self._dynamic_font_widgets = []

        # Bind the configure event to update font sizes dynamically
        self.bind('<Configure>', self.on_root_configure)

        self.create_widgets()

        # Initial font size update after widgets are created
        self.update_font_sizes()

        # Initialize timer state to not running and paused
        self.timer_running = False
        self.is_paused_by_button = True  # Start in a paused state

        # --- Load data from automode.py via temp_selection.json ---
        self.load_initial_therapy_data()

        # Ensure the play/pause button reflects the initial paused state
        self.toggle_btn.config(text="▶")

        # --- Socket Additions ---
        self.start_socket_server()
        # Call update_live_display once to set initial values correctly
        # and then let its after() loop handle subsequent updates.
        self.update_live_display()

    def load_initial_therapy_data(self):
        """Loads therapy parameters from the temp_selection.json file.
        Includes enhanced error handling for file operations and data parsing.
        """
        # --- Debugging: Print the expected path ---
        # This print is crucial for diagnosing path issues.
        print(f"DEBUG: Attempting to load therapy data from: {temp_json_path}")

        # Ensure the directory exists before checking the file
        json_dir = os.path.dirname(temp_json_path)
        if not os.path.isdir(json_dir):
            messagebox.showerror("Directory Not Found",
                                 f"The directory for temp_selection.json does not exist:\n{json_dir}\n"
                                 "Please ensure the 'PythonProject' folder is in the correct location.")
            self.stop_therapy_local()
            return

        if not os.path.exists(temp_json_path):
            messagebox.showwarning("File Not Found",
                                   f"Therapy data file (temp_selection.json) not found at:\n{temp_json_path}\n"
                                   "Please ensure a body part is selected and saved in automode.")
            self.stop_therapy_local()
            return # Exit the function early if file doesn't exist

        try:
            # Check if the path points to a file, not a directory
            if not os.path.isfile(temp_json_path):
                messagebox.showerror("Error",
                                      f"The path '{temp_json_path}' exists but is not a file. "
                                      "Please ensure it points to the temp_selection.json file.")
                self.stop_therapy_local()
                return

            # Check read permissions
            if not os.access(temp_json_path, os.R_OK):
                messagebox.showerror("Permission Error",
                                      f"No read permission for file:\n{temp_json_path}\n"
                                      "Please check file permissions.")
                self.stop_therapy_local()
                return

            # Attempt to open and load the JSON file
            with open(temp_json_path, "r") as f:
                data = json.load(f)

            user_selections = data.get("User Selections", {})
            therapy_data = data.get("Therapy Data", {})
            body_part = data.get("Body Part", "N/A")

            # --- Data Validation and Type Conversion (Crucial for avoiding 'Invalid Argument') ---
            try:
                # Use float() for power as it can be decimal
                self._last_received_avg_power = float(therapy_data.get("Power", 0))
                self.power_var.set(str(self._last_received_avg_power))

                # Use int() for energy and frequency
                self._last_received_target_joule = int(therapy_data.get("Total Energy", 0))
                self.joule_var.set(str(self._last_received_target_joule))

                self._last_received_freq = int(therapy_data.get("Pulse Freq", 0))
                self.freq_var.set(str(self._last_received_freq))

                # Time is in minutes in automode, convert to seconds for internal tracking
                # Added DEBUG print for raw time from JSON
                therapy_time_minutes_raw = therapy_data.get("Time", 0)
                print(f"DEBUG: Raw 'Time' from JSON: {therapy_time_minutes_raw}")

                therapy_time_minutes = float(therapy_time_minutes_raw)
                # Display in minutes, but store internally as seconds
                self.time_var.set(f"{therapy_time_minutes:.2f}")
                self._last_received_target_time_seconds = therapy_time_minutes * 60

            except ValueError as ve:
                messagebox.showerror("Data Type Error",
                                      f"Invalid data type found in temp_selection.json for a numeric field:\n{ve}\n"
                                      "Please ensure 'Total Energy', 'Power', 'Pulse Freq', and 'Time' are valid numbers.")
                print(f"Error during data type conversion: {ve}")
                traceback.print_exc() # Print traceback for value error
                self.stop_therapy_local()
                return

            # Set delivery mode based on the Condition and Body Part
            condition = user_selections.get("Condition", "N/A")
            self.delivery_mode_var.set(f"{body_part.capitalize()} - {condition}")
            self._last_received_delivery_mode = f"{body_part.capitalize()} - {condition}"

            # Initialize therapy start/end times for countdown
            self.total_therapy_duration_sec = self._last_received_target_time_seconds
            print(f"DEBUG: Calculated total_therapy_duration_sec: {self.total_therapy_duration_sec} seconds")

            self.therapy_start_timestamp = 0  # Reset, will be set when play is pressed
            self.therapy_end_timestamp = 0  # Reset, will be set when play is pressed
            self.elapsed_time_at_pause = 0.0 # Reset elapsed time on new load

            self.timer_running = False  # Ensure timer is not running
            self.is_paused_by_button = True  # Ensure initial state is paused

            print("Initial therapy parameters loaded from automode.py. Awaiting user to press Play.")

        except json.JSONDecodeError as e:
            messagebox.showerror("Error", f"Failed to decode temp_selection.json. It might be corrupted or empty:\n{e}")
            print(f"JSON Decode Error: {e}")
            traceback.print_exc() # Print traceback for JSON error
            self.stop_therapy_local()
        except OSError as e:
            # This is the primary place where [Errno 22] Invalid argument would be caught for open()
            messagebox.showerror("File System Error",
                                  f"An operating system error occurred while accessing temp_selection.json:\n{e}\n"
                                  "Please check the file path, name, and permissions.")
            print(f"OS Error while accessing file: {e}")
            traceback.print_exc() # Print traceback for OS error
            self.stop_therapy_local()
        except Exception as e:
            # General catch-all for any other unexpected errors during loading
            messagebox.showerror("Loading Error", f"An unexpected error occurred while loading therapy data:\n{e}")
            print(f"General error during therapy data loading: {e}")
            traceback.print_exc() # Print full traceback for debugging
            self.stop_therapy_local()

    def update_font_sizes(self):
        screen_height = self.winfo_screenheight()

        title_font_size = max(30, int(screen_height / 15))
        display_label_font_size = max(18, int(screen_height / 30))
        unit_label_font_size = max(14, int(screen_height / 40))
        control_button_font_size = max(24, int(screen_height / 20))
        bottom_button_font_size = max(12, int(screen_height / 50))

        for widget_ref, font_type in self._dynamic_font_widgets:
            if widget_ref.winfo_exists():
                if font_type == "title":
                    widget_ref.config(font=("Arial", title_font_size, "bold"))
                elif font_type == "display_label":
                    widget_ref.config(font=("Arial", display_label_font_size, "bold"))
                elif font_type == "unit_label":
                    widget_ref.config(font=("Arial", unit_label_font_size, "bold"))
                elif font_type == "control_button":
                    widget_ref.config(font=("Arial", control_button_font_size))
                elif font_type == "bottom_button":
                    widget_ref.config(font=("Arial", bottom_button_font_size))
                elif font_type == "delivery_mode_label":
                    widget_ref.config(font=("Arial", unit_label_font_size, "bold"))

    def on_root_configure(self, event):
        if event.widget == self:
            self.update_font_sizes()

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=4)
        self.rowconfigure(2, weight=1)

        lbl_title = tk.Label(self, text="Lumino Pro", bg="#2b2b2b", fg="#ff1a53")
        lbl_title.grid(row=0, column=0, columnspan=3, sticky="nw", padx=20, pady=10)
        self._dynamic_font_widgets.append((lbl_title, "title"))

        self.lbl_delivery_mode = tk.Label(self, textvariable=self.delivery_mode_var, bg="#2b2b2b", fg="white",
                                          anchor="w")
        self.lbl_delivery_mode.grid(row=0, column=0, columnspan=3, sticky="sw", padx=20, pady=(0, 10))
        self._dynamic_font_widgets.append((self.lbl_delivery_mode, "delivery_mode_label"))

        tk.Canvas(self, width=140, height=15, bg="#2b2b2b", highlightthickness=0).grid(row=0, column=0, columnspan=3,
                                                                                       sticky="nw", padx=20, pady=50)

        content_frame = tk.Frame(self, bg="#2b2b2b")
        content_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=20, pady=20)
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.columnconfigure(2, weight=1)
        content_frame.rowconfigure(0, weight=1)

        left_panel = tk.Frame(content_frame, bg="#2b2b2b")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=0)
        for i in range(5):
            left_panel.rowconfigure(i, weight=1)
        left_panel.columnconfigure(0, weight=1)

        left_panel_labels_text = ["Energy", "Time ", "pulse freq", "Power", "Delivered J"]

        for i, text in enumerate(left_panel_labels_text):
            lbl = tk.Label(left_panel, text=text, bg="#ff7f2a", fg="white")
            lbl.grid(row=i, column=0, sticky="nsew", pady=2, padx=2)
            self._dynamic_font_widgets.append((lbl, "display_label"))

        btn_frame = tk.Frame(content_frame, bg="#2b2b2b")
        btn_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=0)
        btn_frame.rowconfigure(0, weight=1)
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        self.toggle_btn = tk.Button(btn_frame, text="▶", bg="SystemButtonFace", fg="black", relief="raised")
        self.toggle_btn.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.toggle_btn.config(command=self.toggle_play_pause)
        self._dynamic_font_widgets.append((self.toggle_btn, "control_button"))

        stop_btn = tk.Button(btn_frame, text="■", bg="SystemButtonFace", fg="black", relief="raised")
        stop_btn.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        stop_btn.config(command=self.stop_therapy_local)
        self._dynamic_font_widgets.append((stop_btn, "control_button"))

        right_panel = tk.Frame(content_frame, bg="#2b2b2b")
        right_panel.grid(row=0, column=2, sticky="nsew", padx=10, pady=0)
        for i in range(5):
            right_panel.rowconfigure(i, weight=1)
        right_panel.columnconfigure(0, weight=3)
        right_panel.columnconfigure(1, weight=1)

        lbl_joule_val = tk.Label(right_panel, textvariable=self.joule_var, bg="#ff7f2a", fg="white")
        lbl_joule_val.grid(row=0, column=0, sticky="nsew", pady=2, padx=2)
        self._dynamic_font_widgets.append((lbl_joule_val, "display_label"))
        lbl_joule_unit = tk.Label(right_panel, text="J", bg="#ff7f2a", fg="white")
        lbl_joule_unit.grid(row=0, column=1, sticky="nsew", pady=2, padx=2)
        self._dynamic_font_widgets.append((lbl_joule_unit, "unit_label"))

        lbl_time_val = tk.Label(right_panel, textvariable=self.time_var, bg="#ff7f2a", fg="white")
        lbl_time_val.grid(row=1, column=0, sticky="nsew", pady=2, padx=2)
        self._dynamic_font_widgets.append((lbl_time_val, "display_label"))
        lbl_time_unit = tk.Label(right_panel, text="Min", bg="#ff7f2a", fg="white")
        lbl_time_unit.grid(row=1, column=1, sticky="nsew", pady=2, padx=2)
        self._dynamic_font_widgets.append((lbl_time_unit, "unit_label"))

        lbl_freq_val = tk.Label(right_panel, textvariable=self.freq_var, bg="#ff7f2a", fg="white")
        lbl_freq_val.grid(row=2, column=0, sticky="nsew", pady=2, padx=2)
        self._dynamic_font_widgets.append((lbl_freq_val, "display_label"))
        lbl_freq_unit = tk.Label(right_panel, text="Hz", bg="#ff7f2a", fg="white")
        lbl_freq_unit.grid(row=2, column=1, sticky="nsew", pady=2, padx=2)
        self._dynamic_font_widgets.append((lbl_freq_unit, "unit_label"))

        lbl_power_val = tk.Label(right_panel, textvariable=self.power_var, bg="#ff7f2a", fg="white")
        lbl_power_val.grid(row=3, column=0, sticky="nsew", pady=2, padx=2)
        self._dynamic_font_widgets.append((lbl_power_val, "display_label"))
        lbl_power_unit = tk.Label(right_panel, text="W", bg="#ff7f2a", fg="white")
        lbl_power_unit.grid(row=3, column=1, sticky="nsew", pady=2, padx=2)
        self._dynamic_font_widgets.append((lbl_power_unit, "unit_label"))

        lbl_delivered_j_val = tk.Label(right_panel, textvariable=self.delivered_j_var, bg="#ff7f2a", fg="white")
        lbl_delivered_j_val.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=2, padx=2)
        self._dynamic_font_widgets.append((lbl_delivered_j_val, "display_label"))

        bottom_buttons_frame = tk.Frame(self, bg="#2b2b2b")
        bottom_buttons_frame.grid(row=2, column=0, columnspan=3, sticky="se", padx=20, pady=20)
        bottom_buttons_frame.columnconfigure(0, weight=1)
        bottom_buttons_frame.columnconfigure(1, weight=1)
        bottom_buttons_frame.columnconfigure(2, weight=1)
        bottom_buttons_frame.rowconfigure(0, weight=1)

        btn_back = tk.Button(bottom_buttons_frame, text="Back", bg="#ffdf7f", fg="black", relief="raised",
                             command=self.go_back)
        btn_back.grid(row=0, column=0, padx=5, sticky="e")
        self._dynamic_font_widgets.append((btn_back, "bottom_button"))

        btn_exit = tk.Button(bottom_buttons_frame, text="Exit", bg="#ffdf7f", fg="black", relief="raised",
                             command=self.exit_to_password_screen)
        btn_exit.grid(row=0, column=1, padx=5, sticky="e")
        self._dynamic_font_widgets.append((btn_exit, "bottom_button"))

    def go_back(self):
        print("Going back to the previous screen (closing current window).")
        self.stop_therapy_local()
        self.destroy()

    def exit_to_password_screen(self):
        print("Exiting to password screen...")
        if os.path.exists(PASSWORD_SCREEN_PATH):
            try:
                subprocess.Popen([sys.executable, PASSWORD_SCREEN_PATH])
                print(f"Launched password screen: {PASSWORD_SCREEN_PATH}")
            except Exception as e:
                messagebox.showerror("Launch Error", f"Could not launch password screen:\n{e}")
        else:
            messagebox.showwarning("Script Not Found",
                                   f"The password screen script was not found at:\n{PASSWORD_SCREEN_PATH}")
        self.stop_therapy_local()
        self.destroy()

    def toggle_play_pause(self):
        if self.is_paused_by_button: # If currently paused, try to play
            if self._last_received_avg_power > 0 and self.total_therapy_duration_sec > 0:
                # Calculate remaining time based on total duration minus already elapsed time
                # If this is the very first start, elapsed_time_at_pause will be 0
                remaining_duration = self.total_therapy_duration_sec - self.elapsed_time_at_pause

                # Use a small epsilon to avoid issues with float comparisons near zero
                if remaining_duration <= 0.01:
                    messagebox.showwarning("Therapy Completed", "Therapy time has already elapsed.")
                    self.stop_therapy_local()
                    return

                self.therapy_start_timestamp = time.time()
                self.therapy_end_timestamp = self.therapy_start_timestamp + remaining_duration
                self.timer_running = True
                self.is_paused_by_button = False
                self.toggle_btn.config(text="⏸")
                print(f"DEBUG: Therapy monitor locally resumed/started. Remaining: {remaining_duration:.2f}s, Ends at: {self.therapy_end_timestamp}")
            else:
                messagebox.showwarning("Cannot Start Therapy", "No valid therapy time or power set. Please load therapy data.")
                print("Cannot start: No valid therapy parameters (power or total time is zero).")
                self.is_paused_by_button = True # Ensure it stays in paused state
        else: # If currently playing, pause
            # When pausing, calculate how much time has elapsed so far in the current segment
            if self.therapy_start_timestamp > 0:
                self.elapsed_time_at_pause += (time.time() - self.therapy_start_timestamp)
                # Ensure it doesn't exceed total duration
                if self.elapsed_time_at_pause > self.total_therapy_duration_sec:
                    self.elapsed_time_at_pause = self.total_therapy_duration_sec

            self.timer_running = False
            self.is_paused_by_button = True
            self.toggle_btn.config(text="▶")
            print(f"DEBUG: Therapy monitor locally paused. Elapsed: {self.elapsed_time_at_pause:.2f}s")


    def stop_therapy_local(self):
        self.timer_running = False
        self.is_paused_by_button = True
        self._last_received_target_joule = 0
        self._last_received_avg_power = 0.0
        self._last_received_freq = 0
        self._last_received_target_time_seconds = 0.0
        self._last_received_delivery_mode = "N/A"
        self.therapy_start_timestamp = 0
        self.therapy_end_timestamp = 0
        self.total_therapy_duration_sec = 0
        self.elapsed_time_at_pause = 0.0 # Crucial: reset elapsed time on stop

        self.joule_var.set("0")
        self.power_var.set("0")
        self.freq_var.set("0")
        self.time_var.set("00.00") # Reset display to zero
        self.delivered_j_var.set("0000")
        self.delivery_mode_var.set("N/A")

        self.toggle_btn.config(text="▶")
        print("Therapy monitor locally stopped and reset.")

    def update_live_display(self):
        if self.timer_running and self.therapy_end_timestamp > 0:
            current_time = time.time()
            remaining_time_sec = self.therapy_end_timestamp - current_time

            # Use a small epsilon for floating point comparison to ensure it hits zero
            if remaining_time_sec <= 0.01:
                self.stop_therapy_local()
                print("Therapy session completed based on time.")
                return # Exit the function early after stopping

            minutes_left = remaining_time_sec / 60
            self.time_var.set(f"{minutes_left:.2f}")

            # Calculate true elapsed time based on the new pause/resume logic
            # The time already counted before this current 'play' segment
            # plus the time elapsed since this 'play' segment started.
            current_segment_elapsed = current_time - self.therapy_start_timestamp
            total_elapsed_time_sec = self.elapsed_time_at_pause + current_segment_elapsed
            if total_elapsed_time_sec < 0: total_elapsed_time_sec = 0 # Safety check

            delivered_joules = self._last_received_avg_power * total_elapsed_time_sec
            self.delivered_j_var.set(f"{int(delivered_joules):04d}")

            # Update other displays (these are generally constant during a session)
            self.joule_var.set(str(self._last_received_target_joule))
            self.power_var.set(str(round(self._last_received_avg_power, 2)))
            self.freq_var.set(str(self._last_received_freq))
            self.delivery_mode_var.set(self._last_received_delivery_mode)

        elif not self.timer_running and self.is_paused_by_button:
            # If paused, update 'Time' to show remaining time based on `elapsed_time_at_pause`
            # This ensures the display is correct immediately after pausing.
            remaining_duration_on_pause = self.total_therapy_duration_sec - self.elapsed_time_at_pause
            if remaining_duration_on_pause < 0: remaining_duration_on_pause = 0
            self.time_var.set(f"{remaining_duration_on_pause / 60:.2f}")

            # Also update delivered joules if paused
            delivered_joules_paused = self._last_received_avg_power * self.elapsed_time_at_pause
            self.delivered_j_var.set(f"{int(delivered_joules_paused):04d}")
        else:
            # This block handles the state when the app first loads or after a stop,
            # ensuring the display reflects the initially loaded total_therapy_duration_sec
            # or the reset state.
            if self.total_therapy_duration_sec > 0:
                self.time_var.set(f"{self.total_therapy_duration_sec / 60:.2f}")
            else:
                self.time_var.set("00.00") # Ensure it shows 00.00 if duration is 0


        # Schedule the next update regardless of timer state, so paused state also updates display
        self.after(200, self.update_live_display)

    def start_socket_server(self):
        def server():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(('localhost', 65432))
            except OSError as e:
                print(f"Failed to bind socket: {e}. Port 65432 might be in use. Trying again in 1 second...")
                time.sleep(1) # Wait and let the loop retry
                return # Exit this thread's current attempt, but the outer while True will retry
            sock.listen(1)
            print("Monitoring application listening for data...")
            while True:
                try:
                    conn, addr = sock.accept()
                    with conn:
                        print(f"Connected by {addr}")
                        while True:
                            data = conn.recv(4096)
                            if not data:
                                print("Client disconnected.")
                                # Consider if you want to stop therapy when client disconnects
                                # self.after(0, self.stop_therapy_local)
                                break
                            try:
                                update = json.loads(data.decode('utf-8'))
                                self.after(0, self.process_external_update, update)
                            except json.JSONDecodeError as e:
                                print(f"JSON Decode Error: {e} - Data: {data.decode('utf-8')}")
                            except Exception as e:
                                print("Error parsing update:", e)
                except Exception as e:
                    print(f"Socket server error: {e}. Waiting 1 second before next accept attempt.")
                    time.sleep(1) # Wait before trying to accept new connections again

        threading.Thread(target=server, daemon=True).start()

    def process_external_update(self, update):
        command = update.get('command')

        if command == 'stop_therapy' or command == 'therapy_completed':
            self.stop_therapy_local()
            print(f"Received command: {command}. Local therapy monitor stopped.")
            return

        elif command == 'update_parameters':
            # This part handles updates if another script (like LaserTherapyGUI.py)
            # is actively sending live therapy status.
            if 'set_energy' in update:
                self._last_received_target_joule = update['set_energy']
                self.joule_var.set(str(self._last_received_target_joule))
            if 'set_power' in update:
                self._last_received_avg_power = float(update['set_power'])
                self.power_var.set(str(round(self._last_received_avg_power, 2)))
            if 'frequency' in update:
                self._last_received_freq = update['frequency']
                self.freq_var.set(str(self._last_received_freq))
            if 'set_time_min' in update:
                new_time_minutes = update['set_time_min']
                self._last_received_target_time_seconds = new_time_minutes * 60
                self.time_var.set(f"{new_time_minutes:.2f}")
                # If time is updated while therapy is running, adjust end time
                # NOTE: If this app is the primary timer controller, this adjustment
                # might override local pause/resume logic.
                if self.timer_running and self.therapy_start_timestamp > 0:
                    # Adjust therapy_end_timestamp based on new total duration
                    # and the elapsed time up to this point.
                    # This ensures the timer length changes mid-session.
                    current_elapsed_at_update = time.time() - self.therapy_start_timestamp
                    new_total_elapsed_for_current_segment = self.elapsed_time_at_pause + current_elapsed_at_update
                    self.therapy_end_timestamp = time.time() + (self._last_received_target_time_seconds - new_total_elapsed_for_current_segment)
                    print(f"DEBUG: Timer duration updated externally. New remaining: {(self.therapy_end_timestamp - time.time()):.2f}s")

                self.total_therapy_duration_sec = self._last_received_target_time_seconds

            if 'delivery_mode' in update:
                self._last_received_delivery_mode = update['delivery_mode']
                self.delivery_mode_var.set(self._last_received_delivery_mode)

            # The 'therapy_end_time' handling is still 'pass' as per previous discussion
            # prioritizing local play/pause control.
            if 'therapy_end_time' in update:
                pass


if __name__ == "__main__":
    try:
        app = LuminoProApp()
        app.mainloop()
    except Exception as e:
        print(f"An error occurred while starting or running Lumino Pro App: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)