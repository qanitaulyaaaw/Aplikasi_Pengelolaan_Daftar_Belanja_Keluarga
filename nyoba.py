# Analisis Daftar Belanja dan Anggaran
daftar_belanja = []
total_harga = 0
budget = float(input("Masukkan anggaran keluarga yang tersedia: "))

def display_menu():
    print("\n=== Menu Pengelolaan Daftar Belanja ===")
    print("1. Tambah Item")
    print("2. Hapus Item")
    print("3. Lihat Daftar Belanja")
    print("4. Cek Sisa Anggaran")
    print("5. Selesai")
    return input("Pilih menu (1-5): ")

def add_item():
    global total_harga
    item = input("Nama item: ")
    price = float(input("Harga item: "))
    daftar_belanja.append((item, price))
    total_harga += price
    print(f"{item} telah ditambahkan.")

def remove_item():
    global total_harga
    item = input("Nama item yang dihapus: ")
    for i, (nama, harga) in enumerate(daftar_belanja):
        if nama.lower() == item.lower():
            total_harga -= harga
            daftar_belanja.pop(i)
            print(f"{item} telah dihapus.")
            return
    print(f"{item} tidak ditemukan.")

def view_daftar_belanja():
    print("\n=== Daftar Belanja ===")
    for item, price in daftar_belanja:
        print(f"- {item}: Rp{price}")
    print(f"Total: Rp{total_harga}")

def check_budget():
    sisa = budget - total_harga
    print(f"Sisa anggaran: Rp{sisa}")
    print("Status:", "Anggaran cukup." if sisa >= 0 else "Anggaran kurang.")

def main():
    while True:
        choice = display_menu()
        if choice == '1':
            add_item()
        elif choice == '2':
            remove_item()
        elif choice == '3':
            view_daftar_belanja()
        elif choice == '4':
            check_budget()
        elif choice == '5':
            view_daftar_belanja()
            print("Terima kasih telah menggunakan aplikasi ini!")
            break
        else:
            print("Pilihan tidak valid.")

main()