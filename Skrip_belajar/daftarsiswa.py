import sqlite3
import plotext as plt

# Koneksi ke database
conn = sqlite3.connect("siswa.db")
cursor = conn.cursor()

# Buat tabel jika belum ada
cursor.execute("""
CREATE TABLE IF NOT EXISTS siswa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    nilai INTEGER NOT NULL
)
""")

# Fungsi tambah
def tambah_siswa(nama, nilai):
    cursor.execute("INSERT INTO siswa (nama, nilai) VALUES (?, ?)", (nama, nilai))
    conn.commit()

# Fungsi tampilkan
def tampilkan_siswa():
    cursor.execute("SELECT * FROM siswa")
    semua_data = cursor.fetchall()
    if semua_data:
        print("\n=== DAFTAR SISWA ===")
        for data in semua_data:
            print(f"ID: {data[0]}, Nama: {data[1]}, Nilai: {data[2]}")
    else:
        print("Belum ada data siswa.")

# Fungsi hapus
def hapus_siswa(id_siswa):
    cursor.execute("DELETE FROM siswa WHERE id = ?", (id_siswa,))
    if cursor.rowcount > 0:
        print("Data berhasil dihapus.")
    else:
        print("ID tidak ditemukan.")
    conn.commit()
    
# Fungsi ubah
def ubah_siswa(id_siswa, nama_baru, nilai_baru):
    cursor.execute("UPDATE siswa SET nama = ?, nilai = ? WHERE id = ?", (nama_baru, nilai_baru, id_siswa))
    if cursor.rowcount > 0:
        print("Data berhasil diubah.")
    else:
        print("ID tidak ditemukan.")
    conn.commit()

# Fungsi menampilkan grafik
def tampilkan_grafik():
    cursor.execute("SELECT nama, nilai FROM siswa")
    data = cursor.fetchall()
    if data:
        nama_siswa = [d[0] for d in data]
        nilai_siswa = [d[1] for d in data]

        plt.clear_data()
        plt.bar(nama_siswa, nilai_siswa)
        plt.title("Grafik Nilai Siswa")
        plt.xlabel("Nama")
        plt.ylabel("Nilai")
        plt.show()
    else:
        print("Tidak ada data untuk ditampilkan.")

# Menu utama
while True:
    print("\n=== MENU SISWA ===")
    print("1. Tambah Siswa")
    print("2. Tampilkan Semua Siswa")
    print("3. Hapus Siswa")
    print("4. Ubah Data Siswa")
    print("5. Tampilkan Grafik Nilai")
    print("6. Keluar")
    pilihan = input("Pilih menu (1/2/3/4/5/6): ")

    if pilihan == "1":
        nama = input("Masukkan nama siswa: ")
        nilai = int(input("Masukkan nilai: "))
        tambah_siswa(nama, nilai)

    elif pilihan == "2":
        tampilkan_siswa()

    elif pilihan == "3":
        tampilkan_siswa()
        try:
            id_siswa = int(input("Masukkan ID siswa yang ingin dihapus: "))
            hapus_siswa(id_siswa)
        except ValueError:
            print("ID harus berupa angka!")

    elif pilihan == "4":
        tampilkan_siswa()
        try:
            id_siswa = int(input("Masukkan ID siswa yang ingin diubah: "))
            nama_baru = input("Masukkan nama baru: ")
            nilai_baru = int(input("Masukkan nilai baru: "))
            ubah_siswa(id_siswa, nama_baru, nilai_baru)
        except ValueError:
            print("Input tidak valid!")
            
    elif pilihan == "5":
        tampilkan_grafik()

    elif pilihan == "6":
        print("Keluar dari program.")
        break

    else:
        print("Pilihan tidak valid!")

conn.close()
