import cv2
import imutils
import numpy as np
import pytesseract
import os

# Pastikan Pytesseract sudah diinstal di sistem Anda
# Jika menggunakan Windows, pastikan path Tesseract sudah benar.
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def deteksi_plat(image_path):
    """
    Fungsi untuk mendeteksi plat nomor pada gambar menggunakan OpenCV dan Pytesseract.
    """
    # Membaca gambar
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Gambar tidak ditemukan!")

    img = cv2.resize(img, (600, 400))  # Resize gambar untuk mempermudah deteksi

    # Konversi ke grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 13, 15, 15)  # Menghilangkan noise sambil mempertahankan tepi

    # Deteksi tepi
    edged = cv2.Canny(gray, 30, 200)

    # Temukan kontur
    contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]  # Urutkan berdasarkan ukuran

    screenCnt = None

    # Cari kontur yang memiliki bentuk persegi panjang
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        if len(approx) == 4:  # Jika ditemukan 4 sisi (persegi panjang)
            screenCnt = approx
            break

    if screenCnt is None:
        print("Tidak ada plat nomor yang terdeteksi.")
        return None

    # Gambar kontur pada gambar asli dengan warna hijau
    cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)

    # Buat masker untuk mengekstraksi area plat
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)

    # Crop area plat
    (x, y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    cropped = gray[topx:bottomx+1, topy:bottomy+1]

    # Simpan hasil gambar dan area cropped
    hasil_path = os.path.join(os.path.dirname(image_path), "hasil_deteksi.jpg")
    crop_path = os.path.join(os.path.dirname(image_path), "crop_plate.jpg")

    cv2.imwrite(hasil_path, img)  # Menyimpan gambar dengan kotak deteksi
    cv2.imwrite(crop_path, cropped)  # Menyimpan gambar crop

    # Gunakan pytesseract untuk membaca teks (opsional)
    try:
        text = pytesseract.image_to_string(cropped, config='--psm 11')
        print("Plat nomor terdeteksi:", text.strip())
    except Exception as e:
        print("Gagal membaca teks dari plat:", e)

    return hasil_path
