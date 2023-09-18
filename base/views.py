from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .forms import RoomForm
from .models import Room, Topic, Message


# Create your views here.


def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Invalid username")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or password is incorrect")

    context = {"page": page}
    return render(request, "base/login_register.html", context)


def logoutPage(request):
    logout(request)
    return redirect("home")


def registerPage(request):
    page = "register"
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occurred during registration")

    context = {"page": page, "form": form}
    return render(request, "base/login_register.html", context)


def home(request):
    q = request.GET.get("q") if request.GET.get("q") is not None else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    roomsCount = rooms.count()
    roomMessages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {
        "rooms": rooms,
        "topics": topics,
        "rooms_count": roomsCount,
        "room_messages": roomMessages,
    }
    return render(request, "base/home.html", context)


def room(request, key):
    roomObj = Room.objects.get(id=key)
    roomMessages = roomObj.message_set.all()
    participants = roomObj.participants.all()
    if request.method == "POST":
        newMessage = Message.objects.create(
            user=request.user, room=roomObj, message=request.POST.get("message")
        )
        roomObj.participants.add(request.user)
        return redirect("room", key=roomObj.id)

    context = {
        "room": roomObj,
        "room_messages": roomMessages,
        "participants": participants,
    }
    return render(request, "base/room.html", context)


def userProfile(request, key):
    user = User.objects.get(id=key)
    rooms = user.room_set.all()
    roomMessages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        "user": user,
        "rooms": rooms,
        "room_messages": roomMessages,
        "topics": topics,
    }
    return render(request, "base/profile.html", context=context)


@login_required(login_url="login")
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
        )
        return redirect("home")

    context = {"form": form, "topics": topics}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def updateRoom(request, key):
    roomObj = Room.objects.get(id=key)
    form = RoomForm(instance=roomObj)
    topics = Topic.objects.all()

    if request.user != roomObj.host:
        return HttpResponse("You are not authorized")

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        roomObj.name = request.POST.get("name")
        roomObj.topic = topic
        roomObj.description = request.POST.get("description")
        roomObj.save()
        return redirect("home")

    context = {"form": form, "topics": topics, "room": roomObj}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def deleteRoom(request, key):
    roomObj = Room.objects.get(id=key)

    if request.user != roomObj.host:
        return HttpResponse("You are not authorized")

    if request.method == "POST":
        roomObj.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": roomObj})


@login_required(login_url="login")
def deleteMessage(request, key):
    messageObj = Message.objects.get(id=key)

    if request.user != messageObj.user:
        return HttpResponse("You are not authorized")

    if request.method == "POST":
        messageObj.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": messageObj})
