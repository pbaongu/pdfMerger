import PyPDF2
import tkinter as tk
from tkinter import filedialog

def merge_pdfs(input_pdfs, output_pdf):
    merger = PyPDF2.PdfMerger()

    try:
        for pdf in input_pdfs:
            merger.append(pdf)

        merger.write(output_pdf)
        result_label.config(text=f'Merged PDFs successfully. Result saved to: {output_pdf}', fg='green')

    except Exception as e:
        result_label.config(text=f'Error: {e}', fg='red')

    finally:
        merger.close()

def browse_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        pdf_listbox.insert(tk.END, file_path)

def merge():
    input_pdfs = pdf_listbox.get(0, tk.END)
    output_pdf = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

    if input_pdfs and output_pdf:
        merge_pdfs(input_pdfs, output_pdf)

def reset():
    pdf_listbox.delete(0, tk.END)
    result_label.config(text="", fg='black')

# Tkinter GUI setup
root = tk.Tk()
root.title("PDF Merger")

# Heading Label
heading_label = tk.Label(root, text="PDF Merger", font=("Helvetica", 16, "bold"))
heading_label.pack(pady=10)

# PDF Listbox
pdf_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=5, width=50)
pdf_listbox.pack(pady=10)

# Browse Button
browse_button = tk.Button(root, text="Add PDF", command=browse_pdf)
browse_button.pack()

# Merge Button
merge_button = tk.Button(root, text="Merge PDFs", command=merge, bg='green', fg='white', padx=10, pady=5)
merge_button.pack(pady=10)

# Reset Button
reset_button = tk.Button(root, text="Reset", command=reset, bg='gray', fg='white', padx=10, pady=5)
reset_button.pack(pady=10)

# Result Label
result_label = tk.Label(root, text="", fg='black')
result_label.pack()

# Run the Tkinter event loop
root.mainloop()
