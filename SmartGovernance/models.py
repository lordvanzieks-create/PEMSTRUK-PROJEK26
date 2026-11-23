"""Model untuk menyimpan data pengajuan surat mahasiswa."""


class Pengajuan:
    """Mewakili satu data pengajuan surat administrasi mahasiswa.

    Class ini menerima data melalui argumen posisi (*args) atau kata kunci
    (**kwargs), sehingga data juga mudah dibuat dari baris CSV.
    """

    field_names = (
        "id_pengajuan",
        "tanggal",
        "nama",
        "npm",
        "jenis_surat",
        "keperluan",
        "status",
    )

    def __init__(self, *args, **kwargs):
        """Membuat objek pengajuan dari argumen posisi atau kata kunci."""
        if len(args) > len(self.field_names):
            raise TypeError("Jumlah argumen pengajuan terlalu banyak.")

        data = {}
        for indeks, nama_field in enumerate(self.field_names):
            if indeks < len(args):
                data[nama_field] = args[indeks]
            else:
                data[nama_field] = kwargs.pop(nama_field, "")

        if kwargs:
            nama_tidak_dikenal = ", ".join(kwargs.keys())
            raise TypeError(f"Field tidak dikenal: {nama_tidak_dikenal}")

        # Pengajuan baru secara default memiliki status Menunggu.
        if not data["status"]:
            data["status"] = "Menunggu"

        for nama_field in self.field_names:
            setattr(self, nama_field, str(data[nama_field]))

    def to_dict(self):
        """Mengubah objek menjadi dictionary agar mudah disimpan ke CSV."""
        return {
            nama_field: getattr(self, nama_field)
            for nama_field in self.field_names
        }
