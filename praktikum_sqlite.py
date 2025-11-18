import sqlite3
import tkinter as tk
import tkinter.messagebox as msg
from tkinter import ttk


def koneksi():
    con = sqlite3.connect("prediksi_prodi.db")
    return con


def create_table():
    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi INTEGER NOT NULL,
            fisika INTEGER NOT NULL,
            inggris INTEGER NOT NULL,
            prediksi_fakultas TEXT NOT NULL
        )
    """)
    con.commit()
    con.close()


def insert_nilai(nama: str, biologi: int, fisika: int, inggris: int, prediksi: str):
    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, biologi, fisika, inggris, prediksi))
    con.commit()
    rowid = cur.lastrowid
    con.close()
    return rowid


def read_nilai():
    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        SELECT id, nama_siswa, biologi, fisika, inggris, prediksi_fakultas 
        FROM nilai_siswa ORDER BY id
    """)
    rows = cur.fetchall()
    con.close()
    return rows


create_table()


class AplikasiPrediksi(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikasi Prediksi Prodi")
        self.geometry("700x550")
        self.configure(bg="#EBA206")

        # Frame untuk input
        frm_input = tk.Frame(self, bg="#FFFFFF", padx=15, pady=15)
        frm_input.pack(padx=20, pady=15, fill="x")

        # Input Nama Siswa
        tk.Label(frm_input, text="Nama Siswa:", bg="#FFFFFF", font=("Arial", 10)).grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.ent_nama = tk.Entry(frm_input, width=35, bd=3)
        self.ent_nama.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        # Input Nilai Biologi
        tk.Label(frm_input, text="Nilai Biologi:", bg="#FFFFFF", font=("Arial", 10)).grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.ent_biologi = tk.Entry(frm_input, width=35, bd=3)
        self.ent_biologi.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # Input Nilai Fisika
        tk.Label(frm_input, text="Nilai Fisika:", bg="#FFFFFF", font=("Arial", 10)).grid(
            row=2, column=0, sticky="w", pady=5
        )
        self.ent_fisika = tk.Entry(frm_input, width=35, bd=3)
        self.ent_fisika.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        # Input Nilai Inggris
        tk.Label(frm_input, text="Nilai Inggris:", bg="#FFFFFF", font=("Arial", 10)).grid(
            row=3, column=0, sticky="w", pady=5
        )
        self.ent_inggris = tk.Entry(frm_input, width=35, bd=3)
        self.ent_inggris.grid(row=3, column=1, sticky="w", padx=10, pady=5)

        # Frame untuk tombol
        btn_frame = tk.Frame(frm_input, bg="#FFFFFF")
        btn_frame.grid(row=4, column=0, columnspan=2, pady=15)

        self.btn_submit = tk.Button(
            btn_frame, text="Submit Nilai", width=15, bg="#4CAF50", fg="white",
            font=("Arial", 10, "bold"), command=self.submit_nilai
        )
        self.btn_submit.pack(side="left", padx=5)

        self.btn_refresh = tk.Button(
            btn_frame, text="Refresh Data", width=15, bg="#2196F3", fg="white",
            font=("Arial", 10, "bold"), command=self.refresh_data
        )
        self.btn_refresh.pack(side="left", padx=5)

        # Label untuk hasil prediksi
        self.lbl_hasil = tk.Label(
            self, text="Hasil Prediksi: -", bg="#EBA206", fg="#FFFFFF",
            font=("Arial", 12, "bold"), pady=10
        )
        self.lbl_hasil.pack(pady=10)

        # Treeview untuk menampilkan data
        cols = ("id", "nama", "biologi", "fisika", "inggris", "prediksi")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=8)
        
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=40, anchor="center")
        self.tree.heading("nama", text="Nama Siswa")
        self.tree.column("nama", width=150)
        self.tree.heading("biologi", text="Biologi")
        self.tree.column("biologi", width=80, anchor="center")
        self.tree.heading("fisika", text="Fisika")
        self.tree.column("fisika", width=80, anchor="center")
        self.tree.heading("inggris", text="Inggris")
        self.tree.column("inggris", width=80, anchor="center")
        self.tree.heading("prediksi", text="Prediksi Fakultas")
        self.tree.column("prediksi", width=150, anchor="center")
        
        self.tree.pack(padx=20, pady=(0, 20), fill="both", expand=True)

        # Load data awal
        self.refresh_data()

    def clear_inputs(self):
        self.ent_nama.delete(0, tk.END)
        self.ent_biologi.delete(0, tk.END)
        self.ent_fisika.delete(0, tk.END)
        self.ent_inggris.delete(0, tk.END)
        self.lbl_hasil.config(text="Hasil Prediksi: -")

    def validate_inputs(self):
        nama = self.ent_nama.get().strip()
        biologi_str = self.ent_biologi.get().strip()
        fisika_str = self.ent_fisika.get().strip()
        inggris_str = self.ent_inggris.get().strip()

        if not nama:
            msg.showwarning("Peringatan", "Nama siswa tidak boleh kosong!")
            return None

        try:
            biologi = int(biologi_str)
            fisika = int(fisika_str)
            inggris = int(inggris_str)

            if biologi < 0 or fisika < 0 or inggris < 0:
                raise ValueError("Nilai tidak boleh negatif")
            if biologi > 100 or fisika > 100 or inggris > 100:
                raise ValueError("Nilai tidak boleh lebih dari 100")

        except ValueError as e:
            msg.showerror("Error", f"Nilai harus berupa angka bulat 0-100!\n{str(e)}")
            return None

        return nama, biologi, fisika, inggris

    def prediksi_fakultas(self, biologi: int, fisika: int, inggris: int):
        nilai_max = max(biologi, fisika, inggris)
        
        if biologi == nilai_max:
            return "Kedokteran"
        elif fisika == nilai_max:
            return "Teknik"
        else:
            return "Bahasa"

    def submit_nilai(self):
        val = self.validate_inputs()
        if not val:
            return

        nama, biologi, fisika, inggris = val
        prediksi = self.prediksi_fakultas(biologi, fisika, inggris)

        try:
            new_id = insert_nilai(nama, biologi, fisika, inggris, prediksi)
            self.lbl_hasil.config(text=f"Hasil Prediksi: {prediksi}")
            msg.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
            self.refresh_data()
            self.clear_inputs()
        except Exception as e:
            msg.showerror("Database Error", f"Gagal menyimpan data:\n{str(e)}")

    def refresh_data(self):
        # Hapus data lama di treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            rows = read_nilai()
            for r in rows:
                self.tree.insert("", tk.END, values=r)
        except Exception as e:
            msg.showerror("Database Error", f"Gagal membaca data:\n{str(e)}")


if __name__ == "__main__":
    app = AplikasiPrediksi()
    app.mainloop()