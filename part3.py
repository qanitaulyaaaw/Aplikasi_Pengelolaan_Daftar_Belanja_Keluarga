import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import hashlib
from datetime import datetime

class FamilyShoppingApp:
    def __init__(self):
        # Inisialisasi database
        self.conn = sqlite3.connect('family_shopping.db')
        self.create_tables()

        # Jendela Utama
        self.root = tk.Tk()
        self.root.title("Pengelolaan Belanja Keluarga")
        self.root.geometry("400x300")

        # Judul Selamat Datang
        self.welcome_label = tk.Label(
            self.root, 
            text="Selamat Datang di Aplikasi\nPengelolaan Belanja Keluarga", 
            font=("Arial", 14)
        )
        self.welcome_label.pack(pady=20)

        # Tombol Login
        self.login_button = tk.Button(
            self.root, 
            text="Login", 
            command=self.open_login_window
        )
        self.login_button.pack(pady=10)

        # Tombol Signup
        self.signup_button = tk.Button(
            self.root, 
            text="Signup", 
            command=self.open_signup_window
        )
        self.signup_button.pack(pady=10)

        self.current_user = None

    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Tabel User
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                username TEXT UNIQUE,
                email TEXT UNIQUE,
                password TEXT
            )
        ''')

        # Tabel Daftar Belanja
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shopping_lists (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                title TEXT,
                budget REAL,
                date TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        # Tabel Item Belanja
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shopping_items (
                id INTEGER PRIMARY KEY,
                shopping_list_id INTEGER,
                category TEXT,
                name TEXT,
                price REAL,
                FOREIGN KEY (shopping_list_id) REFERENCES shopping_lists(id)
            )
        ''')

        self.conn.commit()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def open_signup_window(self):
        signup_window = tk.Toplevel(self.root)
        signup_window.title("Signup")
        signup_window.geometry("300x400")

        # Input Nama
        tk.Label(signup_window, text="Nama:").pack()
        name_entry = tk.Entry(signup_window)
        name_entry.pack()

        # Input Username
        tk.Label(signup_window, text="Username:").pack()
        username_entry = tk.Entry(signup_window)
        username_entry.pack()

        # Input Email
        tk.Label(signup_window, text="Email:").pack()
        email_entry = tk.Entry(signup_window)
        email_entry.pack()

        # Input Password
        tk.Label(signup_window, text="Password:").pack()
        password_entry = tk.Entry(signup_window, show="*")
        password_entry.pack()

        def signup():
            name = name_entry.get()
            username = username_entry.get()
            email = email_entry.get()
            password = password_entry.get()

            if not all([name, username, email, password]):
                messagebox.showerror("Error", "Semua field harus diisi!")
                return

            hashed_password = self.hash_password(password)

            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    "INSERT INTO users (name, username, email, password) VALUES (?, ?, ?, ?)",
                    (name, username, email, hashed_password)
                )
                self.conn.commit()
                messagebox.showinfo("Sukses", "Akun berhasil dibuat!")
                signup_window.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username atau email sudah terdaftar!")

        signup_button = tk.Button(signup_window, text="Signup", command=signup)
        signup_button.pack(pady=10)

    def open_login_window(self):
        login_window = tk.Toplevel(self.root)
        login_window.title("Login")
        login_window.geometry("300x250")

        # Input Username
        tk.Label(login_window, text="Username:").pack()
        username_entry = tk.Entry(login_window)
        username_entry.pack()

        # Input Password
        tk.Label(login_window, text="Password:").pack()
        password_entry = tk.Entry(login_window, show="*")
        password_entry.pack()

        def login():
            username = username_entry.get()
            password = password_entry.get()
            hashed_password = self.hash_password(password)

            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = ? AND password = ?", 
                (username, hashed_password)
            )
            user = cursor.fetchone()

            if user:
                self.current_user = user[0]  # ID user
                login_window.destroy()
                self.open_main_menu()
            else:
                messagebox.showerror("Error", "Username atau password salah!")

        login_button = tk.Button(login_window, text="Login", command=login)
        login_button.pack(pady=10)

    def open_main_menu(self):
        main_menu = tk.Toplevel(self.root)
        main_menu.title("Menu Utama")
        main_menu.geometry("300x250")

        # Tombol Daftar Belanja Baru
        new_list_button = tk.Button(
            main_menu, 
            text="Daftar Belanja Baru", 
            command=lambda: self.open_new_shopping_list(main_menu)
        )
        new_list_button.pack(pady=10)

        # Tombol Daftar Belanja Lama
        old_list_button = tk.Button(
            main_menu, 
            text="Daftar Belanja Lama", 
            command=lambda: self.open_old_shopping_lists(main_menu)
        )
        old_list_button.pack(pady=10)

        # Tombol Logout
        logout_button = tk.Button(
            main_menu, 
            text="Logout", 
            command=lambda: [main_menu.destroy(), self.current_user := None]
        )
        logout_button.pack(pady=10)

    def open_new_shopping_list(self, parent_window):
        new_list_window = tk.Toplevel(parent_window)
        new_list_window.title("Daftar Belanja Baru")
        new_list_window.geometry("400x500")

        # Input Anggaran
        tk.Label(new_list_window, text="Set Anggaran:").pack()
        budget_entry = tk.Entry(new_list_window)
        budget_entry.pack()

        # Input Judul Belanja
        tk.Label(new_list_window, text="Judul Belanja:").pack()
        title_entry = tk.Entry(new_list_window)
        title_entry.pack()

        # Input Tanggal Belanja
        tk.Label(new_list_window, text="Tanggal Belanja:").pack()
        date_entry = tk.Entry(new_list_window)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_entry.pack()

        # List Belanja
        shopping_list = []
        list_var = tk.StringVar(value=shopping_list)
        shopping_listbox = tk.Listbox(new_list_window, listvariable=list_var)
        shopping_listbox.pack(pady=10)

        def add_item():
            category = simpledialog.askstring("Kategori", "Masukkan kategori barang:")
            name = simpledialog.askstring("Nama Barang", "Masukkan nama barang:")
            price = simpledialog.askfloat("Harga Barang", "Masukkan harga barang:")

            if all([category, name, price is not None]):
                item = f"{category} - {name} - Rp {price}"
                shopping_list.append(item)
                list_var.set(shopping_list)

        def check_budget_status():
            budget = float(budget_entry.get())
            total_spent = sum(float(item.split(" - ")[-1][3:]) for item in shopping_list)
            sisa_anggaran = budget - total_spent
            messagebox.showinfo("Status Anggaran", f"Sisa Anggaran: Rp {sisa_anggaran}")

        def delete_item():
            selected_indices = shopping_listbox.curselection()
            if selected_indices:
                for index in reversed(selected_indices):
                    del shopping_list[index]
                list_var.set(shopping_list)

        def save_shopping_list():
            budget = float(budget_entry.get())
            title = title_entry.get()
            date = date_entry.get()

            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO shopping_lists (user_id, title, budget, date) VALUES (?, ?, ?, ?)",
                (self.current_user, title, budget, date)
            )
            shopping_list_id = cursor.lastrowid

            for item in shopping_list:
                category, name, price = item.split(" - ")
                price = float(price[3:])
                cursor.execute(
                    "INSERT INTO shopping_items (shopping_list_id, category, name, price) VALUES (?, ?, ?, ?)",
                    (shopping_list_id, category, name, price)
                )

            self.conn.commit()
            messagebox.showinfo("Sukses", "Daftar Belanja Berhasil Disimpan!")
            new_list_window.destroy()

        # Tombol Tambah Item
        add_item_button = tk.Button(new_list_window, text="Tambah Item", command=add_item)
        add_item_button.pack(pady=5)

        # Tombol Cek Status Anggaran
        check_budget_button = tk.Button(new_list_window, text="Cek Status Anggaran", command=check_budget_status)
        check_budget_button.pack(pady=5)

        # Tombol Hapus Item
        delete_item_button = tk.Button(new_list_window, text="Hapus Item", command=delete_item)
        delete_item_button.pack(pady=5)

        # Tombol Simpan
        save_button = tk.Button(new_list_window, text="Simpan", command=save_shopping_list)
        save_button.pack(pady=5)

    def open_old_shopping_lists(self, parent_window):
        old_lists_window = tk.Toplevel(parent_window)
        old_lists_window.title("Daftar Belanja Lama")
        old_lists_window.geometry("400x500")

        cursor = self.conn.cursor()
        cursor.execute("SELECT id, title, date FROM shopping_lists WHERE user_id = ?", (self.current_user,))
        shopping_lists = cursor.fetchall()

        list_var = tk.StringVar(value=[f"{title} - {date}" for _, title, date in shopping_lists])
        shopping_listbox = tk.Listbox(old_lists_window, listvariable=list_var)
        shopping_listbox.pack(pady=10)

        def view_shopping_list():
            selected_indices = shopping_listbox.curselection()
            if selected_indices:
                list_id = shopping_lists[selected_indices[0]][0]
                view_list_details(list_id)

        def view_list_details(list_id):
            details_window = tk.Toplevel(old_lists_window)
            details_window.title("Detail Daftar Belanja")
            details_window.geometry("400x500")

            cursor = self.conn.cursor()
            cursor.execute("SELECT category, name, price FROM shopping_items WHERE shopping_list_id = ?", (list_id,))
            items = cursor.fetchall()

            list_var = tk.StringVar(value=[f"{category} - {name} - Rp {price}" for category, name, price in items])
            details_listbox = tk.Listbox(details_window, listvariable=list_var)
            details_listbox.pack(pady=10)

        def delete_shopping_list():
            selected_indices = shopping_listbox.curselection()
            if selected_indices:
                list_id = shopping_lists[selected_indices[0]][0]
                
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM shopping_items WHERE shopping_list_id = ?", (list_id,))
                cursor.execute("DELETE FROM shopping_lists WHERE id = ?", (list_id,))
                self.conn.commit()

                messagebox.showinfo("Sukses", "Daftar Belanja Berhasil Dihapus!")
                old_lists_window.destroy()
                self.open_old_shopping_lists(parent_window)

        # Tombol Lihat Detail
        view_button = tk.Button(old_lists_window, text="Lihat Detail", command=view_shopping_list)
        view_button.pack(pady=5)

        # Tombol Hapus
        delete_button = tk.Button(old_lists_window, text="Hapus Daftar", command=delete_shopping_list)
        delete_button.pack(pady=5)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FamilyShoppingApp()
    app.run()