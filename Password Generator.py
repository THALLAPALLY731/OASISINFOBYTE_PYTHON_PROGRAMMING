import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip

class PasswordGenerator:
    def __init__(self, master):
        self.master = master
        master.title("Advanced Password Generator")
        master.geometry("400x400")

        self.create_widgets()

    def create_widgets(self):
        # Length slider
        ttk.Label(self.master, text="Password Length:").pack(pady=5)
        self.length_var = tk.IntVar(value=12)
        self.length_slider = ttk.Scale(self.master, from_=4, to=32, orient="horizontal", 
                                       variable=self.length_var, length=200)
        self.length_slider.pack()
        ttk.Label(self.master, textvariable=self.length_var).pack()

        # Character set checkboxes
        self.use_letters = tk.BooleanVar(value=True)
        self.use_numbers = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)

        ttk.Checkbutton(self.master, text="Include Letters", variable=self.use_letters).pack(pady=5)
        ttk.Checkbutton(self.master, text="Include Numbers", variable=self.use_numbers).pack(pady=5)
        ttk.Checkbutton(self.master, text="Include Symbols", variable=self.use_symbols).pack(pady=5)

        # Password complexity
        ttk.Label(self.master, text="Password Complexity:").pack(pady=5)
        self.complexity_var = tk.StringVar(value="Medium")
        complexity_combo = ttk.Combobox(self.master, textvariable=self.complexity_var, 
                                        values=["Low", "Medium", "High"], state="readonly")
        complexity_combo.pack()

        # Generate button
        ttk.Button(self.master, text="Generate Password", command=self.generate_password).pack(pady=10)

        # Password display
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(self.master, textvariable=self.password_var, state="readonly", width=40)
        password_entry.pack(pady=5)

        # Copy button
        ttk.Button(self.master, text="Copy to Clipboard", command=self.copy_to_clipboard).pack()

    def generate_password(self):
        length = self.length_var.get()
        use_letters = self.use_letters.get()
        use_numbers = self.use_numbers.get()
        use_symbols = self.use_symbols.get()
        complexity = self.complexity_var.get()

        if not any([use_letters, use_numbers, use_symbols]):
            messagebox.showerror("Error", "Please select at least one character set.")
            return

        character_set = ""
        if use_letters:
            character_set += string.ascii_letters
        if use_numbers:
            character_set += string.digits
        if use_symbols:
            character_set += string.punctuation

        # Adjust character set based on complexity
        if complexity == "Low":
            character_set = character_set.replace(string.punctuation, "")
        elif complexity == "High":
            character_set += string.ascii_uppercase + string.digits + string.punctuation

        # Generate password
        password = ''.join(random.choice(character_set) for _ in range(length))

        # Ensure password meets complexity requirements
        if complexity == "Medium" and not (any(c.islower() for c in password) and 
                                           any(c.isupper() for c in password) and 
                                           any(c.isdigit() for c in password)):
            return self.generate_password()  # Recursively generate a new password
        elif complexity == "High" and not (any(c.islower() for c in password) and 
                                           any(c.isupper() for c in password) and 
                                           any(c.isdigit() for c in password) and 
                                           any(c in string.punctuation for c in password)):
            return self.generate_password()  # Recursively generate a new password

        self.password_var.set(password)

    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showerror("Error", "No password generated yet.")

if __name__ == "__main__":
    root = tk.Tk()
    password_generator = PasswordGenerator(root)
    root.mainloop()