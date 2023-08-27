from django.shortcuts import render
from .models import Room

# Create your views here.
rooms = Room.objects.all()

def home(request):
    return render(request, 'base/home.html', {'rooms': rooms})

def room(request, id):
    room = Room.objects.get(id=id)
    context = {'room': room}
    return render(request, 'base/room.html', context)