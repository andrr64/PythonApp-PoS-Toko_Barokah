# MODUL STANDAR
import copy
import os
import datetime as dt
import contextlib
import json
from hashlib import sha256

# VARIABEL SPESIAL
__main__    = False    # Variabel ini digunakan untuk menentukan apakah program akan masuk ke program utama (jika bernilai True) atau tidak (False)
__data__    = None     # Variabel ini digunakan untuk menampung data dari file Data/data.json

# VARIABEL GLOBAL
PRODUK      = {
    'nama'   : None,
    'harga'  : 0.0,
    'stok'   : 0,
    'dibeli' : 0,
    'id'     : None
}
TRANSAKSI   = {
    'barang'        : [],
    'kuantitas'     : [],
    'harga_barang'  : [],
    'id'            : "",
    'id_produk'     : [],
    'total_harga'   : 0.0,
    'total_barang'  : 0,
    'pembayaran'    : 0.0,
    'kembalian'     : 0.0,
    'waktu' : None
}
BULAN       = {
    '01': 'Januari',
    '02': 'Februari',
    '03': 'Maret',
    '04': 'April',
    '05': 'Mei',
    '06': 'Juni',
    '07': 'Juli', 
    '08': 'Agustus',
    '09': 'September', 
    '10': 'Oktober', 
    '11': 'November', 
    '12': 'Desember'
}
LEBAR       = 100
TEKS_BORDER = LEBAR-6
PANJANG_NAMA_PRODUK = int(LEBAR/2)
user_input  = None

# METHOD GLOBAL
def clear():
    os.system('cls')
def garis(motif = '='):
    print(motif*LEBAR)
def print_sentral(string : str):
    print(f"|| {string.center(TEKS_BORDER)} ||")
def print_kiri(string : str):
    print(f"|| {string.ljust(TEKS_BORDER)} ||")
def input_user(text : str):
    global user_input
    user_input = input(text)
def peringatan(*args):
    clear()
    garis()
    for pesan in args:
        print_sentral(pesan)
    garis()
    input_user("Ketik apa saja untuk kembali : ")
def ambil_waktu() -> str:
    return (str(dt.datetime.now().strftime("%Y-%m-%d %H:%M")))
def ambil_data():
    global __data__
    with open("Data/data.json", 'r') as file:
        __data__ = json.load(file)
def update_data():
    global __data__
    with open("Data/data.json", 'w') as file:
        json.dump(__data__, file, indent=4, sort_keys=True)
def get_hash(string : str) -> str:
    return sha256(str(string).encode('utf-8')).hexdigest()
def ambil_waktu() -> str:
    return (str(dt.datetime.now().strftime("%Y-%m-%d %H:%M")))

# PROGRAM 
# a. Pengecekan Modul eksternal dan data 
while True:
    try:
        import matplotlib.pyplot as plt
        __main__ = True
        break
    except ModuleNotFoundError:
        clear()
        garis()
        print_kiri("Anda belum menginstall beberapa modul yang diperlukan :")
        print_kiri("~ Matplotlib")
        print_kiri('')
        print_kiri("Jika anda terjebak di tahap ini, silahkan install modul secara manual")
        garis()
        input_user("Ingin menginstall modul? [y/n] : ")
        if user_input in ['y', 'Y']:
            clear()
            garis()
            print_kiri("Menginstall NumPy..................")
            garis()
            os.system('pip install numpy')
            clear()
            garis()
            print_kiri("Menginstall Matplotlib.............")
            garis()
            os.system('pip install matplotlib')
            clear()
        else:
            clear()
            peringatan('Program ini tidak dapat berjalan.....')
            break
        
# b. Program Utama
if __main__ == True:

    # Membuat folder "Data"
    with contextlib.suppress(FileExistsError):
        os.mkdir("Data")
    
    # Mengecek file "data.json" pada folder "Data"
    try:
        with open("Data/data.json", 'r') as file:
            pass
    except FileNotFoundError:
        with open("Data/data.json", 'w') as file:
            json.dump(
                {
                    'produk': [],
                    'transaksi': [],
                    'nama_toko': 'none',
                    'tanggal_hari_ini' : ambil_waktu(),
                    'pendapatan_hari_ini': 0.0,
                    'penjualan_hari_ini': 0
                }, file)

    # Mengambil data dari file "Data/data.json"
    ambil_data()

    # Mengecek nama toko
    if __data__['nama_toko'] == "none":
        clear()
        garis()
        print_sentral("Nama toko tidak ada...")
        garis()
        input_user("Masukkan nama toko : ")
        __data__['nama_toko'] = user_input
        update_data()
        clear()
        peringatan("Nama Toko Berhasil Disimpan")

    # METHOD PROGRAM
    def prg_panjang_data(data) -> int:
        return len(data)
    def prg_panjang_halaman(panjang_data) -> int:
        return  1 if panjang_data <= 15 else (
                int(panjang_data/15) if panjang_data % 15 == 0 else int(panjang_data/15)+1
            )
    def prg_print_detail_data_produk(data, indeks):
        clear( )
        garis( )
        print_sentral("DATA PRODUK")
        garis("-")
        print_kiri(f"Nama    : {data[indeks]['nama']}")
        print_kiri(f"Harga   : Rp {data[indeks]['harga']:,.0f}")
        print_kiri(f"Stok    : {data[indeks]['stok']}")
        print_kiri(f"ID      : {data[indeks]['id']}")
        garis( )
    def prg_print_detail_data_transaksi(id_transaksi : int, mode=1, indeks = None):
        ambil_data()
        if mode == 1:
            data_transaksi = None
            for i in __data__['transaksi']:
                if i['id'] == id_transaksi:
                    data_transaksi = i
                    break
            if data_transaksi is None:
                peringatan('ID TRANSAKSI TIDAK DITEMUKAN!')
            else:
                clear()
                garis()
                print_sentral(f'DATA TRANSAKSI ID {id_transaksi}')
                garis()
                print_kiri(f'{"No".ljust(5)}  |  {"Nama".center(PANJANG_NAMA_PRODUK)}  |  {"HARGA".center(15)}  |  {"PCS".center(5)} ')
                garis('-')
                for i in range(len(data_transaksi['barang'])):
                    harga = f"{data_transaksi['harga_barang'][i]:,.0f}"
                    print_kiri(f"{str(i+1).ljust(5)}  |  {str(data_transaksi['barang'][i]).ljust(PANJANG_NAMA_PRODUK)}  |  {str(harga).ljust(15)}  |  {str(data_transaksi['kuantitas'][i]).ljust(5)} ")
                garis('-')
                print_kiri(f"Total Harga  : Rp {data_transaksi['total_harga']:,.0f}")
                print_kiri(f"Pembayaran   : Rp {data_transaksi['pembayaran']:,.0f}")
                print_kiri(f"Kembalian    : Rp {data_transaksi['kembalian']:,.0f}")
                print_kiri(f"Waktu        : {data_transaksi['waktu']}")
                garis()
                input_user('Ketik apa saja untuk kembali : ')
        else:
            data_transaksi = __data__['transaksi'][indeks]
            clear()
            garis()
            print_sentral(f'DATA TRANSAKSI ID {id_transaksi}')
            garis()
            print_kiri(f'{"No".ljust(5)}  |  {"Nama".center(PANJANG_NAMA_PRODUK)}  |  {"HARGA".center(15)}  |  {"PCS".center(5)} ')
            garis('-')
            for i in range(len(data_transaksi['barang'])):
                harga = f"{data_transaksi['harga_barang'][i]:,.0f}"
                print_kiri(f"{str(i+1).ljust(5)}  |  {str(data_transaksi['barang'][i]).ljust(PANJANG_NAMA_PRODUK)}  |  {str(harga).ljust(15)}  |  {str(data_transaksi['kuantitas'][i]).ljust(5)} ")
            garis('-')
            print_kiri(f"Total Harga  : Rp {data_transaksi['total_harga']:,.0f}")
            print_kiri(f"Pembayaran   : Rp {data_transaksi['pembayaran']:,.0f}")
            print_kiri(f"Kembalian    : Rp {data_transaksi['kembalian']:,.0f}")
            print_kiri(f"Waktu        : {data_transaksi['waktu']}")
            garis()
    def prg_print_data_transaksi_range(data, start, end):
        clear()
        garis()
        print_sentral("DATA TRANSAKSI")
        garis()
        print_kiri(f"{'ID'.center(6)} | {'TOTAL HARGA'.center(15)} | {'PEMBAYARAN'.center(15)} | {'KEMBALIAN'.center(15)} | {'PCS'.center(5)}")
        garis('-')
        for i in range(start, end):
            try:
                total_harga = f"{data[i]['total_harga'] : ,.0f}"
                pembayaran = f"{data[i]['pembayaran'] : ,.0f}"
                kembalian = f"{data[i]['kembalian'] : ,.0f}"
                print_kiri(f"{str(data[i]['id']).ljust(6)} | {str(total_harga).ljust(15)} | {str(pembayaran).ljust(15)} | {str(kembalian).ljust(15)} | {str(data[i]['total_barang']).ljust(5)}")
            except IndexError:
                break
        garis('-')
    def prg_print_data_produk_range(data, start, end):
        garis()
        print_sentral('DATA PRODUK')
        garis()
        print_sentral(f' {"No".ljust(4)} | {"Nama".center(PANJANG_NAMA_PRODUK)} | {"Harga (Rp)".center(15)} | {"Stok".center(6)} | {"Dibeli".center(6)} ')
        garis('-')
        for i in range(start, end):
            try:
                harga = f"{data[i]['harga']:,.0f}"
                print_sentral(f' {str(i+1).ljust(4)} | {str(data[i]["nama"]).ljust(PANJANG_NAMA_PRODUK)} | {harga.ljust(15)} | {str(data[i]["stok"]).ljust(6)} | {str(data[i]["dibeli"]).ljust(6)} ')
            except IndexError:
                break
        garis('-')
    def prg_print_grafik(x, y, judul, ylabel):
        y_min = min(y)
        y_max = max(y)
        y_rata_rata = sum(y) / len(y)
        graph   = plt
        setting = graph.figure()
        setting.set_figwidth(15)
        setting.set_figheight(9)
        graph.plot(x,y, color='#0D4C92', label=ylabel)
        graph.plot([x[0],x[-1]], [y_min,y_min], color='red', label='Terendah', linewidth=1)
        graph.plot([x[0],x[-1]], [y_max,y_max], color='green', label='Tertinggi', linewidth=1)
        graph.plot([x[0],x[-1]], [y_rata_rata,y_rata_rata], color='black', label='Rata-Rata',linewidth=1)
        graph.plot([x[0],x[-1]], [y[0],y[-1]], color='#0D4C92', label='Trend', linewidth = 1.5, alpha = 0.35)
        graph.title(judul)
        graph.legend([ylabel, 'Terendah', 'Tertinggi', 'Rata-Rata', 'Trend'], loc = 'upper center', bbox_to_anchor = (0.5, -0.05), fancybox=True,ncol = 5 )
        graph.plot(x, y, 'o', color="#FF6464")
        graph.ylabel(ylabel, fontsize=13)
        graph.show()

    def prg_menu_utama():
        ambil_data()
        hari_ini = str(dt.datetime.now().strftime("%Y-%m-%d")) 
        if hari_ini != __data__['tanggal_hari_ini'] :
            __data__['tanggal_hari_ini']    = hari_ini
            __data__['pendapatan_hari_ini'] = 0.0
            __data__['penjualan_hari_ini']  = 0 
            update_data()
        clear()
        garis()
        print_sentral(__data__['nama_toko'])
        garis('-')
        print_kiri(f"Pendapatan hari ini  : Rp {__data__['pendapatan_hari_ini']:,.0f}")
        print_kiri(f"Penjualan hari ini   : {__data__['penjualan_hari_ini']} Unit")
        garis('-')
        print_sentral("MENU PROGRAM")
        print_kiri('1. Tambah Data Produk')
        print_kiri('2. Tambah Data Transaksi (Mode Kasir)')
        print_kiri('3. List Data Produk')
        print_kiri('4. List Data Transaksi')
        print_kiri('5. Grafik')
        print_kiri('6. Update Data')
        print_kiri('i. Info program')
        print_kiri('e. Keluar')
        garis()

    def prg_tambah_data_produk():
        global __data__
        while True:
            while True:
                ambil_data()
                exit_ = False
                add_data_success = False
                input_data_produk = copy.deepcopy(PRODUK)
                # 1. Memasukkan nama
                clear()
                garis()
                print_sentral('NAMA PRODUK')
                garis('-')
                print_sentral("Masukkan Nama Produk Anda")
                garis()
                nama_produk = input('Nama Produk\t: ')
                    # 1.1 Mengecek apakah panjang nama lebih dari PANJANG_NAMA_PRODUK atau tidak
                if len(nama_produk) > PANJANG_NAMA_PRODUK:
                    # Jika iya
                    peringatan(f'NAMA PRODUK MAKSIMAL {PANJANG_NAMA_PRODUK} karakter !')
                    exit_ = True
                    break

                    # 1.2 Mengecek apakah user tidak memasukkan nama
                elif nama_produk == " "*len(nama_produk):
                    # Jika iya
                    peringatan('MASUKKAN SEBUAH NAMA!')
                    exit_ = True    
                    break

                # 2. Memasukkan Harga Produk
                clear()
                garis()
                print_sentral('HARGA PRODUK')
                garis('-')
                print_sentral('MASUKKAN HARGA PRODUK TANPA KOMA (,)')
                print_sentral('Contoh : 10000, 20000.25, 3000000')
                garis('-')
                try:
                    harga_produk = float(input('Harga Produk (Rp) : '))
                except ValueError:
                    peringatan('MASUKKAN SEBUAH ANGKA!')
                    exit_ = True
                    break
                    # 2.1 Cek apakah user memasukkan harga kurang dari sama dengan 0
                if harga_produk <= 0:
                    peringatan('MINIMAL HARGA PRODUK ADALAH Rp 1 !')
                    exit_ = True
                    break

                # 3. Memasukkan Stok Tersedia Produk
                clear()
                garis()
                print_sentral('STOK PRODUK')
                garis('-')
                print_sentral("Masukkan Jumlah Stok Produk Anda")
                garis()
                try:
                    stok_produk = int(input('Stok Produk : '))
                except ValueError:
                    peringatan('STOK PRODUK BERUPA BILANGAN BULAT!')
                    exit_ = True
                    break

                # 4. Konfirmasi Data
                clear()
                garis()
                print_sentral('DATA PRODUK BARU')
                garis('-')
                print_kiri(f'Nama  : {nama_produk}')
                print_kiri(f'Harga : Rp {harga_produk:,.2f}')
                print_kiri(f'Sto   : {stok_produk}')
                garis('-')
                input_user('Apakah data sudah benar? [y/n] : ')
                if user_input == 'y':
                    input_data_produk.update({'nama'   : nama_produk})
                    input_data_produk.update({'harga'  : harga_produk})
                    input_data_produk.update({'stok'   : stok_produk})
                    input_data_produk.update({'dibeli' : 0})
                    input_data_produk.update({'id'     : get_hash(str(dt.datetime.today()))})
                    __data__['produk'].append(input_data_produk)
                    update_data()
                    add_data_success = True
                else:
                    exit_ = True
                break

            if exit_:
                exit_ = False
                clear()
                garis()
                print_sentral('INGIN MENGISI DATA PRODUK KEMBALI ?')
                garis()
                input_user('y/n : ')
                if user_input == 'y':
                    continue
                else:
                    break
            elif add_data_success:
                peringatan('DATA BERHASIL DITAMBAH!')
                break
    def prg_tambah_data_transaksi():
        ambil_data()
        if len(__data__['produk']) == 0:
            clear()
            garis()
            print_sentral(" ")
            print_sentral("ANDA TIDAK MEMILIKI SATUPUN PRODUK")
            print_sentral("SILAHKAN TAMBAH DATA PRODUK")
            print_sentral(" ")
            garis()
            input_user('Ketik apa saja untuk kembali : ')
        else:
            data_transaksi_baru = copy.deepcopy(TRANSAKSI)
            while True:
                try:
                    id_transaksi = int(__data__['transaksi'][-1]['id']) + 1
                except IndexError:
                    id_transaksi = 1
                clear()
                garis()
                print_sentral("MODE KASIR")
                print_sentral(f"TRANSAKSI ID : {id_transaksi}")
                garis()
                if len(data_transaksi_baru['barang']) == 0:
                    print_sentral(" ")
                    print_sentral("TIDAK ADA BARANG")
                    print_sentral(" ")
                else:
                    print_sentral(f"{'No'.center(4)}| {'Nama'.center(PANJANG_NAMA_PRODUK-10)} | {'Harga'.center(15)} | {'Pcs'.center(4)} | {'Total'.center(15)}")
                    garis('-')
                    for i in range(len(data_transaksi_baru['barang'])):
                        total = f"{data_transaksi_baru['harga_barang'][i]*data_transaksi_baru['kuantitas'][i]:,.0f}"
                        harga = f"{data_transaksi_baru['harga_barang'][i]:,.0f}"
                        print_kiri(f"{str(i+1).ljust(5)} | {str(data_transaksi_baru['barang'][i]).ljust(PANJANG_NAMA_PRODUK-10)} | {str(harga).ljust(15)} | {str(data_transaksi_baru['kuantitas'][i]).ljust(4)} | {str(total).ljust(15)}")
                    garis('-')
                    print_kiri(f"Total Biaya : Rp {data_transaksi_baru['total_harga']:,.0f}")
                garis('-')
                print_sentral("COMMAND")
                print_sentral("s : search product  |  q : save  | x : save then exit")
                print_sentral("e : exit (data loss) | u : ubah data transaksi")
                garis()
                input_user('Command [s/q/x/e] : ')
                if user_input   == 's':
                    while True:
                        clear()
                        garis()
                        print_sentral('TAMBAH TRANSAKSI VIA SEARCH MODE')
                        garis('-')
                        print_sentral('COMMAND')
                        print_sentral('$ : exit')
                        garis()
                        input_user('Nama produk / Command [$] : ')
                        if user_input == '$':
                            break
                        search_NAME = user_input
                        search_DATA = [i for i in __data__['produk'] if search_NAME in i['nama'] or search_NAME.upper() in i['nama'] or search_NAME.lower() in i['nama'] or search_NAME.title() in i['nama']]
                        if len(search_DATA) == 0:
                            peringatan('NAMA PRODUK YANG ANDA CARI TIDAK DITEMUKAN!')
                        else:
                            search_DATA_PANJANG         = prg_panjang_data(search_DATA)
                            search_DATA_PANJANG_HALAMAN = prg_panjang_halaman(search_DATA_PANJANG)
                            if search_DATA_PANJANG_HALAMAN == 1:
                                while True:
                                    clear()
                                    prg_print_data_produk_range(search_DATA, 0, 15)
                                    print_sentral('COMMAND')
                                    print_sentral('e : kembali')
                                    garis()
                                    input_user('Produk No/Command [e] : ')
                                    if user_input == 'e':
                                        break
                                    else:
                                        try:
                                            indeks = int(user_input)-1
                                            if indeks >= len(search_DATA) or indeks <= -1:
                                                peringatan('ANDA SALAH MEMILIH NOMOR PRODUK!')
                                                continue
                                            elif search_DATA[indeks]['stok']== 0:
                                                peringatan('STOK PRODUK YANG ANDA PILIH KOSONG')
                                            else:
                                                clear()
                                                garis()
                                                prg_print_detail_data_produk(search_DATA, indeks)
                                                print_sentral('COMMAND')
                                                print_sentral('s : search another product')
                                                garis()
                                                input_user('Kuantitas/Command [s] : ')
                                                if user_input == 's':
                                                    break
                                                else:
                                                    try:
                                                        kuantitas = int(user_input)
                                                        if kuantitas <= 0:
                                                            peringatan('KUANTITAS MINIMAL 1 !')
                                                        elif kuantitas > search_DATA[indeks]['stok']:
                                                            peringatan(f'MAKSIMAL PEMBELIAN ADALAH {search_DATA[indeks]["stok"]}')
                                                        else:
                                                            data_transaksi_baru['barang'].      append(search_DATA[indeks]['nama'])
                                                            data_transaksi_baru['harga_barang'].append(search_DATA[indeks]['harga'])
                                                            data_transaksi_baru['kuantitas'].   append(kuantitas)
                                                            data_transaksi_baru['total_harga']  += kuantitas*search_DATA[indeks]['harga']
                                                            data_transaksi_baru['total_barang'] += kuantitas
                                                            search_DATA[indeks]['stok']         -= kuantitas
                                                            search_DATA[indeks]['dibeli']       += kuantitas
                                                            data_transaksi_baru['id']            = id_transaksi
                                                            peringatan('DATA BERHASIL DITAMBAH')
                                                            break
                                                    except ValueError:
                                                        peringatan("INPUT SEBUAH ANGKA!")
                                        except ValueError:
                                            peringatan("PILIHAN TIDAK DITEMUKAN!")
                            else:
                                halaman_ke = 1
                                start = 0
                                while True:
                                    clear()
                                    prg_print_data_produk_range(search_DATA, start, halaman_ke*15)
                                    if halaman_ke == 1:
                                        print_sentral('COMMAND')
                                        print_sentral('n : next | e : exit')
                                        garis()
                                        input_user('Produk Nomor/Command [n/e] : ')
                                        if user_input == 'e':
                                            break
                                        elif user_input == 'n':
                                            halaman_ke  += 1
                                            start       += 15
                                            continue
                                        else:
                                            pass
                                    elif 1 < halaman_ke < search_DATA_PANJANG_HALAMAN:
                                        print_sentral('COMMAND')
                                        print_sentral('n : next | e : exit | b : back')
                                        garis()
                                        input_user('Produk Nomor/Command [n/e/b] : ')
                                        if user_input == 'e':
                                            break
                                        elif user_input == 'n':
                                            halaman_ke  += 1
                                            start       += 15
                                            continue
                                        elif user_input == 'b':
                                            halaman_ke  -= 1
                                            start       -= 15
                                            continue
                                        else:
                                            pass
                                    elif halaman_ke == search_DATA_PANJANG_HALAMAN:
                                        print_sentral('COMMAND')
                                        print_sentral('e : exit | b : back')
                                        garis()
                                        input_user('Produk Nomor/Command [e/b] : ')
                                        if user_input == 'e':
                                            break
                                        elif user_input == 'b':
                                            halaman_ke  -= 1
                                            start       -= 15
                                            continue
                                        else:
                                            pass
                                   
                                    try:
                                        indeks = int(user_input)-1
                                        if indeks >= search_DATA_PANJANG or indeks < 0 or indeks < (halaman_ke-1)*15 or indeks > (halaman_ke+1)*15:
                                            peringatan("PRODUK YANG ANDA PILIH TIDAK DITEMUKAN")
                                        else:
                                            if search_DATA[indeks]['stok'] == 0:
                                                peringatan("STOK PRODUK KOSONG")
                                                continue
                                            while True:
                                                clear()
                                                garis()
                                                print_sentral("COMMAND")
                                                prg_print_detail_data_produk(search_DATA, indeks)
                                                print_sentral("s : cari produk lain")
                                                garis()
                                                input_user("Kuantitas/Command [s] : ")
                                                if user_input == 's':
                                                    break
                                                else:
                                                    try:
                                                        kuantitas = int(user_input)
                                                        if kuantitas <= 0:
                                                            peringatan("MINIMAL PEMBELIAN ADALAH 1 UNIT")
                                                        elif kuantitas > search_DATA[indeks]['stok']:
                                                            peringatan(f" MAKSIMAL PEMBELIAN ADALAH {search_DATA[indeks]['stok']} Unit")
                                                        else:
                                                            data_transaksi_baru['barang'].      append(search_DATA[indeks]['nama'])
                                                            data_transaksi_baru['harga_barang'].append(search_DATA[indeks]['harga'])
                                                            data_transaksi_baru['kuantitas'].   append(kuantitas)
                                                            data_transaksi_baru['total_harga']  += kuantitas*search_DATA[indeks]['harga']
                                                            data_transaksi_baru['total_barang'] += kuantitas
                                                            search_DATA[indeks]['dibeli']       += kuantitas
                                                            search_DATA[indeks]['stok']         -= kuantitas
                                                            peringatan("PRODUK BERHASIL DITAMBAHKAN")
                                                            break
                                                    except ValueError:
                                                        peringatan("COMMAND TIDAK DITEMUKAN")
                                    except ValueError:
                                        peringatan("NOMOR PRODUK YANG ANDA INPUT TIDAK DITEMUKAN")                                     
                elif user_input in 'qx':
                    exit__ = user_input == 'x'
                    if len(data_transaksi_baru['barang']) == 0:
                        peringatan("TIDAK ADA DATA TRANSAKSI!")
                    else:
                        clear()
                        garis()
                        print_sentral("DETAIL TRANSAKSI")
                        garis()
                        print_sentral(f"{'No'.center(5)} | {'Nama'.center(PANJANG_NAMA_PRODUK-10)} | {'Harga'.center(15)} | {'pcs'.center(4)} | {'Total'.center(15)}")
                        garis('-')
                        for i in range(len(data_transaksi_baru['barang'])):
                            total = f"{data_transaksi_baru['harga_barang'][i]*data_transaksi_baru['kuantitas'][i]:,.0f}"
                            harga = f"{data_transaksi_baru['harga_barang'][i]:,.0f}"
                            print_kiri(f"{str(i+1).ljust(5)} | {str(data_transaksi_baru['barang'][i]).ljust(PANJANG_NAMA_PRODUK-10)} | {str(harga).ljust(15)} | {str(data_transaksi_baru['kuantitas'][i]).ljust(4)} | {str(total).ljust(15)}")
                        garis('-')
                        print_kiri(f"Total Biaya : Rp {data_transaksi_baru['total_harga']:,.0f}")
                        garis()
                        try:
                            pembayaran = float(input("Pembayaran : "))
                            if pembayaran <= 0:
                                peringatan("MINIMAL PEMBAYARAN ADALAH RP 1")
                            elif pembayaran < data_transaksi_baru['total_harga']:
                                peringatan("UANG PEMBAYARAN KURANG!")
                            else:
                                data_transaksi_baru['id']           = id_transaksi
                                data_transaksi_baru['waktu']        = ambil_waktu()
                                data_transaksi_baru['total_barang'] = sum(data_transaksi_baru['kuantitas'])
                                data_transaksi_baru['pembayaran']   = pembayaran
                                data_transaksi_baru['kembalian']    = pembayaran - data_transaksi_baru['total_harga']
                                __data__['transaksi'].append(data_transaksi_baru)
                                __data__['pendapatan_hari_ini'] += data_transaksi_baru['total_harga']
                                __data__['penjualan_hari_ini']  += data_transaksi_baru['total_barang']
                                clear()
                                garis()
                                print_sentral('TRANSAKSI BERHASIL')
                                garis()
                                print_kiri(f'TOTAL        : Rp {data_transaksi_baru["total_harga"]:,.0f}')
                                print_kiri(f'PEMBAYARAN   : Rp {pembayaran:,.0f}')
                                print_kiri(f"KEMBALIAN    : Rp {pembayaran-data_transaksi_baru['total_harga']:,.0f}")
                                print_kiri(f"WAKTU        : {ambil_waktu()}")
                                garis()
                                input('Ketik apa saja untuk kembali : ')
                                update_data()
                                ambil_data()
                                data_transaksi_baru = copy.deepcopy(TRANSAKSI)
                                if exit__:
                                    break
                        except ValueError:
                            peringatan("MASUKKAN SEBUAH ANGKA")
                elif user_input == 'e':
                    break
                elif user_input == 'u':
                    while True:
                        if len(data_transaksi_baru['barang']) == 0:
                            peringatan("TIDAK ADA DATA TRANSAKSI")
                            break
                        else:
                            clear()
                            garis()
                            print_sentral(f"DATA TRANSAKSI ID {id_transaksi}")
                            garis('-')
                            print_sentral(f"{'No'.center(4)}| {'Nama'.center(PANJANG_NAMA_PRODUK-10)} | {'Harga'.center(15)} | {'Pcs'.center(4)} | {'Total'.center(15)}")
                            garis('-')
                            for i in range(len(data_transaksi_baru['barang'])):
                                total = f"{data_transaksi_baru['harga_barang'][i]*data_transaksi_baru['kuantitas'][i]:,.0f}"
                                harga = f"{data_transaksi_baru['harga_barang'][i]:,.0f}"
                                print_kiri(f"{str(i+1).ljust(5)} | {str(data_transaksi_baru['barang'][i]).ljust(PANJANG_NAMA_PRODUK-10)} | {str(harga).ljust(15)} | {str(data_transaksi_baru['kuantitas'][i]).ljust(4)} | {str(total).ljust(15)}")
                            garis('-')
                            print_sentral("COMMAND")
                            print_sentral("d : hapus produk | e : exit | u : ubah data")
                            garis()
                            input_user("Command [d/e/h] : ")
                            if user_input == "e":
                                break
                            elif user_input in ['d','u']:
                                clear()
                                garis()
                                print_sentral(f"DATA TRANSAKSI ID {id_transaksi}")
                                garis('-')
                                print_sentral(f"{'No'.center(4)}| {'Nama'.center(PANJANG_NAMA_PRODUK-10)} | {'Harga'.center(15)} | {'Pcs'.center(4)} | {'Total'.center(15)}")
                                garis('-')
                                for i in range(len(data_transaksi_baru['barang'])):
                                    total = f"{data_transaksi_baru['harga_barang'][i]*data_transaksi_baru['kuantitas'][i]:,.0f}"
                                    harga = f"{data_transaksi_baru['harga_barang'][i]:,.0f}"
                                    print_kiri(f"{str(i+1).ljust(5)} | {str(data_transaksi_baru['barang'][i]).ljust(PANJANG_NAMA_PRODUK-10)} | {str(harga).ljust(15)} | {str(data_transaksi_baru['kuantitas'][i]).ljust(4)} | {str(total).ljust(15)}")
                                garis()
                                try:
                                    indeks_produk = int(input("Produk Nomor : "))-1
                                    if indeks_produk >= len(data_transaksi_baru['barang']) or indeks_produk < 0:
                                        peringatan("PRODUK YANG ANDA PILIH TIDAK DITEMUKAN!")
                                    else:
                                        # MENCARI INDEKS PRODUK
                                        INDEKS_PRODUK_DATABASE = 0
                                        for i in range(len(__data__['produk'])):
                                            if __data__['produk'][i]['nama'] == data_transaksi_baru['barang'][indeks_produk]:
                                                INDEKS_PRODUK_DATABASE = i
                                                break
                                        # MENGHAPUS PRODUK
                                        if user_input == 'd':
                                            __data__['produk'][INDEKS_PRODUK_DATABASE] ['stok']   += data_transaksi_baru['kuantitas'][indeks_produk]
                                            __data__['produk'][INDEKS_PRODUK_DATABASE] ['dibeli'] -= data_transaksi_baru['kuantitas'][indeks_produk]
                                            data_transaksi_baru     ['total_harga'] -= data_transaksi_baru['harga_barang'][indeks_produk]*data_transaksi_baru['kuantitas'][indeks_produk]
                                            del data_transaksi_baru ['barang'][indeks_produk]
                                            del data_transaksi_baru ['harga_barang'][indeks_produk]
                                            peringatan("PRODUK BERHASIL DIHAPUS!")
                                            break
                                        # MENGUBAH KUANTITAS
                                        else:
                                            clear()
                                            print(f"Banyak Produk yang dibeli (lama) : {data_transaksi_baru['kuantitas'][indeks_produk]}")
                                            try:
                                                kuantitas_baru = int(input("Banyak Produk yang dibeli (baru) : "))
                                                if kuantitas_baru < 0 :
                                                    peringatan("MINIMAL 1 UNIT!")
                                                elif kuantitas_baru > __data__['produk'][INDEKS_PRODUK_DATABASE]['stok']+data_transaksi_baru['kuantitas'][indeks_produk]:
                                                    __max = __data__['produk'][INDEKS_PRODUK_DATABASE]['stok']+data_transaksi_baru['kuantitas'][indeks_produk]
                                                    peringatan(f"MAKSIMAL PEMBELIAN ADALAH {__max} UNIT")
                                                else:
                                                    selisih = data_transaksi_baru['kuantitas'][indeks_produk]-kuantitas_baru
                                                    __data__['produk'][INDEKS_PRODUK_DATABASE]['stok']   += selisih
                                                    __data__['produk'][INDEKS_PRODUK_DATABASE]['dibeli'] -= selisih  
                                                    data_transaksi_baru['total_harga'] -= data_transaksi_baru['kuantitas'][indeks_produk]*data_transaksi_baru['harga_barang'][indeks_produk]
                                                    data_transaksi_baru['kuantitas'][indeks_produk] = kuantitas_baru
                                                    data_transaksi_baru['total_harga'] += data_transaksi_baru['kuantitas'][indeks_produk]*data_transaksi_baru['harga_barang'][indeks_produk]
                                                    peringatan("Data berhasil diubah")
                                            except ValueError:
                                                peringatan("MASUKKAN SEBUAH ANGKA !")
                                except ValueError:
                                    peringatan("PRODUK YANG ANDA PILIH TIDAK DITEMUKAN")
    def prg_info_program():
        clear()
        garis()
        print_sentral('INFORMASI PROGRAM')
        garis()
        print_kiri('Nama Program   : UMKM Finance')
        print_kiri('Versi          : 1.0')
        print_kiri('Bahasa         : Python')
        print_kiri('Di Desain Oleh : Kelompok 3')
        garis('-')
        print_sentral('UBSI Dewi Sartika B - Ilmu Komputer')
        print_sentral('15.1A.31')
        garis()
        input('Ketik apa saja untuk kembali : ')
    def prg_list_data_transaksi():
        ambil_data()
        panjang_data_TRANSAKSI      = prg_panjang_data(__data__['transaksi'])
        panjang_halaman_TRANSAKSI   = prg_panjang_halaman(panjang_data_TRANSAKSI)
        if panjang_data_TRANSAKSI == 0:
            peringatan("TIDAK ADA TRANSAKSI")
        else:
            halaman_ke  = 1
            start       = 0
            detail      = False
            while True:
                prg_print_data_transaksi_range(__data__['transaksi'], start, halaman_ke*15)
                print_sentral('COMMAND')
                if panjang_halaman_TRANSAKSI == 1:
                    print_sentral("e : exit  |  d : detail transaksi via id")
                    garis()
                    input_user("Command [e/d] : ")
                    if user_input == "e":
                        break
                    elif user_input == "d":
                        detail = True
                else:
                    if halaman_ke == 1:
                        print_sentral('n : next  |  e : exit  |  d : detail transaksi via id')
                        garis()
                        input_user('Command [n/e/d] : ')
                        if user_input == 'e':
                            return 0
                        if user_input == 'n':
                            start += 15
                            halaman_ke += 1
                        elif user_input == 'd':
                            detail = True
                    elif 1 < halaman_ke < panjang_halaman_TRANSAKSI:
                        print_sentral('n : next  |  e : exit  | b : back')
                        print_sentral ('d : detail transaksi via id')
                        garis()
                        input_user('Command [n/e/b/d] : ')
                        if user_input == 'e':
                            return 0
                        if user_input == 'n':
                            start += 15
                            halaman_ke += 1
                        elif user_input == 'b':
                            start -= 15
                            halaman_ke -= 1
                        elif user_input == 'd':
                            detail = True
                    elif halaman_ke == panjang_halaman_TRANSAKSI:
                        print_sentral('b : back  |  e : exit  |  d : detail transaksi via id')
                        garis()
                        input_user('Command [b/e/d] : ')
                        if user_input == 'e':
                            return 0
                        elif user_input == 'b':
                            halaman_ke -= 1
                            start -= 15
                        elif user_input == 'd':
                            detail = True
                if detail:
                    detail = False
                    while True:
                        clear()
                        garis()
                        print_sentral("DETAIL TRANSKASI")
                        garis('-')
                        print_sentral(" ")
                        print_sentral("MASUKKAN ID TRANSAKSI")
                        print_sentral(" ")
                        garis('-')
                        print_sentral("COMMAND")
                        print_sentral("e : kembali")
                        garis()
                        input_user("ID Transaksi/Command [e] : ")
                        if user_input == 'e':
                            break
                        else:
                            try:
                                id_transaksi = int(user_input)
                                prg_print_detail_data_transaksi(id_transaksi)
                            except ValueError:
                                peringatan("COMMAND YANG ANDA PILIH SALAH")
    def prg_list_data_produk():
        ambil_data()
        panjang_data_produk = prg_panjang_data(__data__['produk'])
        if panjang_data_produk == 0:
            peringatan("ANDA TIDAK MEMILIKI PRODUK!")
        else:
            panjang_halaman_produk = prg_panjang_halaman(panjang_data_produk)
            start       = 0
            halaman_ke  = 1
            while True:
                search_mode = False
                clear()
                prg_print_data_produk_range(__data__['produk'], start, halaman_ke*15)
                if panjang_halaman_produk == 1:
                    print_sentral("COMMAND")
                    print_sentral("e : exit")
                    garis()
                    input_user("Command [e] : ")
                    if user_input == 'e':
                        break
                else:
                    if halaman_ke == 1:
                        print_sentral('s : search  |  n : next  |  e : exit')
                        garis()
                        input_user('Command [s/e/n] : ')
                        if user_input == 'e':
                            break
                        elif user_input == 'n':
                            halaman_ke += 1
                            start += 15
                        elif user_input == 's':
                            search_mode = True
                    elif 1 < halaman_ke < panjang_halaman_produk:
                        print_sentral('s : search  |  n : next  |  e : exit  |  b : back')
                        garis()
                        input_user('Command [s/n/b/e] : ')
                        if user_input == 'b':
                            halaman_ke -= 1
                            start -= 15
                        elif user_input == 'e':
                            break
                        elif user_input == 'n':
                            halaman_ke += 1
                            start += 15
                        elif user_input == 's':
                            search_mode = True
                    else:
                        print_sentral('s : search  |  b : back  |  e : exit')
                        garis()
                        input_user('Command [s/b/e] : ')
                        if user_input == 'b':
                            halaman_ke -= 1
                            start -= 15
                        elif user_input == 'e':
                            break
                        elif user_input == 's':
                            search_mode = True
                if search_mode:
                    search_mode = False
                    while True:
                        clear()
                        garis()
                        print_sentral("SEARCH MODE")
                        garis("-")
                        print_sentral(" ")
                        print_sentral("MASUKKAN NAMA PRODUK YANG ANDA CARI")
                        print_sentral(" ")
                        garis("-")
                        print_sentral("COMMAND")
                        print_sentral("$ : exit")
                        garis()
                        search_NAMA = input("Nama Produk : ")
                        if search_NAMA == '$':
                            break
                        else:
                            search_DATA = []
                            for i in __data__['produk']:
                                if search_NAMA in i['nama'] or search_NAMA.lower() in i['nama'] or search_NAMA.title() in i['nama'] or search_NAMA.upper() in i['nama']:
                                    search_DATA.append(i)
                            if len(search_DATA) == 0:
                                peringatan("PRODUK YANG ANDA CARI TIDAK ADA")
                            else:
                                start_s         = 0
                                halaman_s_ke    = 1 
                                panjang_search_DATA     = prg_panjang_data(search_DATA)
                                panjang_search_HALAMAN  = prg_panjang_halaman(panjang_search_DATA)
                                while True:
                                    clear()
                                    prg_print_data_produk_range(search_DATA, start_s, halaman_s_ke*15)
                                    print_sentral("COMMAND")
                                    if panjang_search_HALAMAN == 1:
                                        print_sentral("e : exit")
                                        garis()
                                        input_user("Command [e] : ")
                                        if user_input == 'e':
                                            break
                                    else:
                                        if halaman_s_ke == 1:
                                            print_sentral("n : next  |  e : exit")
                                            garis()
                                            input_user("Command [n/e] : ")
                                            if user_input   == 'n':
                                                start_s         += 15
                                                halaman_s_ke    += 1
                                            elif user_input == 'e':
                                                break
                                        elif 1 < halaman_s_ke < panjang_search_HALAMAN:
                                            print_sentral("n : next  |  e : exit  |  b : back")
                                            garis()
                                            input_user("Command [n/e/b] : ")
                                            if user_input   == 'n':
                                                start_s      += 15
                                                halaman_s_ke += 1
                                            elif user_input == 'e':
                                                break
                                            elif user_input  == 'b':
                                                start_s      -= 15
                                                halaman_s_ke -= 1
                                        elif halaman_s_ke == panjang_search_HALAMAN:
                                            print_sentral("e : exit  |  b : back")
                                            garis()
                                            input_user("Command [e/b] : ")
                                            if user_input   == "e":
                                                break
                                            elif user_input  == "b":
                                                start_s      -= 15
                                                halaman_s_ke -= 1
    def prg_grafik():
        ambil_data()
        if len(__data__['transaksi']) == 0:
            peringatan("TIDAK ADA DATA TRANSAKSI!")
        else:
            while True:
                clear()
                garis()
                print_sentral("GRAFIK")
                garis("-")
                print_kiri("1. Grafik Pendapatan")
                print_kiri("2. Grafik Penjualan Produk")
                print_kiri("e. Kembali")
                garis()
                input_user("Pilihan anda : ")
                if user_input in ['1', '2']:
                    y_title     = "Pendapatan"  if user_input  == '1' else "Penjualan"
                    key         = "total_harga" if user_input  == '1' else "total_barang"
                    while True:
                        set_TAHUN   = []
                        for i in __data__['transaksi']:
                            waktu_data_i = str(i['waktu']).split('-')
                            tahun_data_i = waktu_data_i[0]
                            set_TAHUN.append(tahun_data_i)
                        set_TAHUN = sorted(set(set_TAHUN))
                        clear()
                        garis()
                        print_sentral(f"GRAFIK {y_title.upper()}")
                        garis('-')
                        print_kiri('1. Grafik Harian')                        
                        print_kiri('2. Grafik Bulanan')
                        print_kiri('3. Grafik Tahunan')
                        print_kiri('e. Kembali')
                        garis()
                        input_user("Pilihan anda : ")
                        if user_input == "e":
                            break
                        # GRAFIK HARIAN BULAN X TAHUN Y
                        elif user_input == '1':
                            while True:
                                clear()
                                garis()
                                print_sentral("PILIH TAHUN")
                                garis('-')
                                print_kiri(f"{'No'.center(3)} | Tahun ")
                                garis('-')
                                for i,j in enumerate (set_TAHUN):
                                    print_kiri(f"{ str(i+1).ljust(3)} | {j}")
                                garis('-')
                                print_sentral("COMMAND")
                                print_sentral("e : exit")
                                garis()
                                input_user("Tahun nomor : ")
                                if user_input == 'e':
                                    break
                                else:
                                    try:
                                        indeks_TAHUN    = int(user_input)-1
                                        if indeks_TAHUN < 0 or indeks_TAHUN >= len(set_TAHUN):
                                            peringatan("TAHUN TIDAK DITEMUKAN!")
                                        else:
                                            PILIH_TAHUN     = set_TAHUN[indeks_TAHUN]
                                            set_BULAN       = []
                                            for i in __data__['transaksi'] :
                                                waktu_data_i = i['waktu'].split('-')
                                                if waktu_data_i[0] == PILIH_TAHUN:
                                                    set_BULAN.append(waktu_data_i[1])
                                            set_BULAN = sorted(set(set_BULAN)) 
                                            while True:
                                                clear()
                                                garis()
                                                print_sentral(f'Tahun {PILIH_TAHUN} Bulan ?')
                                                garis('-')
                                                for i in range(len(set_BULAN)):
                                                    print_kiri(f"{str(i+1).ljust(3)}| {BULAN[set_BULAN[i]]}")
                                                garis('-')
                                                print_sentral('COMMAND')
                                                print_sentral('e : exit')
                                                garis()
                                                indeks_BULAN = input('Bulan No. / Command : ')
                                                if indeks_BULAN == 'e':
                                                    break
                                                else:
                                                    try:
                                                        try:
                                                            PILIH_BULAN = set_BULAN [int(indeks_BULAN)-1]
                                                        except IndexError:
                                                            peringatan("Bulan yang anda pilih tidak ada")
                                                        koordinat_X = []
                                                        koordinat_Y = []
                                                        for i in __data__['transaksi']:
                                                            waktu   = str(i['waktu']).split('-')
                                                            hari    = waktu[2].split(' ')
                                                            if waktu[0] == PILIH_TAHUN and waktu[1] == PILIH_BULAN:
                                                                koordinat_X.append(hari[0])
                                                        koordinat_X = sorted(set(koordinat_X))

                                                        for i in koordinat_X:
                                                            y_i = 0
                                                            for j in __data__['transaksi']:
                                                                waktu   = str(j['waktu']).split('-')
                                                                hari    = waktu[2].split(' ')
                                                                if waktu[0] == PILIH_TAHUN and waktu[1] == PILIH_BULAN and hari[0] == i:
                                                                    y_i += j[key]
                                                            koordinat_Y.append(y_i)
                                                            y_i - 0
                                                        prg_print_grafik(koordinat_X, koordinat_Y, f"{y_title} Bulan {BULAN[PILIH_BULAN]} Tahun {PILIH_TAHUN}", y_title)
                                                    except ValueError:
                                                        peringatan("PILIHAN TIDAK DITEMUKAN")   
                                    except ValueError:
                                        peringatan("TAHUN TIDAK DITEMUKAN")
                        # GRAFIK BULANANAN TAHUN X
                        elif user_input == '2':
                            while True:
                                clear()
                                garis()
                                print_sentral("PILIH TAHUN")
                                garis('-')
                                print_kiri(f"{'No'.center(3)} | Tahun ")
                                garis('-')
                                for i,j in enumerate (set_TAHUN):
                                    print_kiri(f"{ str(i+1).ljust(3)} | {j}")
                                garis('-')
                                print_sentral("COMMAND")
                                print_sentral("e : exit")
                                garis()
                                input_user("Tahun nomor : ")
                                if user_input == 'e':
                                    break
                                else:
                                    try:
                                        indeks_TAHUN    = int(user_input)-1
                                        if indeks_TAHUN < 0 or indeks_TAHUN >= len(set_TAHUN):
                                            peringatan("TAHUN TIDAK DITEMUKAN!")
                                        else:
                                            PILIH_TAHUN     = set_TAHUN[indeks_TAHUN]
                                            set_BULAN       = []
                                            for i in __data__['transaksi'] :
                                                waktu_data_i = i['waktu'].split('-')
                                                if waktu_data_i[0] == PILIH_TAHUN:
                                                    set_BULAN.append(waktu_data_i[1])
                                            set_BULAN = sorted(set(set_BULAN)) 
                                            koordinat_X = set_BULAN
                                            koordinat_Y = []

                                            for i in koordinat_X:
                                                y_i = 0
                                                for j in __data__['transaksi']:
                                                    waktu = j['waktu'].split('-')
                                                    if waktu[0] == PILIH_TAHUN and waktu[1] == i:
                                                        y_i += j[key]
                                                koordinat_Y.append(y_i)
                                                y_i = 0
                                            
                                            prg_print_grafik(koordinat_X, koordinat_Y, f"{y_title} Bulanan Tahun {PILIH_TAHUN}", y_title)
                                    except ValueError:
                                        peringatan("TAHUN TIDAK DITEMUKAN")
                        # GRAFIK TAHUNAN
                        elif user_input == '3':
                            koordinat_X = set_TAHUN
                            koordinat_Y = []
                            for i in koordinat_X:
                                y_i = 0
                                for j in __data__['transaksi']:
                                    waktu = j['waktu'].split('-')
                                    if waktu[0] == i:
                                        y_i += j[key]
                                koordinat_Y.append(y_i)
                                y_i = 0
                            prg_print_grafik(koordinat_X, koordinat_Y, f"{y_title.title()} Tahunan", y_title)
                elif user_input == 'e':
                    break
    def prg_update_data():
        while True:
                ambil_data()
                clear()
                garis()
                print_sentral('UPDATE/DELETE DATA')
                garis('-')
                print_kiri("1. Ubah Data Produk")
                print_kiri('2. Hapus Produk')
                print_kiri("3. Hapus Transaksi")
                print_kiri("4. Ubah Nama Toko")
                print_kiri('e. Exit')
                garis('-')
                input_user("Pilihan anda : ")
                if user_input   == 'e':
                    break
                elif user_input == '1':
                    if len(__data__['produk']) == 0:
                        peringatan('ANDA TIDAK MEMILIKI PRODUK')
                    else:
                        while True:
                            ambil_data()
                            clear()
                            garis()
                            print_sentral(' ')
                            print_sentral('SEARCH DATA')
                            print_sentral(' ')
                            garis('-')
                            print_sentral('COMMAND')
                            print_sentral('$ : exit')
                            garis()
                            input_user("Nama Produk/Command [$] : ")
                            if user_input == '$':
                                break
                            else:
                                search_data = []
                                for i in __data__['produk']:
                                    if user_input.lower() in i['nama'] or user_input.upper() in i['nama'] or user_input.title() in i['nama']:
                                        search_data.append(i)
                                if len(search_data) == 0:
                                    peringatan('PRODUK YANG ANDA CARI TIDAK DITEMUKAN')
                                else:
                                    panjang_search_data     = prg_panjang_data(search_data)
                                    panjang_search_halaman  =  prg_panjang_halaman(panjang_search_data)
                                    update__ = False
                                    start = 0
                                    halaman_ke = 1
                                    while True:
                                        clear()
                                        prg_print_data_produk_range(search_data, start, halaman_ke*15)
                                        print_sentral("COMMAND")
                                        if panjang_search_halaman == 1:
                                            print_sentral("e : exit")
                                            garis()
                                            input_user("Produk No?/Command [e] : ")
                                            if user_input == 'e':
                                                break
                                            with contextlib.suppress(ValueError):
                                                indeks_produk = int(user_input)-1
                                                if indeks_produk < 0 or indeks_produk >= len(search_data):
                                                    peringatan("PRODUK YANG ANDA PILIH TIDAK DITEMUKAN")
                                                else:
                                                   update__ = True
                                        else:
                                            if halaman_ke == 1:
                                                print_sentral("n : next  |  e : exit")
                                                garis()
                                                input_user("Produk Nomor/Command [n/e] : ")
                                                if user_input == 'e':
                                                    break
                                                elif user_input == 'n':
                                                    start       += 15
                                                    halaman_ke  +=1
                                                else:
                                                    try:
                                                        indeks_produk = int(user_input)-1
                                                        if indeks_produk < 0 or indeks_produk < start or indeks_produk > halaman_ke*15:
                                                            peringatan("PRODUK YANG ANDA PILIH TIDAK ADA!")
                                                        else:
                                                            update__ = True
                                                    except ValueError:
                                                        continue
                                            elif 1 < halaman_ke < panjang_search_halaman:
                                                print_sentral("n : next  |  e : exit  |  b : back")
                                                garis()
                                                input_user("Produk Nomor/Command [n/e/n] : ")
                                                if user_input == 'e':
                                                    break
                                                elif user_input == 'n':
                                                    start       += 15
                                                    halaman_ke  +=1
                                                elif user_input == 'b':
                                                    start       -= 15
                                                    halaman_ke  -= 1
                                                else:
                                                    try:
                                                        indeks_produk = int(user_input)-1
                                                        if indeks_produk < 0 or indeks_produk < start or indeks_produk > halaman_ke*15:
                                                            peringatan("PRODUK YANG ANDA PILIH TIDAK ADA!")
                                                        else:
                                                            update__ = True
                                                    except ValueError:
                                                        continue
                                            elif halaman_ke == panjang_search_halaman:
                                                print_sentral("b : next  |  e : exit")
                                                garis()
                                                input_user("Produk Nomor/Command [n/e] : ")
                                                if user_input == 'e':
                                                    break
                                                elif user_input == 'b':
                                                    start       -= 15
                                                    halaman_ke  -=1
                                                else:
                                                    try:
                                                        indeks_produk = int(user_input)-1
                                                        if indeks_produk < 0 or indeks_produk < start or indeks_produk > halaman_ke*15:
                                                            peringatan("PRODUK YANG ANDA PILIH TIDAK ADA!")
                                                        else:
                                                            update__ = True
                                                    except ValueError:
                                                        continue
                                        if update__:
                                            update__ = False
                                            while True:
                                                clear
                                                garis()
                                                prg_print_detail_data_produk(search_data, indeks_produk)
                                                print_sentral('COMMAND')
                                                print_sentral('n : ubah nama  |  h : ubah harga  |  s : ubah stok')
                                                print_sentral('e : exit')
                                                garis()
                                                input_user('Command [n/h/s/e] : ')
                                                if user_input   == 'e':
                                                    break
                                                elif user_input == 'n':
                                                    while True:
                                                        clear()
                                                        print(f"Nama Lama \t : {search_data[indeks_produk]['nama']}")
                                                        nama_BARU = input("Nama Baru \t : ")
                                                        if len(nama_BARU) >= 50:
                                                            peringatan(f"MAKSIMAL NAMA ADALAH {PANJANG_NAMA_PRODUK} KARAKTER!")
                                                        else:
                                                            search_data[indeks_produk]['nama'] = nama_BARU
                                                            update_data()
                                                            peringatan("NAMA PRODUK BERHASIL DIUBAH")
                                                            break
                                                elif user_input == 'h':
                                                    while True:
                                                        with contextlib.suppress(ValueError):
                                                            clear()
                                                            garis('-')
                                                            print_sentral('MASUKKAN HARGA PRODUK TANPA KOMA (,)')
                                                            print_sentral('Contoh : 2000, 3000, 200.50')
                                                            garis('-')
                                                            print(f'Harga Lama \t : {search_data[indeks_produk]["harga"]} atau Rp {search_data[indeks_produk]["harga"]:,.0f}')
                                                            harga_BARU = float(input(f'Harga Baru \t : '))
                                                            if harga_BARU < 0:
                                                                peringatan('MINIMAL HARGA MINIMAL Rp 1')
                                                            else:
                                                                search_data[indeks_produk]['harga'] = harga_BARU
                                                                update_data()
                                                                peringatan('HARGA PRODUK BERHASIL DIUBAH !')
                                                                break
                                                elif user_input == 's':
                                                    while True:
                                                        clear()
                                                        with contextlib.suppress(ValueError):
                                                            print(f"Stok lama \t : {search_data[indeks_produk]['stok']}")
                                                            stok_BARU = int(input('Stok baru \t : '))
                                                            if stok_BARU < 0 :
                                                                peringatan('MINIMAL STOK ADALAH 0')
                                                            else:
                                                                search_data[indeks_produk]['stok'] = stok_BARU
                                                                update_data()
                                                                peringatan('STOK BERHASIL DIUBAH!')
                                                                break      
                elif user_input == '2':
                    if len(__data__['produk']) == 0:
                        peringatan('ANDA TIDAK MEMILIKI PRODUK')
                    else:
                        while True:
                            ambil_data()
                            clear()
                            garis()
                            print_sentral(' ')
                            print_sentral('SEARCH DATA')
                            print_sentral(' ')
                            garis('-')
                            print_sentral('COMMAND')
                            print_sentral('$ : exit')
                            garis()
                            input_user("Nama Produk/Command [e] : ")
                            if user_input == '$':
                                break
                            else:
                                search_nama = user_input
                                search_data = [i for i in __data__['produk'] if search_nama in i['nama'] or search_nama.lower() in i['nama'] or search_nama.upper() in i['nama'] or search_nama.title() in i ['nama']]
                                if len(search_data) == 0:
                                    peringatan('PRODUK YANG ANDA CARI TIDAK DITEMUKAN')
                                else:
                                    start      = 0
                                    halaman_ke = 1
                                    search_data_panjang = prg_panjang_data(search_data)
                                    search_data_halaman = prg_panjang_halaman(search_data_panjang)
                                    sucess__ = False
                                    while True:
                                        hapus__ = False
                                        if sucess__:
                                            break
                                        clear()
                                        prg_print_data_produk_range(search_data, start, halaman_ke*15)
                                        print_sentral("COMMAND")
                                        if search_data_halaman == 1:
                                            print_sentral("e : exit")
                                            garis()
                                            input_user("Produk Nomor/Command [e] : ")
                                            if user_input == 'e':
                                                break
                                            else:
                                                try:
                                                    indeks_produk = int(user_input)-1
                                                    if indeks_produk < 0 or indeks_produk >= search_data_panjang:
                                                        peringatan("PRODUK YANG ANDA PILIH TIDAK DITEMUKAN!")
                                                    else:
                                                        hapus__ = True
                                                except ValueError:
                                                    pass
                                        else:
                                            if halaman_ke == 1:
                                                print_sentral("n : next  |  e : exit")
                                                garis()
                                                input_user("Produk Nomor/Command [n/e] : ")
                                                if user_input == 'n':
                                                    start += 15
                                                    halaman_ke += 1
                                                elif user_input == 'e':
                                                    break
                                                else:
                                                    try:
                                                        indeks_produk = int(user_input)-1
                                                        if indeks_produk < 0 or indeks_produk < start or indeks_produk >= halaman_ke*15:
                                                            peringatan("PRODUK YANG ANDA PILIH TIDAK DITEMUKAN")
                                                        else:
                                                            hapus__ = True
                                                    except ValueError:
                                                        pass
                                            elif 1 < halaman_ke  < search_data_halaman:
                                                print_sentral("n : next  |  e : exit  |  b : back")
                                                garis()
                                                input_user("Produk Nomor/Command [n/e/b] : ")
                                                if user_input == 'n':
                                                    start += 15
                                                    halaman_ke += 1
                                                elif user_input == 'b':
                                                    start -= 15
                                                    halaman_ke -= 1
                                                elif user_input == 'e':
                                                    break
                                                else:
                                                    try:
                                                        indeks_produk = int(user_input)-1
                                                        if indeks_produk < 0 or indeks_produk < start or indeks_produk >= halaman_ke*15:
                                                            peringatan("PRODUK YANG ANDA PILIH TIDAK DITEMUKAN")
                                                        else:
                                                            hapus__ = True
                                                    except ValueError:
                                                        pass               
                                            elif halaman_ke == search_data_halaman:
                                                print_sentral("e : exit  |  b : back")
                                                garis()
                                                input_user("Produk Nomor/Command [e/b] : ")
                                                if user_input == 'b':
                                                    start -= 15
                                                    halaman_ke -= 1
                                                elif user_input == 'e':
                                                    break
                                                else:
                                                    try:
                                                        indeks_produk = int(user_input)-1
                                                        if indeks_produk < 0 or indeks_produk < start or indeks_produk >= halaman_ke*15:
                                                            peringatan("PRODUK YANG ANDA PILIH TIDAK DITEMUKAN")
                                                        else:
                                                            hapus__ = True
                                                    except ValueError:
                                                        pass
                                           
                                        if hapus__:
                                            hapus__ = False
                                            while True:
                                                prg_print_detail_data_produk(search_data, indeks_produk)
                                                print_sentral("COMMAND")
                                                print_sentral("y : hapus produk  |  e : exit")
                                                garis()
                                                input_user("Command [y/e] : ")
                                                if user_input == 'e':
                                                    break
                                                elif user_input == 'y':
                                                    clear()
                                                    garis()
                                                    print_sentral(" ")
                                                    print_sentral("APAKAH ANDA YAKIN INGIN MENGHAPUS PRODUK?")
                                                    print_sentral("PRODUK TIDAK BISA DI RECOVERY LAGI SETELAH DIHAPUS!")
                                                    print_sentral(" ")
                                                    garis()
                                                    input_user("Y/n : ")
                                                    if user_input == 'y':
                                                        for i in range(len(__data__['produk'])):
                                                            if __data__['produk'][i]['id'] == search_data[indeks_produk]['id']:
                                                                del __data__['produk'][i]
                                                                del search_data[indeks_produk]
                                                                break
                                                        update_data()
                                                        ambil_data()
                                                        peringatan("DATA PRODUK BERHASIL DIHAPUS!")
                                                        sucess__ = True
                                                        break
                                                    else:
                                                        break
                elif user_input == '3':
                    if __data__['transaksi'] == 0:
                        peringatan('ANDA TIDAK MEMILIKI TRANSAKSI')
                    else:
                        while True:
                            ambil_data()
                            clear()
                            garis()
                            print_sentral('HAPUS TRANSKASI VIA ID')
                            garis('-')
                            print_sentral('COMMAND')
                            print_sentral('e : exit')
                            garis()
                            input_user('ID Transaksi/Command [e] : ')
                            if user_input == 'e':
                                break
                            else:
                                try:
                                    id_tx = int(user_input)
                                    index_tx = None
                                    for i in range(len(__data__['transaksi'])):
                                        if __data__['transaksi'][i]['id'] == id_tx:
                                            index_tx = i
                                            break
                                    if index_tx is None:
                                        peringatan('ID TRANSAKSI TIDAK DITEMUKAN')
                                    else:
                                        while True:
                                            prg_print_detail_data_transaksi(id_tx, mode = 2, indeks=int(index_tx))
                                            garis('-')
                                            print_sentral('COMMAND')
                                            print_sentral('y : hapus transaksi  |  e : exit')
                                            garis()
                                            input_user('Command [y/e] : ')
                                            if user_input == 'y':
                                                waktu_sekarang    = str(dt.date.today()).split('-')
                                                waktu_transaksi   = str(__data__['transaksi'][index_tx]['waktu']).split('-')
                                                tanggal_transaksi = str(waktu_transaksi[2]).split(' ')
                                                if waktu_sekarang[0] == waktu_transaksi[0] and waktu_sekarang[1] == waktu_transaksi[1] and waktu_sekarang[2] == tanggal_transaksi[0] :
                                                    __data__['pendapatan_hari_ini'] -= __data__['transaksi'][index_tx]['total_harga']
                                                    __data__['penjualan_hari_ini']  -= __data__['transaksi'][index_tx]['total_barang']
                                                del __data__['transaksi'][index_tx]
                                                update_data()
                                                ambil_data()
                                                peringatan('TRANSAKSI BERHASIL DIHAPUS')
                                                break
                                            elif user_input == 'e':
                                                break
                                except ValueError:
                                    continue
                elif user_input == '4':
                    clear()
                    print(f"Nama toko lama\t: {__data__['nama_toko']}")
                    __data__.update({'nama_toko' : input("Nama toko baru\t: ")})
                    update_data()
                    peringatan("NAMA TOKO BERHASIL DIUBAH")

    if __name__ == "__main__":
        while True:
            ambil_data()
            clear()
            prg_menu_utama()
            input_user("Pilihan anda : ")
            if user_input   == "1":
                prg_tambah_data_produk()
            elif user_input == '2':
                prg_tambah_data_transaksi()
            elif user_input == '3':
                prg_list_data_produk()
            elif user_input == '4':
                prg_list_data_transaksi()
            elif user_input == '5':
                prg_grafik()
            elif user_input == '6':
                prg_update_data()
            elif user_input == 'i':
                prg_info_program()
            elif user_input == 'e':
                clear()
                break

            