import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import pytesseract
import os
import process_image  # Fungsi deteksi plat

# Fungsi Input Gambar
def input_gambar():
    global img_path
    img_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
    if img_path:
        img = Image.open(img_path).resize((int(image_width), int(image_height)))
        img_tk = ImageTk.PhotoImage(img)
        label1.config(image=img_tk, text="")
        label1.image = img_tk

# Fungsi Proses Gambar
def proses_gambar():
    global img_path
    if not img_path:
        print("Belum ada gambar yang diinput!")
        return
    
    # Membaca gambar
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # ===== Preprocessing 1: CLAHE (Peningkatan Kontras) =====
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    clahe_path = os.path.join(os.path.dirname(img_path), "clahe.jpg")
    cv2.imwrite(clahe_path, enhanced)
    tampilkan_gambar(clahe_path, label2)
    
    # ===== Preprocessing 2: Gaussian Blur =====
    gaussian_blur = cv2.GaussianBlur(enhanced, (3, 3), 0)
    blur_path = os.path.join(os.path.dirname(img_path), "gaussian_blur.jpg")
    cv2.imwrite(blur_path, gaussian_blur)
    tampilkan_gambar(blur_path, label3)
    
    # ===== Preprocessing 3: Adaptive Thresholding =====
    adaptive_thresh = cv2.adaptiveThreshold(gaussian_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                            cv2.THRESH_BINARY, 11, 2)
    thresh_path = os.path.join(os.path.dirname(img_path), "adaptive_thresh.jpg")
    cv2.imwrite(thresh_path, adaptive_thresh)
    tampilkan_gambar(thresh_path, label4)

    # ===== Preprocessing 4: Edge Detection (Canny) =====
    edges = cv2.Canny(adaptive_thresh, 50, 150)
    edges_path = os.path.join(os.path.dirname(img_path), "edges.jpg")
    cv2.imwrite(edges_path, edges)
    tampilkan_gambar(edges_path, label5)
    
    # ===== Proses Morfologi Closing =====
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    closing = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    closing_path = os.path.join(os.path.dirname(img_path), "closing.jpg")
    cv2.imwrite(closing_path, closing)
    tampilkan_gambar(closing_path, label6)

    # ===== Deteksi Plat Nomor =====
    hasil_path = process_image.deteksi_plat(img_path)  # Deteksi plat dari file process_image.py
    if hasil_path:
        tampilkan_gambar(hasil_path, label6)
    else:
        print("Plat nomor tidak terdeteksi!")

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
screen_width = 1024
screen_height = 768
root.geometry(f"{screen_width}x{screen_height}")

# Dimensi area gambar
left_width = screen_width * 0.25
right_width = screen_width * 0.75
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

# Area 6 Gambar
label1 = tk.Label(frame_right, bg="lightblue", text="Gambar Input", borderwidth=2, relief="solid")
label1.place(x=0, y=0, width=image_width, height=image_height)

label2 = tk.Label(frame_right, bg="lightgreen", text="CLAHE", borderwidth=2, relief="solid")
label2.place(x=image_width, y=0, width=image_width, height=image_height)

label3 = tk.Label(frame_right, bg="lightpink", text="Gaussian Blur", borderwidth=2, relief="solid")
label3.place(x=image_width * 2, y=0, width=image_width, height=image_height)

label4 = tk.Label(frame_right, bg="lightyellow", text="Adaptive Threshold", borderwidth=2, relief="solid")
label4.place(x=0, y=image_height, width=image_width, height=image_height)

label5 = tk.Label(frame_right, bg="lightcyan", text="Edge Detection", borderwidth=2, relief="solid")
label5.place(x=image_width, y=image_height, width=image_width, height=image_height)

label6 = tk.Label(frame_right, bg="lightgray", text="Hasil Deteksi Plat", borderwidth=2, relief="solid")
label6.place(x=image_width * 2, y=image_height, width=image_width, height=image_height)

# Menjalankan aplikasi
root.mainloop()
