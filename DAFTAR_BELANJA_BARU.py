import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import json
import os
from datetime import datetime

class AplikasiBelanja:
    def __init__(self, root, pengguna_saat_ini, shopping_lists_dir, parent=None):
        self.root = root
        self.pengguna_saat_ini = pengguna_saat_ini
        self.shopping_lists_dir = shopping_lists_dir
        self.parent = parent
        self.root.title("Menu Utama")
        self.root.geometry("1960x1080") 
        self.tampilan_menu_utama()

    def tampilan_menu_utama(self):
        """Tampilan menu utama setelah login"""
        # Hapus semua widget sebelumnya
        for widget in self.root.winfo_children():
            widget.destroy()

        lama_image_path = "background lama baru.jpg"

        # Load gambar JPG
        image = Image.open(lama_image_path)
        image = image.resize((self.root.winfo_width(), self.root.winfo_height()), Image.LANCZOS)
        bg_image = ImageTk.PhotoImage(image)
        
        # Label untuk background
        bg_label = tk.Label(self.root, image=bg_image)
        bg_label.image = bg_image 
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Buat frame utama di atas background
        frame = tk.Frame(self.root, bg="#ffffff", bd=2)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Judul
        tk.Label(self.root, text=f"Welcome, {self.pengguna_saat_ini}!", font=("Times New Roman", 30)).pack(pady=(260,10))
        
        # Tombol Daftar Belanja Baru
        tk.Button(self.root, text="Daftar Belanja Baru", command=self.tampilan_buat_daftar_belanja, width=40, height=3, bg = "#dfb0d4").pack(pady=(45,10))
        
        # Tombol Daftar Belanja Lama
        tk.Button(self.root, text="Daftar Belanja Lama", command=self.tampilan_daftar_belanja_lama, width=40, height=3, bg = "#76c5de").pack(pady=10)
        
        # Tombol Logout
        tk.Button(self.root, text="Logout", command=self.parent.tampilan_selamat_datang, width=20, height=2, bg = "#de6262").pack(pady=10)
    
    def tampilan_buat_daftar_belanja(self):
        """Tampilan untuk membuat daftar belanja baru"""
        # Hapus semua widget sebelumnya
        for widget in self.root.winfo_children():
            widget.destroy()

        baru_image_path = "background baru.jpg"

        # Load gambar JPG
        image = Image.open(baru_image_path)
        image = image.resize((self.root.winfo_width(), self.root.winfo_height()), Image.LANCZOS)
        bg_image = ImageTk.PhotoImage(image)
        
        # Label untuk background
        bg_label = tk.Label(self.root, image=bg_image)
        bg_label.image = bg_image  
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Buat frame utama di atas background
        frame = tk.Frame(self.root, bg="#ffffff", bd=2)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Set Anggaran
        anggaran_entry = tk.Entry(self.root, width=40, bg = "#ffdcf7")
        anggaran_entry.pack(pady=(370,5))
        
        # Judul Belanja
        judul_entry = tk.Entry(self.root, width=40, bg = "#ffdcf7")
        judul_entry.pack(pady=(30,5))
        
        # Tanggal Belanja
        tanggal_entry = tk.Entry(self.root, width=40, bg = "#ffdcf7")
        tanggal_entry.insert(0, datetime.now().strftime("%d-%m-%Y"))
        tanggal_entry.pack(pady=(42,5))
        
        def lanjut_input_barang():
            try:
                anggaran = float(anggaran_entry.get())
                judul = judul_entry.get()
                tanggal = tanggal_entry.get()
                
                if not judul:
                    messagebox.showerror("Kesalahan", "Judul belanja harus diisi!")
                    return
                
                self.tampilan_input_barang(anggaran, judul, tanggal)
            except ValueError:
                messagebox.showerror("Kesalahan", "Anggaran harus berupa angka!")
        
        # Tombol Lanjut
        tk.Button(self.root, text="Lanjut", command=lanjut_input_barang, width= 15, bg = "#ffc5bb").pack(pady=10)
        
        # Tombol Kembali
        tk.Button(self.root, text="Kembali", width = 20, height= 2, command=self.tampilan_menu_utama, bg = "#de6262").pack(pady=(175,10), padx=(50,1300))
    
    def tampilan_input_barang(self, anggaran, judul, tanggal):
        """Tampilan untuk menginput barang belanja"""
        # Hapus semua widget sebelumnya
        for widget in self.root.winfo_children():
            widget.destroy()

        belanja_image_path = "background daftar belanja.jpg"

        # Load gambar JPG
        image = Image.open(belanja_image_path)
        image = image.resize((self.root.winfo_width(), self.root.winfo_height()), Image.LANCZOS)
        bg_image = ImageTk.PhotoImage(image)
        
        # Label untuk background
        bg_label = tk.Label(self.root, image=bg_image)
        bg_label.image = bg_image  
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Buat frame utama di atas background
        frame = tk.Frame(self.root, bg="#ffffff", bd=2)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Sisa Anggaran
        sisa_anggaran = anggaran
        sisa_anggaran_formatted = f"{sisa_anggaran:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
        sisa_label = tk.Label(self.root, text=f"Sisa Anggaran: Rp {sisa_anggaran_formatted}", font=("Times New Roman", 10))
        sisa_label.pack(pady=(75,5))
        
        # List Belanja
        list_belanja = []
        list_frame = tk.Frame(self.root)
        list_frame.pack(pady=10)
        
        list_treeview = ttk.Treeview(list_frame, columns=("Kategori", "Nama Barang", "Harga"), show="headings")
        list_treeview.heading("Kategori", text="Kategori")
        list_treeview.heading("Nama Barang", text="Nama Barang")
        list_treeview.heading("Harga", text="Harga")
        list_treeview.pack(side=tk.LEFT)
        
        # Kategori
        kategori_entry = tk.Entry(self.root, width=30, bg = "#ffe7e1")
        kategori_entry.pack(pady=(40,5))
        
        # Nama Barang
        nama_barang_entry = tk.Entry(self.root, width=30, bg = "#ffe7e1")
        nama_barang_entry.pack(pady=(35,5))
        
        # Harga Barang
        harga_barang_entry = tk.Entry(self.root, width=30, bg = "#ffe7e1")
        harga_barang_entry.pack(pady=(38,5))
        
        def tambah_barang():
            nonlocal sisa_anggaran
            try:
                kategori = kategori_entry.get()
                nama_barang = nama_barang_entry.get()
                harga_barang = float(harga_barang_entry.get())
                
                if not (kategori and nama_barang):
                    messagebox.showerror("Kesalahan", "Kategori dan nama barang harus diisi")
                    return
                
                if harga_barang > sisa_anggaran:
                    messagebox.showerror("Kesalahan", "Harga barang melebihi sisa anggaran")
                    return
                
                list_belanja.append((kategori, nama_barang, harga_barang))
                harga_barang_formatted = f"{harga_barang:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
                list_treeview.insert("", "end", values=(kategori, nama_barang, f"Rp {harga_barang_formatted}"))
                
                sisa_anggaran -= harga_barang
                sisa_anggaran_formatted = f"{sisa_anggaran:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
                sisa_label.config(text=f"Sisa Anggaran: Rp {sisa_anggaran_formatted}")
                
                # Reset entri
                kategori_entry.delete(0, tk.END)
                nama_barang_entry.delete(0, tk.END)
                harga_barang_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Kesalahan", "Harga barang harus berupa angka")
        
        def hapus_barang():
            nonlocal sisa_anggaran
            selected_item = list_treeview.selection()
            if not selected_item:
                messagebox.showerror("Kesalahan", "Pilih barang yang akan dihapus")
                return
            
            item = list_treeview.item(selected_item[0])
            kategori, nama_barang, harga_str = item['values']
            
            harga = float(harga_str.replace("Rp ", "").replace(".", "").replace(",", "."))
            
            for belanja in list_belanja:
                if belanja[0] == kategori and belanja[1] == nama_barang and belanja[2] == harga:
                    list_belanja.remove(belanja)
                    break
            else:
                messagebox.showerror("Kesalahan", "Item tidak ditemukan dalam daftar belanja")
                return
            
            list_treeview.delete(selected_item[0])
            
            
            sisa_anggaran += harga
            sisa_anggaran_formatted = f"{sisa_anggaran:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
            sisa_label.config(text=f"Sisa Anggaran: Rp {sisa_anggaran_formatted}")
        
        def cek_status():
            if sisa_anggaran >= 0:
                messagebox.showinfo("Status", "Anggaran Cukup")
            else:
                messagebox.showwarning("Status", "Anggaran Tidak Cukup")
        
        def simpan_daftar():
            nama_file = os.path.join(self.shopping_lists_dir, "daftar_belanja.json")

            daftar_belanja = {
                'pengguna': self.pengguna_saat_ini,
                'judul': judul,
                'tanggal': tanggal,
                'total_anggaran': anggaran,
                'sisa_anggaran': sisa_anggaran,
                'list_belanja': list_belanja
            }

            # Inisialisasi data sebagai list kosong
            data = []

            # Jika file database ada, muat data dari file
            if os.path.exists(nama_file):
                with open(nama_file, 'r') as f:
                    try:
                        data = json.load(f)
                        if not isinstance(data, list):  # Pastikan formatnya list
                            data = []
                    except json.JSONDecodeError:  # Jika file kosong atau rusak
                        data = []

            # Tambahkan data baru ke dalam list
            data.append(daftar_belanja)

            # Simpan kembali data ke file
            with open(nama_file, 'w') as f:
                json.dump(data, f, indent=4)

            messagebox.showinfo("Berhasil", "Daftar belanja berhasil disimpan")
            self.tampilan_menu_utama()
    
        
        # Frame untuk tombol
        frame_tombol = tk.Frame(self.root)
        frame_tombol.pack(pady=10)

        # Frame untuk tombol Tambah dan Hapus Barang
        frame_tombol_atas = tk.Frame(self.root)
        frame_tombol_atas.pack(pady=10)

        # Tombol Tambah Barang
        tk.Button(frame_tombol_atas, text="Tambah Barang", command=tambah_barang, width=20, height=2, bg="#ffdad0").pack(side="left", padx=10)

        # Tombol Hapus Barang
        tk.Button(frame_tombol_atas, text="Hapus Barang", command=hapus_barang, width=20, height=2, bg="#f7c7bb").pack(side="left", padx=10)

        # Frame untuk tombol Cek Anggaran dan Simpan
        frame_tombol_bawah = tk.Frame(self.root)
        frame_tombol_bawah.pack(pady=10)

        # Tombol Cek Anggaran
        tk.Button(frame_tombol_bawah, text="Cek Anggaran", command=cek_status, width=20, height=2, bg="#e5b0a3").pack(side="left", padx=10)

        # Tombol Simpan
        tk.Button(frame_tombol_bawah, text="Simpan", command=simpan_daftar, width=20, height=2, bg="#d7a193").pack(side="left", padx=10)
        
        # Tombol Kembali
        tk.Button(self.root, text="Kembali", command=self.tampilan_menu_utama, width= 20, height= 2, bg = "#de6262").pack(pady=(35,10), padx=(50,1300))
    
    def tampilan_daftar_belanja_lama(self):
        for widget in self.root.winfo_children():
             widget.destroy()

        lama_image_path = "background lama.jpg"

        # Load gambar JPG
        image = Image.open(lama_image_path)
        image = image.resize((self.root.winfo_width(), self.root.winfo_height()), Image.LANCZOS)
        bg_image = ImageTk.PhotoImage(image)
        
        # Label untuk background
        bg_label = tk.Label(self.root, image=bg_image)
        bg_label.image = bg_image  
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Buat frame utama di atas background
        frame = tk.Frame(self.root, bg="#ffffff", bd=2)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Frame untuk daftar belanja
        list_frame = tk.Frame(self.root)
        list_frame.pack(pady=(275,10))
        
        # Treeview untuk menampilkan daftar belanja
        list_treeview = ttk.Treeview(list_frame, columns=("Judul", "Tanggal"), show="headings")
        list_treeview.heading("Judul", text="Judul")
        list_treeview.heading("Tanggal", text="Tanggal")
        list_treeview.pack(side=tk.LEFT)
        
        # Nama file database JSON utama
        nama_file = os.path.join(self.shopping_lists_dir, "daftar_belanja.json")
    
        # Baca data dari file JSON jika ada
        if os.path.exists(nama_file):
            with open(nama_file, 'r') as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list):
                        # Filter data untuk pengguna saat ini
                        for daftar in data:
                            if daftar.get('pengguna') == self.pengguna_saat_ini:
                                judul = daftar.get('judul', 'Tidak Ada Judul')
                                tanggal = daftar.get('tanggal', 'Tidak Ada Tanggal')
                                list_treeview.insert("", "end", values=(judul, tanggal), tags=(judul,))
                except json.JSONDecodeError:
                    messagebox.showerror("Kesalahan", "File data belanja rusak!")
        
        def lihat_detail():
            selected_item = list_treeview.selection()
            if not selected_item:
                messagebox.showerror("Kesalahan", "Pilih daftar belanja yang ingin dilihat")
                return

            # Ambil judul dari item yang dipilih
            judul = list_treeview.item(selected_item[0], "values")[0]
            nama_file = os.path.join(self.shopping_lists_dir, "daftar_belanja.json")

            try:
                with open(nama_file, 'r') as f:
                    data = json.load(f)

                # Cari daftar belanja berdasarkan judul
                daftar_belanja = next((d for d in data if d.get('judul') == judul and d.get('pengguna') == self.pengguna_saat_ini), None)
                if not daftar_belanja:
                    messagebox.showerror("Kesalahan", "Daftar belanja tidak ditemukan")
                    return

            except FileNotFoundError:
                messagebox.showerror("Kesalahan", "File data belanja tidak ditemukan")
                return
            except json.JSONDecodeError:
                messagebox.showerror("Kesalahan", "File JSON tidak valid atau rusak")
                return

            for widget in self.root.winfo_children():
                widget.destroy()
    
    # Jendela detail
            detail_window = tk.Frame(self.root)
            detail_window.pack(fill="both", expand=True)
    
            detail_image_path = "background detail.jpg"

    # Load gambar JPG untuk background
            image = Image.open(detail_image_path)
            image = image.resize((self.root.winfo_width(), self.root.winfo_height()), Image.LANCZOS)
            bg_image = ImageTk.PhotoImage(image)
    
    # Label untuk background
            bg_label = tk.Label(detail_window, image=bg_image)
            bg_label.image = bg_image  
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    

    # Frame utama
            frame = tk.Frame(detail_window, bg="#ffffff", bd=2)
            frame.place(relx=0.5, rely=0.5, anchor="center")
    
            tk.Label(frame, text=f"Judul: {daftar_belanja['judul']}", font=("Times New Roman", 15, "bold")).pack(pady=(20, 10))
            tk.Label(frame, text=f"Tanggal: {daftar_belanja['tanggal']}", font=("Times New Roman", 12)).pack(pady=5)
            total_anggaran_formatted = f"{daftar_belanja['total_anggaran']:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
            tk.Label(frame, text=f"Total Anggaran: Rp {total_anggaran_formatted}", font=("Times New Roman", 12)).pack(pady=5)
            sisa_anggaran_formatted = f"{daftar_belanja['sisa_anggaran']:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
            tk.Label(frame, text=f"Sisa Anggaran: Rp {sisa_anggaran_formatted}", font=("Times New Roman", 12)).pack(pady=5)
    
    # Frame untuk daftar barang
            detail_list_frame = tk.Frame(frame)
            detail_list_frame.pack(pady=10)
    
            detail_treeview = ttk.Treeview(detail_list_frame, columns=("Kategori", "Nama Barang", "Harga"), show="headings")
            detail_treeview.heading("Kategori", text="Kategori")
            detail_treeview.heading("Nama Barang", text="Nama Barang")
            detail_treeview.heading("Harga", text="Harga")
            detail_treeview.pack(side=tk.LEFT)
    
            for barang in daftar_belanja['list_belanja']:
                harga_formatted = f"{barang[2]:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
                detail_treeview.insert("", "end", values=(barang[0], barang[1], f"Rp {harga_formatted}"))
    
    # Tombol "Kembali"
            kembali_button = tk.Button(detail_window, text="Kembali", command=self.tampilan_daftar_belanja_lama)
            kembali_button.pack(pady=10)

        def hapus_daftar():
            selected_item = list_treeview.selection()
            if not selected_item:
                messagebox.showerror("Kesalahan", "Pilih daftar belanja yang akan dihapus")
                return
            
            # Ambil judul dari item yang dipilih
            judul = list_treeview.item(selected_item[0], "values")[0]

            # Nama file utama
            nama_file = os.path.join(self.shopping_lists_dir, "daftar_belanja.json")

            try:
                with open(nama_file, 'r') as f:
                    data = json.load(f)

                # Hapus daftar belanja berdasarkan judul
                data = [d for d in data if not (d.get('judul') == judul and d.get('pengguna') == self.pengguna_saat_ini)]

                # Simpan kembali data ke file
                with open(nama_file, 'w') as f:
                    json.dump(data, f, indent=4)

                # Hapus dari Treeview
                list_treeview.delete(selected_item[0])

                messagebox.showinfo("Berhasil", "Daftar belanja berhasil dihapus")

            except FileNotFoundError:
                messagebox.showerror("Kesalahan", "File data belanja tidak ditemukan")
            except json.JSONDecodeError:
                messagebox.showerror("Kesalahan", "File JSON tidak valid atau rusak")
        
        # Tombol Lihat Detail
        tk.Button(self.root, text="Lihat Detail", command=lihat_detail, width = 20, height= 2, bg = "#b5e0f7").pack(pady=5)
        
        # Tombol Hapus Daftar
        tk.Button(self.root, text="Hapus Daftar", command=hapus_daftar, width= 20, height= 2, bg = "#91bad0").pack(pady=5)
        
        # Tombol Kembalii
        tk.Button(self.root, text="Kembali", command=self.tampilan_menu_utama, width= 20, height= 2, bg = "#de6262").pack(pady=(90,10), padx=(50,1300))
