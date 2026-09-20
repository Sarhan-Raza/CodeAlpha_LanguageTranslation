import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator
from langdetect import detect

# Language names and codes
language_codes = {
    "Auto Detect": "auto",
    "English": "en",
    "Urdu": "ur",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Arabic": "ar",
    "Hindi": "hi",
    "Chinese": "zh-CN",
    "Japanese": "ja",
    "Korean": "ko",
    "Russian": "ru",
    "Italian": "it",
    "Turkish": "tr",
    "Portuguese": "pt"
}

# Reverse lookup dictionary
code_to_name = {v.lower(): k for k, v in language_codes.items() if v != "auto"}


def translate_text():
    try:
        text = input_text.get("1.0", tk.END).strip()

        if not text:
            messagebox.showwarning("Warning", "Please enter some text.")
            return

        selected_source = language_codes[source_lang.get()]
        target = language_codes[target_lang.get()]

        # Detect language
        detected_code = detect(text)

        detected_language = code_to_name.get(
            detected_code.lower(),
            detected_code.upper()
        )

        # Use detected language if Auto Detect selected
        source = detected_code if selected_source == "auto" else selected_source

        translated_text = GoogleTranslator(
            source=source,
            target=target
        ).translate(text)

        detected_label.config(
            text=f"Detected Language: {detected_language}"
        )

        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated_text)

    except Exception as e:
        if "too many requests" in str(e).lower():
            messagebox.showerror(
                "Error",
                "Too many requests. Please wait for a few minutes and try again."
            )
        else:
            messagebox.showerror("Error", str(e))



def copy_translation():
    translated = output_text.get("1.0", tk.END).strip()

    if translated:
        root.clipboard_clear()
        root.clipboard_append(translated)
        messagebox.showinfo("Copied", "Translation copied to clipboard.")


# Main Window
root = tk.Tk()
root.title("AI Language Translation Tool")
root.geometry("750x650")
root.resizable(False, False)

# Title
title_label = tk.Label(
    root,
    text="AI Language Translation Tool",
    font=("Arial", 18, "bold")
)
title_label.pack(pady=10)

# Source Language
tk.Label(
    root,
    text="Source Language",
    font=("Arial", 11)
).pack()

source_lang = ttk.Combobox(
    root,
    values=list(language_codes.keys()),
    state="readonly",
    width=30
)
source_lang.pack(pady=5)
source_lang.set("Auto Detect")

# Target Language
tk.Label(
    root,
    text="Target Language",
    font=("Arial", 11)
).pack()

target_lang = ttk.Combobox(
    root,
    values=[lang for lang in language_codes.keys()
            if lang != "Auto Detect"],
    state="readonly",
    width=30
)
target_lang.pack(pady=5)
target_lang.set("Urdu")

# Input Label
tk.Label(
    root,
    text="Enter Text",
    font=("Arial", 11)
).pack(pady=(10, 0))

# Input Text Box
input_text = tk.Text(
    root,
    height=8,
    width=80,
    font=("Arial", 11)
)
input_text.pack(padx=10, pady=5)

# Translate Button
translate_btn = tk.Button(
    root,
    text="Translate",
    command=translate_text,
    width=20,
    font=("Arial", 11)
)
translate_btn.pack(pady=10)

translate_btn.config(state=tk.NORMAL)

#using enter key to translate text
input_text.bind("<Return>", lambda event: translate_text())

# Detected Language Label
detected_label = tk.Label(
    root,
    text="Detected Language: -",
    font=("Arial", 10, "italic")
)
detected_label.pack()

# Output Label
tk.Label(
    root,
    text="Translated Text",
    font=("Arial", 11)
).pack(pady=(10, 0))

# Output Text Box
output_text = tk.Text(
    root,
    height=8,
    width=80,
    font=("Arial", 11)
)
output_text.pack(padx=10, pady=5)

# Copy Button
copy_btn = tk.Button(
    root,
    text="Copy Translation",
    command=copy_translation,
    width=20,
    font=("Arial", 11)
)
copy_btn.pack(pady=10)

# Run Application
root.mainloop()