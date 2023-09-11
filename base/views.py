from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm


# Create your views here.


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q) )
    topics = Topic.objects.all()
    rooms_count = rooms.count()
    context = {'rooms': rooms, 'topics': topics, 'rooms_count': rooms_count}
    return render(request, 'base/home.html', context)


def room(request, key):
    roomObj = Room.objects.get(id=key)
    context = {'room': roomObj}
    return render(request, 'base/room.html', context)


def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def updateRoom(request, key):
    roomObj = Room.objects.get(id=key)
    form = RoomForm(instance=roomObj)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=roomObj)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def deleteRoom(request, key):
    roomObj = Room.objects.get(id=key)
    if request.method == 'POST':
        roomObj.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': roomObj})
