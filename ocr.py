import cv2
import pytesseract
import re

# Load gambar
img_path = "dataset/images/val/100000_3.jpg"
img = cv2.imread(img_path)

if img is None:
    raise FileNotFoundError(f"Gambar '{img_path}' tidak ditemukan!")

# Preprocessing
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# threshold / binarize supaya OCR lebih akurat
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Jalankan OCR (digits only)
custom_config = r'--psm 6 -c tessedit_char_whitelist=0123456789'
text = pytesseract.image_to_string(thresh, config=custom_config)

# Ambil semua angka
numbers = re.findall(r'\d+', text)
print("Angka terdeteksi:", numbers)

# Filter angka >= 100
nominals = [int(n) for n in numbers if int(n) >= 100]

# Hitung jumlah tiap nominal (opsional)
counts = {}
for n in nominals:
    counts[n] = counts.get(n, 0) + 1

print("Nominal terdeteksi:", counts)
