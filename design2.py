import tkinter as tk

# Membuat jendela utama
root = tk.Tk()
root.title("Desain Tombol Warna")

# Fungsi untuk mengganti warna tombol saat ditekan
def ganti_warna():
    tombol.config(bg="#4CAF50", fg="white")  # Warna hijau dan teks putih

# Mendesain tombol dengan warna dan style
tombol = tk.Button(
    root,
    text="Klik Saya", 
    command=ganti_warna,
    font=("Arial", 14, "bold"),  # Mengatur jenis dan ukuran font
    bg="#008CBA",               # Warna latar belakang biru
    fg="white",                 # Warna teks putih
    relief="raised",            # Efek border raised
    bd=4,                       # Border thickness
    padx=20,                    # Padding horizontal
    pady=10                     # Padding vertical
)
tombol.pack(pady=20)

# Menjalankan aplikasi
root.mainloop()
