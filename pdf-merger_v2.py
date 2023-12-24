import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QFileDialog
import fitz  # PyMuPDF

class PDFMergerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("PDF Merger")

        # Heading Label
        heading_label = QLabel("PDF Merger")
        heading_label.setStyleSheet("font-size: 16pt; font-weight: bold;")

        # PDF Listbox
        self.pdf_listbox = QListWidget()
        self.pdf_listbox.setSelectionMode(QListWidget.MultiSelection)

        # Browse Button
        browse_button = QPushButton("Add PDF")
        browse_button.clicked.connect(self.browse_pdf)

        # Move Up Button
        move_up_button = QPushButton("Move Up")
        move_up_button.clicked.connect(self.move_item_up)

        # Move Down Button
        move_down_button = QPushButton("Move Down")
        move_down_button.clicked.connect(self.move_item_down)

        # Merge Button
        self.merge_button = QPushButton("Merge PDFs")
        self.merge_button.clicked.connect(self.merge)
        self.merge_button.setStyleSheet("background-color: green; color: white;")
        self.merge_button.setEnabled(False)  # Initially disabled

        # Reset Button
        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset)
        reset_button.setStyleSheet("background-color: gray; color: white;")

        # Result Label
        self.result_label = QLabel()

        # Layout
        vbox = QVBoxLayout()
        vbox.addWidget(heading_label)
        vbox.addWidget(self.pdf_listbox)

        hbox_buttons = QHBoxLayout()
        hbox_buttons.addWidget(browse_button)
        hbox_buttons.addWidget(move_up_button)
        hbox_buttons.addWidget(move_down_button)
        hbox_buttons.addWidget(self.merge_button)
        hbox_buttons.addWidget(reset_button)
        vbox.addLayout(hbox_buttons)

        vbox.addWidget(self.result_label)
        self.setLayout(vbox)

    def browse_pdf(self):
        file_dialog = QFileDialog()
        file_paths, _ = file_dialog.getOpenFileNames(self, "Select PDF files", "", "PDF files (*.pdf)")
        if file_paths:
            self.pdf_listbox.addItems(file_paths)
            self.merge_button.setEnabled(True)  # Enable the button when PDFs are added

    def move_item_up(self):
        current_row = self.pdf_listbox.currentRow()
        if current_row > 0:
            item = self.pdf_listbox.takeItem(current_row)
            self.pdf_listbox.insertItem(current_row - 1, item)
            self.pdf_listbox.setCurrentRow(current_row - 1)

    def move_item_down(self):
        current_row = self.pdf_listbox.currentRow()
        if current_row < self.pdf_listbox.count() - 1:
            item = self.pdf_listbox.takeItem(current_row)
            self.pdf_listbox.insertItem(current_row + 1, item)
            self.pdf_listbox.setCurrentRow(current_row + 1)

    def merge(self):
        input_pdfs = [self.pdf_listbox.item(i).text() for i in range(self.pdf_listbox.count())]
        output_pdf, _ = QFileDialog.getSaveFileName(self, "Save Merged PDF", "", "PDF files (*.pdf)")

        if input_pdfs and output_pdf:
            self.merge_pdfs(input_pdfs, output_pdf)

    def merge_pdfs(self, input_pdfs, output_pdf):
        pdf_document = fitz.open()

        try:
            for pdf_path in input_pdfs:
                pdf_document.insert_pdf(fitz.open(pdf_path))

            pdf_document.save(output_pdf)
            self.result_label.setText(f'Merged PDFs successfully. Result saved to: {output_pdf}')
            self.result_label.setStyleSheet("color: green;")

        except Exception as e:
            self.result_label.setText(f'Error: {e}')
            self.result_label.setStyleSheet("color: red;")

        finally:
            pdf_document.close()

    def reset(self):
        self.pdf_listbox.clear()
        self.result_label.clear()
        self.merge_button.setEnabled(False)  # Disable the button after reset

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pdf_merger_app = PDFMergerApp()
    pdf_merger_app.show()
    # sys.exit(app.exec_()) 
