# Mengimpor modul os untuk interaksi sistem operasi jika diperlukan
import os
# Mengimpor modul tkinter dasar untuk pembuatan komponen GUI
import tkinter as tk
# Mengimpor modul ttk untuk widget bertema (seperti Combobox & Treeview) dan messagebox untuk dialog pop-up
from tkinter import ttk, messagebox
# Mengimpor mysql.connector untuk mengendalikan koneksi dan operasi database MySQL
import mysql.connector

# --- KONEKSI DATABASE ---
def connect_db():
    return mysql.connector.connect(
        host="localhost",      
        user="root",           
        password="",           
        database="siakad"      
    )

# --- FUNGSI CRUD ---
def load_data():
    for row in tree.get_children():
        tree.delete(row)
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM dosen")
        rows = cursor.fetchall()
        for row in rows:
            tree.insert("", "end", values=row)
        db.close()
    except Exception as e:
        messagebox.showerror("Database Error", f"Gagal mengambil data: {e}")

def tambah_data():
    nip = entry_nip.get()
    nama = entry_nama.get()
    jk = combo_jk.get()
    email = entry_email.get()
    tlp = entry_tlp.get()
    pendidikan = entry_pendidikan.get()
    bidang = entry_bidang.get()

    if not nip or not nama:
        messagebox.showwarning("Warning", "NIP dan Nama Dosen wajib diisi!")
        return

    try:
        db = connect_db()
        cursor = db.cursor()
        sql = "INSERT INTO dosen (nip, nama_dosen, jenis_kelamin, email, no_telepon, pendidikan_terakhir, bidang_keahlian) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (nip, nama, jk, email, tlp, pendidikan, bidang)
        cursor.execute(sql, val)
        db.commit()
        db.close()
        messagebox.showinfo("Sukses", "Data berhasil ditambahkan!")
        clear_fields()
        load_data()
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menambah data: {e}")

def edit_data():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Pilih data di tabel yang ingin diubah!")
        return

    nip = entry_nip.get()
    nama = entry_nama.get()
    jk = combo_jk.get()
    email = entry_email.get()
    tlp = entry_tlp.get()
    pendidikan = entry_pendidikan.get()
    bidang = entry_bidang.get()

    try:
        db = connect_db()
        cursor = db.cursor()
        sql = """UPDATE dosen SET nama_dosen=%s, jenis_kelamin=%s, email=%s, 
                 no_telepon=%s, pendidikan_terakhir=%s, bidang_keahlian=%s WHERE nip=%s"""
        val = (nama, jk, email, tlp, pendidikan, bidang, nip)
        cursor.execute(sql, val)
        db.commit()
        db.close()
        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        clear_fields()
        load_data()
    except Exception as e:
        messagebox.showerror("Error", f"Gagal memperbarui data: {e}")

def hapus_data():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Pilih data di tabel yang ingin dihapus!")
        return

    nip = entry_nip.get()
    confirm = messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus dosen NIP {nip}?")
    if confirm:
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("DELETE FROM dosen WHERE nip = %s", (nip,))
            db.commit()
            db.close()
            messagebox.showinfo("Sukses", "Data berhasil dihapus!")
            clear_fields()
            load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menghapus data: {e}")

def select_item(event):
    selected = tree.selection()
    if selected:
        values = tree.item(selected[0], "values")
        clear_fields()
        entry_nip.insert(0, values[0])
        entry_nama.insert(0, values[1])
        combo_jk.set(values[2])
        entry_email.insert(0, values[3])
        entry_tlp.insert(0, values[4])
        entry_pendidikan.insert(0, values[5])
        entry_bidang.insert(0, values[6])

def clear_fields():
    entry_nip.delete(0, tk.END)
    entry_nama.delete(0, tk.END)
    combo_jk.set("")
    entry_email.delete(0, tk.END)
    entry_tlp.delete(0, tk.END)
    entry_pendidikan.delete(0, tk.END)
    entry_bidang.delete(0, tk.END)

# --- GUI MAIN WINDOW ---
root = tk.Tk()
root.title("Aplikasi Data Dosen - SIAKAD")
root.geometry("900x600")

# --- BAGIAN 1: FORM INPUT (GABUNGAN & PENYANDINGAN WIDGET) ---
frame_form = tk.LabelFrame(root, text=" Form Data Dosen ", padx=10, pady=10)
frame_form.pack(fill="x", padx=15, pady=5)

# Membuat Label dan susunan Grid secara rapi
tk.Label(frame_form, text="NIP:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
entry_nip = tk.Entry(frame_form, width=30)
entry_nip.grid(row=0, column=1, padx=5, pady=2)

tk.Label(frame_form, text="Nama Dosen:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
entry_nama = tk.Entry(frame_form, width=30)
entry_nama.grid(row=1, column=1, padx=5, pady=2)

tk.Label(frame_form, text="Jenis Kelamin:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
combo_jk = ttk.Combobox(frame_form, values=["Laki-laki", "Perempuan"], width=28, state="readonly")
combo_jk.grid(row=2, column=1, padx=5, pady=2)

tk.Label(frame_form, text="Email:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
entry_email = tk.Entry(frame_form, width=30)
entry_email.grid(row=0, column=3, padx=5, pady=2)

tk.Label(frame_form, text="No Telepon:").grid(row=1, column=2, sticky="w", padx=5, pady=2)
entry_tlp = tk.Entry(frame_form, width=30)
entry_tlp.grid(row=1, column=3, padx=5, pady=2)

tk.Label(frame_form, text="Pendidikan Terakhir:").grid(row=2, column=2, sticky="w", padx=5, pady=2)
entry_pendidikan = tk.Entry(frame_form, width=30)
entry_pendidikan.grid(row=2, column=3, padx=5, pady=2)

tk.Label(frame_form, text="Bidang Keahlian:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
entry_bidang = tk.Entry(frame_form, width=30)
entry_bidang.grid(row=3, column=1, padx=5, pady=2)

# --- BAGIAN 2: TOMBOL AKSI (BUTTONS) ---
frame_tombol = tk.Frame(root)
frame_tombol.pack(fill="x", padx=15, pady=5)

btn_tambah = tk.Button(frame_tombol, text="Tambah", command=tambah_data, bg="#4CAF50", fg="white", width=12)
btn_tambah.pack(side="left", padx=5)

btn_edit = tk.Button(frame_tombol, text="Edit / Update", command=edit_data, bg="#2196F3", fg="white", width=12)
btn_edit.pack(side="left", padx=5)

btn_hapus = tk.Button(frame_tombol, text="Hapus", command=hapus_data, bg="#F44336", fg="white", width=12)
btn_hapus.pack(side="left", padx=5)

btn_clear = tk.Button(frame_tombol, text="Clear Form", command=clear_fields, bg="#FF9800", fg="white", width=12)
btn_clear.pack(side="left", padx=5)

# --- BAGIAN 3: TABEL DATA (TREEVIEW) ---
frame_tabel = tk.Frame(root)
frame_tabel.pack(fill="both", expand=True, padx=15, pady=10)

# Membuat kolom tabel sesuai dengan data database
columns = ("nip", "nama", "jk", "email", "tlp", "pendidikan", "bidang")
tree = ttk.Treeview(frame_tabel, columns=columns, show="headings")

# Mengatur judul kolom tabel
tree.heading("nip", text="NIP")
tree.heading("nama", text="Nama Dosen")
tree.heading("jk", text="Jenis Kelamin")
tree.heading("email", text="Email")
tree.heading("tlp", text="No Telepon")
tree.heading("pendidikan", text="Pendidikan")
tree.heading("bidang", text="Bidang Keahlian")

# Mengatur lebar kolom agar pas di layar
tree.column("nip", width=80, anchor="center")
tree.column("nama", width=150)
tree.column("jk", width=90, anchor="center")
tree.column("email", width=130)
tree.column("tlp", width=100)
tree.column("pendidikan", width=110)
tree.column("bidang", width=130)

# Menambahkan Scrollbar agar tabel bisa di-scroll jika datanya banyak
scrollbar = ttk.Scrollbar(frame_tabel, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
tree.pack(fill="both", expand=True)

# Menghubungkan klik tabel ke fungsi select_item milik dosen
tree.bind("<<TreeviewSelect>>", select_item)

# Memuat data otomatis saat aplikasi pertama kali dibuka
load_data()

# Menjalankan aplikasi GUI
root.mainloop()
