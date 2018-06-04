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
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import HttpResponse
from django.http import HttpResponseNotFound
import base64
from datetime import datetime
from .forms import Sign_up_form, CreateEventForm, CreateDate
from .models import Event,Date


def index(request):
    return render(request, 'index.html')

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

#@login_required
def event(request, eventid):
    try:
        event = Event.objects.get(eventUrl = eventid)
        # if event.finishVote == datetime.today():
        #     None

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
        if createform.is_valid():
            event = createform.save(commit=False)
            name = event.name
            event.eventUrl = base64.b64encode(name.encode()).decode()
            event.userId = request.user
            event.save()
            return redirect('event', eventid=event.eventUrl)
     else:
       
        createform = CreateEventForm()
     return render(request, "kandleapp/create.html", {"form": createform, "dateForm": dateForm})
