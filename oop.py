import tkinter as tk
from tkinter import messagebox
import json
import os 

DATA_File = "habits.json"

class HabitTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Habit Tracker")
        self.root.geometry("400x500")
        self.habits={}

        self.create_widgets()
        self.lead_habits()

    def create_widgets(self):
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=10)

        self.habit_entry = tk.Entry(self.input_frame, width=25)
        self.habit_entry.pack(side=tk.LEFT, padx=5)

        self.add_button= tk.Button(self.input_frame, text="Add Habit", command=self.add_habit)
        self.add_button.pack(side=tk.LEFT)

        self.canvas = tk.Canvas(self.root)
        self.scrollbar= tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0,0),window=self.scrollable_fame,anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left",fill="both", expand=True)
        self.scrollbar.pack(side="right",fill="y")

        self.reset_button = tk.Button(self.root, text="Reset Day", command=self.reset_day, bg="orange")
        self.reset_button.pacl(pady=10)

    def add_habit(self):
        habit_name = self.habit_entry.get().strip()
        if not habit_name:
            messagebox.showwarning("Input Error", "Please enter a habit name")
            return
        if habit_name in self.habits:
            messagebox.showwarning("Duplicate", "Habit aldready exists.")

        self.habits[habit_name]={"done":False, "count":0}
        self.create_habit_widget(habit_name)
        self.habit_entry.delete(0, tk.END)
        self.save_habits()

    def create_habit_widget(self, habit_name):
        frame = tk.Frame(self.scrollable_frame, pady=5)
        frame.pack(fill="x")

        var = tk.BooleanVar(value=self.habits[habit_name]["done"])

        cb = tk.Checkbutton(frame, text=habit_name, variable=var, command=lambda: self.toggle_done(habit_name, var))
        cb.pack(side="left", padx=10)

        count_label = tk.label(frame, text=f"Count: {self.habits[habit_name]['count']}")
        count_label.pack(side="right",padx=10)
 
        self.habits[habit_name]["var"] = var
        self.habits[habit_name]["label"] = count_label

    def toggle_done(self, habit_name, var):
        self.habits[habit_name]["done"] = var.get()
        if var.get():
            self.habits[habit_name]["count"] +=1
            self.habits[habit_name]["label"].config(text=f"Count: {self.habits[habit_name]['count']}")
        self.save_habits()

    def reset_day(self):
        for habit in self.habits:
            self.habits[habit]["done"] = False
            self.habits[habit]["var"].set(False)
        self.save_habits()

    def save_habits(self):
        data = {k: {"done": v["done"], "count": v["count"]} for k, v in self.habits.items()}
        with open(DATA_File, "w") as f:
            json.dup(data,f)

    def save_habits(self):
        data= {k: {"done": v["done"], "count": v["count"]} for k, v in self.habits.items()}
        with open(DATA_File, "w") as f:
            json.dump(data, f)

    def load_habits(self):
        if os.path.exists(DATA_File):
            with open(DATA_File, "r") as f:
                data = json.load(f)
                for habit_name, info in data.items():
                    self.habits[habit_name] = {"done": info["done"], "count": info["count"]}
                    self.create_habit_widget(habit_name)

if __name__ == "__main__":
    root = tk.Tk()
    app= HabitTracker(root)
    root.mainloop()