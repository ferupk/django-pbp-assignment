from django.shortcuts import render
from katalog.models import CatalogItem

# TODO: Create your views here.
def show_catalog(request):
    catalog_item_data = CatalogItem.objects.all()
    context = {
        'catalog_list': catalog_item_data,
        'name': "Feru Pratama Kartajaya",
        'student_id': "2106750351"
    }
    return render(request, "katalog.html", context)