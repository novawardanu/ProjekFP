import os
from datetime import datetime
import pandas as pd
from functools import reduce


os.system("cls")

layanan_dokter =  None
obat = None
jml = None   

doc = pd.read_csv("Doctors.csv")
doc = doc.set_index("DoctorID")
med = pd.read_csv("Medicines.csv")
meds = med.set_index("MedicineID")
rev = pd.read_csv("Reviews.csv")
tr = pd.read_csv("Transactions.csv")


def filter_by_specialization(df, specialist):
    return df[df["Spesialist"] == specialist]

def input_nama():
    print("=" * 30)
    print("=" * 30)
    print("    Selamat Datang di CAPER")
    print("=Consultant Apotek Elektronik=")
    print("=" * 30)
    nama = input("Nama: ")
    return nama

def beli_obat():
    global obat, jml
    print(meds)
    obat = int(input("Mau beli obat apa (Masukkan ID Obat): "))
    if obat not in meds.index:
        print("Pilihan obat tidak valid.")
        exit()
    else: 
        print(meds.loc[obat]) 
    jml = int(input("Berapa obat yang mau dibeli : "))
    return obat, jml


nama = input_nama()
layanan = int(input("""
Layanan yang tersedia :
[1] Beli Obat
[2] Konsultasi Dokter
Pilih >>> """))

if layanan == 1:
    obat, jml = beli_obat()

else:
    if layanan == 2:
        print(doc)
        specialist = input("Masukkan spesialisasi dokter yang Anda cari: ").lower()
        filtered_doctors = reduce(filter_by_specialization, [doc, specialist])

        if filtered_doctors.empty:
            print("Maaf, tidak ada dokter dengan spesialisasi tersebut.")
            exit()
        else:
            print(filtered_doctors)
            kode_dokter = int(input("Kode dokter yang akan dikonfirmasikan: "))
            if kode_dokter not in doc.index:
                print("Kode dokter tidak valid.")
                exit()
            else:
                print(doc.loc[kode_dokter])

        layanan_dokter = int(input("""
        Layanan yang tersedia :
        [1] Bertemu Langsung
        [2] Telfon Dokter
        [3] Chat Whatsapp
        Pilih >>> """))
        if layanan_dokter not in [1, 2, 3]:
            print("Pilihan layanan dokter tidak valid.")
            exit()


biaya = lambda x: meds.loc[x, 'Harga'] * jml
consul = lambda x: 250000 if x == 1 else 150000 if x == 2 else 100000

def last(nama):
    back = input("apakah anda ingin kembali ke menu awal ? (y/n) : ").lower()
    if back == "y":
        input_nama()
    elif back == "n":
        print(f"Terima kasih {nama} telah menggunakan aplikasi CAPER")
        exit()
    else :
        print("Maaf, pilihan anda tidak tersedia silahkan pilih lagi") 

def rating(nama):
    rating = int(input("Beri rating untuk layanan (1-5) : "))
    if rating < 1 or rating > 5:
        print("Rating tidak valid.")
        exit()
    komentar = input("Berikan komen untuk pelayanan : ")

    new_review = {
        "Nama Pasien": nama,
        "Rating": rating,
        "Penilaian": komentar
    }

    with open("Reviews.csv", "a") as file:
        file.write(f"{new_review['Nama Pasien']}, {new_review['Rating']}, {new_review['Penilaian']}\n")
    return f"Terima kasih, {nama}, telah memberikan penilaian."

penilaian = rating
def add_transaction(user_name, medicine_price=None, consultation_price=None):
    global biaya, consul, obat, layanan, layanan_dokter, jml

    medicine_id = obat if layanan == 1 else "Konsultasi Dokter"
    kuantitas = jml if layanan == 1 else layanan_dokter if layanan == 2 else None
    total_harga = biaya(obat) if layanan == 1 else consul(layanan_dokter) if layanan == 2 else None
    
    total_harga = total_harga if total_harga is not None else add_transaction(user_name)


    time_now = datetime.now()
    transaction_data = {
        "UserID": user_name,
        "MedicineID": medicine_id,
        "Kuantitas": kuantitas,
        "TotalHarga": total_harga,
        "Tanggal": time_now.strftime("%Y-%m-%d")
    }
    if total_harga is not None:
        with open("Transactions.csv", "a") as file:
            file.write(f"{transaction_data['UserID']},{transaction_data['MedicineID']},"
                        f"{transaction_data['Kuantitas']},{transaction_data['TotalHarga']},"
                        f"{transaction_data['Tanggal']}\n")
    return total_harga


if layanan == 1:
    print(f"{nama} membeli obat {meds.loc[obat, 'NamaObat']} sebanyak {jml}")
else:
    if layanan_dokter == 1:
        print(f"{nama} memilih Bertemu Langsung dengan dokter")
    elif layanan_dokter == 2:
        print(f"{nama} memilih Telfon Dokter")
    elif layanan_dokter == 3:
        print(f"{nama} memilih Chat Whatsapp dengan dokter")

print("=" * 50)
print("Berikut adalah detail pesanan anda")
print("NOTA DIGITAL")
print("=" * 50)
print("Waktu Pembelian Obat :", datetime.now()) if layanan == 1 else print("Waktu Consultasi Dokter : ", datetime.now())
print("Nama Pasien:", nama)
print("Jenis Layanan: Beli Obat") if layanan == 1 else print("Jenis Layanan: Consultasi Dokter")

print(f"Total Harga: Rp {biaya(obat) if layanan == 1 else consul(layanan_dokter)}")
print("=" * 50)
print(penilaian(nama))
add_transaction(nama)
# last(nama)