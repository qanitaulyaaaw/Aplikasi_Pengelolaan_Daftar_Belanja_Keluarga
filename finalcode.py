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

print('')
print('halloo')