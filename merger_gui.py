import os
import logging
import random
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PyPDF2 import PdfMerger


class PDFMergerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("PyDF Merger")
        self.master.geometry("600x400")
        self.master.resizable(False, False)

        # Colors
        bg_color = "#f0f0f0"
        btn_color = "#4CAF50"  # Green
        btn_hover_color = "#45a049"
        text_color = "black"  # Adjust text color as needed

        # Variables
        self.selected_files = []

        # Create GUI elements
        style = ttk.Style()

        # Configure style for buttons
        style.configure(
            "TButton",
            padding=(5, 5, 5, 5),
            font=("Helvetica", 12),
            background=btn_color,
            foreground=text_color,
        )
        style.map(
            "TButton",
            background=[("active", btn_hover_color), ("pressed", btn_hover_color)],
        )

        # Configure style for labels
        style.configure("TLabel", padding=(0, 5, 0, 5), font=("Helvetica", 12), background=bg_color, foreground=text_color)

        # Configure style for entry
        style.configure(
            "TEntry",
            padding=(5, 5, 5, 5),
            font=("Helvetica", 12),
            background="white",
            foreground="black",
        )

        # Configure style for listbox
        style.configure("TListbox", font=("Helvetica", 12), background="white", foreground="black")

        # Frame for padding and background color
        frame = ttk.Frame(self.master, style="TLabel")
        frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.file_listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, font=("Helvetica", 12))
        self.file_listbox.pack(expand=True, fill=tk.BOTH)

        self.add_button = ttk.Button(frame, text="Add PDFs", command=self.add_pdfs)
        self.add_button.pack(pady=10)

        self.output_label = ttk.Label(frame, text="Output PDF Name:")
        self.output_label.pack(pady=5)

        self.output_name = ttk.Entry(frame)
        self.output_name.pack(pady=5)

        self.merge_button = ttk.Button(frame, text="Merge PDFs", command=self.merge_pdfs)
        self.merge_button.pack(pady=10)

        # Configure logging
        self.log_filepath = ""
        logging.basicConfig(level=logging.ERROR)

    def add_pdfs(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        for file in files:
            self.file_listbox.insert(tk.END, file)
        self.selected_files = self.file_listbox.get(0, tk.END)

    def merge_pdfs(self):
        if not self.selected_files:
            messagebox.showwarning("Warning", "No PDFs selected.")
            return

        output_directory = filedialog.askdirectory()
        if not output_directory:
            messagebox.showwarning("Warning", "Output directory not specified.")
            return

        # Create the output directory if it doesn't exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Configure logging with an explicit log file path
        self.log_filepath = os.path.join(output_directory, "merged.log")
        logging.basicConfig(filename=self.log_filepath, level=logging.ERROR)

        user_provided_name = self.output_name.get().strip()
        if not user_provided_name:
            # Generate a random 5-digit number for the PDF name
            random_number = str(random.randint(10000, 99999))
            output_filename = f"{random_number}_merged.pdf"
        else:
            output_filename = f"{user_provided_name}.pdf"

        output_filepath = os.path.join(output_directory, output_filename)

        merger = PdfMerger()

        try:
            # Sort the selected PDF files
            self.selected_files = sorted(self.selected_files)

            for pdf_file in self.selected_files:
                merger.append(pdf_file)

            # Save the merged PDF
            merger.write(output_filepath)
            messagebox.showinfo("Success", f"Merged PDFs into '{output_filepath}'")

        except Exception as e:
            logging.error(f"An error occurred: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
