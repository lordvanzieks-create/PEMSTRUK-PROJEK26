"""Modul untuk membaca dan menyimpan data pengajuan ke file CSV."""

import csv
from pathlib import Path


FIELDNAMES = [
    "id_pengajuan",
    "tanggal",
    "nama",
    "npm",
    "jenis_surat",
    "keperluan",
    "status",
]


class CSVStorage:
    """Mengatur seluruh proses baca dan tulis file pengajuan.csv."""

    def __init__(self, file_path=None):
        """Membuat penyimpanan; lokasi default berada di folder data."""
        if file_path is None:
            folder_project = Path(__file__).resolve().parent
            file_path = folder_project / "data" / "pengajuan.csv"

        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        # Buat file beserta header jika file belum tersedia.
        if not self.file_path.exists():
            self.simpan_semua([])

    def baca_semua(self):
        """Membaca seluruh baris CSV dan mengembalikannya sebagai list."""
        try:
            with open(self.file_path, mode="r", newline="", encoding="utf-8") as file:
                pembaca = csv.DictReader(file)
                data = []
                for baris in pembaca:
                    # Pastikan setiap baris memiliki semua kolom yang dibutuhkan.
                    data.append({field: baris.get(field, "") or "" for field in FIELDNAMES})
                return data
        except FileNotFoundError:
            # Jika file terhapus saat program berjalan, buat ulang file kosong.
            self.simpan_semua([])
            return []
        except csv.Error as error:
            raise ValueError(f"File CSV tidak dapat dibaca: {error}") from error

    def simpan_semua(self, data):
        """Menulis ulang seluruh data ke CSV dengan header kolom."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.file_path, mode="w", newline="", encoding="utf-8") as file:
                penulis = csv.DictWriter(file, fieldnames=FIELDNAMES)
                penulis.writeheader()
                penulis.writerows(data)
        except OSError as error:
            raise OSError(f"Data tidak dapat disimpan: {error}") from error
