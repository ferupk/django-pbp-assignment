from django.urls import path
from katalog.views import show_catalog

# TODO: Implement Routings Here
app_name = 'katalog'

urlpatterns = [
    path('', show_catalog, name='show_catalog'),
]