from django.db import models


class Event(models.Model):
    event_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    event_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.event_name