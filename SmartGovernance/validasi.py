"""Kumpulan fungsi untuk memeriksa data pengajuan."""

JENIS_SURAT = ["Surat Aktif Kuliah", "Surat Pengantar Magang"]
STATUS_PENGAJUAN = ["Menunggu", "Diproses", "Selesai", "Ditolak"]


def validasi_pengajuan(nama, npm, jenis_surat, keperluan):
    """Memastikan seluruh data wajib terisi dan jenis surat valid."""
    if not nama or not nama.strip():
        raise ValueError("Nama mahasiswa wajib diisi.")

    if not npm or not npm.strip():
        raise ValueError("NPM wajib diisi.")

    if not npm.strip().isdigit():
        raise ValueError("NPM harus berisi angka saja.")

    if jenis_surat not in JENIS_SURAT:
        raise ValueError("Silakan pilih jenis surat yang tersedia.")

    if not keperluan or not keperluan.strip():
        raise ValueError("Keperluan surat wajib diisi.")


def validasi_status(status):
    """Memastikan status pengajuan termasuk pilihan yang tersedia."""
    if status not in STATUS_PENGAJUAN:
        raise ValueError("Status pengajuan tidak valid.")
