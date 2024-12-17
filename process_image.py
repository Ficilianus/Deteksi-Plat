import cv2
import os

def process_image(input_path):
    """
    Fungsi untuk memproses gambar input dengan tahapan:
    1. Grayscale
    2. Gaussian Blur (Noise Removal)
    3. Adaptive Thresholding
    4. Edge Detection (Canny)
    5. Crop Plat Nomor (Menggunakan Contour Terbesar)

    Args:
        input_path (str): Path gambar input.

    Returns:
        dict: Dictionary berisi semua hasil tahapan pemrosesan gambar.
        bool: Status apakah plat nomor ditemukan atau tidak.
    """
    results = {}  # Menyimpan hasil gambar di setiap tahapan

    # Pastikan gambar ada
    if not os.path.exists(input_path):
        print("File gambar tidak ditemukan!")
        return None, False

    # 1. Baca Gambar
    img = cv2.imread(input_path)
    if img is None:
        print("Gagal membaca gambar!")
        return None, False
    results['original'] = img  # Simpan gambar asli

    # 2. Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    results['grayscale'] = gray

    # 3. Noise Removal - Gaussian Blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    results['gaussian_blur'] = blur

    # 4. Adaptive Thresholding
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    results['threshold'] = thresh

    # 5. Edge Detection - Canny
    edges = cv2.Canny(thresh, 50, 150)
    results['edges'] = edges

    # 6. Contour Detection & Crop (Plat Nomor)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # Ambil contour terbesar
        contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(contour)

        # Validasi ukuran contour agar masuk akal
        if w > 50 and h > 20:  # Ukuran minimal plat nomor
            crop_img = img[y:y+h, x:x+w]
            results['cropped_plate'] = crop_img
            return results, True  # Berhasil menemukan plat nomor
    # Jika tidak ada kontur atau ukuran tidak valid
    print("Plat nomor tidak terdeteksi.")
    results['cropped_plate'] = None
    return results, False
