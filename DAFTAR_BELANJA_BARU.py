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
    
    def update_sisa_anggaran(self, daftar_belanja):
        # Hitung ulang total belanja dan sisa anggaran
        total_belanja = sum(item[2] for item in daftar_belanja['list_belanja'])
        sisa_anggaran = daftar_belanja['total_anggaran'] - total_belanja

        if sisa_anggaran < 0:
            # Tampilkan peringatan dan cegah pengguna melanjutkan
            messagebox.showerror("Anggaran Melebihi Batas", "Anggaran tidak cukup! Harap kurangi jumlah belanja untuk melanjutkan.")
            return False

        # Format ulang sisa anggaran jika positif
        sisa_anggaran_formatted = f"Rp {sisa_anggaran:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")

        # Periksa apakah self.frame ada, jika tidak buat frame baru
        if not hasattr(self, 'frame') or not self.frame.winfo_exists():
            self.frame = tk.Frame(self.root, bg="#ffffff", bd=2)
            self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Periksa apakah label "Sisa Anggaran" sudah ada, jika ada update, jika tidak buat baru
        for widget in self.frame.winfo_children():
            if isinstance(widget, tk.Label) and "Sisa Anggaran" in widget.cget("text"):
                widget.config(text=f"Sisa Anggaran: {sisa_anggaran_formatted}")
                return True

        # Jika label tidak ditemukan, buat label baru
        self.label_sisa_anggaran = tk.Label(
            self.frame,
            text=f"Sisa Anggaran: {sisa_anggaran_formatted}",
            font=("Times New Roman", 12)
        )
        self.label_sisa_anggaran.pack(pady=5)
        return True


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

            # Memanggil update_sisa_anggaran setelah memilih detail
            self.frame = frame  # Set self.frame untuk digunakan oleh update_sisa_anggaran
            self.update_sisa_anggaran(daftar_belanja)
    
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
    
    
            def edit_daftar():
                selected_item = detail_treeview.selection()
                if not selected_item:
                    messagebox.showerror("Kesalahan", "Pilih item yang akan diedit")
                    return

                # Ambil data dari item yang dipilih
                values = detail_treeview.item(selected_item[0], "values")
                kategori, nama_barang, harga = values

                # Sembunyikan detail_window
                detail_window.pack_forget()

                # Halaman edit daftar
                edit_frame = tk.Frame(self.root, bg="#ffffff")
                edit_frame.pack(fill="both", expand=True)

                edit_image_path = "background edit item.jpg"

                # Load gambar JPG untuk background
                image = Image.open(edit_image_path)
                image = image.resize((self.root.winfo_width(), self.root.winfo_height()), Image.LANCZOS)
                bg_image = ImageTk.PhotoImage(image)

                # Tambahkan margin atas dengan frame kosong
                tk.Frame(edit_frame, height=180, bg="#ffffff").pack()

                # Label untuk background
                bg_label = tk.Label(edit_frame, image=bg_image)
                bg_label.image = bg_image  
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)

                tk.Label(edit_frame, text="Kategori", bg="#ffffff", font=("Arial", 14)).pack(pady=5)
                kategori_entry = tk.Entry(edit_frame, width=45, bg="#ffdcf7")
                kategori_entry.insert(0, kategori)
                kategori_entry.pack(pady=5, padx=10, ipady=3)

                tk.Label(edit_frame, text="Nama Barang", bg="#ffffff", font=("Arial", 14)).pack(pady=5)
                nama_barang_entry = tk.Entry(edit_frame, width=45, bg="#ffdcf7")
                nama_barang_entry.insert(0, nama_barang)
                nama_barang_entry.pack(pady=5, padx=10, ipady=3)

                tk.Label(edit_frame, text="Harga", bg="#ffffff", font=("Arial", 14)).pack(pady=5)
                harga_entry = tk.Entry(edit_frame, width=45, bg="#ffdcf7")
                harga_entry.insert(0, harga.replace("Rp ", "").replace(".", ""))
                harga_entry.pack(pady=5, padx=10, ipady=3)

                def simpan_perubahan():
                    new_kategori = kategori_entry.get()
                    new_nama_barang = nama_barang_entry.get()
                    try:
                        # Ganti koma dengan titik
                        harga_input = harga_entry.get().replace(",", ".")
                        new_harga = float(harga_input)  # Konversi ke float
                    except ValueError:
                        messagebox.showerror("Kesalahan", "Harga harus berupa angka valid")
                        return

                    try:
                        # Hitung ulang total belanja
                        total_belanja_lama = sum(item[2] for item in daftar_belanja['list_belanja'])
                        harga_lama_float = float(harga.replace("Rp ", "").replace(".", "").replace(",", "."))
                        total_belanja_baru = total_belanja_lama - harga_lama_float + new_harga

                        # Periksa apakah melebihi anggaran
                        if total_belanja_baru > daftar_belanja['total_anggaran']:
                            messagebox.showerror("Anggaran Melebihi Batas", "Anggaran tidak cukup! Harap kurangi jumlah belanja untuk melanjutkan.")
                            return

                        # Update Treeview
                        harga_formatted = f"Rp {new_harga:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
                        detail_treeview.item(selected_item[0], values=(new_kategori, new_nama_barang, harga_formatted))

                        # Update JSON
                        for barang in daftar_belanja['list_belanja']:
                            if (
                                barang[0] == kategori and 
                                barang[1] == nama_barang and 
                                barang[2] == float(harga.replace("Rp ", "").replace(".", "").replace(",", "."))
                            ):
                                barang[0] = new_kategori
                                barang[1] = new_nama_barang
                                barang[2] = new_harga
                                break

                        # Simpan kembali ke file JSON
                        with open(nama_file, 'w') as f:
                            json.dump(data, f, indent=4)

                        # Hitung ulang sisa anggaran
                        sisa_anggaran = daftar_belanja['total_anggaran'] - total_belanja_baru

                        # Format ulang sisa anggaran
                        sisa_anggaran_formatted = f"Rp {sisa_anggaran:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
                        # Update label Sisa Anggaran
                        for widget in frame.winfo_children():
                            if isinstance(widget, tk.Label) and "Sisa Anggaran" in widget.cget("text"):
                                widget.config(text=f"Sisa Anggaran: {sisa_anggaran_formatted}")

                        messagebox.showinfo("Berhasil", "Data berhasil diubah")

                        # Kembali ke detail_window
                        edit_frame.pack_forget()
                        detail_window.pack(fill="both", expand=True)

                    except FileNotFoundError:
                        messagebox.showerror("Kesalahan", "File data belanja tidak ditemukan")
                    except json.JSONDecodeError:
                        messagebox.showerror("Kesalahan", "File JSON tidak valid atau rusak")                


                tk.Button(edit_frame, text="Simpan", command=simpan_perubahan, width=20, height=2, bg="#82ccdd", fg="black").pack(pady=20)

                
            # Tombol untuk Edit Daftar
            tk.Button(frame, text="Edit Item", command=edit_daftar, width=20, height=2, bg="#91bad0").pack(side="left", padx=5, pady=5)

            # Tombol "Kembali"
            kembali_button = tk.Button(detail_window, text="Kembali", command=self.tampilan_daftar_belanja_lama)
            kembali_button.pack(pady=10)

            # Fungsi untuk Tambah Item
            def tambah_item():
                for widget in self.root.winfo_children():
                    widget.destroy()

                # Halaman tambah item
                tambah_frame = tk.Frame(self.root, bg="#ffffff")
                tambah_frame.pack(fill="both", expand=True)

                tambah_image_path = "background tambah item.jpg"

                # Load gambar JPG untuk background
                image = Image.open(tambah_image_path)
                image = image.resize((self.root.winfo_width(), self.root.winfo_height()), Image.LANCZOS)
                bg_image = ImageTk.PhotoImage(image)

                # Label untuk background
                bg_label = tk.Label(tambah_frame, image=bg_image)
                bg_label.image = bg_image  
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)

                # Tambahkan margin atas dengan frame kosong
                tk.Frame(tambah_frame, height=180, bg="#ffffff").pack()

                tk.Label(tambah_frame, text="Kategori", bg="#ffffff", font=("Arial", 14)).pack(pady=5)
                kategori_entry = tk.Entry(tambah_frame, width=45, bg="#ffdcf7")
                kategori_entry.pack(pady=5, padx=10, ipady=3)

                tk.Label(tambah_frame, text="Nama Barang", bg="#ffffff", font=("Arial", 14)).pack(pady=5)
                nama_barang_entry = tk.Entry(tambah_frame, width=45, bg="#ffdcf7")
                nama_barang_entry.pack(pady=5, padx=10, ipady=3)

                tk.Label(tambah_frame, text="Harga", bg="#ffffff", font=("Arial", 14)).pack(pady=5)
                harga_entry = tk.Entry(tambah_frame, width=45, bg="#ffdcf7")
                harga_entry.pack(pady=5, padx=10, ipady=3)

                def simpan_item_baru():
                    new_kategori = kategori_entry.get()
                    new_nama_barang = nama_barang_entry.get()
                    try:
                        new_harga = float(harga_entry.get().replace(",", "."))
                    except ValueError:
                        messagebox.showerror("Kesalahan", "Harga harus berupa angka valid")
                        return

                    if not new_kategori or not new_nama_barang or not new_harga:
                        messagebox.showerror("Kesalahan", "Semua kolom harus diisi!")
                        return

                    # Tambahkan item baru ke daftar belanja
                    daftar_belanja['list_belanja'].append([new_kategori, new_nama_barang, new_harga])

                    try:
                        # Validasi anggaran sebelum menyimpan
                        if not self.update_sisa_anggaran(daftar_belanja):
                            # Jika anggaran tidak cukup, hapus item yang baru ditambahkan
                            daftar_belanja['list_belanja'].pop()
                            return

                        # Simpan kembali ke file JSON
                        with open(nama_file, 'w') as f:
                            json.dump(data, f, indent=4)

                        messagebox.showinfo("Berhasil", "Item baru berhasil ditambahkan!")

                        # Hancurkan halaman tambah item
                        tambah_frame.pack_forget()

                        # Pastikan detail_window dibangun ulang
                        self.tampilan_daftar_belanja_lama()  # Menggunakan fungsi ini untuk kembali ke tampilan detail

                    except FileNotFoundError:
                        messagebox.showerror("Kesalahan", "File data belanja tidak ditemukan")
                    except json.JSONDecodeError:
                        messagebox.showerror("Kesalahan", "File JSON tidak valid atau rusak")

                tk.Button(tambah_frame, text="Simpan", command=simpan_item_baru, width=20, height=2, bg="#82ccdd", fg="black").pack(pady=20)

                # Tombol "Kembali"
                tk.Button(tambah_frame, text="Kembali", command=self.tampilan_daftar_belanja_lama, width=20, height=2, bg="#de6262").pack(pady=10)

            # Tombol untuk Tambah Item
            tk.Button(frame, text="Tambah Item", command=tambah_item, width=20, height=2, bg="#82ccdd").pack(side="left", padx=5, pady=5)

            
            # Fungsi untuk Hapus Item
            def hapus_item():
                selected_item = detail_treeview.selection()
                if not selected_item:
                    messagebox.showerror("Kesalahan", "Pilih item yang akan dihapus")
                    return

                # Ambil data dari item yang dipilih
                values = detail_treeview.item(selected_item[0], "values")
                kategori, nama_barang, harga = values

                # Konfirmasi penghapusan
                confirm = messagebox.askyesno("Konfirmasi", f"Apakah Anda yakin ingin menghapus item '{nama_barang}'?")
                if not confirm:
                    return

                try:
                    # Konversi harga dari tampilan ke tipe float
                    harga_float = float(harga.replace("Rp ", "").replace(".", "").replace(",", "."))

                    # Cari dan hapus item dari data JSON
                    for barang in daftar_belanja['list_belanja']:
                        if (
                            barang[0] == kategori
                            and barang[1] == nama_barang
                            and barang[2] == harga_float
                        ):
                            daftar_belanja['list_belanja'].remove(barang)
                            break

                    # Simpan kembali ke file JSON
                    with open(nama_file, 'w') as f:
                        json.dump(data, f, indent=4)

                    # Hapus item dari Treeview
                    detail_treeview.delete(selected_item[0])

                    self.update_sisa_anggaran(daftar_belanja)

                    messagebox.showinfo("Berhasil", f"Item '{nama_barang}' berhasil dihapus")

                except FileNotFoundError:
                    messagebox.showerror("Kesalahan", "File data belanja tidak ditemukan")
                except json.JSONDecodeError:
                    messagebox.showerror("Kesalahan", "File JSON tidak valid atau rusak")


            # Tombol untuk Hapus Item
            tk.Button(frame, text="Hapus Item", command=hapus_item, width=12, height=2, bg="#e74c3c").pack(side="right", padx=5,pady=5)
        
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
