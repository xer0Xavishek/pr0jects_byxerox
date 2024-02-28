import tkinter as tk
from tkinter import ttk
from datetime import datetime

class TodoListApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Modern Todo List")
        self.master.geometry("400x300")
        self.master.configure(bg="#313866")

        self.style = ttk.Style()
        self.style.theme_use("clam")  # Use clam theme as base
        self.style.configure("Treeview", background="#313866", fieldbackground="#313866", foreground="white", font=("Helvetica", 12))
        self.style.map("Treeview", background=[('selected', '#964EC2')])

        self.todo_list = ttk.Treeview(master, columns=("Task", "Date"), selectmode="browse")
        self.todo_list.heading("#0", text="", anchor=tk.CENTER)
        self.todo_list.column("#0", width=30)
        self.todo_list.heading("Task", text="Task", anchor=tk.W)
        self.todo_list.column("Task", width=250)
        self.todo_list.heading("Date", text="Date", anchor=tk.W)
        self.todo_list.column("Date", width=120)
        self.todo_list.pack(pady=10)

        self.add_button = ttk.Button(master, text="Add Task", command=self.open_add_task_window)
        self.add_button.pack(pady=5)

        self.remove_button = ttk.Button(master, text="Remove Task", command=self.remove_task)
        self.remove_button.pack(pady=5)

        self.todo_tasks = {}

        # Bind double-click event to mark task as completed
        self.todo_list.bind("<Double-1>", self.mark_task_as_completed)

    def open_add_task_window(self):
        add_task_window = tk.Toplevel(self.master)
        add_task_window.title("Add Task")
        add_task_window.configure(bg="#313866")

        label = ttk.Label(add_task_window, text="Enter task name:", background="#313866", foreground="white")
        label.pack(pady=5)

        self.task_entry = ttk.Entry(add_task_window, font=("Helvetica", 12))
        self.task_entry.pack(pady=5)

        add_button = ttk.Button(add_task_window, text="Add", command=self.add_task)
        add_button.pack(pady=5)

    def add_task(self):
        task_name = self.task_entry.get().strip()
        if task_name:
            today = datetime.today().strftime('%Y-%m-%d')
            self.todo_tasks[task_name] = today
            self.todo_list.insert("", "end", text="", values=(task_name, today))
            self.task_entry.delete(0, tk.END)

    def remove_task(self):
        selected_item = self.todo_list.selection()
        if selected_item:
            task_name = self.todo_list.item(selected_item, "values")[0]
            del self.todo_tasks[task_name]
            self.todo_list.delete(selected_item)
    def mark_task_as_completed(self, event):
        item = self.todo_list.selection()[0]
        task_name = self.todo_list.item(item, "values")[0]
        self.todo_list.item(item, tags=("completed",))
        self.todo_list.tag_configure("completed", foreground="gray")
        completed_text = task_name + " (Completed)"
        self.todo_list.item(item, values=(completed_text, self.todo_tasks[task_name]))


def main():
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
