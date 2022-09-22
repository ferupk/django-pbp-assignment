from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from mywatchlist.models import MyWatchList

def show_mywatchlist(request):
    data = MyWatchList.objects.all()
    amount_watched = 0
    for item in data:
        if item.watched: 
            amount_watched +=1
    watched_enough = True if amount_watched >= (len(data) - amount_watched) else False
    context = {
        'my_watchlist': data,
        'watched_enough': watched_enough
        
    }
    return render(request, "mywatchlist.html", context)

def show_xml(request):
    data = MyWatchList.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = MyWatchList.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")