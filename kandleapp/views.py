#region Auth moduls
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login, authenticate
from django.contrib import messages
from social_django.models import UserSocialAuth
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from social_core.actions import do_complete
from social_django.utils import psa
from social_django.views import NAMESPACE, _do_login
from django.contrib.auth import REDIRECT_FIELD_NAME
#endregion
#region Django moduls
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import HttpResponse
from django.http import HttpResponseNotFound
#endregion
#region Other moduls
import base64
import re
import string
import random
from datetime import datetime
#endregion
from .forms import Sign_up_form, CreateEventForm, CreateDate, LoginForm
from .models import Event, Date
from django.contrib.auth.models import User


def index(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect(userdash)
            else:
                login_message = 'Enter the username and password correctly'
    else:
        form = LoginForm()
        login_message = ''
    return render(request, 'index.html', {'form': form, 'login_message': login_message})

#region Auth
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

@login_required
def settings(request):
    user = request.user

    try:
        google_login = user.social_auth.get(provider='google-oauth2')
    except UserSocialAuth.DoesNotExist:
        google_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'registration/settings.html', {
        'google_login': google_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect(settings)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'registration/password.html', {'form': form})

@never_cache
@csrf_exempt
@psa('{0}:complete'.format(NAMESPACE))
def complete(request, backend, *args, **kwargs):
    """Authentication complete view"""
    return do_complete(request.backend, _do_login, user=None,
                       redirect_name=REDIRECT_FIELD_NAME, request=request,
                       *args, **kwargs)
#endregion


def showStatistic(request,event):
    dates = event.date_set.all()
    countUserForDates={}
    for date in dates:
        countUserForDates[date.date.strftime('%m/%d/%Y')] = date.users.all().count()
    data = {"countUserForDates": countUserForDates}
    return render(request, "kandleapp/voteResult.html", data)

@login_required
def event(request, eventid):
    try:

        event = Event.objects.get(eventUrl=eventid)
        if event.closedForVote:
            return showStatistic(request, event)
        if event.finishVote == datetime.today():
            event.closedForVote = True
            event.save()
            return showStatistic(request, event)
        if request.method == "POST":
            if 'vote' in request.POST:
                lis = request.POST.getlist("che")
                user = User.objects.get(id=request.user.id)
                if user.date_set.exists():
                    dates=user.date_set.all()
                    newDates=[]
                    for d in dates:
                        if d.eventId.id != event.id:
                            newDates.append(d)
                    user.date_set.clear()
                    user.date_set.set(newDates)
                for i in lis:
                    user.date_set.add(Date.objects.get(dateId=i))
                return redirect(request.path)
            if 'finish vote' in request.POST:
                event.closedForVote = True
                event.save()
                return showStatistic(request, event)
        else:
            dates = event.date_set.all()
            url = request.get_host() + request.get_full_path()
            data = {"event": event, "dates": dates, "url": url}
        return render(request, "kandleapp/events.html", data)
    except Event.DoesNotExist:
        return HttpResponseNotFound("<h2>Event not found</h2>")

@login_required
def create(request):
     dateForm = CreateDate()
     if request.method == "POST":
        
        createform = CreateEventForm(request.POST)
        dateset = request.POST['wishDates']
        dateset = re.sub(r'[{},\]"]|:\[|\],', ' ', dateset).strip()
        dateset = re.split(r"\s+", dateset)
        dates = []
        for i in range(0, len(dateset), 3):
            date = Date(date=datetime.strptime(dateset[i], "%m/%d/%Y").date(), startTime=dateset[i + 1], finishTime=dateset[i + 2])
            date.date = date.date.strftime("%Y-%m-%d")
            dates.append(date)
        if createform.is_valid():
            event = createform.save(commit=False)
            name = event.name
            event.eventUrl = base64.b64encode(name.encode()).decode()
            while (Event.objects.filter(eventUrl=event.eventUrl)):
                r = random.choice(string.ascii_uppercase + string.digits)
                event.eventUrl = base64.b64encode((name+r).encode()).decode()

            event.userId = request.user
            event.save()
            for date in dates:
                event.date_set.add(date, bulk=False)

            return redirect("event/" + event.eventUrl)
     else:
       
        createform = CreateEventForm()
     return render(request, "kandleapp/create.html", {"form": createform, "dateForm": dateForm})
def searchEventsWhereUserInvolved(request):
    events = Event.objects.all()
    user = request.user
    eventWhereUserInvolved = []
    for event in events:
        dates = event.date_set.all()
        isLoopInterruped=False
        for date in dates:
            for u in date.users.all():
                if u.username==user.username and event.userId.id!=user.id:
                    eventWhereUserInvolved.append(event)
                    isLoopInterruped=True
                    break
            if isLoopInterruped:
                break
    return eventWhereUserInvolved


# @login_required
def userdash(request):
    eventWhereUserInvolved=searchEventsWhereUserInvolved(request)
    eventsPublic = Event.objects.all().filter(private=False).filter(closedForVote=False)# .filter(name="fnvhjfbdjvh")
    if eventsPublic.exists():
        eventsPublic = random.choice(eventsPublic)
 
    events = request.user.event_set.all().order_by('name')
    
    url = request.get_host()
    countForHighInterestedEvent = 0
    popularEvent=[]
    # forming popular event
    #region start
    for event in events:
        dates = event.date_set.all()
        uniqUsersForDate=[]
        for date in dates:
            for user in date.users.all():
                if user in uniqUsersForDate:
                    continue
                else:
                    uniqUsersForDate.append(user)
        if uniqUsersForDate.__len__() > countForHighInterestedEvent:
            countForHighInterestedEvent = uniqUsersForDate.__len__()
            popularEvent=[event]
        elif uniqUsersForDate.__len__() == countForHighInterestedEvent:
            popularEvent.append(event)
        popEvent={"events":popularEvent,"peopleCount":countForHighInterestedEvent}
        #endregion
    
    countForUnInterestedEvent = 10000000000000000000
    unpopularEvent=[]
    # forming unpopular events
    #region start
    for event in events:
        dates = event.date_set.all()
        uniqUsersForDate=[]
        for date in dates:
            for user in date.users.all():
                if user in uniqUsersForDate:
                    continue
                else:
                    uniqUsersForDate.append(user)
        if uniqUsersForDate.__len__() < countForUnInterestedEvent:
            countForUnInterestedEvent = uniqUsersForDate.__len__()
            unpopularEvent=[event]
        elif uniqUsersForDate.__len__() == countForUnInterestedEvent:
            unpopularEvent.append(event)
        unpopEvent={"events":unpopularEvent,"peopleCount":countForUnInterestedEvent}
        #endregion

    return render(request, "kandleapp/userPage.html", {"events": events, "url":url,
    "popularEvents":popEvent,"unpopularEvents":unpopEvent,
    "randomEvent":eventsPublic,
    "eventWhereUserInvolved":eventWhereUserInvolved})