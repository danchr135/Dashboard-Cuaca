# Dashboard Analisis Cuaca

Dashboard Streamlit untuk membaca dan menampilkan ringkasan data cuaca harian.
Dashboard menampilkan tren rata-rata suhu, rata-rata tekanan udara, dan rekor
angin terkencang.

## Sumber Data

Sumber data awal adalah file CSV berikut:

```text
data/data_cuaca.csv
```

File tersebut berisi sekitar 1.587.257 baris data mentah. Script
`src/extact.py` menggunakan pandas untuk membaca CSV dan memastikan file dapat
dibaca. Nama script dipertahankan sesuai struktur proyek saat ini.

## Alur Perpindahan Data

```text
CSV mentah
  -> src/extact.py (baca dan cek jumlah baris)
  -> src/load_data.py (muat ke MySQL)
  -> dataset_cuaca.staging_weather
  -> proses agregasi di database
  -> dataset_cuaca.summary_wheater
  -> tampilan/app.py (query dan visualisasi Streamlit)
```

`src/load_data.py` membaca CSV dengan pandas lalu menggunakan SQLAlchemy untuk
menambahkan data ke tabel `staging_weather` pada database MySQL
`dataset_cuaca`. Tabel `summary_wheater` adalah tabel ringkasan yang dibaca
oleh dashboard. Query pembentukan tabel ringkasan belum disimpan sebagai script
SQL di repository ini, sehingga proses agregasinya perlu dijalankan atau
didokumentasikan terpisah dari kode yang tersedia.

## Transformasi Data

Dashboard mengambil kolom berikut dari `summary_wheater`:

| Kolom                    | Kegunaan                      |
| ------------------------ | ----------------------------- |
| `tanggal`                | Sumbu waktu grafik            |
| `rata_rata_suhu`         | Nilai suhu rata-rata harian   |
| `rata_rata_tekanan`      | Nilai tekanan udara rata-rata |
| `rekor_angin_terkencang` | Nilai angin terkuat harian    |

Sebelum divisualisasikan, aplikasi:

1. Mengubah `tanggal` menjadi tipe datetime.
2. Mengubah kolom pengukuran menjadi numerik.
3. Mengonversi suhu dari Fahrenheit ke Celsius dengan rumus
   `(Fahrenheit - 32) * 5 / 9`.
4. Menghapus baris yang tidak memiliki tanggal.
5. Mengurutkan data berdasarkan tanggal.

Hasil transformasi hanya berada di memori aplikasi. Data di MySQL tidak diubah
oleh dashboard.

## Penyimpanan

- Data mentah: `data/data_cuaca.csv`
- Data staging: MySQL `dataset_cuaca.staging_weather`
- Data ringkasan: MySQL `dataset_cuaca.summary_wheater`
- Visualisasi: aplikasi Streamlit di `tampilan/app.py`

Konfigurasi koneksi saat ini menggunakan MySQL lokal dengan user `root` tanpa
password. Untuk deployment, gunakan environment variable atau secrets
Streamlit, bukan menyimpan kredensial di source code.

## Validasi Data

Jalankan validasi dengan:

```powershell
python src/validation.py
```

`src/validation.py` membaca `summary_wheater` dan memeriksa:

- jumlah baris lebih dari nol;
- nilai `NULL` pada setiap kolom; dan
- jumlah baris duplikat.

Validasi dianggap berhasil apabila tabel tidak kosong, tidak memiliki `NULL`,
dan tidak memiliki duplikasi. Pemeriksaan ini adalah pemeriksaan kualitas dasar;
belum mencakup validasi rentang nilai, keunikan tanggal, konsistensi satuan,
atau rekonsiliasi jumlah baris antara CSV, staging, dan tabel ringkasan.

## Menjalankan Dashboard

Pastikan MySQL aktif dan tabel `summary_wheater` tersedia, lalu jalankan dari
akar proyek:

```powershell
python -m streamlit run tampilan/app.py
```

Dependensi utama:

```text
pandas
matplotlib
mysql-connector-python
sqlalchemy
streamlit
```

## Struktur Proyek

```text
Cuaca/
├── data/
│   └── data_cuaca.csv
├── src/
│   ├── extact.py
│   ├── load_data.py
│   └── validation.py
├── tampilan/
│   └── app.py
└── README.md
```
