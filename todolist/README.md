# Tugas 4: Pengimplementasian Form dan Autentikasi Menggunakan Django

Feru Pratama Kartajaya (2106750351) - Kelas E

Link Heroku: https://django-pbp-ferupk.herokuapp.com/todolist/

### Fungsi CSRF Token

Cross Site Request Forgery atau CSRF aalah sebuah ancaman aplikasi web dimana seorang *attacker* menciptakan sebuah web request saat user sedang login, umumnya menggunakan link atau form buatan. Apabila user mengakses link/form tersebut dan membuat web request, kode *attacker* akan diproses. Kode yang diproses dapat melakukan bermacam hal, mulai dari mengambil informasi pribadi user hingga melakukan aksi di website tersebut yang dapat merugikan user.

Untuk melindungi dari CSRF, kita dapat menyisipkan CSRF Token pada form di aplikasi web. Di Django, hal ini dapat dilakukan dengan menyisipkan kode `{% csrf_token %}` di dalam elemen `<form>` pada template HTML. Kode tersebut akan menciptakan sebuah token yang dapat dicocokkan dengan token yang ada di server. Apabila sebuah form yang di-submit tidak memiliki CSRF token yang sama, server tidak akan memproses form tersebut. Pengecekan ini memastikan agar form yang berasal dari sumber lain (misal form buatan dari *attacker*) tidak dapat mengirim web request yang tidak diinginkan.

### Pembuatan Form secara manual

Di Django, kita dapat menggunakan generator seperti `{{ form.as_table }}` pada template HTML untuk membuat sebuah form secara otomatis. Namun, proses ini tidak diwajibkan dan form dapat ditambahkan secara manual.

Gambaran umum membuat form secara manual adalah sebagai berikut:

    * Menambahkan elemen `<form>` untuk menandakan bagian form pada webpage
    * Tentukan format penyajian form (`<table>`, `<div>`, `<p>`, dll.)
    * Gunakan elemen `<input>` untuk menandakan cara input data dari form
    * Tetapkan atribut `type` dari `<input>` sesuai dengan kebutuhan (text, password, submit, dll.)
    * Tetapkan atribut `name` dari `<input>` agar dapat dipanggil saat memproses input.
    * Berikan cara untuk submit form (return key, submit button, dll.)

### Proses alur data

Proses alur data mulai dari submisi form hingga munculnya data di webpage adalah sebagai berikut:

    * Client meminta webpage HTML dengan form
    * Server menciptakan render webpage tersebut dan mengembalikannya kepada client
    * Client mengisi data pada form tersebut dan melakukan submisi
    * Server menerima request dari user yang mengandung data yang diisi dalam form
    * Server memproses data tersebut sesuai dengan keperluan dan menyimpan hasilnya
    * Server menciptakan render webpage baru dengan tambahan data yang telah diproses
    * Webpage dengan data baru ditampilkan kepada client

### Implementasi autentikasi pada aplikasi Django

Aplikasi `todolist` merupakan tambahan dari proyek Django yang dimulai pada Tugas 2. Tahap implementasi yakni seperti berikut:

   1. **Pembuatan aplikasi**

      Pada `cmd`, ubah direktori ke proyek Django dan aktifkan *virtual environment*. Setelah itu, jalankan `python manage.py startapp todolist`. Perintah ini akan membuat folder baru untuk aplikasi `todolist` beserta kerangka dasarnya.

   2. **Mengakses *path* aplikasi**

      Buatlah sebuah folder `templates` di dalam folder `todolist`. Di sana, buatlah file `todolist.html` yang akan dipakai sebagai template utama aplikasi (pengisian template akan dilakukan di poin 5). Pada `views.py` di folder `todolist`, import fungsi `render` dan buatlah sebuah fungsi `show_todolist` yang menerima request dari client. Fungsi ini akan mengembalikan hasil fungsi `render` dengan parameter request dan `todolist.html` sebagai template. 
      
      ```python
      def show_todolist(request):
          return render(request, 'todolist.html')
      ```

      Kemudian, buatlah file `urls.py` di folder `todolist`. Di file tersebut, import fungsi yang telah dibuat dan tetapkan nama aplikasi sebagai `todolist`. Setelah itu, tambahkan path berikut pada list `urlpatterns` pada file `urls.py` di folder `todolist` dan `project_django`:

      ```python
      # Untuk urls.py di folder todolist
      app_name = 'todolist'

      urlpatterns = [
          path('', show_todolist, name='show_todolist'),
      ]

      # Untuk urls.py di folder project_django
      urlpatterns = [
          ...
          path('todolist/', include('todolist.urls')),
      ]
      ```

      Pada `settings.py` di folder `project_django`, tambahkan aplikasi ke dalam list `INSTALLED_APPS`.

      ```python
      INSTALLED_APPS = [
          ...,
          'todolist',
      ]
      ```

      Sekarang, aplikasi dapat diakses melalui http://localhost:8000/todolist
   
   3. **Model `Task`**

      Pada `models.py` di folder `todolist`, import module `models`. Buatlah sebuah kelas `Task` yang menerima parameter `models.Model` dan berikan atribut seperti berikut:

      ```python
      class Task(models.Model):
          user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
          date = models.DateField()
          title = models.CharField(max_length=255)
          description = models.TextField()
      ```

      Untuk menyimpan model tersebut ke database lokal, jalankan `python manage.py makemigrations` di `cmd` untuk membuat migrasi dan `python manage.py migrate` untuk menyimpannya.

   4. **Implementasi autentikasi dengan form**

      Pada `views.py` di folder `todolist`, import perangkat-perangkat berikut:
         
         * Fungsi `redirect`, `authenticate`, `login`, `logout`, `login_required`, dan `reverse`
         * Module `messages`
         * Class `UserCreationForm` dan `HttpResponseRedirect`

      Buatlah fungsi `register` yang menerima request dari client. Fungsi ini akan menampilkan halaman `register` serta memproses data yang ada dalam form saat submit. Apabila data registrasi valid, akun akan dibuat dan client diarahkan ke halaman `login`. Apabila tidak, halaman `register` akan di-reset ulang.

      ```python
      def register(request):
          form = UserCreationForm()

          if request.method == "POST":
              form = UserCreationForm(request.POST)
              if form.is_valid():
                  form.save()
                  messages.success(request, 'Akun berhasil dibuat!')
                  return redirect('todolist:login')
              else:
                  messages.info(request, 'Ada yang bermasalah, coba lagi dan ikuti instruksi!')

          context = {'form':form}
          return render(request, 'register.html', context)
      ```

      Buatlah fungsi `login_user` yang menerima request dari client. Fungsi ini akan menampilkan halaman `login` serta memproses data yang ada dalam form saat submit. Apabila ada akun yang sesuai, login berhasil dan client diarahkan ke halaman `todolist`. Apabila tidak, halaman `login` akan di-reset ulang. Fungsi ini juga akan membuat cookie `current_user` yang dapat digunakan nantinya.

      ```python
      def login_user(request):
          if request.method == 'POST':
              username = request.POST.get('username')
              password = request.POST.get('password')
              user = authenticate(request, username=username, password=password)
                  if user is not None:
                      login(request, user)
                      response = HttpResponseRedirect(reverse('todolist:show_todolist'))
                      response.set_cookie('current_user', username)
                      return response
                  else:
                      messages.info(request, 'Username atau password salah, coba lagi!')

          context = {}
          return render(request, 'login.html', context)
      ```

      Buatlah fungsi `logout_user` yang menerima request dari client. Fungsi ini akan mengakibatkan logout dari akun dan client diarahkan ke halaman `login`. Fungsi ini juga akan menghapus cookie `current_user` yang ada.

      ```python
      def logout_user(request):
          logout(request)
          response = HttpResponseRedirect(reverse('todolist:login'))
          response.delete_cookie('current_user')
          return response
      ```

      Buatlah file `register.html` dan `login.html` di folder `templates` dan buatlah tampilan webpage dalam format HTML. Untuk melakukan registrasi dan login, tambahkan elemen `<form>` dengan metode HTTP POST. Di antara elemen `<form>`, tambahkan *text box* yang dapat diisi informasi dengan elemen `<input>` serta button yang akan digunakan untuk submit form. Setiap `<input>` perlu didefinisikan tipenya sesuai informasi yang akan diisi (username, password, submit).

      ```html
      <!-- Entry "Username" pada register.html -->
      <form method="POST" >  
          {% csrf_token %}  
          <table class="table-login">   
              <tr>
                  <td><label for="id_username">Username </label></td>
                  <td>
                      <input type="text" name="username" maxlength="150" autocapitalize="none" autofocus required id="id_username" title="150 characters or fewer. Letters, digits and @/./+/-/_ only." >
                  </td>
              </tr>
              ...
          </table>
      </form>

      <!-- Entry "Password" dan button "Login" pada login.html -->
      <form method="POST">
          {% csrf_token %}
          <table class="table-login">
              ...
              <tr>
                  <td>Password </td>
                  <td><input type="password" name="password" placeholder="Password"></td>
              </tr>
              <tr>
                <td colspan="2"><input class="btn-common" type="submit" value="Login"></td>
              </tr>
        </table>
      </form>
      ```

      Pada `urls.py` di folder `todolist`, import fungsi-fungsi yang baru saja dibuat di `views.py`. Tambahkan path berikut pada list `urlpatterns` agar mereka dapat diakses oleh client:

      ```python
      urlpatterns = [
          ...,
          path('register/', register, name='register'),
          path('login/', login_user, name='login'),
          path('logout/', logout_user, name='logout'),
      ]
      ```

      Untuk merestriksi akses ke halaman utama `todolist`, tambahkan tag berikut pada fungsi `show_wishlist`:
      
      ```python
      @login_required(login_url='/todolist/login/')
      def show_todolist(request):
          ...
      ```
   
   5. **Halaman utama `todolist`**

      Pada `mywatchlist.html` di folder `templates`, buatlah tampilan webpage dalam format HTML. `todolist` disajikan dalam bentuk tabel yang akan diisi dengan bermacam task yang dibuat oleh client. Tambahkan juga tombol untuk melakukan logout seperti berikut:

      ```html
      <!-- Button "Logout" pada todolist.html -->
      <td style="background-color: transparent;"><a href="{% url 'todolist:logout' %}"><button class="btn-common">Logout</button></a></td>
      ```

      Untuk menambahkan data task dilanjutkan di poin berikutnya.

   6. **Halaman pembuatan Task**

      Buatlah file `forms.py` di folder `todolist`. Di file tersebut, import class Modelform dan model Task yang telah dibuat sebelumnya. Buatlah sebuah kelas `CreateTaskForm` yang menerima parameter `ModelForm` dan inner class Meta di dalamnya. Simpan model Task pada variabel `model` dan field parameter yang akan diisi melewati form (`title` dan `description`) pada variabel `fields`.

      Pada `views.py` di folder `todolist`, import class `date` dan `CreateTaskForm` yang telah dibuat sebelumnya. Buatlah fungsi `create_task` yang menerima request dari client. Fungsi ini akan menampilkan halaman `create-task` serta memproses data yang ada dalam form saat submit. Apabila data task valid, task tersebut akan terbentuk dan client diarahkan ke halaman `todolist`. Apabila tidak, halaman `create-task` akan di-reset ulang.

      ```python
      @login_required(login_url='/todolist/login/')
      def create_task(request):
          form = CreateTaskForm()

          if request.method == "POST":
              form = CreateTaskForm(request.POST)
              if form.is_valid():
                  task_data = form.save(commit=False)
                  task_data.user = request.user
                  task_data.date = date.today()
                  task_data.save()
                  form.save_m2m()
                  messages.success(request, 'Task berhasil ditambahkan!')
                  return redirect('todolist:show_todolist')
              else:
                  messages.info(request, 'Ada yang bermasalah, coba lagi!')

          context = {
              'form': form,
              'current_user': request.COOKIES['current_user'],
          }
          return render(request, 'create_task.html', context)
      ```

      Buatlah file `create_task.html` di folder `templates` dan buatlah tampilan webpage dalam format HTML. Seperti halaman `register` dan `login`, tambahkan elemen `<form>` dengan metode HTTP POST untuk menerima input dari client.

      Pada `urls.py` di folder `todolist`, import fungsi `create_task` dan tambahkan path berikut pada list `urlpatterns` agar dapat diakses oleh client:

      ```python
      urlpatterns = [
          ...,
          path('create-task/', create_task, name='create_task'),
      ]
      ```

      Pada `views.py` di folder `todolist`, ubah fungsi `show_todolist` untuk mengembalikan hasil render dengan `context`. Untuk data `Task` yang akan ditampilkan, kita dapat mengambilnya dengan fungsi `filter(user=request.user)`.

      ```python
      @login_required(login_url='/todolist/login/')
      def show_todolist(request):
          data = Task.objects.filter(user=request.user)
          context = {
              'task_list': data,
              'current_user': request.COOKIES['current_user'],
          }
          return render(request, 'todolist.html', context)
      ```

      Pada `todolist.html` di folder `templates`, tambahkan for loop untuk menambahkan data `Task` ke dalam tabel `todolist`. Karena data berupa model, setiap `Task` perlu diakses setiap atributnya secara langsung. Selain itu, tambahkan juga tombol untuk menambahkan `Task` seperti berikut:

      ```html  
      <!-- Button "Tambah Task Baru" pada todolist.html -->
      <td style="background-color: transparent;"><a href="{% url 'todolist:create_task' %}"><button class="btn-common">Tambah Task Baru</button></a></td>
      ```

   7. **Routing URL**

      Poin ini sudah dijelaskan pada poin-poin sebelumnya saat menambahkan path ke list `urlpatterns`.

   8. **Deployment ke Heroku**

      Di `cmd`, git add, commit, dan push semua perubahan ke repository GitHub. Deployment akan mulai secara otomatis dan aplikasi dapat diakses melalui link aplikasi Heroku setelah selesai.
   
   9. **Testing akun dan pembuatan Task**

      Setelah mengakses aplikasi di https://django-pbp-ferupk.herokuapp.com/todolist/, buatlah 2 akun berbeda. Setelah itu, buatlah 3 task baru untuk setiap akun.

   * **BONUS: Implementasi dasar CRUD pada Task**

      NOTE: Langkah berikut dilakukan sebelum deployment ke Heroku

      Pada `models.py` di folder `todolist`, tambahkan atribut `is_finished` pada class `Task` dengan default value `False`. Atribut ini akan digunakan sebagai flag apabila `Task` sudah dilakukan. Lalu, update model di database lokal dengan menjalankan `python manage.py makemigrations` dan `python manage.py migrate` untuk menyimpannya.
      
      Pada `todolist.html` di folder `templates`, tambahkan 3 kolom yang akan digunakan untuk menampilkan status `Task`, mengubah status `Task`, dan menghapus `Task`. Untuk mengubah status dan menghapus `Task`, gunakan elemen `<form>` dengan metode HTTP POST. Berikan elemen `<input>` untuk menyimpan primary key dari `Task` serta perintah yang akan dilakukan. Gunakan atribut `name=` untuk memberikan tanda pada input yang bisa dipanggil nanti dan `value=` untuk menyimpan nilai yang dapat dibandingkan.

      ```html
      <table>
          <tr>
              ...
              <th style="width: 6%;" class="todolist">Status</th>
              <th style="width: 6%;" class="todolist">Ubah Status</th>
              <th style="width: 6%;" class="todolist">Hapus Task</th>
          </tr>
          {% for task in task_list %}
              <tr>
                  ...
                  {% if task.is_finished %}
                      <td class="todolist" style="background-color: green;">Selesai</td>
                  {% else %}
                      <td class="todolist" style="background-color: red;">Belum Selesai</td>
                  {% endif %}
                  <td class="todolist" style="background-color: white;">
                      <form method="POST">
                          {% csrf_token %}
                          <input type="hidden" name="id" value="{{task.pk}}">
                          {% if task.is_finished %}
                              <input type="hidden" name="update_task" value="not_done">
                          {% else %}
                              <input type="hidden" name="update_task" value="done">
                          {% endif %}
                          <input type="submit" name="submit" value="⇄" style="border: none; background-color: transparent; font-size: 24px;">
                      </form>
                  </td>
                  <td class="todolist" style="background-color: rgb(55, 36, 29); font-size: 24px;">
                      <form method="POST">
                          {% csrf_token %}
                          <input type="hidden" name="id" value="{{task.pk}}">
                          <input type="hidden" name="delete_task" value="delete">
                          <input type="submit" name="submit" value="❌" style="border: none; background-color: transparent; font-size: 24px;">
                      </form>
                  </td>
              </tr>
          {% endfor %}
          ...
      </table>
      ```

      Pada `views.py` di folder `todolist`, ubah fungsi `show_todolist` untuk memproses metode request POST. Gunakan `name` yang telah diberikan pada input sebelumnya untuk mengambil `Task` dan perintahnya. Setelah itu, cek perintah apa yang terjadi. Apabila perintah yang terjadi adalah `update_task`, ubah nilai atribut `is_finished` dari `Task` sesuai dengan yang diminta. Apabila perintah yang terjadi adalah `delete_task`, hapus `Task` tersebut dari database menggunakan fungsi `delete`.

      ```python
      def show_todolist(request):
          data = Task.objects.filter(user=request.user)

          if request.method == "POST":
              id = request.POST.get('id')
              task = Task.objects.filter(pk=id).first()

              update_task = request.POST.get('update_task')
              delete_task = request.POST.get('delete_task')

              if update_task == "done":
                  task.is_finished = True
                  task.save()
                  messages.success(request, 'Status Task berhasil diubah!')
              elif update_task == "not_done":
                  task.is_finished = False
                  task.save()
                  messages.success(request, 'Status Task berhasil diubah!')
        
              if delete_task == "delete":
                  try:
                      task.delete()
                      messages.success(request, 'Task berhasil dihapus!')
                  except AttributeError:
                      pass
          ...
      ```

      Sekarang, client dapat mengubah status dari `Task` serta menghapusnya.



# Tugas 5: Web Design Using HTML, CSS, and CSS Framework

Feru Pratama Kartajaya (2106750351) - Kelas E

Link Heroku: https://django-pbp-ferupk.herokuapp.com/todolist/

### Inline, internal, dan external CSS

Inline CSS digunakan untuk menambahkan styling pada satu elemen tertentu. Atribut `style=` ditambahkan pada tag suatu elemen dan dapat diberikan style CSS yang sesuai. Inline CSS memiliki prioritas yang paling tinggi sehingga dapat digunakan untuk meng-override kumpulan style lain yang diberikan pada elemen seperti class. Namun, Inline CSS dapat mudah mengotori template HTML karena lokasinya di dalam tag elemen.

Internal CSS mendefinisikan style dari dalam file HTML itu sendiri dengan menggunakan elemen `<style>` di bagian `<head>` dari template, sedangkan External CSS mendefinisikan style dari sebuah file tersendiri yang dapat dihubungkan dengan template. Kedua metode CSS ini dapat mendefinisikan style untuk satu macam elemen, atau sebuah class atau id yang dapat diberikan kepada elemen. External CSS memudahkan perubahan style untuk banyak webpage dan membuat susunan file lebih rapih, namun kalah prioritas dengan Internal CSS.

### Tag HTML5

   * `<head>`: Karakteristik dan metadata dari webpage (Judul, *viewport*, *styling*, dll.)
   * `<title>`: Judul halaman webpage (tampil di tab browser)
   * `<meta>`: Metadata webpage
   * `<style>`: Internal CSS
   * `<header>, <body>, <footer>`: Isi dari webpage
   * `<div>`: Kontainer elemen HTML yang digunakan untuk membuat bagian-bagian webpage
   * `<h1> - <h6>`: Heading dalam 6 ukuran
   * `<table>, <tr>, <th>, <td>`: Tabel, baris tabel, header tabel, dan cell tabel
   * `<p>`: Paragraf
   * `<span>`: Kontainer inline yang digunakan untuk markup teks
   * `<a>`: Hyperlink yang dapat diakses
   * `<nav>`: Area link navigasi webpage
   * `<form>`: Area form yang dapat mengirimkan informasi ke server
   * `<label>`: Label untuk elemen tertentu
   * `<input>, <textarea>`: Area input untuk mengisi data
   * `<button>`: Tombol yang dapat mengakibatkan *event*
   * `<img>, <video>`: Embed gambar/video pada webpage

   dan masih banyak lagi.

### CSS Selector

   * Element Selector

     Selector ini menggunakan tag HTML untuk memberikan *styling*.

     ```css
     h1 {
         text-align: center;
         font-size: 24px;
     }
     ```
    
   * ID Selector

     Selector ini menggunakan ID yang dapat diberikan kepada elemen HTML untuk memberikan *styling*. Sebuah elemen hanya dapat memiliki satu ID unik.
      
     ```css
     #colored {
         color: yellow;
         background-color: purple;
     }
     ```
     ```html
     <span id="colored">Colored Text</span>
     ```

   * Class Selector

     Selector ini menggunakan class yang dapat diberikan kepada elemen HTML untuk memberikan *styling*. Sebuah elemen dapat memiliki class sebanyak apapun. Class Selector dapat dikhususkan untuk elemen tertentu.

     ```css
     .thick-font {
         font-size: 18px;
         font-weight: bold;
     }

     p.square {
         padding: 10px;
         background-color: green;
     }
     ```
     ```html
     <p class="square thick-font">Sample Text</p>
     ```

   * Descendant Selector

     Selector ini memberikan *styling* pada elemen tertentu yang berada di dalam sebuah elemen.
     
     ```css
     div p {
        color: white;
         background-color: red;
     }
     ```
     ```html
     <div>
         <p>Paragraph 1</p> <!-- Terpengaruh -->
         <span>
             <p>Paragraph 2</p> <!-- Terpengaruh -->
         </span>
     </div>
     ```

   * Child Selector
   
     Selector ini memberikan *styling* pada elemen tertentu yang merupakan anak langsung dari sebuah elemen.

     ```css
     div > p {
        color: white;
         background-color: red;
     }
     ```
     ```html
     <div>
         <p>Paragraph 1</p> <!-- Terpengaruh -->
         <span>
             <p>Paragraph 2</p> <!-- Tidak terpengaruh -->
         </span>
     </div>
     ```

   * Adjacent Sibling Selector
     
     Selector ini memberikan *styling* pada elemen tertentu yang tepat setelah sebuah elemen.

     ```css
     div + p {
        color: white;
         background-color: red;
     }
     ```
     ```html
     <div>
         <p>Paragraph 1</p> <!-- Tidak terpengaruh -->
     </div>
     <p>Paragraph 2</p> <!-- Terpengaruh -->
     <p>Paragraph 3</p> <!-- Tidak terpengaruh -->
     ```

   * General Sibling Selector
     
     Selector ini memberikan *styling* pada elemen tertentu yang berada setelah sebuah elemen.

     ```css
     div ~ p {
        color: white;
         background-color: red;
     }
     ```
     ```html
     <div>
         <p>Paragraph 1</p> <!-- Tidak terpengaruh -->
     </div>
     <p>Paragraph 2</p> <!-- Terpengaruh -->
     <p>Paragraph 3</p> <!-- Terpengaruh -->
     ```

   * Universal Selector
     
     Selector ini memberikan *styling* pada semua elemen HTML.

      ```css
      * {
          font-family: "Bahnschrift", Tahoma;
          background-color:  transparent;
      }
      ```

### Implementasi Web Design dengan CSS dan Bootstrap

   1. **CSS dan Bootstrap**
   
      Sebelum dapat mendesain webpage, stylesheet CSS dan Bootstrap perlu dihubungkan ke template terlebih dahulu.
   
      * Buatlah direktori `static\css` di folder utama dan tambahkan file `style.css` di dalamnya. File ini akan digunakan sebagai external stylesheet CSS.

      * Pada `base.html` di folder `templates` utama, hubungkan file static dengan `{% load static %}`. Lalu, tambahkan stylesheet CSS dan Bootstrap menggunakan elemen `<link>`.

      ```html
      <head>
          ...
          <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous">
          <link rel="stylesheet" href="{% static 'css/style.css' %}">
          ...
      </head>
      ```

      Sekarang, template HTML dapat didesain menggunakan class-class CSS dan Bootstrap dengan menambahkan `{% extends 'base.html' %}` di awal dokumen.

   2. **Web design**

      Secara garis besar, web design pada `todolist` adalah sebagai berikut:

         * Keempat halaman memiliki `navbar` di atas yang menunjukkan judul halaman dan di bawah yang berperan sebagai footer. Untuk halaman `todolist` dan `create-task`, `navbar` di atas akan menampilkan nama user yang sedang login serta button untuk logout.

         * Keempat halaman memiliki bagian yang dapat menampilkan berbagai notifikasi berdasarkan aksi user (Gagal login, mengubah status Task, membuat Task, dll.)

         * Untuk halaman `login`, `register`, dan `create-task`, form disajikan di dalam container `div-form` dan menggunakan class-class form Bootstrap seperti `form-group` dan `form-control`. Link untuk berpindah antar halaman juga ditambahkan untuk kemudahan navigasi (Berpindah dari `login` dan `register`, kembali ke `todolist` dari `create-task`)

         * Untuk halaman `todolist`, setiap Task disajikan dalam format `card` dari Bootstrap. Judul dan urutan Task diberikan sebagai `header` dari `card`, sedangkan `body` dari `card` digunakan untuk menampilkan deskripsi, tanggal pembuatan, dan status Task. Tombol untuk mengubah status dan menghapus Task ditampilkan pada `footer` dari `card`. `Card` terakhir digunakan sebagai tombol untuk membuat task baru. Styling dari `div` dan `card` sudah disesuaikan sebagaimana terdapat maksimal 2 `card` per baris.

   3. ***Responsive web design***

      Untuk implementasi *responsive web design*, beberapa fitur sudah ditangani oleh metadata `viewport` dan class-class dari Bootstrap seperti `navbar-expand`, `d-flex`, dan lainnya. Untuk aplikasi `todolist`, masih diperlukan penyesuaian untuk ukuran `<div>` pada form, ukuran `<card>`, dan ukuran font judul. Penyesuaian dapat dilakukan dengan menggunakan *media query* untuk ukuran layar tertentu.

      ```css
      .page-title {
          font-size: 36px;
      }

      .card-size-adjust {
          width: 45%;
      }

      .form-size-adjust {
          width: 60%
      }

      @media (max-width: 666px) {
          .card-size-adjust {
              width: auto;
              min-width: 45%;
          }

          .form-size-adjust {
              width: auto;
              max-width: 90%;
          }
      }

      @media (max-width: 375px) {
          .page-title {
              font-size: 24px;
          }
      }
      ```

      Sekarang, webpage akan menyesuaikan diri untuk layar berukuran kecil.

   * **BONUS: Animasi pada `card`**
      
      Pseudo-class dari CSS dapat digunakan untuk mengdikte *styling* sebuah elemen dalam keadaan tertentu. Untuk menambahkan efek pada `card` saat *cursor* berada di atasnya, kita dapat menggunakan pseudo-class `hover`. Untuk aplikasi `todolist`, `card` akan berubah warna menjadi keemasan dan menampilkan teks `hint` untuk tombol status dan delete saat terjadi `hover`.

      ```css
      .card-task {
          border: 2px solid black;
          transition: 0.5s;
      }

      .card-task:hover {
          background-color: wheat;
          border: 2px solid black;
      }

      .card-task:hover span.hint {
          opacity: 1;
      }

      span.hint {
          font-size: 12px;
          padding-top: 10px;
          text-align: center;
          color: rgba(0, 0, 0, 0.5);
          opacity: 0;
          transition: 0.5s;
      }
      ```

      Logika yang sama juga diterapkan untuk setiap tombol dan `card` tambah Task dengan tambahan pseudo-class `active`.