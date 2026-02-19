import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import lmsPage
import re

COLORS = {
    "bg_card": "#FFFFFF",
    "primary": "#2C3E50",
    "accent": "#3498DB",
    "accent_hover": "#2980B9",
    "text": "#34495E",
}


def verify_login():
    student_id = entry_id.get().strip().upper()  # convert input to uppercase

    if student_id == "":
        messagebox.showwarning("Input Required", "Please write your student ID.")
        return

    # Pattern: 20YY[F or S]-XXX-NNN
    pattern = r"^20\d{2}[FS]-[A-Z]{3,7}-\d{3,5}$"

    if not re.match(pattern, student_id):
        messagebox.showerror(
            "Invalid ID Format",
            "Student ID must be in this format:\n\n2025F-BDS-017\nor 2025S-BDS-025\n(All capital letters)"
        )
        return

    # Login successful
    messagebox.showinfo("Login Successful", f"Welcome, Student {student_id}!")
    root.withdraw()
    lmsPage.open_lms_window(root, student_id)


root = tk.Tk()
root.title("Student Login")
root.geometry("1000x860")

canvas = tk.Canvas(root, highlightthickness=0, bg=COLORS["primary"])
canvas.pack(fill="both", expand=True)

image_path = "background.jpg"
original_image = None
bg_item = None

if os.path.exists(image_path):
    try:
        original_image = Image.open(image_path)
        bg_image = ImageTk.PhotoImage(original_image.resize((1, 1)))
        bg_item = canvas.create_image(0, 0, image=bg_image, anchor="nw")
    except Exception as e:
        print(f"Image load error: {e}")

card_frame = tk.Frame(root, bg=COLORS["bg_card"], bd=0)

header_stripe = tk.Frame(card_frame, bg=COLORS["primary"], height=80)
header_stripe.pack(fill="x")
header_stripe.pack_propagate(False)

tk.Label(header_stripe, text="LMS PORTAL", font=("Helvetica", 20, "bold"),
         bg=COLORS["primary"], fg="white").pack(expand=True)

form_frame = tk.Frame(card_frame, bg=COLORS["bg_card"])
form_frame.pack(pady=40, padx=40, fill="x")

tk.Label(form_frame, text="Write your student id", font=("Helvetica", 11, "bold"),
         bg=COLORS["bg_card"], fg=COLORS["text"]).pack(anchor="w", pady=(0, 5))

entry_id = tk.Entry(form_frame, font=("Helvetica", 12), relief="flat", bg="#F0F3F4", justify="center")
entry_id.pack(fill="x", ipady=8)
tk.Frame(form_frame, bg=COLORS["accent"], height=2).pack(fill="x")

def on_enter(e):
    btn_submit['background'] = COLORS["accent_hover"]

def on_leave(e):
    btn_submit['background'] = COLORS["accent"]

btn_submit = tk.Button(card_frame, text="LOGIN", font=("Helvetica", 12, "bold"),
                       bg=COLORS["accent"], fg="white",
                       activebackground=COLORS["accent_hover"], activeforeground="white",
                       relief="flat", cursor="hand2", command=verify_login)
btn_submit.bind("<Enter>", on_enter)
btn_submit.bind("<Leave>", on_leave)
btn_submit.pack(pady=20, ipadx=40, ipady=8)

def resize_ui(event):
    w = event.width
    h = event.height
    if original_image and bg_item:
        try:
            img_w, img_h = original_image.size
            ratio = max(w / img_w, h / img_h)
            new_size = (int(img_w * ratio), int(img_h * ratio))
            resized_image = original_image.resize(new_size, Image.Resampling.LANCZOS)
            new_photo = ImageTk.PhotoImage(resized_image)
            canvas.itemconfig(bg_item, image=new_photo)
            canvas.image = new_photo
            canvas.coords(bg_item, (w - new_size[0]) // 2, (h - new_size[1]) // 2)
        except:
            pass
    canvas.create_window(w // 2, h // 2, window=card_frame, width=380, height=420)

canvas.bind("<Configure>", resize_ui)

root.mainloop()