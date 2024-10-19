import tkinter as tk
from tkinter import ttk
import threading
import time
import pyautogui
from PIL import Image
import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

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

        # Initialize threading variables
        self.running = False
        self.thread = None
        self.screenshot_interval = 5  # seconds
        self.screenshot_folder = "screenshots"

        # Create screenshot folder if it doesn't exist
        if not os.path.exists(self.screenshot_folder):
            os.makedirs(self.screenshot_folder)

        # Define survivor icon regions (replace with your actual coordinates)
        self.survivor_regions = {
            "Survivor 1": (80, 410, 95, 80),
            "Survivor 2": (80, 505, 95, 80),
            "Survivor 3": (80, 590, 95, 80),
            "Survivor 4": (80, 675, 95, 80),
        }

        # Load hooked state templates
        self.hooked_templates = {}
        template_folder = "hooked_templates"
        for survivor in self.survivors:
            template_path = os.path.join(template_folder, f"{survivor.lower().replace(' ', '')}_hooked.png")
            if os.path.exists(template_path):
                template_image = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
                self.hooked_templates[survivor] = template_image
            else:
                print(f"Template for {survivor} not found at {template_path}")

        # To avoid counting the same hook multiple times
        self.previous_hook_states = {survivor: False for survivor in self.survivors}

        # Threshold for template matching
        self.threshold = 0.8  # You may need to fine-tune this value

    def start_detection(self):
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.thread = threading.Thread(target=self.capture_and_analyze_screenshots, daemon=True)
        self.thread.start()
        print("Detection started.")

    def stop_detection(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        print("Detection stopped.")

    def capture_and_analyze_screenshots(self):
        while self.running:
            screenshot = pyautogui.screenshot()
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            for survivor, region in self.survivor_regions.items():
                x, y, w, h = region
                survivor_img = screenshot_cv[y:y+h, x:x+w]
                
                template = self.hooked_templates.get(survivor)
                if template is not None:
                    # Resize survivor_img to match template size
                    survivor_img_resized = cv2.resize(survivor_img, (template.shape[1], template.shape[0]))
                    
                    # Convert both images to grayscale
                    survivor_gray = cv2.cvtColor(survivor_img_resized, cv2.COLOR_BGR2GRAY)
                    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
                    
                    # Compute SSIM between the two images
                    similarity, _ = ssim(survivor_gray, template_gray, full=True)
                    print(f"{survivor} - Similarity: {similarity:.4f}")

                    hooked = similarity >= self.threshold
                    if hooked and not self.previous_hook_states[survivor]:
                        self.hook_counts[survivor] += 1
                        self.label_vars[survivor].set(f"Hooks: {self.hook_counts[survivor]}")
                        print(f"{survivor} has been hooked! Total hooks: {self.hook_counts[survivor]}")
                    
                    self.previous_hook_states[survivor] = hooked

                    # Debug: Save images for inspection
                    self.save_debug_images(survivor, survivor_img_resized, similarity)

            time.sleep(self.screenshot_interval)

    def save_debug_images(self, survivor, survivor_img, similarity):
        debug_folder = "debug_images"
        if not os.path.exists(debug_folder):
            os.makedirs(debug_folder)
        
        cv2.imwrite(os.path.join(debug_folder, f"{survivor}_region.png"), survivor_img)
        cv2.imwrite(os.path.join(debug_folder, f"{survivor}_similarity_{similarity:.4f}.png"), survivor_img)

def main():
    root = tk.Tk()
    app = DBDHookDetectorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()