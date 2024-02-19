import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime, time, timedelta
import winsound
import threading

class AlarmClockApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Alarm Clock App")

        self.current_time_label = ttk.Label(master, text="")
        self.current_time_label.pack(pady=10)

        self.new_alarm_button = ttk.Button(master, text="Set New Alarm", command=self.open_new_alarm_window)
        self.new_alarm_button.pack(pady=5)

        self.alarms_frame = ttk.Frame(master)
        self.alarms_frame.pack(pady=10)

        self.alarms_label = ttk.Label(self.alarms_frame, text="Alarms:")
        self.alarms_label.grid(row=0, column=0, columnspan=2, pady=5)

        self.alarms = []
        self.load_alarms()
        self.refresh_alarm_list()

        self.refresh_time()
        self.update_current_time()

    def refresh_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.current_time_label.config(text=f"Current Time: {current_time}")
        self.master.after(1000, self.refresh_time)

    def update_current_time(self):
        current_time = datetime.now().time()
        for alarm in self.alarms:
            if alarm.enabled and alarm.time == current_time:
                threading.Thread(target=self.ring_alarm, args=(alarm,)).start()
        self.master.after(1000, self.update_current_time)

    def open_new_alarm_window(self):
        new_alarm_window = tk.Toplevel(self.master)
        new_alarm_window.title("Set New Alarm")

        time_label = ttk.Label(new_alarm_window, text="Alarm Time (HH:MM):")
        time_label.grid(row=0, column=0, padx=5, pady=5)
        self.time_entry = ttk.Entry(new_alarm_window)
        self.time_entry.grid(row=0, column=1, padx=5, pady=5)

        set_button = ttk.Button(new_alarm_window, text="Set Alarm", command=self.set_alarm)
        set_button.grid(row=1, column=0, columnspan=2, pady=5)

    def set_alarm(self):
        alarm_time_str = self.time_entry.get()
        try:
            alarm_time = datetime.strptime(alarm_time_str, "%H:%M").time()
        except ValueError:
            messagebox.showerror("Error", "Invalid time format. Please use HH:MM.")
            return

        new_alarm = Alarm(alarm_time)
        self.alarms.append(new_alarm)
        self.refresh_alarm_list()
        self.save_alarms()

    def refresh_alarm_list(self):
        for widget in self.alarms_frame.winfo_children():
            widget.destroy()

        for i, alarm in enumerate(self.alarms):
            alarm_label = ttk.Label(self.alarms_frame, text=f"{alarm.time.strftime('%H:%M')} {'(Enabled)' if alarm.enabled else '(Disabled)'}")
            alarm_label.grid(row=i+1, column=0, columnspan=2, pady=2)

            enable_disable_button = ttk.Button(self.alarms_frame, text="Disable" if alarm.enabled else "Enable", command=lambda alarm=alarm: self.toggle_alarm(alarm))
            enable_disable_button.grid(row=i+1, column=2, padx=5)

            delete_button = ttk.Button(self.alarms_frame, text="Delete", command=lambda alarm=alarm: self.delete_alarm(alarm))
            delete_button.grid(row=i+1, column=3, padx=5)

    def toggle_alarm(self, alarm):
        alarm.enabled = not alarm.enabled
        self.refresh_alarm_list()
        self.save_alarms()

    def delete_alarm(self, alarm):
        self.alarms.remove(alarm)
        self.refresh_alarm_list()
        self.save_alarms()

    def ring_alarm(self, alarm):
        winsound.Beep(1000000, 2000000)
        response = messagebox.askyesno("Alarm", f"It's time for your alarm set at {alarm.time.strftime('%H:%M')}. Do you want to snooze?")
        if response:
            # Snooze for 5 minutes
            alarm.time = (datetime.combine(datetime.today(), alarm.time) + timedelta(minutes=5)).time()
            threading.Thread(target=self.ring_alarm, args=(alarm,)).start()

    def load_alarms(self):
        # Load alarms from a file or database
        pass

    def save_alarms(self):
        # Save alarms to a file or database
        pass

class Alarm:
    def __init__(self, time, enabled=True):
        self.time = time
        self.enabled = enabled

def main():
    root = tk.Tk()
    app = AlarmClockApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
