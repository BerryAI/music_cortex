from django.contrib import admin
from apis.models import User_Station, Track


 
class TrackAdmin(admin.ModelAdmin):
    search_fields = ['track_id', 'provider_track_id', 'senzari_track_id', 'title', 'singer', 'release']

admin.site.register(Track, TrackAdmin)

admin.site.register(User_Station)