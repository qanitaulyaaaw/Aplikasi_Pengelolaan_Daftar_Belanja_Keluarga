import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os

# Pastikan file AplikasiBelanja sudah terimport dengan benar
from DAFTAR_BELANJA_BARU import AplikasiBelanja 
from HALAMAN_DAFTAR import AplikasiDaftar

class AplikasiBelanjaKeluarga:
    def __init__(self, root):
        self.root = root
        self.root.title("PlanIt")
        self.root.geometry("1960x1080")

        # Direktori untuk menyimpan data
        self.users_file = "users.json"
        self.shopping_lists_dir = "shopping_lists"

        # Pastikan direktori untuk menyimpan data ada
        if not os.path.exists(self.shopping_lists_dir):
            os.makedirs(self.shopping_lists_dir)

        # Inisialisasi data pengguna
        self.users = self.load_users()

        # Inisialisasi pengguna saat ini
        self.pengguna_saat_ini = None

        # Tampilan awal (Selamat Datang)
        self.tampilan_selamat_datang()

    def load_users(self):
        """Memuat data pengguna dari file JSON"""
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                return json.load(f)
        return {}

    def save_users(self):
        """Menyimpan data pengguna ke file JSON"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)

    def tampilan_selamat_datang(self):
        """Tampilan selamat datang"""
        for widget in self.root.winfo_children():
            widget.destroy() 

        welcome_image_path = "background welcome.jpg"

        # Load gambar JPG
        if os.path.exists(welcome_image_path):
            image = Image.open(welcome_image_path)
            image = image.resize((self.root.winfo_width(), self.root.winfo_height()), Image.LANCZOS)
            bg_image = ImageTk.PhotoImage(image)

            # Label untuk background
            bg_label = tk.Label(self.root, image=bg_image)
            bg_label.image = bg_image
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Tombol Login
        tk.Button(self.root, text="Login", font=("Times New Roman", 15), bg="#006989", fg="#f3f7ec", command=self.tampilan_login, width=20, height=2).pack(pady=(400, 10))
        # Tombol Daftar
        tk.Button(self.root, text="Daftar", font=("Times New Roman", 15), bg="#006989", fg="#f3f7ec", command=self.tampilan_daftar, width=20, height=2).pack(pady=(50, 130))

    def tampilan_login(self):
        """Tampilan login"""
        for widget in self.root.winfo_children():
            widget.destroy()

        login_image_path = "background login.jpg"

        # Load gambar JPG
        if os.path.exists(login_image_path):
            image = Image.open(login_image_path)
            image = image.resize((self.root.winfo_width(), self.root.winfo_height()), Image.LANCZOS)
            bg_image = ImageTk.PhotoImage(image)

            # Label untuk background
            bg_label = tk.Label(self.root, image=bg_image)
            bg_label.image = bg_image
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Username
        username_entry = tk.Entry(self.root, width=40, bg="#d2e8fe")
        username_entry.pack(pady=(350, 30))

        # Password
        password_entry = tk.Entry(self.root, show="*", width=40, bg="#d2e8fe")
        password_entry.pack(pady=(30, 130))

        def proses_login():
            username = username_entry.get()
            password = password_entry.get()

            # Validasi login
            if username in self.users and self.users[username]['password'] == password:
                self.pengguna_saat_ini = username
                
                self.tampilan_menu_utama()
            else:
                messagebox.showerror("Login Gagal", "Username atau password salah")

        # Tombol Login
        tk.Button(self.root, text="Login", command=proses_login, bg="#b3f9ff", width=30, height=2).pack(pady=(5, 1))

        # Tombol Kembali
        tk.Button(self.root, text="Kembali", command=self.tampilan_selamat_datang, bg="#f08080", width=20, height=2).pack(pady=(100, 10), padx=(50, 1300))

    def tampilan_menu_utama(self):
        """Tampilan menu utama setelah login"""
        for widget in self.root.winfo_children():
            widget.destroy()

        messagebox.showinfo("Selamat datang", "Selamat datang di aplikasi utama!")

        app = AplikasiBelanja(self.root, self.pengguna_saat_ini, self.shopping_lists_dir,self)

    def tampilan_daftar(self):
        """Menampilkan tampilan pendaftaran tanpa jendela baru"""
        for widget in self.root.winfo_children():
            widget.destroy()

        AplikasiDaftar(self.root, self)

# Inisialisasi dan menjalankan aplikasi
if __name__ == "__main__":
    root = tk.Tk()
    app = AplikasiBelanjaKeluarga(root)
    root.mainloop()  
