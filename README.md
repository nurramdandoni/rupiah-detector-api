# rupiah-detector-api
Deteksi Nominal Rupiah via foto from esp32

## Project Structure

![alt text](<Screenshot 2025-12-05 at 15.28.29.png>)

## Preparing

1. Membuat virtual env untuk menjalankan project 'python3 -m venv .venv'
2. Aktivasi env 'source .venv/bin/activate'
3. Install dependency 'pip3 install -r requirements.txt'

## Add more train
1. Untuk meningkatkan akurasi bisa menggunakan https://www.makesense.ai/ untuk melakukan training image labeling

## Training Model First
1. jalankan 'yolo train model=yolo11m-cls.pt data=dataset epochs=50 imgsz=256'

### Retraining
1. jalankan 'yolo train model=runs/classify/exp/weights/best.pt data=dataset epochs=20 imgsz=256'

