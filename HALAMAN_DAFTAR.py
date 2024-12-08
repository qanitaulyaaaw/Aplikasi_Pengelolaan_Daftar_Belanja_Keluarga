import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os

class AplikasiDaftar:
    def __init__(self, root, app_login):
        self.root = root
        self.app_login = app_login  
        self.root.title("Pendaftaran")
        self.root.geometry("1960x1080")  
        self.users = app_login.users  

    
        self.tampilan_daftar()

    def tampilan_daftar(self):
        """Tampilan pendaftaran"""
        for widget in self.root.winfo_children():
            widget.destroy()

        daftar_image_path = "background daftar.jpg"

        if os.path.exists(daftar_image_path):
            image = Image.open(daftar_image_path)
            image = image.resize((self.root.winfo_width(), self.root.winfo_height()), Image.LANCZOS) 
            bg_image = ImageTk.PhotoImage(image)

            bg_label = tk.Label(self.root, image=bg_image)
            bg_label.image = bg_image  
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)  

        else:
            messagebox.showerror("Error", "File gambar tidak ditemukan!")

        frame = tk.Frame(self.root, bg="#ffffff", bd=2)
        frame.place(relx=0.5, rely=0.5, anchor="center")

    
        nama_entry = tk.Entry(self.root, width=50, bg="#ffc5bb")
        nama_entry.pack(pady=(295, 10))

        username_entry = tk.Entry(self.root, width=50, bg="#ffc5bb")
        username_entry.pack(pady=(35, 10))

        email_entry = tk.Entry(self.root, width=50, bg="#ffc5bb")
        email_entry.pack(pady=(40, 15))

        password_entry = tk.Entry(self.root, show="*", width=50, bg="#ffc5bb")
        password_entry.pack(pady=(35, 15))

        def proses_daftar():
            nama = nama_entry.get()
            username = username_entry.get()
            email = email_entry.get()
            password = password_entry.get()

            if not (nama and username and email and password):
                messagebox.showerror("Kesalahan", "Semua kolom harus diisi!")
                return

            if username in self.users:
                messagebox.showerror("Kesalahan", "Username sudah ada!")
                return

            self.users[username] = {
                'nama': nama,
                'email': email,
                'password': password
            }
            self.app_login.save_users()  
          
            messagebox.showinfo("Berhasil", "Akun berhasil dibuat! Silakan login.")

            self.app_login.tampilan_login()

        tk.Button(self.root, text="Daftar", command=proses_daftar, width=20, height=2, bg="#b3f9ff").pack(pady=10)

        def kembali_ke_login():
            """Fungsi untuk kembali ke tampilan login"""
            self.app_login.tampilan_login()

        tk.Button(self.root, text="Kembali", command=kembali_ke_login, width=20, height=2, bg="#f08080").pack(pady=10)
