from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Event(models.Model):
	eventId = models.UUIDField()
	name = models.TextField()
	description = models.TextField()
	startVote = models.DateTimeField()
	finishVote = models.DateTimeField()
	userId = models.ForeignKey(User, on_delete = models.CASCADE)
	
class Date(models.Model):
	dateId = models.AutoField(db_column='dateId', primary_key=True)
	date = models.DateField()
	startTime = models.TimeField()
	finishTime = models.TimeField()
	eventId = models.ForeignKey(Event, on_delete = models.CASCADE)
	users = models.ManyToManyField(User)
	
