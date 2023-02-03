from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Attendant as AttendantModel
from .models import Event as EventModel
from .models import Room as RoomModel
from .models import User as UserModel
from .forms import FormRoom, FormEvent, LoginForm, SingInForm


##########################
###       Utils        ###
##########################

# Room utils
def get_rooms():
    return RoomModel.objects.all().order_by('-creation_date')


def get_room_capacity(name):
    room = RoomModel.objects.get(name=name)
    return room.capacity


# Event utils
def get_event(name):
    return EventModel.objects.get(name=name)


def get_events():
    return EventModel.objects.all().order_by('-creation_date')


def get_public_events():
    return EventModel.objects.filter(is_public=True).order_by('-creation_date')


# User utils
def get_user_events(user):
    return AttendantModel.objects.filter(user=user)


##########################
### Template functions ###
##########################

def delete_room(request, name):
    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_staff:
        messages.error(request, 'You do not have permissions to delete rooms')
        return redirect('home')

    room = RoomModel.objects.get(name=name)
    events = len(room.get_events())
    if events < 1:
        messages.info(request, f'The room {room.name} has been deleted')
        room.delete()
        return redirect('rooms')

    messages.error(request, f"The room {room.name} still has events")
    return redirect('rooms')


def cancel_event(request, name):
    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_staff:
        messages.error(request, 'You do not have permissions to cancel events')
        return redirect('home')

    event = get_event(name)
    event.delete()

    messages.info(request, f"The event {event.name} has been canceled")
    return redirect('home')


def cancel_subscription(request, name):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    event = get_event(name)
    attend = AttendantModel.objects.get(user=user, event=event)
    attend.delete()

    messages.info(request, f"Your place to the event {event.name} has been canceled")
    return redirect('profile')


def book_event(request, name):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    event = get_event(name)

    if AttendantModel.objects.filter(user=user, event=event):
        messages.error(request, f"I'm sorry, you already have a place booked for {event}.")
    elif event.get_availability() > 0:
        new_attend = AttendantModel(user=user, event=event)
        new_attend.save()
        messages.success(request, f"Congratulations! Now you have a place for {event}.")
    else:
        messages.warning(request, f"I'm sorry, there are not any place available for {event}.")

    return redirect('home')


######################
### Template views ###
######################

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user

    events = get_events() if user.is_staff else get_public_events()
    context = {
        'user': user,
        'title': 'Events',
        'events': events
    }
    return render(request, 'index.html', context)


def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    context = {
        'user': user,
        'title': 'Profile',
        'events': get_user_events(user),
    }
    return render(request, 'profile.html', context)


def event_details(request, name):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    event = get_event(name)
    context = {
        'user': user,
        'title': event.name,
        'event': event
    }
    return render(request, 'event_details.html', context)


def rooms(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_staff:
        messages.error(request, f"I'm sorry, you do not have permissions")
        return redirect('home')

    user = request.user
    rooms = get_rooms()
    context = {
        'user': user,
        'title': 'Rooms',
        'rooms': rooms,
    }
    return render(request, 'rooms.html', context)


def add_room(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_staff:
        messages.error(request, f"I'm sorry, you do not have permissions to add rooms")
        return redirect('home')

    if request.method == 'POST':
        form = FormRoom(request.POST)
        if form.is_valid():
            data_form = form.cleaned_data
            room = RoomModel(
                name=data_form.get('name'),
                capacity=data_form.get('capacity'),
            )
            room.save()
            messages.success(request, f"The room {room.name} has been created")
            return redirect('rooms')
        else:
            messages.error(request, f"I'm sorry, an error has occurred. Check if the room does not exists and try again")
            return redirect('add_room')

    user = request.user
    context = {
        'user': user,
        'title': 'Add new Room',
        'form': FormRoom(),
    }
    return render(request, 'add_room.html', context)


def add_event(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_staff:
        messages.error(request, f"I'm sorry, you do not have permissions to add events")
        return redirect('home')

    if request.method == 'POST':
        form = FormEvent(request.POST)
        if form.is_valid():
            data_form = form.cleaned_data
            event = EventModel(
                room=data_form.get('room'),
                name=data_form.get('name'),
                description=data_form.get('description'),
                date=data_form.get('date'),
                is_public=data_form.get('is_public'),
            )
            event.save()
            messages.success(request, f"The event {event.name} has been created")
            return redirect('home')
        else:
            messages.error(request, f"I'm sorry, an error has occurred. Check if the event does not exists and try again")
            return redirect('add-event')

    user = request.user
    context = {
        'user': user,
        'title': 'Add new Event',
        'form': FormEvent(),
    }
    return render(request, 'add_event.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data_form = form.cleaned_data
            username = data_form.get('username')
            password = data_form.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, f"Invalid username or password, please check your information")
                return redirect('login')

    context = {
        'title': 'Log in',
        'form': LoginForm()
    }
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')


def sing_in(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SingInForm(request.POST)
        if form.is_valid():
            data_form = form.cleaned_data
            user = UserModel(
                first_name=data_form.get('first_name'),
                last_name=data_form.get('last_name'),
                is_staff=data_form.get('is_staff'),
                username=data_form.get('username'),
                email=data_form.get('email'),
                password=make_password(data_form.get('password'))
            )
            user.save()
            messages.success(request, f"The user has been created")
            return redirect('home')
        else:
            messages.error(request, f"I'm sorry, an error has occurred. May the username already exists.")
            return redirect('sing_in')

    context = {
        'title': 'Sing in',
        'form': SingInForm()
    }
    return render(request, 'sing_in.html', context)
