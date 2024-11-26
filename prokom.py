import csv
import os
from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime

# Global variables
current_frame = None
current_budget = 0
current_category_budget = 0
shopping_list_items = []
shopping_list_title = ""
shopping_list_date = ""
current_category = ""

# Create necessary CSV files
def create_tables():
    # User data table
    if not os.path.exists('user_data.csv'):
        with open('user_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'username', 'email', 'password'])
    
    # Budget data table
    if not os.path.exists('budget_data.csv'):
        with open('budget_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['total_budget', 'category', 'category_budget'])
    
    # Shopping history table
    if not os.path.exists('old_shopping_list.csv'):
        with open('old_shopping_list.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['title', 'date', 'total_spent', 'category'])

# Switch to a new frame
def switch_frame(new_frame):
    global current_frame
    if current_frame is not None:
        current_frame.destroy()
    current_frame = new_frame
    current_frame.pack(fill="both", expand=True)

# Welcome frame
def show_welcome_frame():
    welcome_frame = Frame(root)
    Label(welcome_frame, text="Selamat Datang di Aplikasi Belanja!", font=("Arial", 14)).pack(pady=20)
    Button(welcome_frame, text="Mulai", font=("Arial", 12), command=show_menu_frame).pack(pady=10)
    switch_frame(welcome_frame)

# Main menu frame
def show_menu_frame():
    menu_frame = Frame(root)
    Label(menu_frame, text="Menu Utama", font=("Arial", 14)).pack(pady=20)
    Button(menu_frame, text="Atur Anggaran", font=("Arial", 12), command=show_set_budget_frame).pack(pady=10)
    Button(menu_frame, text="Keluar", font=("Arial", 12), command=root.quit).pack(pady=10)
    switch_frame(menu_frame)

# Budget setting frame
def show_set_budget_frame():
    global total_budget_entry, category_var, category_budget_entry
    budget_frame = Frame(root)
    
    Label(budget_frame, text="Atur Anggaran Belanja", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)
    
    Label(budget_frame, text="Total Anggaran (Rp):", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
    total_budget_entry = Entry(budget_frame, font=("Arial", 12))
    total_budget_entry.grid(row=1, column=1, padx=10, pady=5)
    
    Label(budget_frame, text="Kategori Belanja:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=10, pady=5)
    categories = ["Makanan", "Transportasi", "Utilitas", "Hiburan", "Lainnya"]
    category_var = StringVar(value=categories[0])
    category_dropdown = OptionMenu(budget_frame, category_var, *categories)
    category_dropdown.grid(row=2, column=1, padx=10, pady=5)
    
    Label(budget_frame, text="Anggaran Kategori (Rp):", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=10, pady=5)
    category_budget_entry = Entry(budget_frame, font=("Arial", 12))
    category_budget_entry.grid(row=3, column=1, padx=10, pady=5)
    
    Button(budget_frame, text="Simpan", font=("Arial", 12), command=save_budget).grid(row=4, column=0, columnspan=2, pady=10)
    Button(budget_frame, text="Kembali", font=("Arial", 12), command=show_menu_frame).grid(row=5, column=0, columnspan=2, pady=5)
    
    switch_frame(budget_frame)

def save_budget():
    global current_budget, current_category_budget, current_category
    try:
        total_budget = float(total_budget_entry.get())
        category_budget = float(category_budget_entry.get())
        category = category_var.get()
        
        if total_budget <= 0 or category_budget <= 0:
            raise ValueError("Anggaran harus lebih besar dari 0.")
        if category_budget > total_budget:
            raise ValueError("Anggaran kategori tidak boleh melebihi total anggaran.")
        
        current_budget = total_budget
        current_category_budget = category_budget
        current_category = category
        
        with open('budget_data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_budget, current_category, current_category_budget])
        
        shopping_list_items.clear()
        show_shopping_list_title_frame()
    
    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Shopping list title frame
def show_shopping_list_title_frame():
    global shopping_list_title, shopping_list_date
    title_frame = Frame(root)
    
    Label(title_frame, text="Buat Daftar Belanja", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)
    
    Label(title_frame, text="Judul Daftar:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    title_entry = Entry(title_frame, font=("Arial", 12))
    title_entry.grid(row=1, column=1, padx=10, pady=5)
    
    Label(title_frame, text="Tanggal:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
    date_entry = Entry(title_frame, font=("Arial", 12))
    date_entry.insert(0, datetime.now().strftime("%d-%m-%Y"))
    date_entry.grid(row=2, column=1, padx=10, pady=5)
    
    def proceed():
        nonlocal shopping_list_title, shopping_list_date
        shopping_list_title = title_entry.get()
        shopping_list_date = date_entry.get()
        
        if not shopping_list_title:
            messagebox.showerror("Error", "Judul daftar belanja harus diisi!")
        else:
            show_shopping_item_entry_frame()
    
    Button(title_frame, text="Lanjutkan", font=("Arial", 12), command=proceed).grid(row=3, column=0, columnspan=2, pady=10)
    switch_frame(title_frame)

# Shopping item entry frame
def show_shopping_item_entry_frame():
    item_frame = Frame(root)
    
    Label(item_frame, text="Tambah Barang", font=("Arial", 14)).grid(row=0, column=0, columnspan=3, pady=10)
    
    Label(item_frame, text="Nama Barang:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    item_name_entry = Entry(item_frame, font=("Arial", 12))
    item_name_entry.grid(row=1, column=1, padx=10, pady=5)
    
    Label(item_frame, text="Harga (Rp):", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
    item_price_entry = Entry(item_frame, font=("Arial", 12))
    item_price_entry.grid(row=2, column=1, padx=10, pady=5)
    
    def add_item():
        try:
            item_name = item_name_entry.get()
            item_price = float(item_price_entry.get())
            if not item_name or item_price <= 0:
                raise ValueError("Nama barang harus diisi dan harga lebih dari 0.")
            
            shopping_list_items.append({'name': item_name, 'price': item_price})
            messagebox.showinfo("Sukses", f"Barang '{item_name}' ditambahkan!")
            item_name_entry.delete(0, END)
            item_price_entry.delete(0, END)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    Button(item_frame, text="Tambah", font=("Arial", 12), command=add_item).grid(row=3, column=0, columnspan=2, pady=10)
    Button(item_frame, text="Selesai", font=("Arial", 12), command=show_menu_frame).grid(row=4, column=0, columnspan=2, pady=5)
    switch_frame(item_frame)

# Main application
root = Tk()
root.title("Aplikasi Pengelolaan Belanja")
root.geometry("500x400")

create_tables()
show_welcome_frame()

root.mainloop()
