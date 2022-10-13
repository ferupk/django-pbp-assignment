# Tugas 6: Javascript dan AJAX

Feru Pratama Kartajaya (2106750351) - Kelas E

Link Heroku: https://django-pbp-ferupk.herokuapp.com/todolist/

### Asynchronous dan Synchronous Programming

   Dalam penerapan Synchronous Programming, setiap request yang dikirimkan client perlu diproses oleh server satu per satu. Saat server memproses request, client harus menunggu hingga request tersebut selesai sebelum server dapat memproses request lainnya. Untuk menampilkan response, server akan mengirim webpage baru yang akan ditampilkan kepada client setelah reload.

   Dalam penerapan Asynchronous Programming, server dapat memproses beberapa request berbeda sekaligus. Setiap ada request yang selesai, server akan langsung mengirimkan response ke client tanpa menghambat proses lainnya. Asynchronous Programming membuat interaksi dengan server lebih cepat dan efisien, serta menghilangkan kebutuhan untuk melakukan reload webpage setelah setiap aksi.

### Event-Driven Programming

   Event-Driven Programming adalah paradigma programming di mana cara kerja program didiktat oleh aksi yang dilakukan oleh user. Dalam web development, setiap aksi yang dilakukan oleh client merupakan sebuah 'event' yang dapat digunakan untuk memanggil suatu proses yang menangani 'event' tersebut (disebut juga 'event handler').

   Terdapat beberapa cara untuk menerapkan Event-Driven Programming menggunakan JavaScript dan AJAX, yakni:

   * Menghubungkan elemen-elemen pada HTML dengan fungsi JavaScript menggunakan parameter-parameter `event` HTML

   ```html
      <!-- Alert akan muncul saat button di-klik -->
      <button onclick="openAlert()">Munculkan Alert</button>
      <script>function openAlert() {alert("Halo!")}</script>
   ```

   * Memeriksa event melewati ID dan HTML DOM

   ```html
      <!-- Alert akan muncul saat button di-klik -->
      <button id="alertButton">Munculkan Alert</button>
      <script>
          document.getElementById("alertButton").onclick = function() {openAlert()};
          function openAlert() {alert("Halo!")}
      </script>
   ```

   * Memeriksa event melewati ID dan fungsi `addEventListener`

   ```html
      <!-- Alert akan muncul saat button di-klik -->
      <button id="alertButton">Munculkan Alert</button>
      <script>
          document.getElementById("alertButton").addEventListener("click", openAlert);
          function openAlert() {alert("Halo!")}
      </script>
   ```
   
   Dalam program `todolist`, terdapat beberapa penerapan Event-Driven Programming. Pertama adalah fungsi `refreshTasks` yang berfungsi untuk menampilkan semua Task dari user. Terdapat parameter pada elemen `<body>` bernama `onload=` yang dihubungkan kepada fungsi tersebut. Saat webpage di-load, fungsi `refreshTasks` akan langsung dipanggil dan menampilkan Task milik user. Selain itu, ada juga fungsi `addNewTask` untuk membuat Task baru dan `deleteTask` yang menghapus salah satu Task yang ada. Kedua fungsi tersebut terhubung pada elemen button-nya masing-masing melalui parameter `onclick=`. Fungsi `refreshTasks` juga akan dipanggil saat memproses kedua fungsi tersebut untuk menampilkan kumpulan Task setelah terjadi operasi.

### Asynchronous Programming dengan AJAX

AJAX adalah sebuah metode programming dimana JavaScript dan XML digunakan untuk memproses aksi pada webpage secara asynchronous. Saat sebuah event terjadi, fungsi JavaScript yang bersangkutan akan mengirimkan sebuah `XMLHttpRequest` ke server untuk diproses. Setelah itu, server mengembalikan response dan fungsi JavaScript dapat melakukan operasi pada webpage berdasarkan response tersebut.

Sebagai contoh, misalkan kita ingin menerapkan fungsi refresh data secara asinkronus pada webpage. Maka kita dapat menerapkan AJAX dengan metode GET. Untuk penerapan AJAX, kita dapat menggunakan library JQuery.

```html
<script>
    $(document).ready(function(){
        $("refreshButton").click(function() {
            $.get("application/json", function(data) {
                // Operasi refresh dilakukan di sini
            });
        });
    });
</script>
<button id="refreshButton">Refresh</button>
```

Selain itu, kita juga dapat menggunakan Fetch API dengan fungsi `fetch()`.

```html
<script>
    async function refresh() {
        const data = await fetch("application/json").then((response) => response.json());
        // Operasi refresh dilakukan di sini
    }
</script>
<button onclick=refresh()>Refresh</button>
```

### Implementasi fungsionalitas dengan AJAX
   
Penerapan AJAX pada kode ini menggunakan Fetch API `fetch()`.

   1. **AJAX GET: Pengambilan Task**

      Pada `views.py` di folder `todolist`, buatlah fungsi `show_json` yang mengembalikan data `Task` user dalam format JSON. Data ini akan digunakan untuk menampilkan `Task` dengan fungsi JavaScript. Tambahkan juga path untuk mengakses data tersebut pada `urls.py`

      ```python
      # views.py
      def show_json(request):
          data = Task.objects.filter(user=request.user)
          return HttpResponse(serializers.serialize("json", data), content_type="application/json")

      # urls.py
      urlpatterns = [
          ...
          path('json/', show_json, name='show_json'),
      ]
      ```

      Pada `todolist.html` di folder `templates`, buatlah sebuah fungsi JavaScript bernama `refreshTasks` yang akan digunakan untuk melakukan `refresh` pada kumpulan Task user. Fungsi `fetch()` digunakan untuk mengambil data dalam format JSON. Kemudian, fungsi mengiterasi setiap task dan menambahkannya dalam format `card` hingga membentuk sebuah kumpulan string HTML. Akhirnya, sebuah `<div>` dengan ID khusus akan diisi dengan informasi HTML yang telah dibuat.

      ```js
      async function refreshTasks() {
        const tasks = await fetch("{% url 'todolist:show_json' %}").then((response) => response.json());

        let htmlCards = '';
        tasks.forEach((task, i) => {
            var status = '', update = '';
            if (task.fields.is_finished) {
                status = "✔️ Selesai";
                update = "not_done";
            } else {
                status = "❌ Belum Selesai";
                update = "done";
            }

            htmlCards += ... // menambahkan card untuk setiap Task
        });

        htmlCards += ... // card untuk menambahkan Task
        
        document.getElementById("cards").innerHTML = htmlCards
      }
      ```
      ```html
      <body onload=refreshTasks()> <!-- panggil fungsi saat load webpage -->
          <div id="cards" class="d-flex justify-content-center mt-4 mb-5" style="flex-wrap: wrap; "></div>
      </body>
      ```

   2. **AJAX POST: Pembuatan Task**

      Form pembuatan Task akan disajikan dalam format `Modal` dari BootStrap, maka kita perlu menambahkan script JavaScript dari BootStrap terlebih dahulu.

      ```html
      <!-- base.html -->
      <head>
        ...
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-OERcA2EqjJCMA+/3y+gxIOqMEjwtxJY7qPCqsdltbNJuaOe923+mo//f6V8Qbsw3" crossorigin="anonymous"></script>
        ...
      </head>
      ```

      Pada `todolist.html` di folder `templates`, buatlah `Modal` yang akan muncul saat meng-klik `card` pembuatan Task dan tambahkan form untuk membuat Task di dalamnya. Gunakan atribut `data-bs-dismiss=` untuk menghilangkan `Modal` saat submit form.

      ```html
      <!-- Tambahkan target modal pada card untuk menambah Task -->
      ...
      <div class="card mx-3 my-3 card-size-adjust card-create" style="min-height: 200px;"> +
          ...
          <a role="button" data-bs-toggle="modal" data-bs-target="#addTask" class="stretched-link"></a> +
      </div>;
      ...

      <!-- Modal form -->
      <div class="modal fade" id="addTask" tabindex="-1" aria-labelledby="addTaskLabel" aria-hidden="true">
          <div class="modal-dialog">
              <div class="modal-content">
                  <div class="modal-header bg-success">
                      <h1 class="modal-title fs-5 text-white" id="addTaskLabel">Tambah Task Baru</h1>
                      <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                  </div>
                  <form>
                      {% csrf_token %}
                      <div class="modal-body">
                          <div class="form-group my-3">
                              <label>Title</label>
                              <input class="form-control" type="text" name="title" placeholder="Title" autofocus required>
                          </div>
                          <div class="form-group my-3">
                              <label>Description</label>
                              <textarea class="form-control" name="description" placeholder="Description" rows="4"></textarea>
                          </div>
                      </div>
                      <div class="modal-footer">
                          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                          <button type="submit" name="submit" class="btn btn-success" data-bs-dismiss="modal">Tambah Task</button>
                      </div>
                  </form>
              </div>
          </div>
      </div>
      ```

      Pada `views.py` di folder `todolist`, buatlah fungsi `add_task` yang menambahkan Task dari data Form dan mengembalikan HttpResponse berdasarkan keberhasilan proses. Tambahkan juga path untuk mengakses fungsi tersebut pada `urls.py`.

      ```python
      # views.py
      def add_task(request):
          form = CreateTaskForm()

          if request.method == 'POST':
              form = CreateTaskForm(request.POST)
              if form.is_valid():
                  task_data = form.save(commit=False)
                  task_data.user = request.user
                  task_data.date = date.today()
                  task_data.save()
                  form.save_m2m()
                  return HttpResponse("Task Added", status=201)

          return HttpResponseNotFound()

      # urls.py
      urlpatterns = [
          ...
          path('add/', add_task, name='add_task'),
      ]
      ```

      Pada `todolist.html` di folder `templates`, buatlah sebuah fungsi JavaScript bernama `addNewTask` yang akan digunakan untuk menambahkan Task dengan data form dalam `Modal`. Fungsi `fetch()` digunakan untuk menghubungkan data dari form dengan fungsi yang ada di `views.py`. Gunakan ID khusus untuk memilih form dengan fungsi `querySelector`. Setelah penambahan Task diproses, lakukan refresh dan kosongkan isi form.

      ```js
      function addNewTask() {
        fetch("{% url 'todolist:add_task' %}", {method: "POST", body: new FormData(document.querySelector("#addForm"))}).then(refreshTasks);
        document.getElementById("addForm").reset();
        return false;
      }
      ```

      ```html
      <form id="addForm" onsubmit="return false;">
          {% csrf_token %}
          <div class="modal-body">
              <div class="form-group my-3">
                  <label>Title</label>
                  <input class="form-control" type="text" name="title" placeholder="Title" autofocus required>
              </div>
              <div class="form-group my-3">
                  <label>Description</label>
                  <textarea class="form-control" name="description" placeholder="Description" rows="4"></textarea>
              </div>
          </div>
          <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              <button type="submit" name="submit" class="btn btn-success" data-bs-dismiss="modal" onclick="addNewTask()">Tambah Task</button> <!-- panggil fungsi saat klik button -->
          </div>
      </form>
      ```

   3. **(BONUS) AJAX DELETE: Penghapusan Task**

      Pada `views.py` di folder `todolist`, buatlah fungsi `delete_task` yang menghapus Task dan mengembalikan HttpResponse berdasarkan keberhasilan proses. Tambahkan juga path untuk mengakses fungsi tersebut pada `urls.py`. Fungsi ini akan menerima parameter `id` dari Task yang didapat dari URL.

      ```python
      # views.py
      def delete_task(request, id):
          if request.method == 'DELETE':
              task = Task.objects.filter(pk=id)
              task.delete()
              return HttpResponse("Task Deleted", status=204)
        
           return HttpResponseNotFound()

      # urls.py
      urlpatterns = [
          ...
          path('delete/<int:id>', delete_task, name='delete_task'),
      ]
      ```

      Pada `todolist.html` di folder `templates`, buatlah sebuah fungsi JavaScript bernama `deleteTask` yang akan digunakan untuk menghapus Task berdasarkan ID. Fungsi `fetch()` digunakan untuk menghubungkan dengan fungsi yang ada di `views.py`. Fungsi ini akan menerima parameter `id` yang digunakan sebagai argumen pada URL. Setelah penghapusan Task diproses, lakukan refresh.

      ```js
      function deleteTask(id) {
        fetch(`/todolist/delete/${id}`, {method: "DELETE", headers: {"X-CSRFToken": "{{csrf_token}}" }}).then(refreshTasks);
        return false;
      }
      ```

      ```html
      <form onsubmit="return false;">
          {% csrf_token %}
          <button class="btn btn-delete" type="submit" name="submit" onclick="deleteTask(' + task.pk + ')">❌</button> <!-- panggil fungsi saat klik button -->
      </form>
      ```