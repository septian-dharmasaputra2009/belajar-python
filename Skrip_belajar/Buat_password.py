import re

def cek_password():
    while True:
        password = input("Masukkan password: ")
        flag = 0

        if len(password) < 8:
            flag = -1
            print("Password terlalu pendek (minimal 8 karakter).")

        elif not re.search("[a-z]", password):
            flag = -1
            print("Password harus mengandung huruf kecil.")

        elif not re.search("[A-Z]", password):
            flag = -1
            print("Password harus mengandung huruf besar.")

        elif not re.search("[0-9]", password):
            flag = -1
            print("Password harus mengandung angka.")

        else:
            flag = 0
            print("✅ Password valid!")
            break  # keluar dari while jika valid

        if flag == -1:
            print("❌ Password tidak valid. Coba lagi.\n")

# Jalankan fungsi
cek_password()
