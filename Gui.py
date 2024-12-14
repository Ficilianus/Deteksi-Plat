import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
import pytesseract

# Konfigurasi path untuk Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Variabel untuk warna
warna_bg = "#000000"  # Warna background utama
warna_frame_kiri = "#2A2A2A"  # Warna frame kiri
warna_btn = "#4D4D4D"  # Warna tombol
warna_frame_kanan = "#1A1A1A"  # Warna frame kanan
warna_placeholder = "#2A2A2A"  # Warna placeholder gambar
warna_teks_btn = "#D8D9DA"  # Warna teks pada tombol

# Variabel global
loaded_image = None  # Untuk menyimpan gambar yang diunggah
image_path = None  # Path ke gambar yang diunggah

# Fungsi untuk tombol 'Input Gambar'
def input_gambar():
    global loaded_image, image_path
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg *.bmp")])
    if file_path:
        image_path = file_path  # Simpan path gambar
        
        # Baca gambar menggunakan OpenCV
        img = cv2.imread(file_path)
        
        # Dapatkan ukuran frame_gambar untuk menyesuaikan gambar
        frame_width = frame_gambar.winfo_width()  # Lebar frame untuk menampilkan gambar
        frame_height = frame_gambar.winfo_height()  # Tinggi frame untuk menampilkan gambar
        
        # Dapatkan ukuran asli gambar
        height, width = img.shape[:2]
        
        # Hitung faktor skala untuk menjaga rasio aspek
        scaling_factor_width = frame_width / width
        scaling_factor_height = frame_height / height
        scaling_factor = min(scaling_factor_width, scaling_factor_height)  # Pilih faktor skala terkecil
        
        # Resize gambar dengan mempertahankan rasio aspek
        img_resized = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
        
        # Konversi gambar ke format RGB
        img_resized = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)

        # Konversi ke format PIL dan kemudian ke ImageTk
        img_pil = Image.fromarray(img_resized)
        loaded_image = ImageTk.PhotoImage(img_pil)

        # Tampilkan gambar di label
        frame_gambar_content.config(image=loaded_image)
        frame_gambar_content.image = loaded_image

# Fungsi untuk memproses gambar
def proses_gambar():
    if image_path:
        # Baca gambar menggunakan OpenCV
        img = cv2.imread(image_path)
        
        # Konversi ke grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Bilateral filter untuk menghaluskan gambar
        gray = cv2.bilateralFilter(gray, 13, 15, 15)

        # Deteksi tepi menggunakan Canny
        edged = cv2.Canny(gray, 30, 200)

        # Temukan kontur
        contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours[0], key=cv2.contourArea, reverse=True)[:10]
        screenCnt = None

        # Cari kontur dengan 4 titik (seperti pelat nomor)
        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)
            if len(approx) == 4:
                screenCnt = approx
                break

        # Periksa apakah ada kontur ditemukan
        if screenCnt is None:
            result_label.config(text="Plat tidak terdeteksi", fg="red")
        else:
            # Buat mask untuk memotong area pelat nomor
            mask = np.zeros(gray.shape, np.uint8)
            new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1)
            new_image = cv2.bitwise_and(img, img, mask=mask)

            # Potong area pelat nomor
            (x, y) = np.where(mask == 255)
            if x.size > 0 and y.size > 0:
                (topx, topy) = (np.min(x), np.min(y))
                (bottomx, bottomy) = (np.max(x), np.max(y))
                Cropped = gray[topx:bottomx+1, topy:bottomy+1]

                # OCR pada area yang dipotong
                text = pytesseract.image_to_string(Cropped, config='--psm 11')
                result_label.config(text=f"Plat Nomor Terdeteksi: {text.strip()}", fg="green")
            else:
                result_label.config(text="Plat tidak terdeteksi", fg="red")

# Fungsi untuk tombol 'Keluar'
def keluar():
    root.destroy()

# Membuat GUI
root = tk.Tk()
root.title("Deteksi Plat")
root.geometry("800x600")
root.configure(bg=warna_bg)  # Menggunakan variabel warna

# Frame kiri untuk tombol
frame_kiri = tk.Frame(root, bg=warna_frame_kiri, width=200, height=600)
frame_kiri.pack(side="left", fill="y")

# Tombol 'Input Gambar'
btn_input_gambar = tk.Button(
    frame_kiri, text="Input Gambar", bg=warna_btn, fg=warna_teks_btn, command=input_gambar
)
btn_input_gambar.pack(pady=30, padx=20, fill="x")

# Tombol 'Proses Gambar'
btn_proses_gambar = tk.Button(
    frame_kiri, text="Proses Gambar", bg=warna_btn, fg=warna_teks_btn, command=proses_gambar
)
btn_proses_gambar.pack(pady=10, padx=20, fill="x")

# Tombol 'Keluar'
btn_keluar = tk.Button(
    frame_kiri, text="Keluar", bg=warna_btn, fg=warna_teks_btn, command=keluar
)
btn_keluar.pack(pady=10, padx=20, fill="x")

# Area untuk menampilkan gambar (kanan)
frame_gambar = tk.Frame(root, bg=warna_frame_kanan, width=600, height=600)
frame_gambar.pack(side="right", fill="both", expand=True)

# Menambahkan placeholder di frame_gambar
frame_gambar_content = tk.Label(frame_gambar, bg=warna_placeholder, width=100, height=50)
frame_gambar_content.pack(padx=30, pady=30, expand=True)

# Label untuk hasil deteksi plat
result_label = tk.Label(frame_gambar, text="", bg=warna_frame_kanan, fg="white", font=("Arial", 14))
result_label.pack(pady=10)

root.mainloop()
