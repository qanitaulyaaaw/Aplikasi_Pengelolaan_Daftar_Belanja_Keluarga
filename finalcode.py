import csv
import os
from tkinter import *
from tkinter import messagebox

# Variabel global (DHIAZ)
current_frame = None

# Membuat tabel pengguna jika belum ada (DHIAZ)
def create_user_table():
    if not os.path.exists('user_data.csv'):
        with open('user_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'username', 'email', 'password'])  # Header

# Menyimpan data pengguna ke dalam file CSV (DHIAZ)
def save_user_data(name, username, email, password):
    with open('user_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, username, email, password])
    
    messagebox.showinfo("Success", "Pendaftaran akun berhasil! Silakan login kembali.")
    show_login_frame()

# Pendaftaran pengguna (KIRANA)
def register_user(name_entry, username_entry, email_entry, password_entry):
    name = name_entry.get()
    username = username_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    
    # Validasi input
    if not name or not username or not email or not password:
        messagebox.showerror("Error", "Semua kolom wajib diisi.")
        return
    if len(password) < 8:
        messagebox.showerror("Error", "Password harus memiliki minimal 8 karakter.")
        return
    
    # Memeriksa data pengguna
    try:
        with open('user_data.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row[1] == username:
                    messagebox.showerror("Error", "Username telah digunakan.")
                    return
                if row[2] == email:
                    messagebox.showerror("Error", "Email telah digunakan.")
                    return
    except FileNotFoundError:
        create_user_table()
    
    save_user_data(name, username, email, password)
