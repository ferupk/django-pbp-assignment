# Tugas 4: Pengimplementasian Form dan Autentikasi Menggunakan Django

Feru Pratama Kartajaya (2106750351) - Kelas E

Link Heroku: https://django-pbp-ferupk.herokuapp.com/todolist/

### Fungsi CSRF token

Placeholder

### Pembuatan Form secara manual

Placeholder

### Proses alur data

Placeholder

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
                  messages.success(request, 'Account created successfully!')
                  return redirect('todolist:login')
              else:
                  messages.info(request, 'Something went wrong, try again and make sure the rules are followed!')

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
                      messages.info(request, 'Wrong username or password, try again!')

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
                  messages.success(request, 'Task added successfully!')
                  return redirect('todolist:show_todolist')
              else:
                  messages.info(request, 'Something went wrong, try again!')

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
      <!-- Button "Create New Task" pada todolist.html -->
      <td style="background-color: transparent;"><a href="{% url 'todolist:create_task' %}"><button class="btn-common">Create New Task</button></a></td>
      ```

   6. **Routing URL**
      Poin ini sudah dijelaskan pada poin-poin sebelumnya saat menambahkan path ke list `urlpatterns`.

   7. **Deployment ke Heroku**

      Di `cmd`, git add, commit, dan push semua perubahan ke repository GitHub. Deployment akan mulai secara otomatis dan aplikasi dapat diakses melalui link aplikasi Heroku setelah selesai.
   
   8. **Testing akun dan pembuatan Task**
      Setelah mengakses aplikasi di https://django-pbp-ferupk.herokuapp.com/todolist/, buatlah 2 akun berbeda. Setelah itu, buatlah 3 task baru untuk setiap akun.
   
   bonus

   tambahkan is_finished pada models