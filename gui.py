import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from main import main as process_video
import os

class FootballAnalysisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Football Analysis System")
        self.root.geometry("600x400")
        
        # Configuration
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.processing = False

        # Create GUI elements
        self.create_widgets()
        
        # Set default output path
        self.output_path.set(os.path.abspath('output_videos/output_video.avi'))

    def create_widgets(self):
        # Input Section
        input_frame = ttk.LabelFrame(self.root, text="Input Video")
        input_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(input_frame, text="Source File:").grid(row=0, column=0, padx=5)
        ttk.Entry(input_frame, textvariable=self.input_path, width=50).grid(row=0, column=1)
        ttk.Button(input_frame, text="Browse", command=self.browse_input).grid(row=0, column=2, padx=5)

        # Output Section
        output_frame = ttk.LabelFrame(self.root, text="Output Video")
        output_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(output_frame, text="Output Path:").grid(row=0, column=0, padx=5)
        ttk.Entry(output_frame, textvariable=self.output_path, width=50).grid(row=0, column=1)
        ttk.Button(output_frame, text="Change", command=self.browse_output).grid(row=0, column=2, padx=5)

        # Control Section
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=20)

        self.process_btn = ttk.Button(
            control_frame, 
            text="Start Processing", 
            command=self.start_processing
        )
        self.process_btn.pack(side=tk.LEFT, padx=5)

        self.open_btn = ttk.Button(
            control_frame, 
            text="View Output", 
            command=self.open_output,
            state=tk.DISABLED
        )
        self.open_btn.pack(side=tk.LEFT, padx=5)

        # Status Label
        self.status_label = ttk.Label(self.root, text="Ready")
        self.status_label.pack(pady=10)

    def browse_input(self):
        filetypes = [
            ('Video Files', '*.mp4 *.avi *.mov'),
            ('All files', '*.*')
        ]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.input_path.set(filename)
            self.open_btn.config(state=tk.DISABLED)

    def browse_output(self):
        initial_file = os.path.basename(self.output_path.get())
        filename = filedialog.asksaveasfilename(
            defaultextension=".avi",
            filetypes=[('AVI files', '*.avi')],
            initialfile=initial_file
        )
        if filename:
            self.output_path.set(filename)

    def start_processing(self):
        if not self.input_path.get():
            messagebox.showerror("Error", "Please select an input video file")
            return

        if not os.path.exists(self.input_path.get()):
            messagebox.showerror("Error", "Input file does not exist")
            return

        # Disable buttons during processing
        self.process_btn.config(state=tk.DISABLED)
        self.open_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Processing...")

        # Start processing in a separate thread
        processing_thread = threading.Thread(
            target=self.run_analysis_pipeline,
            daemon=True
        )
        processing_thread.start()

    def run_analysis_pipeline(self):
        try:
            # Create output directory if it doesn't exist
            output_dir = os.path.dirname(self.output_path.get())
            os.makedirs(output_dir, exist_ok=True)

            # Run your video processing pipeline
            process_video(
                input_path=self.input_path.get(),
                output_path=self.output_path.get()
            )

            # Update UI on success
            self.root.after(0, self.on_processing_success)

        except Exception as e:
            self.root.after(0, self.on_processing_error, str(e))

    def on_processing_success(self):
        self.process_btn.config(state=tk.NORMAL)
        self.open_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Processing Complete")
        messagebox.showinfo("Success", "Video processing completed successfully!")

    def on_processing_error(self, error_msg):
        self.process_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Ready")
        messagebox.showerror("Processing Error", f"An error occurred:\n{error_msg}")

    def open_output(self):
        output_file = self.output_path.get()
        if os.path.exists(output_file):
            os.startfile(output_file)
        else:
            messagebox.showerror("Error", "Output file not found")

def main():
    root = tk.Tk()
    app = FootballAnalysisGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()