import tkinter as tk
from tkinter import ttk, messagebox

def caesar_cipher(text, shift, mode='encrypt'):
    result = ""
    shift = shift if mode == 'encrypt' else -shift
    for char in text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

def vigenere_cipher(text, key, mode='encrypt'):
    result = ""
    key = key.lower()
    key_len = len(key)
    for i, char in enumerate(text):
        if char.isalpha():
            shift = ord(key[i % key_len]) - 97
            if mode == 'decrypt':
                shift = -shift
            shift_base = 65 if char.isupper() else 97
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

def generate_playfair_matrix(key):
    key = "".join(dict.fromkeys(key.replace("J", "I")))
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    matrix = []
    used = set(key)
    key += "".join(letter for letter in alphabet if letter not in used)
    for i in range(0, 25, 5):
        matrix.append(key[i:i + 5])
    return matrix

def find_positions(matrix, char):
    for i, row in enumerate(matrix):
        if char in row:
            return i, row.index(char)

def playfair_cipher(text, key, mode='encrypt'):
    matrix = generate_playfair_matrix(key.upper())
    text = text.upper().replace("J", "I").replace(" ", "")
    if len(text) % 2 != 0:
        text += "X"
    result = ""
    step = 1 if mode == 'encrypt' else -1
    for i in range(0, len(text), 2):
        a, b = text[i], text[i + 1]
        row_a, col_a = find_positions(matrix, a)
        row_b, col_b = find_positions(matrix, b)
        if row_a == row_b:
            result += matrix[row_a][(col_a + step) % 5]
            result += matrix[row_b][(col_b + step) % 5]
        elif col_a == col_b:
            result += matrix[(row_a + step) % 5][col_a]
            result += matrix[(row_b + step) % 5][col_b]
        else:
            result += matrix[row_a][col_b]
            result += matrix[row_b][col_a]
    return result

def encrypt_or_decrypt():
    cipher = cipher_choice.get()
    mode = mode_choice.get()
    text = input_text.get("1.0", tk.END).strip()
    key = key_entry.get().strip()

    if not text:
        messagebox.showwarning("Warning", "Please enter text.")
        return

    if cipher == "Caesar":
        try:
            shift = int(key)
        except ValueError:
            messagebox.showwarning("Warning", "Caesar cipher requires a numeric key.")
            return
        result = caesar_cipher(text, shift, mode)
    elif cipher == "Vigenère":
        if not key.isalpha():
            messagebox.showwarning("Warning", "Vigenère cipher requires an alphabetic key.")
            return
        result = vigenere_cipher(text, key, mode)
    elif cipher == "Playfair":
        if not key.isalpha():
            messagebox.showwarning("Warning", "Playfair cipher requires an alphabetic key.")
            return
        result = playfair_cipher(text, key, mode)

    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)
    output_text.config(state=tk.DISABLED)

def update_key_visibility(*args):
    cipher = cipher_choice.get()
    if cipher == "Caesar":
        key_label.config(text="Shift:")
        key_entry.pack(side=tk.LEFT, padx=5)
    elif cipher == "Vigenère" or cipher == "Playfair":
        key_label.config(text="Key:")
        key_entry.pack(side=tk.LEFT, padx=5)

root = tk.Tk()
root.title("Text Encryption App")
root.geometry("400x400")

cipher_choice = tk.StringVar(value="Caesar")
mode_choice = tk.StringVar(value="encrypt")

# Cipher selection
ttk.Label(root, text="Select Cipher:").pack(pady=5)
cipher_menu = ttk.Combobox(root, textvariable=cipher_choice, values=["Caesar", "Vigenère", "Playfair"], state="readonly")
cipher_menu.pack(pady=5)
cipher_choice.trace_add('write', update_key_visibility)

# Mode selection
mode_frame = ttk.Frame(root)
mode_frame.pack(pady=5)
ttk.Radiobutton(mode_frame, text="Encrypt", variable=mode_choice, value="encrypt").pack(side=tk.LEFT, padx=10)
ttk.Radiobutton(mode_frame, text="Decrypt", variable=mode_choice, value="decrypt").pack(side=tk.LEFT, padx=10)

# Text input
ttk.Label(root, text="Input Text:").pack(pady=5)
input_text = tk.Text(root, height=5, width=40)
input_text.pack(pady=5)

# Key input
key_frame = ttk.Frame(root)
key_frame.pack(pady=5)
key_label = ttk.Label(key_frame, text="Key:")
key_label.pack(side=tk.LEFT)
key_entry = ttk.Entry(key_frame, width=20)
key_entry.pack(side=tk.LEFT, padx=5)

# Output
ttk.Label(root, text="Output:").pack(pady=5)
output_text = tk.Text(root, height=5, width=40, state=tk.DISABLED)
output_text.pack(pady=5)

# Buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)
encrypt_button = ttk.Button(button_frame, text="Process", command=encrypt_or_decrypt)
encrypt_button.pack(side=tk.LEFT, padx=5)
clear_button = ttk.Button(button_frame, text="Clear", command=lambda: input_text.delete("1.0", tk.END))
clear_button.pack(side=tk.LEFT, padx=5)

update_key_visibility()
root.mainloop()
