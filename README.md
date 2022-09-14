# Tugas 2: Pengenalan Aplikasi Django dan Models View Template (MVT) pada Django

Feru Pratama Kartajaya (2106750351) - Kelas E

Link Heroku: https://django-pbp-ferupk.herokuapp.com/katalog/

### Bagan *request client* aplikasi Django

![Bagan request](https://github.com/ferupk/django-pbp-assignment/blob/main/request_diagram.png)

### Mengapa menggunakan *virtual environment*?

*Virtual environment* digunakan dalam pengembangan proyek Django untuk menetapkan sebuah *coding environment* yang terpisah dari lingkungan Python lainnya. Dengan *virtual environment*, *packages* dan *dependencies* dapat disesuaikan untuk mendukung proyek yang kita lakukan. Apabila kita mengembangkan proyek Django tanpa virtual environment, dapat terjadi konflik antara versi *dependencies* yang berbeda antara proyek tersebut dengan proyek-proyek lainnya maupun pada lingkungan Python pada komputer. Mengembangkan proyek dengan versi *dependencies* yang tidak sesuai dapat menimbulkan banyak masalah pada aplikasi.

### Implementasi konsep Model-View-Template

*Source code* sudah mempersiapkan banyak hal untuk aplikasi `katalog` seperti template html, model item katalog, dan fixture data, serta pengaturan untuk deployment Heroku seperti Procfile. Sebelum memulai, kita harus melakukan `python manage.py makemigrations` dan `python manage.py migrate` untuk menetapkan model ke database lokal, lalu memasukkan data ke dalam database menggunakan `python manage.py loaddata initial_catalog_data.json`.

Cara untuk mengimplementasikan poin 1-4 adalah sebagai berikut:

   1. **Pengambilan data dari Model**

      Pada `views.py` di folder 'wishlist', import CatalogItem dari file `models.py` di folder yang sama. Lalu, kita definisikan sebuah fungsi `show_catalog` yang akan menerima request dari client. Saat fungsi dipanggil, semua Model CatalogItem yang berada di database akan disimpan ke suatu variabel menggunakan fungsi `CatalogItem.objects.all`. Semua data yang akan ditampilkan di webpage — nama, NPM, dan data katalog — disimpan ke dalam sebuah dict `context`. Akhirnya, fungsi mengembalikan hasil fungsi `render` dengan `katalog.html` sebagai template dan `context` sebagai data yang mengisi webpage.

   2. **Routing kepada fungsi `views`**

      Pada `urls.py` di folder `katalog`, import fungsi `path` dari module Django dan `show_catalog` dari `views.py` di folder yang sama. Untuk melakukan routing kepada `show_catalog`, definisikan sebuah path di dalam list `urlpatterns`. Sebagai parameter, `show_catalog` digunakan sebagai HttpResponse. Pada `urls.py` di folder 'project_django', tambahkan routing dengan mendefinisikan path ke aplikasi `katalog`. Sebagai response, tambahkan url dari `urls.py` di folder `katalog` menggunakan fungsi `include`.
   
   3. **Pemetaan data ke HTML**

      Pada `wishlist.html` di folder `katalog/templates`, pemetaan dilakukan untuk menampilkan data yang di-render pada fungsi di `views.py`. Sintaks yang digunakan adalah `{{data}}`, dengan `data` merupakan variabel-variabel yang disimpan pada `context`. Nama dan NPM dapat disisipkan di baris kode yang sesuai. Untuk tabel katalog, kita dapat mengiterasi list item dan memanggil setiap atributnya.
   
   4. **Deployment ke Heroku**
      
      Buatlah sebuah aplikasi baru di Heroku dan catat nama aplikasi tersebut serta API key akun. Pada repositori untuk proyek Django, tambahkan dua buah `repository secret` untuk Actions. Nama aplikasi disimpan pada `HEROKU_APP_NAME` dan API key disimpan pada `HEROKU_API_KEY`. Sekarang, perubahan pada source code dapat di-push ke repositori untuk melakukan deployment.