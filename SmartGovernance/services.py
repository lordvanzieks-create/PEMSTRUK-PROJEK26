"""Logika utama pengelolaan, pencarian, dan pengurutan pengajuan."""

from datetime import date

from models import Pengajuan
from storage import CSVStorage
from validasi import validasi_pengajuan, validasi_status


class PengajuanService:
    """Menghubungkan model, validasi, algoritma, dan penyimpanan CSV."""

    KOLOM_SORTING = ["nama", "npm", "tanggal", "status"]

    def __init__(self, storage=None):
        """Menerima penyimpanan khusus atau memakai file CSV utama."""
        self.storage = storage if storage is not None else CSVStorage()

    def semua_pengajuan(self):
        """Mengambil seluruh data pengajuan dari file CSV."""
        return self.storage.baca_semua()

    def buat_id(self, data=None):
        """Membuat ID unik dengan pola SG-TANGGAL-NOMOR."""
        if data is None:
            data = self.semua_pengajuan()

        tanggal_hari_ini = date.today().strftime("%Y%m%d")
        awalan = f"SG-{tanggal_hari_ini}-"
        nomor_terbesar = 0

        for item in data:
            id_lama = item.get("id_pengajuan", "")
            if id_lama.startswith(awalan):
                try:
                    nomor = int(id_lama.replace(awalan, "", 1))
                    if nomor > nomor_terbesar:
                        nomor_terbesar = nomor
                except ValueError:
                    # Abaikan ID lama yang format nomornya tidak sesuai.
                    continue

        return f"{awalan}{nomor_terbesar + 1:03d}"

    def tambah_pengajuan(self, nama, npm, jenis_surat, keperluan):
        """Memvalidasi lalu menambahkan satu pengajuan baru ke CSV."""
        validasi_pengajuan(nama, npm, jenis_surat, keperluan)
        data = self.semua_pengajuan()

        pengajuan = Pengajuan(
            id_pengajuan=self.buat_id(data),
            tanggal=date.today().isoformat(),
            nama=nama.strip(),
            npm=npm.strip(),
            jenis_surat=jenis_surat,
            keperluan=keperluan.strip(),
            status="Menunggu",
        )

        data.append(pengajuan.to_dict())
        self.storage.simpan_semua(data)
        return pengajuan.to_dict()

    def edit_pengajuan(self, id_pengajuan, nama, npm, jenis_surat, keperluan):
        """Memperbarui informasi mahasiswa pada pengajuan yang dipilih."""
        validasi_pengajuan(nama, npm, jenis_surat, keperluan)
        data = self.semua_pengajuan()

        for item in data:
            if item["id_pengajuan"] == id_pengajuan:
                item["nama"] = nama.strip()
                item["npm"] = npm.strip()
                item["jenis_surat"] = jenis_surat
                item["keperluan"] = keperluan.strip()
                self.storage.simpan_semua(data)
                return item

        raise KeyError("Data pengajuan yang akan diubah tidak ditemukan.")

    def ubah_status(self, id_pengajuan, status_baru):
        """Mengubah status pengajuan berdasarkan ID."""
        validasi_status(status_baru)
        data = self.semua_pengajuan()

        for item in data:
            if item["id_pengajuan"] == id_pengajuan:
                item["status"] = status_baru
                self.storage.simpan_semua(data)
                return item

        raise KeyError("Data pengajuan yang akan diubah tidak ditemukan.")

    def hapus_pengajuan(self, id_pengajuan):
        """Menghapus data berdasarkan ID dan menyimpan hasilnya ke CSV."""
        data = self.semua_pengajuan()
        data_baru = [item for item in data if item["id_pengajuan"] != id_pengajuan]

        if len(data_baru) == len(data):
            raise KeyError("Data pengajuan yang akan dihapus tidak ditemukan.")

        self.storage.simpan_semua(data_baru)

    def cari_pengajuan(self, kata_kunci, data=None):
        """Mencari nama, NPM, atau ID menggunakan algoritma Linear Search."""
        if data is None:
            data = self.semua_pengajuan()

        kata_kunci = kata_kunci.strip().casefold()
        if not kata_kunci:
            return data

        hasil = []
        # Linear Search: periksa data satu per satu sampai seluruh data selesai.
        for item in data:
            if (
                kata_kunci in item.get("nama", "").casefold()
                or kata_kunci in item.get("npm", "").casefold()
                or kata_kunci in item.get("id_pengajuan", "").casefold()
            ):
                hasil.append(item)

        return hasil

    def bubble_sort(self, data, key, descending=False):
        """Mengurutkan data dengan Bubble Sort tanpa sorted() atau sort()."""
        hasil = data.copy()
        jumlah_data = len(hasil)

        # Bubble Sort: bandingkan dua data berdekatan lalu tukar bila perlu.
        for i in range(jumlah_data - 1):
            ada_perubahan = False
            for j in range(jumlah_data - i - 1):
                nilai_kiri = key(hasil[j])
                nilai_kanan = key(hasil[j + 1])

                if descending:
                    perlu_tukar = nilai_kiri < nilai_kanan
                else:
                    perlu_tukar = nilai_kiri > nilai_kanan

                if perlu_tukar:
                    hasil[j], hasil[j + 1] = hasil[j + 1], hasil[j]
                    ada_perubahan = True

            if not ada_perubahan:
                break

        return hasil

    def urutkan_pengajuan(self, kolom, descending=False, data=None):
        """Mengurutkan data berdasarkan nama, NPM, tanggal, atau status."""
        if kolom not in self.KOLOM_SORTING:
            raise ValueError("Kolom pengurutan tidak tersedia.")

        if data is None:
            data = self.semua_pengajuan()

        # Lambda dipakai sebagai fungsi untuk mengambil nilai kolom.
        fungsi_kunci = lambda item: item.get(kolom, "").casefold()
        return self.bubble_sort(data, key=fungsi_kunci, descending=descending)
