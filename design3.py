import tkinter as tk

# Membuat jendela utama
root = tk.Tk()
root.title("Desain Tombol Warna")

# Mendesain tombol dengan warna dan gaya dari awal
tombol = tk.Button(
    root,
    text="Klik Saya", 
    font=("Arial", 14, "bold"),  # Mengatur jenis dan ukuran font
    bg="#4CAF50",               # Warna latar belakang hijau
    fg="white",                 # Warna teks putih
    padx=20,                    # Padding horizontal
    pady=10,                    # Padding vertical
    activebackground="#45a049", # Warna latar belakang saat tombol aktif/diklik
    activeforeground="white"    # Warna teks saat tombol aktif/diklik
)
tombol.pack(pady=20)

# Menjalankan aplikasi
root.mainloop()
