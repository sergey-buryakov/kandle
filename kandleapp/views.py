from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import HttpResponse
import base64
from .forms import CreateEventForm
from .models import Event

def index(request):
    return render(request, 'index.html')

def event(request):
    events = Event.objects.all()
    return render(request, "kandleapp/events.html", {"events": events})

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