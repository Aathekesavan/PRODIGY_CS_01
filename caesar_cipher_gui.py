#!/usr/bin/env python3
"""
Caesar Cipher GUI - A premium, modern desktop application for encrypting,
decrypting, and brute-forcing Caesar ciphers using CustomTkinter.

Created for PRODIGY_CS_01.
"""

import tkinter as tk
import customtkinter as ctk
from caesar_cipher import CaesarCipher

# Set visual appearance
ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

class CaesarCipherGUI(ctk.CTk):
    """Modern Desktop GUI for Caesar Cipher Tool."""

    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Caesar Cipher - Premium Cryptography Tool")
        self.geometry("1000x700")
        self.minimum_width = 800
        self.minimum_height = 600
        self.minsize(self.minimum_width, self.minimum_height)

        # Setup variables
        self.shift_numbers_setting = tk.BooleanVar(value=False)
        self.shift_var = tk.StringVar(value="3")
        self.shift_var.trace_add("write", self.on_shift_entry_change)

        # Configure layout grid (1 row, 2 columns: Sidebar & Main Area)
        self.grid_columnconfigure(0, weight=1)  # Sidebar (fixed width)
        self.grid_columnconfigure(1, weight=5)  # Main panel (stretches)
        self.grid_rowconfigure(0, weight=1)

        self._create_sidebar()
        self._create_main_panel()

    def _create_sidebar(self):
        """Creates the sleek left sidebar for settings and info."""
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.sidebar_frame.grid_rowconfigure(5, weight=1)  # Spacer row

        # Title / Logo
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="🛡️ METACIPHER", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.subtitle_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Caesar Cipher Desktop Edition", 
            font=ctk.CTkFont(size=12, slant="italic"),
            text_color="gray"
        )
        self.subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        # Separator line
        self.separator = ctk.CTkFrame(self.sidebar_frame, height=2, fg_color="gray30")
        self.separator.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        # Settings Header
        self.settings_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="SETTINGS", 
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.settings_label.grid(row=3, column=0, padx=20, pady=(15, 5), sticky="w")

        # Number Shift Option
        self.num_shift_switch = ctk.CTkSwitch(
            self.sidebar_frame, 
            text="Shift Numbers (0-9)",
            variable=self.shift_numbers_setting
        )
        self.num_shift_switch.grid(row=4, column=0, padx=20, pady=10, sticky="w")

        # Theme Configuration Section
        self.appearance_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Appearance Mode:", 
            font=ctk.CTkFont(size=11)
        )
        self.appearance_label.grid(row=6, column=0, padx=20, pady=(10, 5), sticky="ws")
        
        self.appearance_optionemenu = ctk.CTkOptionMenu(
            self.sidebar_frame, 
            values=["Dark", "Light", "System"],
            command=self.change_appearance_mode
        )
        self.appearance_optionemenu.grid(row=7, column=0, padx=20, pady=(0, 20), sticky="w")

    def _create_main_panel(self):
        """Creates the main panel containing the tab view for operations."""
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Tabview for different operations
        self.tabview = ctk.CTkTabview(self.main_frame)
        self.tabview.grid(row=0, column=0, sticky="nsew")
        self.tabview.add("Encrypt & Decrypt")
        self.tabview.add("Brute-Force Decrypt")

        self._build_encrypt_decrypt_tab()
        self._build_brute_force_tab()

    def _build_encrypt_decrypt_tab(self):
        """Builds the layout of the primary Encrypt & Decrypt tab."""
        tab = self.tabview.tab("Encrypt & Decrypt")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=1)
        
        # Grid rows: 0 (labels), 1 (text boxes), 2 (shift slider), 3 (action buttons)
        tab.grid_rowconfigure(1, weight=2)  # Input and Output take most space
        tab.grid_rowconfigure(2, weight=0)  # Slider takes minimal space
        tab.grid_rowconfigure(3, weight=0)  # Buttons

        # Left Column: Input Box Header
        self.input_label = ctk.CTkLabel(
            tab, 
            text="Input Text / Message", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.input_label.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")

        # Right Column: Output Box Header
        self.output_label = ctk.CTkLabel(
            tab, 
            text="Output Result", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.output_label.grid(row=0, column=1, padx=15, pady=(15, 5), sticky="w")

        # Left Column: Input Text Area
        self.input_text = ctk.CTkTextbox(tab, wrap="word", font=ctk.CTkFont(size=13))
        self.input_text.grid(row=1, column=0, padx=15, pady=5, sticky="nsew")
        self.input_text.insert("0.0", "Type your plaintext or ciphertext here...")

        # Right Column: Output Text Area
        self.output_text = ctk.CTkTextbox(tab, wrap="word", font=ctk.CTkFont(size=13))
        self.output_text.grid(row=1, column=1, padx=15, pady=5, sticky="nsew")
        self.output_text.configure(state="normal")
        self.output_text.insert("0.0", "Your processed message will appear here...")
        self.output_text.configure(state="disabled")

        # Frame for Shift Control (spanning both columns)
        self.controls_frame = ctk.CTkFrame(tab, fg_color="transparent")
        self.controls_frame.grid(row=2, column=0, columnspan=2, padx=15, pady=20, sticky="ew")
        self.controls_frame.grid_columnconfigure(1, weight=1)  # Slider stretches

        # Shift Entry & Label
        self.shift_label = ctk.CTkLabel(self.controls_frame, text="Shift Key Value:", font=ctk.CTkFont(weight="bold"))
        self.shift_label.grid(row=0, column=0, padx=(0, 10), pady=5)

        self.shift_entry = ctk.CTkEntry(self.controls_frame, width=60, textvariable=self.shift_var, justify="center")
        self.shift_entry.grid(row=0, column=2, padx=(10, 0), pady=5)

        # Shift Slider
        self.shift_slider = ctk.CTkSlider(
            self.controls_frame, 
            from_=0, 
            to=25, 
            number_of_steps=25, 
            command=self.on_slider_move
        )
        self.shift_slider.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.shift_slider.set(3)

        # Frame for Action Buttons (spanning both columns)
        self.buttons_frame = ctk.CTkFrame(tab, fg_color="transparent")
        self.buttons_frame.grid(row=3, column=0, columnspan=2, padx=15, pady=(0, 15), sticky="ew")
        self.buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Encrypt Button
        self.encrypt_button = ctk.CTkButton(
            self.buttons_frame, 
            text="🔒 Encrypt", 
            command=self.run_encrypt,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.encrypt_button.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        # Decrypt Button
        self.decrypt_button = ctk.CTkButton(
            self.buttons_frame, 
            text="🔓 Decrypt", 
            command=self.run_decrypt,
            fg_color="transparent",
            border_width=2,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.decrypt_button.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Copy Output Button
        self.copy_button = ctk.CTkButton(
            self.buttons_frame, 
            text="📋 Copy Output", 
            command=self.copy_to_clipboard,
            fg_color="gray30",
            hover_color="gray40",
            font=ctk.CTkFont(size=14)
        )
        self.copy_button.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

    def _build_brute_force_tab(self):
        """Builds the layout of the Brute-Force Decrypt tab."""
        tab = self.tabview.tab("Brute-Force Decrypt")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(2, weight=1)  # The results grid takes the remainder space

        # Input Row
        self.bf_input_label = ctk.CTkLabel(
            tab, 
            text="Enter text to brute-force (tries all 25 shifts):", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.bf_input_label.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")

        # Text input panel
        self.bf_input_text = ctk.CTkTextbox(tab, height=100, wrap="word", font=ctk.CTkFont(size=13))
        self.bf_input_text.grid(row=1, column=0, padx=15, pady=5, sticky="ew")
        self.bf_input_text.insert("0.0", "Khoor, Zruog!")

        # Visual Grid Header / Controls
        self.bf_action_frame = ctk.CTkFrame(tab, fg_color="transparent")
        self.bf_action_frame.grid(row=2, column=0, padx=15, pady=10, sticky="ew")
        self.bf_action_frame.grid_columnconfigure(0, weight=1)

        self.bf_button = ctk.CTkButton(
            self.bf_action_frame, 
            text="💥 Run Brute Force Decryption", 
            command=self.run_brute_force,
            fg_color="#A12424",
            hover_color="#851D1D",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.bf_button.grid(row=0, column=0, padx=0, pady=5, sticky="ew")

        # Scrollable Frame for Brute-Force Outputs
        self.bf_scrollable_frame = ctk.CTkScrollableFrame(tab, label_text="Possible Shifts Decryptions")
        self.bf_scrollable_frame.grid(row=3, column=0, padx=15, pady=(5, 15), sticky="nsew")
        self.bf_scrollable_frame.grid_columnconfigure(1, weight=1)  # The decrypted text column stretches

    def on_slider_move(self, value):
        """Callback for slider adjustment, updates the shift value textbox."""
        # Temporal flag to prevent recursion trace triggers
        self._updating_from_slider = True
        self.shift_var.set(str(int(value)))
        self._updating_from_slider = False

    def on_shift_entry_change(self, *args):
        """Handles manual integer changes in the Shift Value Entry Box."""
        if getattr(self, "_updating_from_slider", False):
            return
        
        val_str = self.shift_var.get()
        if not val_str:
            return
            
        try:
            val = int(val_str)
            # Sync slider with modulo shift value (0-25)
            self.shift_slider.set(val % 26)
        except ValueError:
            pass  # Let user finish typing

    def change_appearance_mode(self, new_appearance_mode: str):
        """Sets appearance mode (Dark, Light, System)."""
        ctk.set_appearance_mode(new_appearance_mode)

    def run_encrypt(self):
        """Performs encryption operation and displays result."""
        input_content = self.input_text.get("0.0", "end-1c").strip()
        if not input_content or input_content == "Type your plaintext or ciphertext here...":
            self.show_error("Input message is empty!")
            return

        try:
            shift = int(self.shift_var.get())
        except ValueError:
            self.show_error("Shift key must be an integer!")
            return

        encrypted = CaesarCipher.encrypt(input_content, shift, self.shift_numbers_setting.get())
        self.update_output_box(encrypted)

    def run_decrypt(self):
        """Performs decryption operation and displays result."""
        input_content = self.input_text.get("0.0", "end-1c").strip()
        if not input_content or input_content == "Type your plaintext or ciphertext here...":
            self.show_error("Input message is empty!")
            return

        try:
            shift = int(self.shift_var.get())
        except ValueError:
            self.show_error("Shift key must be an integer!")
            return

        decrypted = CaesarCipher.decrypt(input_content, shift, self.shift_numbers_setting.get())
        self.update_output_box(decrypted)

    def run_brute_force(self):
        """Computes and renders all 25 decryptions in the scrollable view."""
        # Clear previous scroll contents
        for widget in self.bf_scrollable_frame.winfo_children():
            widget.destroy()

        input_content = self.bf_input_text.get("0.0", "end-1c").strip()
        if not input_content:
            self.show_error("Enter ciphertext to brute force!")
            return

        brute_results = CaesarCipher.brute_force(input_content, self.shift_numbers_setting.get())

        for index, (shift, decrypted) in enumerate(brute_results.items()):
            # Row container
            row_frame = ctk.CTkFrame(self.bf_scrollable_frame, fg_color="transparent")
            row_frame.grid(row=index, column=0, columnspan=3, padx=5, pady=3, sticky="ew")
            row_frame.grid_columnconfigure(1, weight=1)

            # Key label
            key_label = ctk.CTkLabel(
                row_frame, 
                text=f"Shift {shift:02d}:", 
                font=ctk.CTkFont(weight="bold", size=12),
                width=60
            )
            key_label.grid(row=0, column=0, padx=5, pady=2, sticky="w")

            # Decrypted Text Box
            text_entry = ctk.CTkEntry(
                row_frame, 
                font=ctk.CTkFont(size=12)
            )
            text_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
            text_entry.insert(0, decrypted)
            text_entry.configure(state="readonly")

            # Mini Copy Button for this specific shift row
            mini_copy = ctk.CTkButton(
                row_frame,
                text="📋 Copy",
                width=60,
                fg_color="gray30",
                hover_color="gray40",
                command=lambda text=decrypted: self.copy_custom(text)
            )
            mini_copy.grid(row=0, column=2, padx=5, pady=2, sticky="e")

    def update_output_box(self, content):
        """Safely updates output read-only textbox."""
        self.output_text.configure(state="normal")
        self.output_text.delete("0.0", "end")
        self.output_text.insert("0.0", content)
        self.output_text.configure(state="disabled")

    def copy_to_clipboard(self):
        """Copies the text inside output result box to OS clipboard."""
        text = self.output_text.get("0.0", "end-1c")
        if text and text != "Your processed message will appear here...":
            self.clipboard_clear()
            self.clipboard_append(text)
            self.show_toast("Copied to clipboard!")
        else:
            self.show_error("No result to copy!")

    def copy_custom(self, text):
        """Clipboard helper for brute force mini-buttons."""
        self.clipboard_clear()
        self.clipboard_append(text)
        self.show_toast("Copied result!")

    def show_error(self, message):
        """Helper to show warning modal."""
        # Simple non-blocking customtkinter dialog or status message
        dialog = ctk.CTkTabview(self) # just to bypass and make it custom
        # For simplicity and style, we will create a clean popup window
        popup = ctk.CTkToplevel(self)
        popup.title("Warning")
        popup.geometry("300x120")
        popup.resizable(False, False)
        # Center popup on master
        popup.transient(self)
        popup.grab_set()

        label = ctk.CTkLabel(popup, text=f"⚠️ {message}", font=ctk.CTkFont(size=13, weight="bold"))
        label.pack(padx=20, pady=(20, 15))

        btn = ctk.CTkButton(popup, text="OK", width=80, command=popup.destroy)
        btn.pack(pady=(0, 10))

    def show_toast(self, message):
        """Renders a temporary message banner or indicator."""
        # Since Tkinter doesn't do toast easily, we can display a temporary label
        toast = ctk.CTkToplevel(self)
        toast.overrideredirect(True)
        # Position top-center of master
        x = self.winfo_x() + (self.winfo_width() // 2) - 100
        y = self.winfo_y() + 50
        toast.geometry(f"200x40+{x}+{y}")
        toast.configure(fg_color="gray10")

        lbl = ctk.CTkLabel(toast, text=message, text_color="green", font=ctk.CTkFont(weight="bold"))
        lbl.pack(fill="both", expand=True)
        # Fade out and destroy after 1.5 seconds
        self.after(1500, toast.destroy)


if __name__ == "__main__":
    app = CaesarCipherGUI()
    app.mainloop()
