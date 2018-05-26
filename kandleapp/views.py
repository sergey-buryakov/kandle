<<<<<<< HEAD
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import HttpResponse
from django.http import HttpResponseNotFound
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
import base64
from .forms import Sign_up_form, CreateEventForm
from .models import Event

def index(request):
    return render(request, 'index.html')

def sign_up(request):
    if request.method == 'POST':
        form = Sign_up_form(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(index)
    else:
        form = Sign_up_form()
    return render(request, "registration/sign_up.html", {"form": form})

def event(request, eventid):
    try:
        event = Event.objects.get(eventId = eventid)
        eventname = event.name
        eventdescr = event.description

        data = {"name": eventname, "description": eventdescr}
        return render(request, "kandleapp/events.html", data)
    except Event.DoesNotExist:
        return HttpResponseNotFound("<h2>Event not found</h2>")
    # events = Event.objects.all()
    # return render(request, "kandleapp/events.html", {"events": events})

def create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        return HttpResponse("<p>Name: {0}, decr: {1}</p>".format(name, description))
        # event = Event()
        # name = request.POST.get("name")
        # event.name = name
        # event.description = request.POST.get("description")
        # name = name.encode()
        # event.eventId = base64.b64encode(name).decode()
        # event.save()
        # return HttpResponseRedirect("/event")
    else:
        createform = CreateEventForm()
        return render(request, "kandleapp/create.html", {"form": createform})