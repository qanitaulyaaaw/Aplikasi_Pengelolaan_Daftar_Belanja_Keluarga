import tkinter as tk

# Membuat jendela utama
root = tk.Tk()
root.title("Contoh Ganti Warna Tombol")

# Fungsi untuk mengganti warna tombol saat ditekan
def ganti_warna():
    tombol.config(bg="blue", fg="white")  # Ganti warna latar belakang dan teks

# Membuat tombol dengan warna default
tombol = tk.Button(root, text="Klik Saya", command=ganti_warna)
tombol.pack(pady=20)

# Menjalankan aplikasi
root.mainloop()
