import tkinter as tk
import time

class PomodoroTimer:
    def __init__(self, master):
        self.master = master
        self.master.title("Pomodoro Timer")
        self.master.configure(bg="black")

        self.minutes = 25
        self.seconds = 0
        self.is_running = False

        self.label = tk.Label(master, text=f"{self.minutes:02}:{self.seconds:02}", font=("Helvetica", 48), fg="white", bg="black")
        self.label.pack(pady=20)

        self.start_button = tk.Button(master, text="Start", command=self.start_timer, bg="black", fg="white")
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.pause_button = tk.Button(master, text="Pause", command=self.pause_timer, state=tk.DISABLED, bg="black", fg="white")
        self.pause_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(master, text="Reset", command=self.reset_timer, bg="black", fg="white")
        self.reset_button.pack(side=tk.LEFT, padx=10)

        self.set_time_button = tk.Button(master, text="Set Time", command=self.set_time_limit, bg="black", fg="white")
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
        popup.configure(bg="black")

        label = tk.Label(popup, text="Enter time limit (minutes):", fg="white", bg="black")
        label.pack(pady=10)

        entry = tk.Entry(popup)
        entry.pack(pady=10)

        confirm_button = tk.Button(popup, text="Set", command=lambda: self.confirm_time_limit(popup, entry.get()), bg="black", fg="white")
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
    root.configure(bg="black")
    timer = PomodoroTimer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
