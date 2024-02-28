import tkinter as tk
from tkinter import ttk
import time

class PomodoroTimer:
    def __init__(self, master):
        self.master = master
        self.master.title("Pomodoro Timer")
        
        self.style = ttk.Style()
        self.style.theme_create("velvet", parent="clam", settings={
            "TButton": {
                "configure": {"background": "#313866", "foreground": "white", "font": ("Helvetica", 12)},
                "map": {"background": [("active", "#50409A")],
                        "foreground": [("active", "white")],
                        "relief": [("active", "flat")]}
            },
            "TLabel": {
                "configure": {"foreground": "white", "background": "#313866", "font": ("Helvetica", 48)}
            }
        })
        self.style.theme_use("velvet")

        self.minutes = 25
        self.seconds = 0
        self.is_running = False

        self.label = ttk.Label(master, text=f"{self.minutes:02}:{self.seconds:02}")
        self.label.pack(pady=20)

        self.start_button = ttk.Button(master, text="Start", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.pause_button = ttk.Button(master, text="Pause", command=self.pause_timer, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = ttk.Button(master, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        self.set_time_button = ttk.Button(master, text="Set Time", command=self.set_time_limit)
        self.set_time_button.pack(side=tk.LEFT, padx=10)

        self.timer_id = None

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.update_timer()

    def update_timer(self):
        if self.minutes == 0 and self.seconds == 0:
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            return

        if self.seconds == 0:
            self.minutes -= 1
            self.seconds = 59
        else:
            self.seconds -= 1

        self.label.config(text=f"{self.minutes:02}:{self.seconds:02}")
        self.timer_id = self.master.after(1000, self.update_timer)

    def pause_timer(self):
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        if self.timer_id:
            self.master.after_cancel(self.timer_id)

    def reset_timer(self):
        self.is_running = False
        self.minutes = 25
        self.seconds = 0
        self.label.config(text=f"{self.minutes:02}:{self.seconds:02}")
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        if self.timer_id:
            self.master.after_cancel(self.timer_id)

    def set_time_limit(self):
        self.pause_timer()  # Pause timer before setting new time

        popup = tk.Toplevel()
        popup.title("Set Time Limit")

        label = tk.Label(popup, text="Enter time limit (minutes):")
        label.pack(pady=10)

        entry = tk.Entry(popup)
        entry.pack(pady=10)

        confirm_button = ttk.Button(popup, text="Set", command=lambda: self.confirm_time_limit(popup, entry.get()))
        confirm_button.pack(pady=10)

    def confirm_time_limit(self, popup, time_limit):
        try:
            self.minutes = int(time_limit)
            self.seconds = 0
            self.update_display()
            popup.destroy()
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter a valid integer.")

    def update_display(self):
        self.label.config(text=f"{self.minutes:02}:{self.seconds:02}")

def main():
    root = tk.Tk()
    root.configure(bg="#313866")
    timer = PomodoroTimer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
