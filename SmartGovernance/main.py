"""File utama untuk menjalankan aplikasi Smart Governance."""

import tkinter as tk

from ui import SmartGovernanceApp


def main():
    """Membuat jendela utama lalu menjalankan event loop Tkinter."""
    root = tk.Tk()
    SmartGovernanceApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
