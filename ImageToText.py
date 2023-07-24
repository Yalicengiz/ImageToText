from smtplib import SMTP_SSL_PORT
import pytesseract
from PIL import Image, ImageTk
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.scrolledtext as scrolledtext
import pyperclip
from tkinter import filedialog
from tkinter import messagebox

__author__ = "Yalicengiz"
__date__ = "2023-07-14"

# Extend ttk.Combobox to open dropdown when clicked
class CustomCombobox(ttk.Combobox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bind the button click event
        self.bind("<Button-1>", self.popup)

    def popup(self, event):
        # Generate dropdown event
        self.event_generate("<Down>")


class App:
    def __init__(self, window):
        # Specify Tesseract OCR path
        pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

        # Get Tesseract supported languages
        self.tesseract_languages = pytesseract.get_languages(config='')
        # Capitalize each language for a cleaner look
        self.tesseract_languages = [lang.capitalize() for lang in self.tesseract_languages]
        # Add default option to the languages list
        self.languages = ["Select a Language"] + self.tesseract_languages

        # Create main window
        self.window = window
        self.window.title("Screenshot OCR")
        self.frame = tk.Frame(window)
        self.frame.pack(padx=10, pady=10)

        # Language selection dropdown menu
        self.lang_option = tk.StringVar(window)
        # Set default language
        self.lang_option.set(self.languages[0])
        self.language_selector = CustomCombobox(self.frame, textvariable=self.lang_option, values=self.languages, width=30)
        self.language_selector.bind("<FocusIn>", self.language_selector_clicked)
        self.language_selector.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="w")

        # Screenshot upload button
        self.upload_screenshot_button = tk.Button(self.frame, text="Load Screenshot", command=self.load_screenshot, width=30)
        self.upload_screenshot_button.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="w")

        # Create the second window (hidden initially)
        self.text_window = tk.Toplevel(window)
        self.text_window.title("OCR Text")
        self.text_window.geometry("+{}+{}".format(window.winfo_x(), window.winfo_y()))
        self.text_window.withdraw()

        # Text area and scrollbar for text display
        self.text_field = scrolledtext.ScrolledText(self.text_window, width=70, height=30, font=("Helvetica", 16))
        self.text_field.pack(padx=10, pady=10, fill="both", expand=True)

        # Text copy button
        self.copy_button = tk.Button(self.text_window, text="Copy Text", command=self.copy_text)
        self.copy_button.pack(padx=10, pady=10, fill="x")

        # Screenshot label
        self.screenshot_label = tk.Label(window)
        self.screenshot_label.pack(padx=10, pady=10, fill="x")

    def load_screenshot(self):
        # Get selected language
        tesseract_lang = self.lang_option.get()

        # Check if a language has been selected
        if tesseract_lang == "Select a Language" or tesseract_lang == "Click Here to Select a Language":
            messagebox.showinfo("Error", "Please select a language.")
            self.lang_option.set("Click Here to Select a Language")
            return

        # Open file dialog to select a screenshot
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
        if file_path:
            # Load the screenshot and display it
            image = Image.open(file_path)
            img = ImageTk.PhotoImage(image)
            self.screenshot_label.configure(image=img)
            self.screenshot_label.image = img
            # Extract text from the screenshot
            self.extract_text(image, tesseract_lang)

    def extract_text(self, image, tesseract_lang):
        # Perform OCR on the screenshot
        text = pytesseract.image_to_string(image, lang=tesseract_lang)
        # Display the extracted text
        self.text_field.delete(1.0, tk.END)
        self.text_field.insert(tk.END, text)
        # Show the text window if it's hidden
        if not self.text_window.winfo_viewable():
            self.text_window.deiconify()

    def copy_text(self):
        # Get the text from the text field
        text = self.text_field.get(1.0, tk.END)
        # Copy the text to the clipboard
        pyperclip.copy(text)

    def language_selector_clicked(self, event):
        # Set the first real language as selected when the dropdown is clicked while the default option is active
        if self.lang_option.get() == "Select a Language" or self.lang_option.get() == "Click Here to Select a Language":
            self.lang_option.set(self.languages[1])


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
