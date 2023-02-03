from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Room(models.Model):
    name          = models.CharField(max_length=255, primary_key=True)
    capacity      = models.IntegerField(default=0)
    creation_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def __int__(self):
        return self.capacity

    def get_name(self):
        return self.name

    def get_capacity(self):
        return self.capacity

    def get_events(self):
        events = Event.objects.filter(room=self.name)
        # active_events = map(Event.is_active, events)
        return events


class Event(models.Model):
    name          = models.CharField(max_length=255, primary_key=True)
    room          = models.ForeignKey(Room, on_delete=models.CASCADE)
    description   = models.TextField(default='')
    date          = models.DateTimeField()
    is_public = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_room(self):
        return self.room

    def is_active(self):
        return self.date > datetime.now()

    def get_availability(self):
        attendants = len(Attendant.objects.filter(event=self.name))
        return self.room.capacity - attendants


class Attendant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    subscription_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event.name

    def get_user(self):
        return self.user

    def get_event(self):
        return self.event



