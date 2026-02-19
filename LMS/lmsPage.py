import database
import tkinter as tk
from tkinter import ttk, messagebox
import books
from books import data_science_books
import re

# Colors
COLORS = {
    "bg_main": "#E8ECF4",
    "bg_card": "#FFFFFF",
    "primary": "#2C3E50",
    "accent": "#3498DB",
    "accent_hover": "#2980B9",
    "danger": "#E74C3C",
    "danger_hover": "#C0392B",
    "neutral": "#95A5A6",
    "neutral_hover": "#7F8C8D",
    "text": "#34495E",
    "light_text": "#7F8C8D"
}

# Static Data
STATIC_BOOKS = data_science_books


def create_button(parent, text, bg_color, hover_color, command=None):
    btn = tk.Button(parent, text=text, font=("Helvetica", 10, "bold"), bg=bg_color, fg="white",
                    activebackground=hover_color, activeforeground="white",
                    relief="flat", cursor="hand2", borderwidth=0, command=command)
    btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))
    return btn


def open_lms_window(login_window, student_id):
    database.create_table()
    lms_window = tk.Toplevel()
    lms_window.title(f"Library Management System - {student_id}")
    lms_window.configure(bg=COLORS["bg_main"])

    # --- DYNAMIC GEOMETRY ---
    screen_height = lms_window.winfo_screenheight()
    app_height = min(880, int(screen_height * 0.9))
    x_c = int((lms_window.winfo_screenwidth() / 2) - (550 / 2))
    y_c = int((screen_height / 2) - (app_height / 2))
    lms_window.geometry(f"550x{app_height}+{x_c}+{y_c}")

    def on_close():
        login_window.destroy()

    lms_window.protocol("WM_DELETE_WINDOW", on_close)

    def logout():
        confirm = messagebox.askyesno("Logout", "Are you sure you want to log out?")
        if confirm:
            lms_window.destroy()
            login_window.deiconify()

    # 1. Header
    header_frame = tk.Frame(lms_window, bg=COLORS["primary"], height=80)
    header_frame.pack(fill="x", side="top")
    header_frame.pack_propagate(False)

    tk.Label(header_frame, text="LIBRARY MANAGER", font=("Helvetica", 20, "bold"),
             bg=COLORS["primary"], fg="white").pack(pady=25)

    # 2. Main Card Frame
    card_frame = tk.Frame(lms_window, bg=COLORS["bg_card"], bd=0, highlightthickness=0)
    card_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # 3. Bottom Frame
    bottom_frame = tk.Frame(card_frame, bg=COLORS["bg_card"])
    bottom_frame.pack(side="bottom", fill="x", pady=20)

    # --- Helper Functions ---
    def refresh_stock_label():
        """Updates the stock label based on the currently selected dropdown item."""
        current_book = book_dropdown.get()
        if current_book in STATIC_BOOKS:
            qty_label.config(text=f"In Stock: {STATIC_BOOKS[current_book]}")
        else:
            qty_label.config(text="In Stock: -")

    def load_books():
        books_listbox.delete(0, tk.END)
        books_data = database.get_books(student_id)



        for row in books_data:
            book_title = row[1]

            # Format: ID | Book Name | Date
            books_listbox.insert(tk.END, f"{row[0]} | {book_title} | {row[2]}")

    def return_book_action():
        selected = books_listbox.curselection()
        if not selected:
            messagebox.showwarning("Error", "Please select a book to return")
            return

        list_item = books_listbox.get(selected[0])
        parts = list_item.split(" | ")

        if len(parts) >= 2:
            book_id = parts[0].strip()
            book_title = parts[1].strip()

            # 1. Update Database
            database.delete_book(book_id)

            # 2. Update Stock
            if book_title in STATIC_BOOKS:
                STATIC_BOOKS[book_title] += 1

                if book_dropdown.get() == book_title:
                    refresh_stock_label()
            else:
                print(f"DEBUG: Could not find '{book_title}' in list.")

            load_books()
        else:
            messagebox.showerror("Error", "Could not parse book data.")

    # --- Bottom Buttons ---
    btn_remove = create_button(
        bottom_frame, "RETURN SELECTED", COLORS["danger"], COLORS["danger_hover"],
        command=return_book_action
    )
    btn_remove.pack(pady=(0, 10), ipadx=20, ipady=5, anchor="center")

    btn_logout = create_button(bottom_frame, "LOGOUT", COLORS["neutral"], COLORS["neutral_hover"], command=logout)
    btn_logout.pack(ipadx=40, ipady=5, anchor="center")

    # --- Middle Content ---
    content_container = tk.Frame(card_frame, bg=COLORS["bg_card"])
    content_container.pack(side="top", fill="both", expand=True)

    form_frame = tk.Frame(content_container, bg=COLORS["bg_card"])
    form_frame.pack(pady=10)

    labels = ["Student Name", "Student Email", "Phone Number"]
    entries = {}

    for i, label_text in enumerate(labels):
        tk.Label(form_frame, text=label_text, font=("Helvetica", 10, "bold"), bg=COLORS["bg_card"],
                 fg=COLORS["text"]).grid(row=i * 2, column=0, sticky="w", pady=(0, 5))
        entry = tk.Entry(form_frame, width=30, font=("Helvetica", 11), relief="flat", bg="#F0F3F4")
        entry.grid(row=i * 2 + 1, column=0, ipady=5, padx=5, pady=(0, 15))
        entries[label_text] = entry

    tk.Label(form_frame, text="Select Book", font=("Helvetica", 10, "bold"), bg=COLORS["bg_card"],
             fg=COLORS["text"]).grid(row=6, column=0, sticky="w", pady=(0, 5))

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TCombobox", fieldbackground="#F0F3F4", background="white", arrowsize=15)

    book_dropdown = ttk.Combobox(form_frame, width=28, font=("Helvetica", 11), state="readonly")
    book_dropdown['values'] = list(STATIC_BOOKS.keys())
    book_dropdown.set("Select a Book")
    book_dropdown.grid(row=7, column=0, ipady=5, padx=5)

    qty_label = tk.Label(form_frame, text="In Stock: -", font=("Helvetica", 9), bg=COLORS["bg_card"],
                         fg=COLORS["light_text"])
    qty_label.grid(row=8, column=0, sticky="e", pady=5)

    def on_combobox_select(event):
        refresh_stock_label()

    book_dropdown.bind("<<ComboboxSelected>>", on_combobox_select)

    # --- Validation ---
    def validate_phone(phone_str):
        return phone_str.isdigit() and 10 <= len(phone_str) <= 15

    def validate_email(email_str):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email_str) is not None

    def issue_book_action():
        name = entries["Student Name"].get().strip()
        email = entries["Student Email"].get().strip()
        phone = entries["Phone Number"].get().strip()
        book = book_dropdown.get()

        if not name or not email or not phone or book == "Select a Book":
            messagebox.showwarning("Missing Info", "Please fill all fields and select a book.")
            return

        if not validate_phone(phone):
            messagebox.showerror("Invalid Phone", "Phone number must be digits only (10-15 chars).")
            return

        if not validate_email(email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return

        # Stock Check
        current_stock = STATIC_BOOKS.get(book, 0)

        if current_stock <= 0:
            messagebox.showerror("Out of Stock", f"Sorry, '{book}' is currently out of stock.")
            return

        # Issue Book
        database.issue_book(student_id, name, email, phone, book)

        # Decrease Stock
        STATIC_BOOKS[book] -= 1
        refresh_stock_label()

        messagebox.showinfo("Success", "Book issued successfully")



        load_books()

    btn_add = create_button(
        content_container, "ISSUE BOOK", COLORS["accent"], COLORS["accent_hover"],
        command=issue_book_action
    )
    btn_add.pack(pady=5, ipadx=40, ipady=5)

    ttk.Separator(content_container, orient="horizontal").pack(fill="x", padx=20, pady=10)

    tk.Label(content_container, text="Currently Borrowed", font=("Helvetica", 10, "bold"), bg=COLORS["bg_card"],
             fg=COLORS["text"]).pack(pady=5)

    list_frame = tk.Frame(content_container, bg=COLORS["bg_card"])
    list_frame.pack(padx=20, pady=5, fill="both", expand=True)

    books_listbox = tk.Listbox(list_frame, width=40, height=5, font=("Courier", 10),
                               bg="#F9FAFB", fg=COLORS["text"], bd=0, highlightthickness=0,
                               selectbackground=COLORS["accent"])
    books_listbox.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=books_listbox.yview)
    scrollbar.pack(side="right", fill="y")
    books_listbox.config(yscrollcommand=scrollbar.set)

    load_books()