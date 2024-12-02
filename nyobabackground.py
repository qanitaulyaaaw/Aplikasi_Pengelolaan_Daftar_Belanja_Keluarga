import tkinter as tk
from PIL import Image, ImageTk
import os

# Membuat jendela utama
root = tk.Tk()
root.title("Background dari Gambar")
root.geometry("400x500")

# Membuka gambar dari file
background_image = Image.open(r"C:\Users\Lenovo\Desktop\latihan vscode\background.jpg")
background_photo = ImageTk.PhotoImage(background_image)

# Menambahkan gambar sebagai background
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)  # Mengisi seluruh area

# Menambahkan teks di atas background
label = tk.Label(root, text="Selamat Datang!", font=("Arial", 24), bg="white", fg="black")
label.pack(pady=50)

root.mainloop()
