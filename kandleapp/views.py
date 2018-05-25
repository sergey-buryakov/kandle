from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import HttpResponse
from django.http import HttpResponseNotFound
import base64
from .forms import CreateEventForm
from .models import Event

def index(request):
    return render(request, 'index.html')

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