import tkinter as tk
from tkinter import ttk

class DBDHookDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DBD Hook Detector")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        # Create a frame for controls
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)

        # Start Button
        self.start_button = ttk.Button(control_frame, text="Start Detection", command=self.start_detection)
        self.start_button.pack(side=tk.LEFT, padx=5)

        # Stop Button
        self.stop_button = ttk.Button(control_frame, text="Stop Detection", command=self.stop_detection, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Separator
        separator = ttk.Separator(self.root, orient='horizontal')
        separator.pack(fill=tk.X, pady=10)

        # Create a frame for displaying hook counts
        display_frame = ttk.Frame(self.root, padding="10")
        display_frame.pack(fill=tk.BOTH, expand=True)

        # Labels for each survivor
        self.survivors = ["Survivor 1", "Survivor 2", "Survivor 3", "Survivor 4"]
        self.hook_counts = {survivor: 0 for survivor in self.survivors}
        self.label_vars = {}

        for i, survivor in enumerate(self.survivors):
            label = ttk.Label(display_frame, text=survivor)
            label.grid(row=i, column=0, sticky=tk.W, pady=5)

            count_var = tk.StringVar(value="Hooks: 0")
            count_label = ttk.Label(display_frame, textvariable=count_var)
            count_label.grid(row=i, column=1, sticky=tk.E, pady=5)

            self.label_vars[survivor] = count_var

    def start_detection(self):
        # Placeholder for starting the detection process
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        print("Detection started.")

    def stop_detection(self):
        # Placeholder for stopping the detection process
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        print("Detection stopped.")

def main():
    root = tk.Tk()
    app = DBDHookDetectorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()