from django.db import models

class User_Station(models.Model):    
    station_id = models.CharField(primary_key=True, max_length=128)
    #TODO:
    client_name = models.CharField(max_length=64)
    user_id = models.CharField(max_length=128)
    station_session_id = models.CharField(max_length=64)
    init_time = models.DateTimeField('time created', auto_now_add=True)
    update_time = models.DateTimeField('time last modified', auto_now=True)
