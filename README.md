# SewaSmash - Sistem Booking Lapangan Badminton

SewaSmash adalah aplikasi web berbasis Django yang dirancang untuk memudahkan proses manajemen dan pemesanan lapangan badminton secara online. Aplikasi ini hadir sebagai solusi atas berbagai kendala dalam sistem booking manual yang tidak efisien dan rawan kesalahan. Melalui SewaSmash, pengguna dapat melakukan pemesanan lapangan kapan saja dengan tampilan jadwal yang real-time serta pilihan waktu dan lapangan yang fleksibel. Proses booking yang sederhana, antarmuka yang ramah pengguna, dan konfirmasi otomatis menjadikan pengalaman pengguna lebih nyaman dan praktis. Bagi pengelola, sistem ini menawarkan dashboard administrasi yang komprehensif untuk memantau, menyetujui, dan mengatur jadwal pemesanan secara terpusat. Dengan fitur-fitur tersebut, SewaSmash menjadi solusi digital yang efektif untuk meningkatkan efisiensi operasional dan kepuasan pelanggan dalam layanan penyewaan lapangan badminton.

## Prasyarat

- Python 3.10 atau lebih baru
- pip (Python package installer)
- Git

## Instalasi

1. Clone repository
```bash
git clone https://github.com/nashedalii/Kelompok-5-PPL-UAS.git
cd Kelompok-5-PPL-UAS
```

2. Buat virtual environment
```bash
python -m venv venv
```

3. Aktifkan virtual environment
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Install dependencies
```bash
pip install -r requirements.txt
```

5. Jalankan migrasi database
```bash
python manage.py migrate
```

6. Buat superuser (admin)
```bash
python manage.py createsuperuser
```

7. Jalankan server development
```bash
python manage.py runserver
```

## Penggunaan

1. Akses aplikasi
- Buka browser dan kunjungi `http://127.0.0.1:8000`
- Untuk akses admin: `http://127.0.0.1:8000/admin`

2. Fitur Admin
- Login menggunakan akun superuser
- Kelola data lapangan (court)
- Kelola pemesanan (booking)
- Lihat laporan dan statistik
- Approve/reject pemesanan

3. Fitur Pengguna
- Lihat ketersediaan lapangan
- Buat pemesanan lapangan
- Pilih waktu dan durasi
- Lihat status pemesanan
- Lihat jadwal lapangan

## Struktur Proyek

```
├── SewaSmash/                    # Aplikasi utama
│   ├── migrations/               # Database migrations
│   ├── templates/SewaSmash/      # Template HTML
│   │   ├── admin_booking_form.html   # Form admin untuk booking
│   │   ├── base.html                # Template dasar
│   │   ├── booking_confirmation.html # Konfirmasi booking
│   │   ├── booking_delete.html      # Konfirmasi hapus booking
│   │   ├── booking_detail.html      # Detail booking
│   │   ├── booking_form.html        # Form booking user
│   │   ├── booking_list.html        # Daftar booking
│   │   ├── dashboard.html           # Dashboard admin
│   │   ├── homepage.html            # Halaman utama
│   │   ├── login.html              # Halaman login
│   │   └── schedule.html           # Jadwal lapangan
│   ├── templatetags/              # Custom template tags
│   │   └── booking_extras.py      # Helper functions untuk template
│   ├── admin.py                  # Konfigurasi admin
│   ├── forms.py                  # Form definitions
│   ├── models.py                 # Model database
│   ├── urls.py                   # URL routing
│   └── views.py                  # View logic
├── static/                      # File statis (CSS, JS, images)
├── manage.py                    # Command-line utility
└── requirements.txt             # Dependencies
```

## Fitur

- Sistem booking online 24/7
- Manajemen lapangan dan jadwal
- Dashboard admin
- Sistem approval booking
- Pencegahan booking ganda
- Riwayat pemesanan
- Interface responsif

## Kontribusi

1. Fork repository
2. Buat branch fitur baru (`git checkout -b fitur-baru`)
3. Commit perubahan (`git commit -am 'Menambah fitur baru'`)
4. Push ke branch (`git push origin fitur-baru`)
5. Buat Pull Request

## Lisensi

Proyek ini dilisensikan di bawah Kelompok 5 PPL - UAS 
