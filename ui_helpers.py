import tkinter as tk
from tkinter import ttk


def toggle_password_visibility(show_pass_var, password_entry):
    if show_pass_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="•")  # Changed from "*" to a bold bullet dot


def apply_theme_colors(is_dark_mode, root, password_entry, style, theme_btn, light_theme, dark_theme):
    colors = dark_theme if is_dark_mode else light_theme

    # FIX: Using 'bg' instead of 'main_bg' to match your actual theme keys
    root.config(background=colors["bg"])
    password_entry.config(background=colors["entry_bg"], foreground=colors["text"], insertbackground=colors["text"])

    # Configure TTK widget element global maps
    style.theme_use("clam")  # Using 'clam' allows custom background overrides on Windows buttons

    style.configure(".", background=colors["bg"], foreground=colors["text"])
    style.configure("TLabelframe", background=colors["bg"], foreground=colors["text"])
    style.configure("TLabelframe.Label", background=colors["bg"], foreground=colors["text"], font=("Arial", 10, "bold"))
    style.configure("TLabel", background=colors["bg"], foreground=colors["text"])
    style.configure("TCheckbutton", background=colors["bg"], foreground=colors["text"])

    # Forced matching theme style layout properties for buttons
    style.configure("TButton",
                    background=colors["entry_bg"],
                    foreground=colors["text"],
                    bordercolor=colors["frame_bg"],
                    lightcolor=colors["entry_bg"],
                    darkcolor=colors["entry_bg"],
                    font=("Arial", 10, "bold"),
                    focuscolor="none")

    # Hover states (Changes color slightly when moving mouse over buttons)
    style.map("TButton",
              background=[("active", colors["frame_bg"])],
              foreground=[("active", colors["text"])])
