import cv2
import os
import sys

# ======================
# Load gambar
# ======================
if len(sys.argv) < 2:
    print("Usage: python cropper_fast.py image.jpg")
    exit(1)

img_path = sys.argv[1]
img = cv2.imread(img_path)

if img is None:
    raise FileNotFoundError(f"Gambar '{img_path}' tidak ditemukan!")

clone = img.copy()
cropping = False
start_point = (0, 0)
end_point = (0, 0)

# Folder output
nominal = "100000"
out_dir = f"../dataset/val/{nominal}"
os.makedirs(out_dir, exist_ok=True)

counter = len(os.listdir(out_dir)) + 1


def mouse_crop(event, x, y, flags, param):
    global start_point, end_point, cropping, counter

    if event == cv2.EVENT_LBUTTONDOWN:
        start_point = (x, y)
        end_point = (x, y)
        cropping = True

    elif event == cv2.EVENT_MOUSEMOVE and cropping:
        end_point = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        cropping = False
        end_point = (x, y)

        x1, y1 = start_point
        x2, y2 = end_point
        x_min, x_max = sorted([x1, x2])
        y_min, y_max = sorted([y1, y2])

        cropped = clone[y_min:y_max, x_min:x_max]

        if cropped.size > 0:
            filename = f"{out_dir}/{nominal}_{counter}.jpg"
            cv2.imwrite(filename, cropped)
            print(f"[Saved] {filename}")
            counter += 1


cv2.namedWindow("Cropper", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Cropper", 1280, 720)  # tidak fullscreen
cv2.setMouseCallback("Cropper", mouse_crop)

print("🟩 Klik & drag untuk crop")
print("❌ Tekan 'q' untuk keluar")

while True:
    frame = clone.copy()

    if cropping:
        cv2.rectangle(frame, start_point, end_point, (0, 255, 0), 2)

    cv2.imshow("Cropper", frame)
    key = cv2.waitKey(10)

    if key == ord("q"):
        break

cv2.destroyAllWindows()
