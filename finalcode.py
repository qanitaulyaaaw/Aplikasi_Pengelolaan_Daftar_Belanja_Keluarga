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

# Login pengguna (KENI)
def login_user(username_entry, password_entry):
    username = username_entry.get()
    password = password_entry.get()
    
    try:
        with open('user_data.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  
            for row in reader:
                if row[1] == username and row[3] == password:
                    messagebox.showinfo("Success", "Login berhasil!")
                    show_menu_frame()
                    return
        messagebox.showerror("Error", "Username atau password tidak valid.")
    except FileNotFoundError:
        messagebox.showerror("Error", "Database pengguna tidak ditemukan.")


# Mengganti isi jendela (KENI)
def switch_frame(new_frame):
    global current_frame
    if current_frame is not None:
        current_frame.destroy()
    current_frame = new_frame
    current_frame.pack(expand=True, fill="both", padx=20, pady=20)

# Jendela menu daftar belanja (KENI)
def show_menu_frame():
    menu_frame = Frame(root)
    
    Label(menu_frame, text="Pilih Menu Daftar Belanja", font=("Arial", 12)).pack(pady=10)
    Button(menu_frame, text="Daftar Belanja Baru", font=("Arial", 10), command=show_budget_frame).pack(pady=5)
    Button(menu_frame, text="Daftar Belanja Lama", font=("Arial", 10), command=show_old_list_frame).pack(pady=5)
    Button(menu_frame, text="Logout", font=("Arial", 10), command=show_main_frame).pack(pady=10)
    
    switch_frame(menu_frame)

# Jendela anggaran (KENI)
def show_budget_frame():
    budget_frame = Frame(root)

    Label(budget_frame, text="Masukkan Anggaran", font=("Arial", 12)).pack(pady=10)
    budget_entry = Entry(budget_frame, font=("Arial", 10))
    budget_entry.pack(pady=5)

    def next_frame():
        budget = budget_entry.get()
        if not budget.isdigit():
            messagebox.showerror("Error", "Anggaran harus berupa angka.")
            return
        show_title_date_frame(budget)

    Button(budget_frame, text="Lanjutkan", font=("Arial", 10), command=next_frame).pack(pady=10)
    Button(budget_frame, text="Kembali", font=("Arial", 10), command=show_menu_frame).pack(pady=10)

    switch_frame(budget_frame)

# Main Tkinter setup (KENI)
root = Tk()
root.title("Aplikasi Pengelolaan Daftar Belanja Keluarga")
root.geometry("400x400")

create_user_table()
show_welcome_frame()

root.mainloop()