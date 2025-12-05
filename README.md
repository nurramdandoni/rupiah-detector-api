# rupiah-detector-api
Deteksi Nominal Rupiah via foto from esp32

## Project Structure

rupiah-detector/
├─ .venv/
├─ requirements.txt
├─ app.py                 # Flask API (serving)
├─ model/                 # akan berisi model.pt setelah training
│   └─ best.pt
├─ dataset/
│   ├─ images/
│   │  ├─ train/
│   │  └─ val/
│   └─ labels/
│      ├─ train/
│      └─ val/
└─ data.yaml              # config untuk training YOLO

## Preparing

1. Membuat virtual env untuk menjalankan project 'python3 -m venv .venv'
2. Aktivasi env 'source .venv/bin/activate'
3. Install dependency 'pip install -r requirements.txt'

