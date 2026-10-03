# CitraDigital7 - Prototype Verifikasi Ijazah

Prototype ini dibuat untuk membaca **nomor ijazah menggunakan OCR** dan mendeteksi **keberadaan tanda tangan** pada citra ijazah.

## Tujuan

Sistem mampu:

1. Membaca nomor ijazah menggunakan OCR.
2. Meningkatkan kualitas citra sebelum proses OCR.
3. Mendeteksi keberadaan tanda tangan menggunakan thresholding dan morphology.
4. Menghasilkan hasil verifikasi berdasarkan nomor ijazah dan tanda tangan.
5. Membandingkan metode enhancement menggunakan nilai Character Error Rate (CER).

## Pipeline Sistem

```text
Citra Ijazah
     ↓
Perbaikan Orientasi
     ↓
Grayscale
     ↓
Image Enhancement
     ↓
 ┌───────────────────────┬────────────────────────┐
 ↓                       ↓
Area Nomor Ijazah        Area Tanda Tangan
 ↓                       ↓
Brightness Adjustment    Grayscale
 ↓                       ↓
OCR                      Thresholding Otsu
 ↓                       ↓
Nomor Ijazah             Morphology
                         ↓
                    Signature Detection
 └───────────────────────┴────────────────────────┘
                         ↓
                  Hasil Verifikasi
```

## Metode yang Digunakan

### 1. Grayscale

Citra berwarna dikonversi menjadi citra grayscale untuk menyederhanakan informasi intensitas sebelum dilakukan enhancement dan pengolahan lebih lanjut.

### 2. Brightness Adjustment

Brightness Adjustment digunakan dengan menambahkan nilai intensitas sebesar 30.

```text
alpha = 1.0
beta = 30
```

Metode ini digunakan pada area nomor ijazah sebelum OCR.

### 3. Contrast Stretching

Contrast Stretching memperluas rentang intensitas citra dari nilai minimum dan maksimum menjadi rentang 0-255.

### 4. Histogram Equalization

Histogram Equalization digunakan untuk meratakan distribusi intensitas piksel agar kontras citra meningkat.

### 5. OCR

OCR dilakukan menggunakan **Tesseract OCR** dengan konfigurasi:

```text
--psm 7
```

Sistem kemudian mengambil karakter angka da
