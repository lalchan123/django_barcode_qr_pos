# Django Barcode & QR POS (MVT)

## Requirements
- Python 3.10+
- USB barcode scanner (keyboard/HID mode recommended)
- Optional thermal receipt printer (58mm or 80mm)

## Windows setup
```bat
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations products sales
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000/

## First use
1. Open Products > Add Product.
2. Enter a unique SKU and barcode value. Code 128 accepts common alphanumeric values. EAN-13 requires 13 digits.
3. Save; barcode and QR images are generated in `media/barcodes/`.
4. Open Print labels and print the product label.
5. Open POS, focus the scan box, and scan. Most USB scanners type the code and send Enter.
6. Complete Sale & Print Receipt.

## Scanner notes
- Connect the scanner by USB and configure it as USB HID Keyboard.
- Configure a suffix of Enter/CR after each scan.
- Test in Notepad first. If the code appears followed by a new line, the scanner is sending keyboard input correctly.
- This starter uses a keyboard-wedge USB scanner. Serial/COM scanners need a different integration.

## Important production notes
This is a local starter project, not yet a production-ready multi-user POS. Before live deployment add authentication/permissions, store/warehouse separation, tax rules, payment methods, audit logs, backups, invoice numbering concurrency protection, stock movement ledger, and HTTPS/security settings. Replace the sample store name and configure receipt printer paper size in the browser print dialog.
