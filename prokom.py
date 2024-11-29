import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import reportlab.pdfgen.canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime

class AplikasiBelanjaKeluarga:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Pengelolaan Belanja Keluarga")
        self.root.geometry("400x600")
        
        # Inisialisasi database
        self.conn = sqlite3.connect('belanja_keluarga.db')
        self.cursor = self.conn.cursor()
        
        # Buat tabel jika belum ada
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                nama TEXT,
                username TEXT UNIQUE,
                email TEXT UNIQUE,
                password TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS daftar_belanja (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                judul TEXT,
                tanggal TEXT,
                anggaran REAL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS item_belanja (
                id INTEGER PRIMARY KEY,
                daftar_belanja_id INTEGER,
                kategori TEXT,
                nama_barang TEXT,
                harga REAL,
                FOREIGN KEY(daftar_belanja_id) REFERENCES daftar_belanja(id)
            )
        ''')
        
        self.conn.commit()
        
        # Variabel global
        self.current_user = None
        self.current_daftar_belanja_id = None
        
        # Tampilan awal
        self.halaman_selamat_datang()
    
    def halaman_selamat_datang(self):
        # Hapus semua widget sebelumnya
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Judul
        tk.Label(self.root, text="Selamat Datang", font=("Arial", 20)).pack(pady=20)
        
        # Tombol Login
        tk.Button(self.root, text="Login", command=self.halaman_login).pack(pady=10)
        
        # Tombol Daftar
        tk.Button(self.root, text="Daftar", command=self.halaman_daftar).pack(pady=10)
    
    def halaman_login(self):
        # Hapus semua widget sebelumnya
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Judul
        tk.Label(self.root, text="Login", font=("Arial", 20)).pack(pady=20)
        
        # Username
        tk.Label(self.root, text="Username").pack()
        username_entry = tk.Entry(self.root, width=30)
        username_entry.pack(pady=5)
        
        # Password
        tk.Label(self.root, text="Password").pack()
        password_entry = tk.Entry(self.root, show="*", width=30)
        password_entry.pack(pady=5)
        
        # Tombol Login
        def login():
            username = username_entry.get()
            password = password_entry.get()
            
            self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = self.cursor.fetchone()
            
            if user:
                self.current_user = user[0]  # ID pengguna
                self.halaman_menu_utama()
            else:
                messagebox.showerror("Login Gagal", "Username atau password salah")
        
        tk.Button(self.root, text="Login", command=login).pack(pady=10)
        
        # Kembali ke halaman selamat datang
        tk.Button(self.root, text="Kembali", command=self.halaman_selamat_datang).pack(pady=5)
    
    def halaman_daftar(self):
        # Hapus semua widget sebelumnya
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Judul
        tk.Label(self.root, text="Daftar Akun", font=("Arial", 20)).pack(pady=20)
        
        # Nama
        tk.Label(self.root, text="Nama").pack()
        nama_entry = tk.Entry(self.root, width=30)
        nama_entry.pack(pady=5)
        
        # Username
        tk.Label(self.root, text="Username").pack()
        username_entry = tk.Entry(self.root, width=30)
        username_entry.pack(pady=5)
        
        # Email
        tk.Label(self.root, text="Email").pack()
        email_entry = tk.Entry(self.root, width=30)
        email_entry.pack(pady=5)
        
        # Password
        tk.Label(self.root, text="Password").pack()
        password_entry = tk.Entry(self.root, show="*", width=30)
        password_entry.pack(pady=5)
        
        # Tombol Daftar
        def daftar():
            nama = nama_entry.get()
            username = username_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            
            try:
                self.cursor.execute(
                    "INSERT INTO users (nama, username, email, password) VALUES (?, ?, ?, ?)", 
                    (nama, username, email, password)
                )
                self.conn.commit()
                messagebox.showinfo("Berhasil", "Akun berhasil dibuat")
                self.halaman_login()
            except sqlite3.IntegrityError:
                messagebox.showerror("Gagal", "Username atau email sudah terdaftar")
        
        tk.Button(self.root, text="Daftar", command=daftar).pack(pady=10)
        
        # Kembali ke halaman selamat datang
        tk.Button(self.root, text="Kembali", command=self.halaman_selamat_datang).pack(pady=5)
    
    def halaman_menu_utama(self):
        # Hapus semua widget sebelumnya
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Judul
        tk.Label(self.root, text="Menu Utama", font=("Arial", 20)).pack(pady=20)
        
        # Tombol Daftar Belanja Baru
        tk.Button(self.root, text="Daftar Belanja Baru", command=self.halaman_buat_daftar_belanja).pack(pady=10)
        
        # Tombol Daftar Belanja Lama
        tk.Button(self.root, text="Daftar Belanja Lama", command=self.halaman_daftar_belanja_lama).pack(pady=10)
        
        # Tombol Logout
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=10)
    
    def halaman_buat_daftar_belanja(self):
        # Hapus semua widget sebelumnya
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Judul
        tk.Label(self.root, text="Buat Daftar Belanja Baru", font=("Arial", 20)).pack(pady=20)
        
        # Judul Daftar Belanja
        tk.Label(self.root, text="Judul Daftar Belanja").pack()
        judul_entry = tk.Entry(self.root, width=30)
        judul_entry.pack(pady=5)
        
        # Tanggal Belanja
        tk.Label(self.root, text="Tanggal Belanja").pack()
        tanggal_entry = tk.Entry(self.root, width=30)
        tanggal_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        tanggal_entry.pack(pady=5)
        
        # Anggaran
        tk.Label(self.root, text="Anggaran").pack()
        anggaran_entry = tk.Entry(self.root, width=30)
        anggaran_entry.pack(pady=5)
        
        def buat_daftar():
            judul = judul_entry.get()
            tanggal = tanggal_entry.get()
            anggaran = float(anggaran_entry.get())
            
            # Simpan daftar belanja
            self.cursor.execute(
                "INSERT INTO daftar_belanja (user_id, judul, tanggal, anggaran) VALUES (?, ?, ?, ?)",
                (self.current_user, judul, tanggal, anggaran)
            )
            self.conn.commit()
            
            # Ambil ID daftar belanja yang baru dibuat
            self.current_daftar_belanja_id = self.cursor.lastrowid
            
            # Pindah ke halaman input item
            self.halaman_input_item_belanja()
        
        tk.Button(self.root, text="Lanjut", command=buat_daftar).pack(pady=10)
        
        # Tombol Kembali
        tk.Button(self.root, text="Kembali", command=self.halaman_menu_utama).pack(pady=5)
    
    def halaman_input_item_belanja(self):
        # Hapus semua widget sebelumnya
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Ambil anggaran saat ini
        self.cursor.execute("SELECT anggaran FROM daftar_belanja WHERE id = ?", (self.current_daftar_belanja_id,))
        anggaran = self.cursor.fetchone()[0]
        
        # Label Sisa Anggaran
        sisa_anggaran_var = tk.StringVar()
        sisa_anggaran_var.set(f"Sisa Anggaran: Rp {anggaran:,.2f}")
        sisa_anggaran_label = tk.Label(self.root, textvariable=sisa_anggaran_var, font=("Arial", 16))
        sisa_anggaran_label.pack(pady=10)
        
        # Kategori
        tk.Label(self.root, text="Kategori Barang").pack()
        kategori_entry = tk.Entry(self.root, width=30)
        kategori_entry.pack(pady=5)
        
        # Nama Barang
        tk.Label(self.root, text="Nama Barang").pack()
        nama_barang_entry = tk.Entry(self.root, width=30)
        nama_barang_entry.pack(pady=5)
        
        # Harga Barang
        tk.Label(self.root, text="Harga Barang").pack()
        harga_barang_entry = tk.Entry(self.root, width=30)
        harga_barang_entry.pack(pady=5)
        
        # Treeview untuk list belanja
        columns = ('Kategori', 'Nama Barang', 'Harga')
        tree = ttk.Treeview(self.root, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        tree.pack(pady=10)
        
        def tambah_item():
            kategori = kategori_entry.get()
            nama_barang = nama_barang_entry.get()
            harga_barang = float(harga_barang_entry.get())
            
            # Cek sisa anggaran
            nonlocal anggaran
            if harga_barang > anggaran:
                messagebox.showerror("Error", "Harga barang melebihi sisa anggaran")
                return
            
            # Simpan item ke database
            self.cursor.execute(
                "INSERT INTO item_belanja (daftar_belanja_id, kategori, nama_barang, harga) VALUES (?, ?, ?, ?)",
                (self.current_daftar_belanja_id, kategori, nama_barang, harga_barang)
            )
            self.conn.commit()
            
            # Update treeview
            tree.insert('', 'end', values=(kategori, nama_barang, harga_barang))
            
            # Kurangi anggaran
            anggaran -= harga_barang
            sisa_anggaran_var.set(f"Sisa Anggaran: Rp {anggaran:,.2f}")
            
            # Reset entri
            kategori_entry.delete(0, tk.END)
            nama_barang_entry.delete(0, tk.END)
            harga_barang_entry.delete(0, tk.END)
        
        def hapus_item():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Peringatan", "Pilih item yang akan dihapus")
                return
            
            # Ambil detail item yang akan dihapus
            item_values = tree.item(selected_item[0])['values']
            
            # Kembalikan harga ke anggaran
            nonlocal anggaran
            anggaran += item_values[2]
            sisa_anggaran_var.set(f"Sisa Anggaran: Rp {anggaran:,.2f}")
            
            # Hapus dari database
            self.cursor.execute(
                "DELETE FROM item_belanja WHERE daftar_belanja_id = ? AND nama_barang = ? AND harga = ?",
                (self.current_daftar_belanja_id, item_values[1], item_values[2])
            )
            self.conn.commit()
            
            # Hapus dari treeview
            tree.delete(selected_item)
        
        def simpan_dan_kembali():
            # Update anggaran akhir di database
            self.cursor.execute(
                "UPDATE daftar_belanja SET anggaran = ? WHERE id = ?",
                (anggaran, self.current_daftar_belanja_id)
            )
            self.conn.commit()
            
            # Kirim email dengan PDF
            try:
                # Fungsi untuk membuat PDF (sederhana)
                def buat_pdf():
                    pdf_path = f"daftar_belanja_{self.current_daftar_belanja_id}.pdf"
                    c = reportlab.pdfgen.canvas.Canvas(pdf_path, pagesize=letter)
                    
                    # Ambil detail daftar belanja
                    self.cursor.execute("SELECT * FROM daftar_belanja WHERE id = ?", (self.current_daftar_belanja_id,))
                    daftar = self.cursor.fetchone()
                    
                    # Ambil items belanja
                    self.cursor.execute("SELECT * FROM item_belanja WHERE daftar_belanja_id = ?", (self.current_daftar_belanja_id,))
                    items = self.cursor.fetchall()
                    
                    # Tulis judul
                    c.setFont("Helvetica-Bold", 16)
                    c.drawString(50, 750, f"Daftar Belanja: {daftar[2]}")
                    c.setFont("Helvetica", 12)
                    c.drawString(50, 730, f"Tanggal: {daftar[3]}")
                    c.drawString(50, 710, f"Anggaran Awal: Rp {daftar[4]:,.2f}")
                    
                    # Tulis detail items
                    c.drawString(50, 680, "Daftar Belanja:")
                    y = 660
                    for item in items:
                        c.drawString(70, y, f"{item[2]} - {item[3]}: Rp {item[4]:,.2f}")
                        y -= 20
                    
                    c.save()
                    return pdf_path
                
                # Fungsi kirim email
                def kirim_email(pdf_path):
                    # Ambil email pengguna
                    self.cursor.execute("SELECT email FROM users WHERE id = ?", (self.current_user,))
                    email = self.cursor.fetchone()[0]
                    
                    # Konfigurasi email (gunakan email Anda sendiri)
                    sender_email = "email_anda@gmail.com"
                    sender_password = "password_app_anda"
                    
                    # Buat pesan email
                    msg = MIMEMultipart()
                    msg['From'] = sender_email
                    msg['To'] = email
                    msg['Subject'] = "Daftar Belanja Baru"
                    
                    body = "Terlampir daftar belanja baru Anda dalam format PDF"
                    msg.attach(MIMEText(body, 'plain'))
                    
                    # Lampirkan PDF
                    with open(pdf_path, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                    
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f"attachment; filename= {pdf_path}")
                    msg.attach(part)
                    
                    # Kirim email
                    try:
                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.starttls()
                        server.login(sender_email, sender_password)
                        server.send_message(msg)
                        server.quit()
                        messagebox.showinfo("Berhasil", "Daftar belanja telah dikirim ke email Anda")
                    except Exception as e:
                        messagebox.showerror("Kesalahan Email", str(e))
                
                # Buat PDF dan kirim email
                pdf_path = buat_pdf()
                kirim_email(pdf_path)
                
                # Kembalikan ke menu utama
                self.halaman_menu_utama()
            
            except Exception as e:
                messagebox.showerror("Kesalahan", str(e))
        
        # Tombol-tombol
        tk.Button(self.root, text="Tambah Item", command=tambah_item).pack(pady=5)
        tk.Button(self.root, text="Hapus Item", command=hapus_item).pack(pady=5)
        tk.Button(self.root, text="Simpan & Kembali", command=simpan_dan_kembali).pack(pady=5)
        tk.Button(self.root, text="Kembali", command=self.halaman_menu_utama).pack(pady=5)
    
    def halaman_daftar_belanja_lama(self):
        # Hapus semua widget sebelumnya
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Judul
        tk.Label(self.root, text="Daftar Belanja Lama", font=("Arial", 20)).pack(pady=20)
        
        # Treeview untuk daftar belanja lama
        columns = ('ID', 'Judul', 'Tanggal', 'Anggaran')
        tree = ttk.Treeview(self.root, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        tree.pack(pady=10)
        
        # Ambil daftar belanja untuk user saat ini
        self.cursor.execute("SELECT id, judul, tanggal, anggaran FROM daftar_belanja WHERE user_id = ?", (self.current_user,))
        daftar_belanja = self.cursor.fetchall()
        
        for belanja in daftar_belanja:
            tree.insert('', 'end', values=belanja)
        
        def lihat_detail():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Peringatan", "Pilih daftar belanja")
                return
            
            # Ambil ID daftar belanja
            daftar_belanja_id = tree.item(selected_item[0])['values'][0]
            
            # Buka detail daftar belanja
            self.lihat_detail_daftar_belanja(daftar_belanja_id)
        
        def hapus_daftar():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Peringatan", "Pilih daftar belanja")
                return
            
            # Konfirmasi penghapusan
            konfirmasi = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus daftar belanja ini?")
            if konfirmasi:
                # Ambil ID daftar belanja
                daftar_belanja_id = tree.item(selected_item[0])['values'][0]
                
                # Hapus item belanja terkait
                self.cursor.execute("DELETE FROM item_belanja WHERE daftar_belanja_id = ?", (daftar_belanja_id,))
                
                # Hapus daftar belanja
                self.cursor.execute("DELETE FROM daftar_belanja WHERE id = ?", (daftar_belanja_id,))
                
                self.conn.commit()
                
                # Refresh daftar
                tree.delete(selected_item)
        
        # Tombol-tombol
        tk.Button(self.root, text="Lihat Detail", command=lihat_detail).pack(pady=5)
        tk.Button(self.root, text="Hapus Daftar", command=hapus_daftar).pack(pady=5)
        tk.Button(self.root, text="Kembali", command=self.halaman_menu_utama).pack(pady=5)
    
    def lihat_detail_daftar_belanja(self, daftar_belanja_id):
        # Hapus semua widget sebelumnya
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Ambil detail daftar belanja dengan error handling
        try:
            self.cursor.execute("SELECT * FROM daftar_belanja WHERE id = ? AND user_id = ?", (daftar_belanja_id, self.current_user))
            daftar = self.cursor.fetchone()
            
            if not daftar:
                messagebox.showerror("Error", "Daftar belanja tidak ditemukan atau tidak valid")
                self.halaman_daftar_belanja_lama()
                return
            
            # Judul
            tk.Label(self.root, text=f"Detail Daftar Belanja: {daftar[2]}", font=("Arial", 20)).pack(pady=20)
            
            # Informasi Daftar Belanja
            tk.Label(self.root, text=f"Tanggal: {daftar[3]}", font=("Arial", 12)).pack()
            
            # Hitung total belanja
            total_belanja = 0
            
            # Treeview untuk item belanja
            columns = ('Kategori', 'Nama Barang', 'Harga')
            tree = ttk.Treeview(self.root, columns=columns, show='headings')
            
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100, anchor='center')
            
            tree.pack(pady=10)
            
            # Ambil item belanja
            self.cursor.execute("SELECT * FROM item_belanja WHERE daftar_belanja_id = ?", (daftar_belanja_id,))
            items = self.cursor.fetchall()
            
            if not items:
                tk.Label(self.root, text="Tidak ada item belanja", font=("Arial", 12)).pack()
            else:
                for item in items:
                    harga = item[4]
                    total_belanja += harga
                    tree.insert('', 'end', values=(item[2], item[3], f"Rp {harga:,.2f}"))
            
            # Tampilkan total belanja dan sisa anggaran
            tk.Label(self.root, text=f"Anggaran Awal: Rp {daftar[4]:,.2f}", font=("Arial", 12)).pack()
            tk.Label(self.root, text=f"Total Belanja: Rp {total_belanja:,.2f}", font=("Arial", 12)).pack()
            tk.Label(self.root, text=f"Sisa Anggaran: Rp {daftar[4] - total_belanja:,.2f}", font=("Arial", 12)).pack()
            
            # Tombol Kembali
            tk.Button(self.root, text="Kembali", command=self.halaman_daftar_belanja_lama).pack(pady=5)
        
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
            self.halaman_daftar_belanja_lama()

# Fungsi utama untuk menjalankan aplikasi
def main():
    root = tk.Tk()
    app = AplikasiBelanjaKeluarga(root)
    root.mainloop()

if __name__ == "__main__":
    main()