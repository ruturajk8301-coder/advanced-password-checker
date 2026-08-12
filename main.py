import tkinter as tk
from tkinter import ttk
from entropy_engine import calculate_entropy
from generator_engine import generate_secure_password
from theme_config import LIGHT_THEME, DARK_THEME
from ui_helpers import toggle_password_visibility, apply_theme_colors

# Global dark mode state tracking flag
is_dark_mode = True


def toggle_theme():
    global is_dark_mode
    is_dark_mode = not is_dark_mode

    # Flip button text indicator state
    theme_btn.config(text="☀  Light Mode" if is_dark_mode else "🌙  Dark Mode")

    # Use layout configuration helper function
    apply_theme_colors(is_dark_mode, root, password_entry, style, theme_btn, LIGHT_THEME, DARK_THEME)

    # Force the checklist engine to instantly update text background maps
    update_strength()


def handle_generate_button():
    secure_pass = generate_secure_password()
    password_entry.delete(0, tk.END)
    password_entry.insert(0, secure_pass)
    update_strength()


def reset_button_text():
    copy_btn.config(text="📋 Copy")


def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(password_entry.get())
    copy_btn.config(text="✔ Copied!")
    # noinspection PyTypeChecker
    root.after(1500, reset_button_text)


def draw_circular_progress(percentage, fill_color, track_color):
    """Dynamically renders a sleek donut-chart gauge indicator via Canvas properties."""
    gauge_canvas.delete("all")

    # Mathematical bounding coordinates for outer rings
    coord = (10, 10, 110, 110)

    # 1. Base track circle
    gauge_canvas.create_arc(coord, start=0, extent=359.9, fill="", outline=track_color, width=12, style="arc")

    # 2. FIX: Limit the maximum sweep angle to -359.99 so Tkinter doesn't hide the full circle ring
    extent_angle = -(percentage / 100) * 360
    if extent_angle == -360:
        extent_angle = -359.99

    if percentage > 0:
        gauge_canvas.create_arc(coord, start=90, extent=extent_angle, fill="", outline=fill_color, width=12,
                                style="arc")

    # 3. Center percentage numerical font summary indicator strings
    gauge_canvas.create_text(60, 60, text=f"{int(percentage)}%", fill="white" if is_dark_mode else "black",
                             font=("Arial", 14, "bold"))


def update_strength(*_args):
    password = password_entry.get()
    entropy, checks = calculate_entropy(password)

    # Dynamic colors based on theme mode
    green_color = "#4CAF50" if is_dark_mode else "green"
    red_color = "#FF5252" if is_dark_mode else "red"
    orange_color = "orange"
    yellow_color = "#E5A93C"

    current_bg = DARK_THEME["frame_bg"] if is_dark_mode else LIGHT_THEME["frame_bg"]
    window_bg = DARK_THEME["bg"] if is_dark_mode else LIGHT_THEME["bg"]
    track_color = "#333333" if is_dark_mode else "#E0E0E0"

    # Match background of canvas immediately to container panel backgrounds
    gauge_canvas.config(background=current_bg, highlightbackground=current_bg)

    # Update Requirement Checklist text & backgrounds seamlessly
    chk_lower.config(text="✔ Lowercase (a-z)" if checks["lower"] else "✘ Lowercase (a-z)",
                     foreground=green_color if checks["lower"] else red_color, background=current_bg)

    chk_upper.config(text="✔ Uppercase (A-Z)" if checks["upper"] else "✘ Uppercase (A-Z)",
                     foreground=green_color if checks["upper"] else red_color, background=current_bg)

    chk_digit.config(text="✔ Number (0-9)" if checks["digit"] else "✘ Number (0-9)",
                     foreground=green_color if checks["digit"] else red_color, background=current_bg)

    chk_special.config(text="✔ Special Character" if checks["special"] else "✘ Special Character",
                       foreground=green_color if checks["special"] else red_color, background=current_bg)

    chk_length.config(text="✔ Length (Minimum 8 chars)" if checks["length"] else "✘ Length (Minimum 8 chars)",
                      foreground=green_color if checks["length"] else red_color, background=current_bg)

    # Live Dashboard Metric Label Updates
    entropy_lb1.config(text=f"Entropy: {entropy:.2f} bits", background=current_bg)
    length_lb1.config(text=f"Length: {len(password)} characters", background=current_bg)

    # Smart assessment metric assignments tracking circle gauges
    # Count how many total character criteria checks are passing successfully out of 5
    passed_checks_count = sum([checks["lower"], checks["upper"], checks["digit"], checks["special"], checks["length"]])

    if not password:
        draw_circular_progress(0, "gray", track_color)
        result_lb1.config(text="Strength: Empty", foreground="white" if is_dark_mode else "black")
        recommendation_lb1.config(text="💡 Enter or generate a password to begin analysis.",
                                  foreground="white" if is_dark_mode else "black", background=window_bg)
    elif entropy < 40 or not checks["length"]:
        draw_circular_progress(25, red_color, track_color)
        result_lb1.config(text="Strength: Very Weak", foreground="red")
        if not checks["length"]:
            recommendation_lb1.config(text="Aahh,.. seek of it.",
                                      foreground="#FF5252", background=window_bg)
        else:
            recommendation_lb1.config(text="Too much comman paterns, sequences, or repetitions seems to me.",
                                      foreground="#FF5252", background=window_bg)
    elif entropy < 60 or passed_checks_count < 4:
        draw_circular_progress(50, orange_color, track_color)
        result_lb1.config(text="Strength: Weak", foreground="orange")
        recommendation_lb1.config(text="Can be better than this, add more chanracters too.",
                                  foreground="orange", background=window_bg)
    elif entropy < 80 or passed_checks_count < 5:
        # If any checklist criteria is failing (like a missing Uppercase), cap the score at 75% max!
        draw_circular_progress(75, yellow_color, track_color)
        result_lb1.config(text="Strength: Strong", foreground=yellow_color)
        recommendation_lb1.config(text="Good, Not Bad, but can be better than this..",
                                  foreground=yellow_color, background=window_bg)
    else:
        # Only awards a perfect 100% green ring if every single criteria requirement is satisfied!
        draw_circular_progress(100, green_color, track_color)
        result_lb1.config(text="Strength: Very Strong", foreground=green_color)
        recommendation_lb1.config(text="yeah!!, you got me.",
                                  foreground=green_color, background=window_bg)


# --- GUI Layout Window Configurations ---
root = tk.Tk()
root.title("Advanced Password Checker")
root.geometry("480x680")
root.resizable(width=True, height=True)

style = ttk.Style(root)
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill="both", expand=True)

# Top Bar Header Area
header_frame = ttk.Frame(main_frame)
header_frame.pack(fill="x", pady=(0, 15))

title_lb1 = ttk.Label(header_frame, text="🔐 Security Dashboard", font=("Arial", 14, "bold"))
title_lb1.pack(side="left")

theme_btn = ttk.Button(header_frame, text="☀  Light Mode", command=toggle_theme)
theme_btn.pack(side="right")

instruction_lb1 = ttk.Label(main_frame, text="Analyze password security & generate safe options:",
                            font=("Arial", 10, "italic"))
instruction_lb1.pack(anchor="w", pady=(0, 10))

# Password Entry Box
password_entry = tk.Entry(main_frame, width=40, font=("Times New Roman", 12, "bold"), show="•")
password_entry.pack(fill="x", pady=(0, 5))


show_pass_var = tk.BooleanVar(value=False)
show_pass_btn = ttk.Checkbutton(
    main_frame,
    text="Show Password",
    variable=show_pass_var,
    command=lambda: toggle_password_visibility(show_pass_var, password_entry)
)
show_pass_btn.pack(anchor="w", pady=(0, 15))

# Side-by-Side Action Button Container
button_frame = ttk.Frame(main_frame)
button_frame.pack(fill="x", pady=(0, 15))

gen_password_btn = ttk.Button(button_frame, text="🔑 Generate Secure Password", command=handle_generate_button)
gen_password_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))

copy_btn = ttk.Button(button_frame, text="📋 Copy", command=copy_to_clipboard, width=10)
copy_btn.pack(side="right")

# --- Visual Security Score Panel (Card Container Layout Grid) ---
score_frame = ttk.LabelFrame(main_frame, text=" Security Metrics ", padding="12")
score_frame.pack(fill="x", pady=(0, 15))

# Sub-containers splitting metrics (text labels left, canvas ring graphic right)
metrics_data_frame = ttk.Frame(score_frame)
metrics_data_frame.pack(side="left", fill="both", expand=True)

result_lb1 = ttk.Label(metrics_data_frame, text="Strength: Empty", font=("Arial", 11, "bold"))
result_lb1.pack(anchor="w", pady=(5, 8))

entropy_lb1 = ttk.Label(metrics_data_frame, text="Entropy: 0.00 bits", font=("Arial", 10))
entropy_lb1.pack(anchor="w", pady=2)

length_lb1 = ttk.Label(metrics_data_frame, text="Length: 0 characters", font=("Arial", 10))
length_lb1.pack(anchor="w", pady=2)

# Custom Canvas Ring Circle configuration slot packed directly to the right side
gauge_canvas = tk.Canvas(score_frame, width=120, height=120, bd=0, highlightthickness=0)
gauge_canvas.pack(side="right", padx=(10, 0))

# --- Visual Checklist Panel Container ---
checklist_frame = ttk.LabelFrame(main_frame, text=" Password Analysis Breakdown ", padding="12")
checklist_frame.pack(fill="x", pady=(0, 15))

chk_lower = ttk.Label(checklist_frame, font=("Arial", 10))
chk_lower.pack(anchor="w", pady=2)

chk_upper = ttk.Label(checklist_frame, font=("Arial", 10))
chk_upper.pack(anchor="w", pady=2)

chk_digit = ttk.Label(checklist_frame, font=("Arial", 10))
chk_digit.pack(anchor="w", pady=2)

chk_special = ttk.Label(checklist_frame, font=("Arial", 10))
chk_special.pack(anchor="w", pady=2)

chk_length = ttk.Label(checklist_frame, font=("Arial", 10))
chk_length.pack(anchor="w", pady=2)

# --- Live Recommendation Bar ---
recommendation_lb1 = tk.Label(
    main_frame,
    text="💡 Enter or generate a password to begin analysis.",
    font=("Arial", 10, "bold"),
    wraplength=440,
    justify="left",
    anchor="w",
    bd=0,
    highlightthickness=0
)
recommendation_lb1.pack(fill="x", pady=(10, 0))

# Global runtime event triggers
password_entry.bind("<KeyRelease>", update_strength)

# Initialize application layout states completely
update_strength()

apply_theme_colors(is_dark_mode, root, password_entry, style, theme_btn, LIGHT_THEME, DARK_THEME)

root.mainloop()
