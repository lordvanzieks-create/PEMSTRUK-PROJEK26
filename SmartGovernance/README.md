# Smart Governance

**Sistem Informasi Pengajuan dan Pelacakan Surat Administrasi Mahasiswa** adalah aplikasi desktop sederhana untuk mencatat pengajuan surat mahasiswa dan memantau status pengerjaannya. Aplikasi dibuat menggunakan Python, Tkinter, dan file CSV tanpa database atau framework tambahan.

## Fitur Aplikasi

- Dashboard jumlah seluruh pengajuan, Menunggu, Diproses, dan Selesai.
- Form pengajuan Surat Aktif Kuliah dan Surat Pengantar Magang.
- ID pengajuan dibuat otomatis.
- Menampilkan daftar pengajuan dalam tabel.
- Pencarian berdasarkan nama, NPM, atau ID pengajuan dengan Linear Search.
- Pengurutan berdasarkan nama, NPM, tanggal, atau status dengan Bubble Sort.
- Mengubah status menjadi Menunggu, Diproses, Selesai, atau Ditolak.
- Menambah, mengedit, dan menghapus data.
- Validasi data wajib dan penyimpanan permanen pada file CSV.

## Teknologi yang Digunakan

- Python 3
- Tkinter dan ttk untuk tampilan desktop
- CSV untuk penyimpanan data
- `unittest` untuk pengujian program

Seluruh library yang digunakan merupakan bagian dari Python, sehingga tidak perlu memasang framework atau database tambahan.

## Struktur Folder

```text
SmartGovernance/
├── main.py                 # Titik awal untuk menjalankan aplikasi
├── ui.py                   # Tampilan dan interaksi Tkinter
├── models.py               # Class/model Pengajuan
├── services.py             # CRUD, Linear Search, dan Bubble Sort
├── storage.py              # Baca dan tulis file CSV
├── validasi.py             # Validasi input dan status
├── data/
│   └── pengajuan.csv       # Penyimpanan data pengajuan
├── tests/
│   └── test_services.py    # Unit test fitur layanan
└── README.md               # Dokumentasi project
```

## Fungsi Setiap File

| File | Fungsi |
|---|---|
| `main.py` | Menjalankan jendela utama aplikasi. |
| `ui.py` | Mengatur dashboard, form, tabel, pencarian, dan tombol. |
| `models.py` | Menyediakan class `Pengajuan` untuk merepresentasikan satu data. |
| `services.py` | Mengelola tambah, edit, hapus, ubah status, searching, dan sorting. |
| `storage.py` | Menangani pembacaan dan penulisan data CSV menggunakan `with open()`. |
| `validasi.py` | Memeriksa input wajib, jenis surat, dan status. |
| `data/pengajuan.csv` | Menyimpan data agar tetap ada setelah aplikasi ditutup. |
| `tests/test_services.py` | Menguji fitur utama menggunakan `unittest`. |

## Cara Menjalankan Program

1. Pastikan Python 3 sudah terpasang.
2. Ekstrak folder `SmartGovernance`.
3. Buka terminal atau Command Prompt pada folder `SmartGovernance`.
4. Jalankan perintah:

   ```bash
   python main.py
   ```

   Pada Windows, perintah berikut juga dapat digunakan:

   ```bash
   py main.py
   ```

5. Jendela aplikasi akan terbuka. Data yang ditambahkan akan tersimpan di `data/pengajuan.csv`.

## Cara Menjalankan Unit Testing

Jalankan terminal pada folder utama project, kemudian gunakan:

```bash
python -m unittest discover -s tests -v
```

Pada Windows:

```bash
py -m unittest discover -s tests -v
```

Pengujian mencakup penambahan dan penyimpanan data, Linear Search, Bubble Sort, validasi data kosong, serta proses edit, ubah status, dan hapus.

## Ketentuan Pemrograman yang Diterapkan

- Minimal dua class: `Pengajuan`, `CSVStorage`, dan `PengajuanService`.
- `*args` dan `**kwargs`: digunakan pada constructor class `Pengajuan`.
- Lambda: digunakan sebagai fungsi kunci pengurutan pada `services.py`.
- Searching: Linear Search pada method `cari_pengajuan()`.
- Sorting: Bubble Sort pada method `bubble_sort()`.
- File: semua operasi baca/tulis CSV memakai `with open()`.
- Penanganan kesalahan: menggunakan `try-except` pada pembacaan file dan interaksi aplikasi.
- Validasi: menggunakan `raise ValueError` ketika input tidak sesuai.
- Modul dipisah agar tampilan, model, layanan, penyimpanan, dan validasi tidak menumpuk dalam satu file.

## Tabel Refactoring

| No. | Perbaikan kualitas kode | Sebelum refactoring | Setelah refactoring | Manfaat |
|---|---|---|---|---|
| 1 | Memisahkan penyimpanan data | Proses baca/tulis CSV bercampur dengan fitur aplikasi. | Proses CSV dipusatkan di `storage.py`. | Lebih mudah dirawat dan diuji. |
| 2 | Memisahkan validasi | Pemeriksaan input dapat berulang di beberapa bagian program. | Validasi dipusatkan di `validasi.py`. | Aturan input lebih konsisten. |
| 3 | Memisahkan tampilan dan logika | Kode tampilan dan pengolahan data berpotensi berada dalam satu file. | Tkinter berada di `ui.py`, sedangkan proses data berada di `services.py`. | Struktur lebih jelas dan mudah dipresentasikan. |
| 4 | Menggunakan fungsi algoritma terpisah | Pencarian dan pengurutan dapat tercampur dengan kode tampilan. | Linear Search dan Bubble Sort dibuat sebagai method layanan. | Algoritma lebih mudah diuji dengan unit test. |

## Catatan Penggunaan

- Status awal pengajuan baru adalah **Menunggu**.
- Untuk mengedit data atau mengubah status, pilih salah satu baris pada tabel terlebih dahulu.
- Tombol **Edit Data** menyimpan perubahan nama, NPM, jenis surat, dan keperluan.
- Tombol **Ubah Status** menyimpan status yang dipilih pada form.
- Tombol **Hapus** meminta konfirmasi sebelum menghapus data.
