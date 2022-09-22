# Tugas 3: Pengimplementasian Data Delivery Menggunakan Django

Feru Pratama Kartajaya (2106750351) - Kelas E

Link Heroku: https://django-pbp-ferupk.herokuapp.com/mywatchlist/
   * View in: [HTML](https://django-pbp-ferupk.herokuapp.com/mywatchlist/html/) | [XML](https://django-pbp-ferupk.herokuapp.com/mywatchlist/xml/) | [JSON](https://django-pbp-ferupk.herokuapp.com/mywatchlist/json/)

### HTML, XML, dan JSON

HTML dan XML merupakan contoh dari *markup language*, yaitu sebuah format yang digunakan untuk mendikte struktur dari sebuah dokumen menggunakan tag. Namun, kegunaan utama keduanya berbeda. HTML digunakan untuk menyatakan struktur dan penampilan dari sebuah webpage yang dapat didukung dengan bahasa lainnya seperti CSS dan JavaScript, sedangkan XML digunakan untuk penyimpanan dan transfer data yang terlibat dalam webpage.

JSON merupakan turunan dari bahasa JavaScript dan umumnya digunakan untuk menyimpan objek-objek data. Walaupun sintaksnya mirip dengan JavaScript, JSON dapat digunakan sebagai penyimpanan data untuk berbagai macam bahasa pemrograman.

### Mengapa menggunakan *data delivery*?

Terdapat bermacam situasi dalam pengembangan aplikasi web di mana data dari satu tempat perlu diakses dari tempat lain. Mau data itu disimpan di sebuah database atau hanya sekedar referensi, diperlukan sebuah cara untuk mengirim data ke berbagai tempat. Dengan implementasi *data delivery*, kita dapat menyimpan data dalam sebuah format (XML, JSON, dll.) dan mengaksesnya dari tempat lain.

### Implementasi *data delivery* pada aplikasi Django

Aplikasi `mywatchlist` merupakan tambahan dari proyek Django yang dimulai pada Tugas 2. Tahap implementasi yakni seperti berikut:

   1. **Pembuatan aplikasi**

      Pada `cmd`, ubah direktori ke proyek Django dan aktifkan *virtual environment*. Setelah itu, jalankan `python manage.py startapp mywatchlist`. Perintah ini akan membuat folder baru untuk aplikasi `mywatchlist` beserta kerangka dasarnya.

   2. **Mengakses *path* aplikasi**

      Pada `views.py` di folder `mywatchlist`, buatlah sebuah fungsi `show_mywatchlist` yang menerima request dari client dan mengembalikan `HttpResponse` sebagai *placeholder* yang dapat diubah nanti. Kemudian, import fungsi tersebut ke `urls.py` di folder `mywatchlist` dan tetapkan nama aplikasi `mywatchlist`. Setelah itu, tambahkan kedua path berikut pada list `urlpatterns` untuk menghubungkan path ke aplikasi:

      ```python
      # Untuk urls.py di folder mywatchlist
      urlpatterns = [
          path('', show_mywatchlist, name='show_mywatchlist'),
      ]

      # Untuk urls.py di folder project_django
      urlpatterns = [
          ...
          path('mywatchlist/', include('mywatchlist.urls')),
      ]
      ```

      Pada `settings.py` di folder `project_django`, tambahkan aplikasi ke dalam list `INSTALLED_APPS`.

      ```python
      INSTALLED_APPS = [
          ...,
          'mywatchlist',
      ]
      ```

      Sekarang, aplikasi dapat diakses melalui http://localhost:8000/mywatchlist
   
   3. **Model `MyWatchList`**

      Pada `models.py` di folder `mywatchlist`, import module `models`. Buatlah sebuah kelas `MyWatchList` yang menerima parameter `models.Model` dan berikan atribut seperti berikut:

      ```python
      class MyWatchList(models.Model):
          watched = models.BooleanField()
          title = models.CharField(max_length=255)
          rating = models.IntegerField()
          release_date = models.DateField()
          review = models.TextField()
      ```

      Untuk menyimpan model tersebut ke database lokal, jalankan `python manage.py makemigrations` di `cmd` untuk membuat migrasi dan `python manage.py migrate` untuk menyimpannya.

   4. **Penyimpanan data ke database**
      
      Buatlah sebuah folder baru `fixtures` di dalam folder `mywatchlist`. Pada folder tersebut, buatlah file `initial_mywatchlist_data.json` sebagai file untuk menyimpan data model dan tambahkan data film dengan format seperti berikut:

      ```json
      [
         ...
          {
              "model": "mywatchlist.mywatchlist",
              "pk": 6,
              "fields": {
                  "watched": false,
                  "title": "Everything Everywhere All at Once",
                  "rating": 5,
                  "release_date": "2022-04-08",
                  "review": "Led by an outstanding Michelle Yeoh, Everything Everywhere All at Once lives up to its title with an expertly calibrated assault on the senses."
              }
          },
         ...
      ]
      ```

      Setelah semua data ditambahkan di dalam *fixture*, masukkan data tersebut ke dalam database dengan menjalankan `python manage.py loaddata initial_mywatchlist_data.json` di `cmd`.
   
   5. **Implementasi *data delivery***
      * HTML

         Pada `views.py` di folder `mywatchlist`, ubah fungsi `show_mywatchlist` yang dibuat sebelumnya. Simpan semua model pada database di dalam variabel `data` menggunakan fungsi `MyWatchList.objects.all`.
         Simpan semua data yang ingin ditampilkan pada webpage ke dalam sebuah dict `context`. Akhirnya, kembalikan HttpResponse menggunakan fungsi `render` dengan parameter `mywatchlist.html` sebagai template dan `context` sebagai data yang mengisi webpage.

         Buatlah sebuah folder baru `templates` di dalam folder `mywatchlist`. Pada folder tersebut, buatlah file `mywatchlist.html` sebagai template halaman HTML yang akan digunakan pada fungsi render sebelumnya. Sajikan informasi watchlist dalam bentuk tabel dengan isinya berupa data yang telah disimpan pada `context`. Karena data kita berupa list model, setiap film perlu diiterasi dan diakses setiap atributnya secara langsung.

         Pada `urls.py` di folder `mywatchlist`, tambahkan path khusus pada list `urlpatterns` untuk mengakses fungsi tersebut.

         ```python
         urlpatterns = [
             ...
             path('html/', show_mywatchlist, name='show_mywatchlist'),
         ]
         ```

         **BONUS**: Pada fungsi `show_watchlist`, simpan nilai boolean `watched_enough` untuk menandakan apabila film yang telah ditonton lebih banyak daripada yang belum. Cara untuk mendapatkan nilai boolean tersebut seperti berikut:

         ```python
         amount_watched = 0
         # data = kumpulan data film
         for item in data:
             if item.watched: 
                 amount_watched +=1
         watched_enough = True if amount_watched >= (len(data) - amount_watched) else False
         ```

         Dengan menyimpan variabel ini sebagai `context` kita dapat menyampaikan pesan khusus di webpage yang bersesuaian dengan jumlah film yang telah ditonton.

      * XML dan JSON
      
         Pada `views.py` di folder `mywatchlist`, import class `HttpResponse` dan module `serializers`. Setelah itu, buatlah sebuah fungsi `show_xml` yang menerima request dari client. Simpan semua model pada database di dalam variabel `data` menggunakan fungsi `MyWatchList.objects.all`. Lalu, kembalikan sebuah HttpResponse dengan parameter serialisasi data menjadi XML dan tetapkan `content_type` untuk XML.

         ```python
         return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")
         ```

         Pada `urls.py` di folder `mywatchlist`, import fungsi `show_xml` dan tambahkan path khusus pada list `urlpatterns` untuk mengakses fungsi tersebut.

         ```python
         urlpatterns = [
             ...
             path('xml/', show_xml, name='show_xml'),
         ]
         ```

         Untuk implementasi JSON, prosedur sama persis kecuali setiap instance `xml` diubah dengan `json`.
   
   6. **Deployment ke Heroku**

      Pada `Procfile`, tambahkan perintah `python manage.py loaddata initial_mywatchlist_data.json` pada script agar data `mywatchlist` dapat digunakan setelah deployment aplikasi. Akhirnya, git add, commit, dan push semua perubahan ke repository GitHub. Deployment akan mulai secara otomatis dan aplikasi dapat diakses melalui link aplikasi Heroku setelah selesai.