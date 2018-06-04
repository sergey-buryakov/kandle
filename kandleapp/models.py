from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Event(models.Model):
	eventUrl = models.TextField()
	name = models.TextField()
	description = models.TextField()
	startVote = models.DateField()
	finishVote = models.DateField()
	userId = models.ForeignKey(User, on_delete = models.CASCADE)
	private = models.BooleanField(default=True)
	closedForVote = models.BooleanField(default=False)
	
class Date(models.Model):
	dateId = models.AutoField(db_column='dateId', primary_key=True)
	date = models.DateField(null=False)
	startTime = models.TimeField(null=False)
	finishTime = models.TimeField(null=False)
	eventId = models.ForeignKey(Event, on_delete = models.CASCADE)
	users = models.ManyToManyField(User)

