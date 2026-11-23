"""Unit test untuk fitur utama PengajuanService."""

import tempfile
import unittest
from pathlib import Path

from services import PengajuanService
from storage import CSVStorage


class TestPengajuanService(unittest.TestCase):
    """Menguji tambah, cari, sorting, validasi, dan pengelolaan pengajuan."""

    def setUp(self):
        """Membuat file CSV sementara agar pengujian tidak mengubah data utama."""
        self.temp_dir = tempfile.TemporaryDirectory()
        lokasi_csv = Path(self.temp_dir.name) / "pengajuan_test.csv"
        self.service = PengajuanService(CSVStorage(lokasi_csv))

    def tearDown(self):
        """Menghapus folder sementara setelah setiap pengujian."""
        self.temp_dir.cleanup()

    def tambah_contoh(self, nama, npm):
        """Membantu membuat data pengajuan untuk beberapa test."""
        return self.service.tambah_pengajuan(
            nama,
            npm,
            "Surat Aktif Kuliah",
            "Keperluan administrasi kampus",
        )

    def test_tambah_dan_simpan_data(self):
        """Data baru memiliki ID otomatis dan tersimpan pada CSV."""
        data = self.tambah_contoh("Brilian", "2517052051")
        hasil_baca = self.service.semua_pengajuan()

        self.assertTrue(data["id_pengajuan"].startswith("SG-"))
        self.assertEqual(len(hasil_baca), 1)
        self.assertEqual(hasil_baca[0]["nama"], "Brilian")
        self.assertEqual(hasil_baca[0]["status"], "Menunggu")

    def test_linear_search(self):
        """Pencarian dapat menemukan data berdasarkan nama, NPM, dan ID."""
        data = self.tambah_contoh("Brilian", "2517052051")
        self.tambah_contoh("Andi", "2517052002")

        hasil_nama = self.service.cari_pengajuan("bril")
        hasil_npm = self.service.cari_pengajuan("2002")
        hasil_id = self.service.cari_pengajuan(data["id_pengajuan"])

        self.assertEqual(len(hasil_nama), 1)
        self.assertEqual(hasil_nama[0]["nama"], "Brilian")
        self.assertEqual(len(hasil_npm), 1)
        self.assertEqual(len(hasil_id), 1)

    def test_bubble_sort_nama(self):
        """Bubble Sort mengurutkan nama dari A ke Z tanpa fungsi bawaan."""
        self.tambah_contoh("Citra", "2517052003")
        self.tambah_contoh("Andi", "2517052002")
        self.tambah_contoh("Budi", "2517052001")

        hasil = self.service.urutkan_pengajuan("nama")
        daftar_nama = [item["nama"] for item in hasil]

        self.assertEqual(daftar_nama, ["Andi", "Budi", "Citra"])

    def test_validasi_data_kosong(self):
        """Nama yang kosong harus ditolak dengan ValueError."""
        with self.assertRaises(ValueError):
            self.service.tambah_pengajuan(
                "",
                "2517052051",
                "Surat Aktif Kuliah",
                "Keperluan administrasi kampus",
            )

    def test_edit_status_dan_hapus(self):
        """Data dapat diedit, status dapat diubah, lalu data dapat dihapus."""
        data = self.tambah_contoh("Brilian", "2517052051")
        id_data = data["id_pengajuan"]

        self.service.edit_pengajuan(
            id_data,
            "Brilian M",
            "2517052051",
            "Surat Pengantar Magang",
            "Persyaratan magang",
        )
        self.service.ubah_status(id_data, "Diproses")
        hasil_edit = self.service.semua_pengajuan()[0]

        self.assertEqual(hasil_edit["nama"], "Brilian M")
        self.assertEqual(hasil_edit["jenis_surat"], "Surat Pengantar Magang")
        self.assertEqual(hasil_edit["status"], "Diproses")

        self.service.hapus_pengajuan(id_data)
        self.assertEqual(self.service.semua_pengajuan(), [])


if __name__ == "__main__":
    unittest.main()
