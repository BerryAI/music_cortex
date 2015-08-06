from django.db import models

class User_Station(models.Model):    
    station_id = models.CharField(max_length=128)
    #TODO:
    client_name = models.CharField(max_length=64)
    user_id = models.CharField(max_length=128)
    station_session_id = models.CharField(max_length=64)
    last_track_id = models.CharField(max_length=128)    #TODO:
    init_time = models.DateTimeField('time created', auto_now_add=True)
    update_time = models.DateTimeField('time last modified', auto_now=True)

    class Meta:
        unique_together = (("client_name","user_id"),)
