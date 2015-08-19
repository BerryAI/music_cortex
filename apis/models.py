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


class Track(models.Model):    
    track_id = models.CharField(primary_key=True, max_length=128)
    provider_track_id = models.CharField(max_length=64)
    #TODO:maybe more generic instead of hardcode senzari
    senzari_track_id = models.CharField(max_length=64)
    title = models.CharField(max_length=128)
    singer = models.CharField(max_length=64)      
    genre = models.CharField(max_length=32)
    release =  models.CharField(max_length=512)  
    #TODO:url field
    cover_url = models.CharField(max_length=512)  
    has_download_url =models.BooleanField(default=False) #models.CharField(max_length=1024) 
    #TODO:default   
    format =  models.CharField(max_length=32, default='320-mp3-mpeg-full')
    service_provider = models.CharField(max_length=32)    
    init_time = models.DateTimeField('time created', auto_now_add=True)
    update_time = models.DateTimeField('time last modified', auto_now=True)


    class Meta:
        ordering = ['-init_time','title','singer','genre']
    
    def __unicode__(self):
        return self.title + u' by ' + self.singer
    