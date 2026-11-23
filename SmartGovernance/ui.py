"""Tampilan desktop Smart Governance menggunakan Tkinter dan ttk."""

import tkinter as tk
from tkinter import messagebox, ttk

from services import PengajuanService
from validasi import JENIS_SURAT, STATUS_PENGAJUAN


class SmartGovernanceApp:
    """Membuat dashboard, form pengajuan, tabel, dan tombol pengelolaan data."""

    def __init__(self, root, service=None):
        """Menyiapkan jendela aplikasi dan seluruh komponen tampilannya."""
        self.root = root
        self.service = service if service is not None else PengajuanService()
        self.id_terpilih = None

        self.root.title("Smart Governance - Pengajuan Surat Mahasiswa")
        self.root.geometry("1180x720")
        self.root.minsize(980, 620)
        self.root.configure(bg="#eeeeee")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self._atur_style()

        self.var_cari = tk.StringVar()
        self.var_jenis = tk.StringVar(value=JENIS_SURAT[0])
        self.var_status = tk.StringVar(value=STATUS_PENGAJUAN[0])
        self.var_urut = tk.StringVar(value="Nama")
        self.var_arah = tk.StringVar(value="A-Z")

        self._buat_tampilan()
        self.muat_data()

    def _atur_style(self):
        """Mengatur tampilan komponen agar konsisten dengan warna netral."""
        self.style.configure("TFrame", background="#eeeeee")
        self.style.configure("Card.TFrame", background="#ffffff")
        self.style.configure("TLabel", background="#eeeeee", foreground="#222222", font=("Arial", 10))
        self.style.configure("Title.TLabel", background="#eeeeee", foreground="#111111", font=("Arial", 19, "bold"))
        self.style.configure("Sub.TLabel", background="#eeeeee", foreground="#666666", font=("Arial", 9))
        self.style.configure("CardTitle.TLabel", background="#ffffff", foreground="#666666", font=("Arial", 9))
        self.style.configure("CardValue.TLabel", background="#ffffff", foreground="#111111", font=("Arial", 20, "bold"))
        self.style.configure("TLabelframe", background="#ffffff", bordercolor="#cccccc")
        self.style.configure("TLabelframe.Label", background="#ffffff", foreground="#222222", font=("Arial", 10, "bold"))
        self.style.configure("TButton", font=("Arial", 9), padding=(9, 6))
        self.style.configure("Primary.TButton", background="#333333", foreground="#ffffff")
        self.style.map("Primary.TButton", background=[("active", "#555555")])
        self.style.configure("Treeview", font=("Arial", 9), rowheight=27, background="#ffffff", fieldbackground="#ffffff")
        self.style.configure("Treeview.Heading", font=("Arial", 9, "bold"), background="#dddddd", foreground="#222222")
        self.style.map("Treeview", background=[("selected", "#d5d5d5")], foreground=[("selected", "#111111")])

    def _buat_tampilan(self):
        """Menyusun header, ringkasan, form, dan tabel data."""
        utama = ttk.Frame(self.root, padding=16)
        utama.pack(fill="both", expand=True)

        # Bagian judul aplikasi.
        header = ttk.Frame(utama)
        header.pack(fill="x", pady=(0, 12))
        ttk.Label(header, text="Smart Governance", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Sistem Informasi Pengajuan dan Pelacakan Surat Administrasi Mahasiswa",
            style="Sub.TLabel",
        ).pack(anchor="w", pady=(3, 0))

        # Kartu ringkasan dashboard.
        self.frame_ringkasan = ttk.Frame(utama)
        self.frame_ringkasan.pack(fill="x", pady=(0, 12))
        self.label_total = self._buat_kartu(self.frame_ringkasan, "Total Pengajuan", 0)
        self.label_menunggu = self._buat_kartu(self.frame_ringkasan, "Menunggu", 1)
        self.label_diproses = self._buat_kartu(self.frame_ringkasan, "Diproses", 2)
        self.label_selesai = self._buat_kartu(self.frame_ringkasan, "Selesai", 3)
        self.label_ditolak = self._buat_kartu(self.frame_ringkasan, "Ditolak", 4)

        # Area utama: form di kiri dan data di kanan.
        konten = ttk.Frame(utama)
        konten.pack(fill="both", expand=True)
        konten.columnconfigure(0, weight=0, minsize=310)
        konten.columnconfigure(1, weight=1)
        konten.rowconfigure(0, weight=1)

        self._buat_form(konten)
        self._buat_tabel(konten)

    def _buat_kartu(self, parent, judul, kolom):
        """Membuat satu kartu angka ringkasan dashboard."""
        kartu = ttk.Frame(parent, style="Card.TFrame", padding=12)
        kartu.grid(row=0, column=kolom, sticky="nsew", padx=(0 if kolom == 0 else 8, 0))
        parent.columnconfigure(kolom, weight=1)
        ttk.Label(kartu, text=judul, style="CardTitle.TLabel").pack(anchor="w")
        nilai = ttk.Label(kartu, text="0", style="CardValue.TLabel")
        nilai.pack(anchor="w", pady=(4, 0))
        return nilai

    def _buat_form(self, parent):
        """Membuat input data dan tombol tambah, edit, status, serta hapus."""
        form = ttk.LabelFrame(parent, text="Form Pengajuan", padding=12)
        form.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        form.columnconfigure(0, weight=1)

        ttk.Label(form, text="Nama Mahasiswa").grid(row=0, column=0, sticky="w", pady=(0, 4))
        self.entry_nama = ttk.Entry(form)
        self.entry_nama.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        ttk.Label(form, text="NPM").grid(row=2, column=0, sticky="w", pady=(0, 4))
        self.entry_npm = ttk.Entry(form)
        self.entry_npm.grid(row=3, column=0, sticky="ew", pady=(0, 10))

        ttk.Label(form, text="Jenis Surat").grid(row=4, column=0, sticky="w", pady=(0, 4))
        self.combo_jenis = ttk.Combobox(
            form,
            textvariable=self.var_jenis,
            values=JENIS_SURAT,
            state="readonly",
        )
        self.combo_jenis.grid(row=5, column=0, sticky="ew", pady=(0, 10))

        ttk.Label(form, text="Keperluan").grid(row=6, column=0, sticky="w", pady=(0, 4))
        self.text_keperluan = tk.Text(
            form,
            height=4,
            wrap="word",
            font=("Arial", 9),
            relief="solid",
            borderwidth=1,
            highlightthickness=0,
        )
        self.text_keperluan.grid(row=7, column=0, sticky="ew", pady=(0, 10))

        ttk.Label(form, text="Status Pengajuan").grid(row=8, column=0, sticky="w", pady=(0, 4))
        self.combo_status = ttk.Combobox(
            form,
            textvariable=self.var_status,
            values=STATUS_PENGAJUAN,
            state="readonly",
        )
        self.combo_status.grid(row=9, column=0, sticky="ew", pady=(0, 12))

        tombol = ttk.Frame(form)
        tombol.grid(row=10, column=0, sticky="ew")
        tombol.columnconfigure(0, weight=1)
        tombol.columnconfigure(1, weight=1)

        ttk.Button(tombol, text="Tambah", style="Primary.TButton", command=self.tambah_data).grid(
            row=0, column=0, sticky="ew", padx=(0, 4), pady=3
        )
        ttk.Button(tombol, text="Edit Data", command=self.edit_data).grid(
            row=0, column=1, sticky="ew", padx=(4, 0), pady=3
        )
        ttk.Button(tombol, text="Ubah Status", command=self.ubah_status).grid(
            row=1, column=0, sticky="ew", padx=(0, 4), pady=3
        )
        ttk.Button(tombol, text="Hapus", command=self.hapus_data).grid(
            row=1, column=1, sticky="ew", padx=(4, 0), pady=3
        )
        ttk.Button(tombol, text="Bersihkan Form", command=self.bersihkan_form).grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=(7, 0)
        )

        ttk.Label(
            form,
            text="Pilih satu baris pada tabel untuk mengedit atau mengubah status.",
            style="Sub.TLabel",
            wraplength=270,
        ).grid(row=11, column=0, sticky="w", pady=(12, 0))

    def _buat_tabel(self, parent):
        """Membuat area pencarian, pengurutan, dan tabel daftar pengajuan."""
        area = ttk.Frame(parent)
        area.grid(row=0, column=1, sticky="nsew")
        area.columnconfigure(0, weight=1)
        area.rowconfigure(1, weight=1)

        kontrol = ttk.LabelFrame(area, text="Pencarian dan Pengurutan", padding=10)
        kontrol.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        kontrol.columnconfigure(0, weight=1)

        baris_cari = ttk.Frame(kontrol)
        baris_cari.grid(row=0, column=0, sticky="ew")
        baris_cari.columnconfigure(0, weight=1)
        self.entry_cari = ttk.Entry(baris_cari, textvariable=self.var_cari)
        self.entry_cari.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        self.entry_cari.bind("<Return>", lambda event: self.cari_data())
        ttk.Button(baris_cari, text="Cari", command=self.cari_data).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(baris_cari, text="Reset", command=self.reset_pencarian).grid(row=0, column=2)

        baris_urut = ttk.Frame(kontrol)
        baris_urut.grid(row=1, column=0, sticky="w", pady=(9, 0))
        ttk.Label(baris_urut, text="Urutkan:").pack(side="left", padx=(0, 5))
        ttk.Combobox(
            baris_urut,
            textvariable=self.var_urut,
            values=["Nama", "NPM", "Tanggal", "Status"],
            state="readonly",
            width=12,
        ).pack(side="left", padx=(0, 7))
        ttk.Combobox(
            baris_urut,
            textvariable=self.var_arah,
            values=["A-Z", "Z-A"],
            state="readonly",
            width=7,
        ).pack(side="left", padx=(0, 7))
        ttk.Button(baris_urut, text="Terapkan", command=self.urutkan_data).pack(side="left")

        tabel_frame = ttk.LabelFrame(area, text="Daftar Pengajuan", padding=8)
        tabel_frame.grid(row=1, column=0, sticky="nsew")
        tabel_frame.columnconfigure(0, weight=1)
        tabel_frame.rowconfigure(0, weight=1)

        kolom = ("id", "tanggal", "nama", "npm", "jenis", "status")
        self.tree = ttk.Treeview(tabel_frame, columns=kolom, show="headings", selectmode="browse")
        self.tree.heading("id", text="ID Pengajuan")
        self.tree.heading("tanggal", text="Tanggal")
        self.tree.heading("nama", text="Nama")
        self.tree.heading("npm", text="NPM")
        self.tree.heading("jenis", text="Jenis Surat")
        self.tree.heading("status", text="Status")

        self.tree.column("id", width=145, minwidth=125, anchor="w")
        self.tree.column("tanggal", width=90, minwidth=85, anchor="center")
        self.tree.column("nama", width=145, minwidth=110)
        self.tree.column("npm", width=105, minwidth=90)
        self.tree.column("jenis", width=155, minwidth=130)
        self.tree.column("status", width=90, minwidth=80, anchor="center")

        scrollbar_y = ttk.Scrollbar(tabel_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(tabel_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        self.tree.bind("<<TreeviewSelect>>", self.pilih_data)

    def _ambil_form(self):
        """Mengambil nilai yang sedang dimasukkan pada form."""
        return {
            "nama": self.entry_nama.get(),
            "npm": self.entry_npm.get(),
            "jenis_surat": self.var_jenis.get(),
            "keperluan": self.text_keperluan.get("1.0", "end-1c"),
        }

    def _perbarui_ringkasan(self, data):
        """Menghitung jumlah pengajuan untuk setiap ringkasan dashboard."""
        jumlah_menunggu = sum(1 for item in data if item["status"] == "Menunggu")
        jumlah_diproses = sum(1 for item in data if item["status"] == "Diproses")
        jumlah_selesai = sum(1 for item in data if item["status"] == "Selesai")
        jumlah_ditolak = sum(1 for item in data if item["status"] == "Ditolak")

        self.label_total.config(text=str(len(data)))
        self.label_menunggu.config(text=str(jumlah_menunggu))
        self.label_diproses.config(text=str(jumlah_diproses))
        self.label_selesai.config(text=str(jumlah_selesai))
        self.label_ditolak.config(text=str(jumlah_ditolak))

    def muat_data(self, data_tampil=None):
        """Memuat data terbaru dan memperbarui isi tabel serta dashboard."""
        try:
            semua_data = self.service.semua_pengajuan()
            self._perbarui_ringkasan(semua_data)

            if data_tampil is None:
                data_tampil = semua_data

            # Kosongkan tabel sebelum menampilkan data terbaru.
            for item_id in self.tree.get_children():
                self.tree.delete(item_id)

            for item in data_tampil:
                self.tree.insert(
                    "",
                    "end",
                    iid=item["id_pengajuan"],
                    values=(
                        item["id_pengajuan"],
                        item["tanggal"],
                        item["nama"],
                        item["npm"],
                        item["jenis_surat"],
                        item["status"],
                    ),
                )
        except (OSError, ValueError, KeyError) as error:
            messagebox.showerror("Kesalahan", str(error))

    def _data_sesuai_filter(self):
        """Mengambil data berdasarkan kata pencarian dan pengurutan aktif."""
        kata_kunci = self.var_cari.get().strip()
        data = self.service.cari_pengajuan(kata_kunci)
        kolom = self.var_urut.get().lower()
        descending = self.var_arah.get() == "Z-A"
        return self.service.urutkan_pengajuan(kolom, descending, data)

    def tambah_data(self):
        """Menyimpan pengajuan baru setelah validasi berhasil dilakukan."""
        form = self._ambil_form()
        try:
            data_baru = self.service.tambah_pengajuan(**form)
            messagebox.showinfo("Berhasil", f"Pengajuan berhasil ditambahkan.\nID: {data_baru['id_pengajuan']}")
            self.bersihkan_form()
            self.muat_data(self._data_sesuai_filter())
        except (ValueError, OSError) as error:
            messagebox.showerror("Data belum dapat disimpan", str(error))

    def edit_data(self):
        """Menyimpan perubahan data pada baris yang sedang dipilih."""
        if not self.id_terpilih:
            messagebox.showwarning("Pilih Data", "Pilih data pada tabel yang ingin diedit.")
            return

        form = self._ambil_form()
        try:
            self.service.edit_pengajuan(self.id_terpilih, **form)
            messagebox.showinfo("Berhasil", "Data pengajuan berhasil diperbarui.")
            self.bersihkan_form()
            self.muat_data(self._data_sesuai_filter())
        except (ValueError, OSError, KeyError) as error:
            messagebox.showerror("Data belum dapat diperbarui", str(error))

    def ubah_status(self):
        """Mengubah status pengajuan yang sedang dipilih pada tabel."""
        if not self.id_terpilih:
            messagebox.showwarning("Pilih Data", "Pilih data pada tabel terlebih dahulu.")
            return

        try:
            self.service.ubah_status(self.id_terpilih, self.var_status.get())
            messagebox.showinfo("Berhasil", "Status pengajuan berhasil diubah.")
            self.muat_data(self._data_sesuai_filter())
        except (ValueError, OSError, KeyError) as error:
            messagebox.showerror("Status belum dapat diubah", str(error))

    def hapus_data(self):
        """Menghapus pengajuan setelah pengguna menyetujui konfirmasi."""
        if not self.id_terpilih:
            messagebox.showwarning("Pilih Data", "Pilih data pada tabel yang ingin dihapus.")
            return

        setuju = messagebox.askyesno("Konfirmasi Hapus", "Yakin ingin menghapus pengajuan ini?")
        if not setuju:
            return

        try:
            self.service.hapus_pengajuan(self.id_terpilih)
            messagebox.showinfo("Berhasil", "Data pengajuan berhasil dihapus.")
            self.bersihkan_form()
            self.muat_data(self._data_sesuai_filter())
        except (OSError, KeyError) as error:
            messagebox.showerror("Data belum dapat dihapus", str(error))

    def pilih_data(self, _event=None):
        """Mengisi form berdasarkan baris yang dipilih pada tabel."""
        pilihan = self.tree.selection()
        if not pilihan:
            return

        self.id_terpilih = pilihan[0]
        try:
            data = self.service.semua_pengajuan()
            for item in data:
                if item["id_pengajuan"] == self.id_terpilih:
                    self.entry_nama.delete(0, "end")
                    self.entry_nama.insert(0, item["nama"])
                    self.entry_npm.delete(0, "end")
                    self.entry_npm.insert(0, item["npm"])
                    self.var_jenis.set(item["jenis_surat"])
                    self.var_status.set(item["status"])
                    self.text_keperluan.delete("1.0", "end")
                    self.text_keperluan.insert("1.0", item["keperluan"])
                    break
        except (OSError, ValueError) as error:
            messagebox.showerror("Kesalahan", str(error))

    def bersihkan_form(self):
        """Mengosongkan form dan menghilangkan pilihan pada tabel."""
        self.id_terpilih = None
        self.entry_nama.delete(0, "end")
        self.entry_npm.delete(0, "end")
        self.var_jenis.set(JENIS_SURAT[0])
        self.var_status.set(STATUS_PENGAJUAN[0])
        self.text_keperluan.delete("1.0", "end")
        for pilihan in self.tree.selection():
            self.tree.selection_remove(pilihan)

    def cari_data(self):
        """Menampilkan hasil pencarian nama, NPM, atau ID pengajuan."""
        try:
            self.muat_data(self._data_sesuai_filter())
        except (ValueError, OSError) as error:
            messagebox.showerror("Pencarian Gagal", str(error))

    def reset_pencarian(self):
        """Menghapus kata pencarian dan menampilkan seluruh data."""
        self.var_cari.set("")
        self.muat_data()

    def urutkan_data(self):
        """Menerapkan Bubble Sort sesuai kolom dan arah yang dipilih."""
        try:
            self.muat_data(self._data_sesuai_filter())
        except (ValueError, OSError) as error:
            messagebox.showerror("Pengurutan Gagal", str(error))
