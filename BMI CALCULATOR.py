import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class BMICalculator:
    def __init__(self, master):
        self.master = master
        master.title("BMI Calculator")
        master.geometry("600x400")

        self.create_widgets()
        self.create_database()

    def create_widgets(self):
        # User input fields
        tk.Label(self.master, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self.master)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.master, text="Weight (kg):").grid(row=1, column=0, padx=5, pady=5)
        self.weight_entry = tk.Entry(self.master)
        self.weight_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.master, text="Height (m):").grid(row=2, column=0, padx=5, pady=5)
        self.height_entry = tk.Entry(self.master)
        self.height_entry.grid(row=2, column=1, padx=5, pady=5)

        # Calculate button
        self.calculate_button = tk.Button(self.master, text="Calculate BMI", command=self.calculate_bmi)
        self.calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Result display
        self.result_label = tk.Label(self.master, text="")
        self.result_label.grid(row=4, column=0, columnspan=2, pady=5)

        # Graph
        self.figure, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.get_tk_widget().grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def create_database(self):
        self.conn = sqlite3.connect('bmi_data.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bmi_records
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT,
             weight REAL,
             height REAL,
             bmi REAL,
             date TEXT)
        ''')
        self.conn.commit()

    def calculate_bmi(self):
        try:
            name = self.name_entry.get()
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())

            if weight <= 0 or height <= 0:
                raise ValueError("Weight and height must be positive numbers.")

            bmi = weight / (height ** 2)
            category = self.classify_bmi(bmi)

            result = f"BMI: {bmi:.2f} - {category}"
            self.result_label.config(text=result)

            # Save to database
            self.save_bmi(name, weight, height, bmi)

            # Update graph
            self.update_graph(name)

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def classify_bmi(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    def save_bmi(self, name, weight, height, bmi):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO bmi_records (name, weight, height, bmi, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, weight, height, bmi, date))
        self.conn.commit()

    def update_graph(self, name):
        self.cursor.execute('''
            SELECT date, bmi FROM bmi_records
            WHERE name = ? ORDER BY date
        ''', (name,))
        data = self.cursor.fetchall()

        if data:
            dates, bmis = zip(*data)
            self.ax.clear()
            self.ax.plot(dates, bmis, marker='o')
            self.ax.set_title(f"BMI Trend for {name}")
            self.ax.set_xlabel("Date")
            self.ax.set_ylabel("BMI")
            self.ax.tick_params(axis='x', rotation=45)
            self.figure.tight_layout()
            self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    bmi_calculator = BMICalculator(root)
    root.mainloop()