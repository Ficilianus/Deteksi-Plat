import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import os
import process_image
from tkinter import messagebox
import process_image

# Fungsi Input Gambar
def input_gambar():
    global img_path
    img_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
    if img_path:
        img = Image.open(img_path).resize((int(image_width), int(image_height)))
        img_tk = ImageTk.PhotoImage(img)
        label1.config(image=img_tk, text="")
        label1.image = img_tk
# Fungsi untuk memproses gambar 
def proses_gambar():
    global img_path
    if not img_path:
        messagebox.showerror("Error", "Silakan input gambar terlebih dahulu!")
        return

    # Panggil fungsi pemrosesan gambar
    results, status = process_image.process_image(img_path)

    if not status:  # Jika plat nomor tidak ditemukan
        messagebox.showwarning("Peringatan", "Plat nomor tidak dapat ditemukan pada gambar.")
    else:
        # Tampilkan hasil gambar di setiap tahap
        tampilkan_gambar(img_path, label1)  # Gambar asli
           
        # Grayscale
        cv2.imwrite("temp_grayscale.jpg", results['grayscale'])
        tampilkan_gambar("temp_grayscale.jpg", label2)

        # Gaussian Blur
        cv2.imwrite("temp_blur.jpg", results['gaussian_blur'])
        tampilkan_gambar("temp_blur.jpg", label3)

        # Adaptive Thresholding
        cv2.imwrite("temp_thresh.jpg", results['threshold'])
        tampilkan_gambar("temp_thresh.jpg", label4)

        # Edge Detection
        cv2.imwrite("temp_edges.jpg", results['edges'])
        tampilkan_gambar("temp_edges.jpg", label5)

        # Gambar kendaraan dengan border plat nomor
        cv2.imwrite("temp_with_border.jpg", results['detected_plate_with_border'])
        tampilkan_gambar("temp_with_border.jpg", label6)

        # Crop Plat Nomor
        if results['cropped_plate'] is not None:
            cv2.imwrite("temp_crop.jpg", results['cropped_plate'])
            tampilkan_gambar("temp_crop.jpg", label7)

# Fungsi Tampilkan Gambar
def tampilkan_gambar(path, label):
    img = Image.open(path).resize((int(image_width), int(image_height)))
    img_tk = ImageTk.PhotoImage(img)
    label.config(image=img_tk, text="")
    label.image = img_tk

# Fungsi Keluar
def keluar():
    root.destroy()

# ===== GUI Setup =====
root = tk.Tk()
root.title("Aplikasi Deteksi Plat Nomor")

# Perbesar ukuran GUI
screen_width = 1280
screen_height = 768
root.geometry(f"{screen_width}x{screen_height}")

# Dimensi area gambar
left_width = screen_width * 0.2
right_width = screen_width * 0.8
image_width = right_width / 3
image_height = screen_height / 2
img_path = None

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

# Area 7 Gambar
label1 = tk.Label(frame_right, bg="lightblue", text="Gambar Input", borderwidth=2, relief="solid")
label1.place(x=0, y=0, width=image_width, height=image_height)

label2 = tk.Label(frame_right, bg="lightgreen", text="Grayscale", borderwidth=2, relief="solid")
label2.place(x=image_width, y=0, width=image_width, height=image_height)

label3 = tk.Label(frame_right, bg="lightpink", text="Gaussian Blur", borderwidth=2, relief="solid")
label3.place(x=image_width * 2, y=0, width=image_width, height=image_height)

label4 = tk.Label(frame_right, bg="lightyellow", text="Thresholding", borderwidth=2, relief="solid")
label4.place(x=image_width * 3, y=0, width=image_width, height=image_height)

label5 = tk.Label(frame_right, bg="lightcyan", text="Edge Detection", borderwidth=2, relief="solid")
label5.place(x=0, y=image_height, width=image_width, height=image_height)

label6 = tk.Label(frame_right, bg="lightgray", text="Hasil Deteksi Plat", borderwidth=2, relief="solid")
label6.place(x=image_width, y=image_height, width=image_width, height=image_height)

label7 = tk.Label(frame_right, bg="lightcoral", text="Crop Plat Nomor", borderwidth=2, relief="solid")
label7.place(x=image_width * 2, y=image_height, width=image_width, height=image_height)

# Menjalankan aplikasi
root.mainloop()
