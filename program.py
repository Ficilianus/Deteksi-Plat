import cv2
import imutils
import numpy as np
import pytesseract
import matplotlib.pyplot as plt

# Konfigurasi path untuk Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Path ke gambar
image_path = r'image1.jpg'

# Baca gambar
img = cv2.imread(image_path, cv2.IMREAD_COLOR)
if img is None:
    print(f"Error: Tidak dapat membaca gambar pada path {image_path}. Pastikan path benar.")
    exit()

# Ubah ukuran gambar untuk konsistensi
img = cv2.resize(img, (600, 400))

# Konversi ke grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Bilateral filter untuk menghaluskan gambar
gray = cv2.bilateralFilter(gray, 13, 15, 15)

# Deteksi tepi menggunakan Canny
edged = cv2.Canny(gray, 30, 200)

# Temukan kontur
contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
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
    print("No contour detected")
else:
    cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)

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
else:
    print("Tidak ada area yang terdeteksi untuk dipotong.")
    exit()

# OCR pada area yang dipotong
text = pytesseract.image_to_string(Cropped, config='--psm 11')
print("Programming_fever's License Plate Recognition\n")
print("Detected license plate Number is:", text)

# Tampilkan gambar menggunakan matplotlib
def display_image(image, title="Image"):
    plt.figure(figsize=(10, 5))
    if len(image.shape) == 3:  # Gambar berwarna
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    else:  # Gambar grayscale
        plt.imshow(image, cmap='gray')
    plt.title(title)
    plt.axis("off")
    plt.show()

# Tampilkan gambar asli dan hasil cropping
display_image(cv2.resize(img, (500, 300)), title="Original Image")
display_image(cv2.resize(Cropped, (400, 200)), title="Cropped License Plate")
