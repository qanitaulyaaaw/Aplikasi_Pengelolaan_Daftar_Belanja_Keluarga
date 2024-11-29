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
    
# Jendela selamat datang (KIRANA)
def show_welcome_frame():
    welcome_frame = Frame(root)
    
    Label(
        welcome_frame, 
        text="Selamat Datang di Aplikasi\nPengelolaan Daftar Belanja Keluarga", 
        font=("Arial", 12), 
        justify="center"
    ).pack(pady=20)
    Button(welcome_frame, text="Mulai", font=("Arial", 10), command=show_main_frame).pack(pady=10)
    
    switch_frame(welcome_frame)
    
# Jendela daftar (DHIAZ)
def show_register_frame():
    register_frame = Frame(root)
    
    Label(register_frame, text="Sign Up", font=("Arial", 12)).grid(row=0, column=0, columnspan=2, pady=10)
    
    Label(register_frame, text="Nama:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    name_entry = Entry(register_frame, font=("Arial", 10))
    name_entry.grid(row=1, column=1, padx=10, pady=5)
    
    Label(register_frame, text="Username:", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
    username_entry = Entry(register_frame, font=("Arial", 10))
    username_entry.grid(row=2, column=1, padx=10, pady=5)
    
    Label(register_frame, text="Email:", font=("Arial", 10)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
    email_entry = Entry(register_frame, font=("Arial", 10))
    email_entry.grid(row=3, column=1, padx=10, pady=5)
    
    Label(register_frame, text="Password:", font=("Arial", 10)).grid(row=4, column=0, padx=10, pady=5, sticky="w")
    password_entry = Entry(register_frame, show="*", font=("Arial", 10))
    password_entry.grid(row=4, column=1, padx=10, pady=5)
    
    Button(register_frame, text="Sign Up", font=("Arial", 10), 
           command=lambda: register_user(name_entry, username_entry, email_entry, password_entry)).grid(row=5, column=0, columnspan=2, pady=10)
    Button(register_frame, text="Kembali", font=("Arial", 10), command=show_main_frame).grid(row=6, column=0, columnspan=2, pady=5)
    
    switch_frame(register_frame)


# Jendela login (KIRANA)
def show_login_frame():
    login_frame = Frame(root)
    
    Label(login_frame, text="Login Akun", font=("Arial", 12)).grid(row=0, column=0, columnspan=2, pady=10)
    
    Label(login_frame, text="Username:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    username_entry = Entry(login_frame, font=("Arial", 10))
    username_entry.grid(row=1, column=1, padx=10, pady=5)
    
    Label(login_frame, text="Password:", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
    password_entry = Entry(login_frame, show="*", font=("Arial", 10))
    password_entry.grid(row=2, column=1, padx=10, pady=5)
    
    Button(login_frame, text="Login", font=("Arial", 10), 
           command=lambda: login_user(username_entry, password_entry)).grid(row=3, column=0, columnspan=2, pady=10)
    Button(login_frame, text="Kembali", font=("Arial", 10), command=show_main_frame).grid(row=4, column=0, columnspan=2, pady=5)
    
    switch_frame(login_frame)

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

# Jendela judul dan tanggal daftar belanja (kirana)
def show_title_date_frame(budget):
    title_date_frame = Frame(root)

    Label(title_date_frame, text="Masukkan Judul dan Tanggal Daftar Belanja", font=("Arial", 12)).pack(pady=10)

    # Mendefinisikan label dan entry field terlebih dahulu
    title_label = Label(title_date_frame, text="Judul", font=("Arial", 10))
    title_label.pack(pady=5)
    title_entry = Entry(title_date_frame, font=("Arial", 10))
    title_entry.pack(pady=5)

    date_label = Label(title_date_frame, text="Tanggal (DD-MM-YYYY)", font=("Arial", 10))
    date_label.pack(pady=5)
    date_entry = Entry(title_date_frame, font=("Arial", 10))
    date_entry.pack(pady=5)

    def next_frame():
        title = title_entry.get()
        date = date_entry.get()
        if not title or not date:
            messagebox.showerror("Error", "Semua kolom wajib diisi.")
            return
        messagebox.showinfo("Success", "Daftar belanja berhasil dibuat.")
        show_menu_frame()

    Button(title_date_frame, text="Lanjutkan", font=("Arial", 10), command=next_frame).pack(pady=10)
    Button(title_date_frame, text="Kembali", font=("Arial", 10), command=show_budget_frame).pack(pady=10)

    switch_frame(title_date_frame)

# Main Tkinter setup (KENI)
root = Tk()
root.title("Aplikasi Pengelolaan Daftar Belanja Keluarga")
root.geometry("400x400")

create_user_table()
show_welcome_frame()

root.mainloop()
