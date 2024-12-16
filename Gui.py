import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import process_image  # Mengimpor file kedua

def input_gambar():
    global img_path
    img_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
    if img_path:
        img = Image.open(img_path)
        img = img.resize((int(image_width), int(image_height)))  # Resize untuk ditampilkan di area gambar 1
        img_tk = ImageTk.PhotoImage(img)
        label1.config(image=img_tk)
        label1.image = img_tk

def proses_gambar():
    global img_path
    if not img_path:
        print("Belum ada gambar yang diinput!")
        return
    
    # Memanggil fungsi pemrosesan di file process_image.py
    hasil_path = process_image.deteksi_plat(img_path)  # Fungsi ini akan memproses gambar dan mengembalikan path hasil
    
    # Menampilkan hasil pada area gambar 2
    img = Image.open(hasil_path)
    img = img.resize((int(image_width), int(image_height)))  # Resize untuk ditampilkan di area gambar 2
    img_tk = ImageTk.PhotoImage(img)
    label2.config(image=img_tk)
    label2.image = img_tk

def keluar():
    root.destroy()

# Inisialisasi Tkinter
root = tk.Tk()
root.title("Aplikasi Deteksi Plat")

# Mendapatkan ukuran layar
screen_width = 1024
screen_height =768


# Mengatur ukuran window mengikuti layar
root.geometry(f"{screen_width}x{screen_height}")

# Dimensi pembagian
left_width = screen_width * 0.25
right_width = screen_width * 0.75
image_width = right_width / 2
image_height = screen_height / 2
img_path = None  # Untuk menyimpan path gambar input

# Frame kiri untuk tombol
frame_left = tk.Frame(root, width=left_width, height=screen_height, bg="lightgray")
frame_left.pack(side="left", fill="y")

btn_input = tk.Button(frame_left, text="Input Gambar", command=input_gambar, width=20)
btn_input.pack(pady=10)

btn_proses = tk.Button(frame_left, text="Proses Gambar", command=proses_gambar, width=20)
btn_proses.pack(pady=10)

btn_keluar = tk.Button(frame_left, text="Keluar", command=keluar, width=20)
btn_keluar.pack(pady=10)

# Frame kanan untuk menampilkan gambar
frame_right = tk.Frame(root, width=right_width, height=screen_height, bg="white")
frame_right.pack(side="right", fill="both", expand=True)

# Membuat Canvas untuk menambahkan garis
canvas = tk.Canvas(frame_right, width=right_width, height=screen_height, bg="white", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Menambahkan garis pembagi
canvas.create_line(right_width / 2, 0, right_width / 2, screen_height, fill="black", width=3)
canvas.create_line(0, screen_height / 2, right_width, screen_height / 2, fill="black", width=3)

# Membagi area gambar menjadi 2 bagian
label1 = tk.Label(canvas, bg="lightblue", text="Gambar Input", borderwidth=2, relief="solid")
label1.place(x=0, y=0, width=image_width, height=image_height)

label2 = tk.Label(canvas, bg="lightgreen", text="Hasil Proses", borderwidth=2, relief="solid")
label2.place(x=image_width, y=0, width=image_width, height=image_height)

label3 = tk.Label(canvas, bg="lightpink", text="Gambar 3", borderwidth=2, relief="solid")
label3.place(x=0, y=image_height, width=image_width, height=image_height)

label4 = tk.Label(canvas, bg="lightyellow", text="Gambar 4", borderwidth=2, relief="solid")
label4.place(x=image_width, y=image_height, width=image_width, height=image_height)


# Menjalankan aplikasi
root.mainloop()
