import tkinter as tk
import pickle
from tkinter import messagebox

class Task:
    def __init__(self, title, description='', priority='Low', due_date=None, completed=False):
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = completed

class TodoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do List App")
        
        # Load tasks from local storage
        self.load_tasks()
        
        # Create GUI elements
        self.task_listbox = tk.Listbox(master, width=50, height=15)
        self.task_listbox.pack(pady=10)
        self.refresh_task_list()
        
        self.add_button = tk.Button(master, text="Add Task", command=self.open_add_task_window)
        self.add_button.pack(side=tk.LEFT, padx=10)
        
        self.edit_button = tk.Button(master, text="Edit Task", command=self.edit_task)
        self.edit_button.pack(side=tk.LEFT, padx=10)
        
        self.delete_button = tk.Button(master, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT, padx=10)
        
        self.mark_complete_button = tk.Button(master, text="Mark as Complete", command=self.mark_complete)
        self.mark_complete_button.pack(side=tk.LEFT, padx=10)
        
        self.master.protocol("WM_DELETE_WINDOW", self.save_and_exit)

    def open_add_task_window(self):
        add_window = tk.Toplevel(self.master)
        add_window.title("Add Task")

        title_label = tk.Label(add_window, text="Title:")
        title_label.grid(row=0, column=0, padx=10, pady=5)
        self.title_entry = tk.Entry(add_window, width=40)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        desc_label = tk.Label(add_window, text="Description:")
        desc_label.grid(row=1, column=0, padx=10, pady=5)
        self.desc_entry = tk.Entry(add_window, width=40)
        self.desc_entry.grid(row=1, column=1, padx=10, pady=5)

        add_button = tk.Button(add_window, text="Add", command=self.add_task)
        add_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

    def add_task(self):
        title = self.title_entry.get()
        description = self.desc_entry.get()
        new_task = Task(title=title, description=description)
        self.tasks.append(new_task)
        self.refresh_task_list()
        self.save_tasks()
        self.master.focus_set()

    def edit_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            selected_task = self.tasks[selected_index[0]]
            edit_window = tk.Toplevel(self.master)
            edit_window.title("Edit Task")

            title_label = tk.Label(edit_window, text="Title:")
            title_label.grid(row=0, column=0, padx=10, pady=5)
            self.title_entry = tk.Entry(edit_window, width=40)
            self.title_entry.grid(row=0, column=1, padx=10, pady=5)
            self.title_entry.insert(tk.END, selected_task.title)

            desc_label = tk.Label(edit_window, text="Description:")
            desc_label.grid(row=1, column=0, padx=10, pady=5)
            self.desc_entry = tk.Entry(edit_window, width=40)
            self.desc_entry.grid(row=1, column=1, padx=10, pady=5)
            self.desc_entry.insert(tk.END, selected_task.description)

            save_button = tk.Button(edit_window, text="Save", command=lambda: self.save_edit(selected_index))
            save_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

    def save_edit(self, selected_index):
        title = self.title_entry.get()
        description = self.desc_entry.get()
        self.tasks[selected_index[0]].title = title
        self.tasks[selected_index[0]].description = description
        self.refresh_task_list()
        self.save_tasks()
        self.master.focus_set()

    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            del self.tasks[selected_index[0]]
            self.refresh_task_list()
            self.save_tasks()

    def mark_complete(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            self.tasks[selected_index[0]].completed = True
            self.refresh_task_list()
            self.save_tasks()

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "[X]" if task.completed else "[ ]"
            self.task_listbox.insert(tk.END, f"{status} {task.title}")

    def load_tasks(self):
        try:
            with open("tasks.pkl", "rb") as file:
                self.tasks = pickle.load(file)
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self):
        with open("tasks.pkl", "wb") as file:
            pickle.dump(self.tasks, file)

    def save_and_exit(self):
        self.save_tasks()
        self.master.destroy()

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
