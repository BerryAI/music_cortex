
import os
import os.path
import shutil
import time
import json
import requests
import csv
import uuid

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper

from apis.models import *
from mcx.settings import TOKEN


omnifone_url = 'https://gateway-prod.core-aws.ribob03.net:443/api'
_authorization = 'b5ac9cdb:6c682f4ef33d3f04ed75c43de3bb6d56'

senzari_url = 'http://api.musicgraph.com/api/v2'
api_key = '1cd705639b7cb9846c9d1cda9c3a6324'
senzari_account_id = '2445581183408'



#TODO:using decorator
def validate_token(request):
    token = request.REQUEST.get('token', '')    
    return token == TOKEN
        


def cleanup_data(data):
    if type(data) == list:
        for d in data:
            d.pop('id', None)  
            d.pop('spotify_id', None)  
            d.pop('musicbrainz_id', None)
            d.pop('artist_ref_id', None)
            d.pop('musicbrainz_image_url', None)
            d.pop('album_artist_id', None)
            d.pop('album_ref_id', None)
            d.pop('track_artist_id', None)
            d.pop('track_spotify_id', None)
            d.pop('track_album_id', None)
            d.pop('track_musicbrainz_id', None)
            d.pop('track_album_ref_id', None)  
            d.pop('track_artist_ref_id', None)  
            d.pop('track_ref_id', None)  
    else:
        data.pop('id', None)  
        data.pop('spotify_id', None)  
        data.pop('musicbrainz_id', None)
        data.pop('artist_ref_id', None)
        data.pop('musicbrainz_image_url', None)
        data.pop('album_artist_id', None)
        data.pop('album_ref_id', None)
        data.pop('track_artist_id', None)
        data.pop('track_spotify_id', None)
        data.pop('track_album_id', None)
        data.pop('track_musicbrainz_id', None)
        data.pop('track_album_ref_id', None)  
        data.pop('track_artist_ref_id', None)  
        data.pop('track_ref_id', None)         
    return data    


def artists(request):
    if not validate_token(request):
        return HttpResponse(json.dumps({'msg':'Not Authorized!'}), content_type="application/json", status=401)
    payload = {'api_key':api_key}
    errors = [] 
    name = request.GET.get('name', '')
    #TODO:when no any meaningful request param sent
    r = None
    if name:        
        payload.update({'name':name})        
    similar =  request.GET.get('similar', '')
    if similar:        
        payload.update({'similar_to':similar})            
    decade =  request.GET.get('decade', '')
    if decade:        
        payload.update({'decade':decade})        
    genre =  request.GET.get('genre', '')
    if genre:        
        payload.update({'genre':genre})        
    country =  request.GET.get('country', '')
    if country:
        payload.update({'country':country})
    try:    
        r = requests.get(senzari_url+'/artist/search', params=payload, timeout=90)
    except  requests.exceptions.ReadTimeout as e:
        errors.append('senzari reading timeout!')
    except  requests.exceptions.ConnectTimeout as e:
        errors.append('senzari connect timeout!')
    except Exception as e:
        #check if doing mocking development, and if so just return some mock objects
        #r = None  
        pass

    data = r.json()['data']
    data = cleanup_data(data)
    return HttpResponse(json.dumps(data), content_type="application/json")




def albums(request):
    if not validate_token(request):
        return HttpResponse(json.dumps({'msg':'Not Authorized!'}), content_type="application/json", status=401)
    payload = {'api_key':api_key}
    errors = [] 
    title = request.GET.get('title', '')
    r = None
    if title:
        payload.update({'title':title})        
    artist_name =  request.GET.get('artist_name', '')
    if artist_name:        
        payload.update({'artist_name':artist_name})            
    decade =  request.GET.get('decade', '')
    if decade:        
        payload.update({'decade':decade})        
    genre =  request.GET.get('genre', '')
    if genre:        
        payload.update({'genre':genre})  

    try:    
        r = requests.get(senzari_url+'/album/search', params=payload, timeout=90)
    except  requests.exceptions.ReadTimeout as e:
        errors.append('senzari reading timeout!')
    except  requests.exceptions.ConnectTimeout as e:
        errors.append('senzari connect timeout!')
    except Exception as e:
        #check if doing mocking development, and if so just return some mock objects
        #r = None  
        pass
    data = r.json()['data']
    data = cleanup_data(data)
    return HttpResponse(json.dumps(data), content_type="application/json")



def tracks(request):
    if not validate_token(request):
        return HttpResponse(json.dumps({'msg':'Not Authorized!'}), content_type="application/json", status=401)
    payload = {'api_key':api_key}
    errors = [] 
    title = request.GET.get('title', '')
    r = None
    if title:
        payload.update({'title':title})        
    artist_name =  request.GET.get('artist_name', '')
    if artist_name:        
        payload.update({'artist_name':artist_name})            
    decade =  request.GET.get('decade', '')
    if decade:        
        payload.update({'decade':decade})        
    genre =  request.GET.get('genre', '')
    if genre:        
        payload.update({'genre':genre})  

    try:    
        r = requests.get(senzari_url+'/track/search', params=payload, timeout=90)
    except  requests.exceptions.ReadTimeout as e:
        errors.append('senzari reading timeout!')
    except  requests.exceptions.ConnectTimeout as e:
        errors.append('senzari connect timeout!')
    except Exception as e:
        #check if doing mocking development, and if so just return some mock objects
        #r = None  
        pass
    data = r.json()['data']
    data = cleanup_data(data)
    return HttpResponse(json.dumps(data), content_type="application/json")


def recommend(request):
    if not validate_token(request):
        return HttpResponse(json.dumps({'msg':'Not Authorized!'}), content_type="application/json", status=401)
    
    errors = [] 
    start = request.GET.get('start', '')
    user_id = request.GET.get('device_id', '')
    headers = {'Content-type': 'application/json',  'Accept': 'application/json'}
    #check the token, and find the client for that token. For now, assume rokid. TODO:
    
    
    if not User_Station.objects.filter(client_name='rokid', user_id=user_id).exists():
        #no station created yet for this user_id. So create it
        #First check if a user profile existing in senzari for this user, if not, create one
        #payload.update({'user_id':user_id})
        

        
        print 'creating the user...'
        #no this user profile yet, create one
         
        try:    
            r = requests.post(senzari_url+'/user?api_key='+api_key, data=json.dumps({'user_id':user_id}), headers=headers)
        except  requests.exceptions.ReadTimeout as e:
            errors.append('senzari reading timeout!')
        except  requests.exceptions.ConnectTimeout as e:
            errors.append('senzari connect timeout!')
        except Exception as e:
            #check if doing mocking development, and if so just return some mock objects
            #r = None  
            pass
        print 'after creating user, r:', r.json()  
        #verify user created
        try:    
            r = requests.get(senzari_url+'/user/'+senzari_account_id+':'+user_id+'?api_key='+api_key, headers=headers, timeout=90)
        except  requests.exceptions.ReadTimeout as e:
            errors.append('senzari reading timeout!')
        except  requests.exceptions.ConnectTimeout as e:
            errors.append('senzari connect timeout!')
        except Exception as e:
            #check if doing mocking development, and if so just return some mock objects
            #r = None  
            pass
        print 'getting the user after creating, r:', r.json()

   

        #if no start specified, return an error
        if not start:            
            return HttpResponse(json.dumps({'msg':'You need to start from somewhere. Please provide an artist name that you want to start with!'}), content_type="application/json", status=404)
        #create the station
        #first find the id for the artist
        
        try:    
            r = requests.get(senzari_url+'/artist/search?api_key='+api_key, params={'name':start}, timeout=90)
        except  requests.exceptions.ReadTimeout as e:
            errors.append('senzari reading timeout!')
        except  requests.exceptions.ConnectTimeout as e:
            errors.append('senzari connect timeout!')
        except Exception as e:
            #check if doing mocking development, and if so just return some mock objects
            #r = None  
            pass
        print 'finding the artist id, r:', r.json()
        artist_id = r.json()['data'][0]['id']
        print 'artist_id:', artist_id
        #so far, assume only one artist
        
        try:    
            r = requests.post(senzari_url+'/user/'+senzari_account_id+':'+user_id+'/stations?api_key='+api_key, data=json.dumps({'artist_ids':artist_id}), headers=headers)
        except  requests.exceptions.ReadTimeout as e:
            errors.append('senzari reading timeout!')
        except  requests.exceptions.ConnectTimeout as e:
            errors.append('senzari connect timeout!')
        except Exception as e:
            #check if doing mocking development, and if so just return some mock objects
            #r = None  
            pass
        print 'created the station, r:', r.json()  
        station_id = r.json()['data']['station_id']
        station_session_id = r.json()['data']['station_session_id']
        print 'creating User_Station...'
        us = User_Station(station_id=station_id, station_session_id=station_session_id, client_name='rokid', user_id=user_id)
        us.save()

        #now get the first recommendation to the user

        try:    
            r = requests.get(senzari_url+'/station/'+station_id+'/'+station_session_id+'?api_key='+api_key, params={'action':'first'}, headers=headers)
        except  requests.exceptions.ReadTimeout as e:
            errors.append('senzari reading timeout!')
        except  requests.exceptions.ConnectTimeout as e:
            errors.append('senzari connect timeout!')
        except Exception as e:
            #check if doing mocking development, and if so just return some mock objects
            #r = None  
            pass
        data = r.json()['data']
        track_id = data['id'] 
        us.last_track_id = track_id
        us.save()
   
    else:
        #assume one user has only one station
        #TODO:deal with station session expiration
        ustation =  User_Station.objects.get(client_name='rokid', user_id=user_id)
        payload = {}
        last_track_play_info = request.GET.get('last_track_play_info', '')
        if (not start) and last_track_play_info:
            #provide feedback to the station
            feedback_playload = {'id':ustation.last_track_id}
            if last_track_play_info == 'like':
                feedback_playload.update({'feedback':'like_song'})
            else:
                feedback_playload.update({'feedback':'unlike_song'})    
            try:    
                r = requests.post(senzari_url+'/station/'+ustation.station_id+'/'+ustation.station_session_id+'/feedback?api_key='+api_key, data=json.dumps(feedback_playload), headers=headers)
            except  requests.exceptions.ReadTimeout as e:
                errors.append('senzari reading timeout!')
            except  requests.exceptions.ConnectTimeout as e:
                errors.append('senzari connect timeout!')
            except Exception as e:
                #check if doing mocking development, and if so just return some mock objects
                #r = None  
                pass
            print 'After providing feedback, r:', r 
        if not start:
            payload = {'action':'next'}
        else:
            #update the station. For senzari, need to first delete the existing station, then create a new
            try:    
                r = requests.delete(senzari_url+'/user/'+senzari_account_id+':'+user_id+'/stations/'+ustation.station_id+'?api_key='+api_key, headers=headers)
            except  requests.exceptions.ReadTimeout as e:
                errors.append('senzari reading timeout!')
            except  requests.exceptions.ConnectTimeout as e:
                errors.append('senzari connect timeout!')
            except Exception as e:
                #check if doing mocking development, and if so just return some mock objects
                #r = None  
                pass
            print 'deleting existing station, r:', r
            #generate a new station
            #first find the artist id
            
            try:    
                r = requests.get(senzari_url+'/artist/search?api_key='+api_key, params={'name':start}, timeout=90)
            except  requests.exceptions.ReadTimeout as e:
                errors.append('senzari reading timeout!')
            except  requests.exceptions.ConnectTimeout as e:
                errors.append('senzari connect timeout!')
            except Exception as e:
                #check if doing mocking development, and if so just return some mock objects
                #r = None  
                pass
            print 'After finding the artist, r:', r.json()
            artist_id = r.json()['data'][0]['id']
            print 'artist_id:', artist_id

            
            try:    
                r = requests.post(senzari_url+'/user/'+senzari_account_id+':'+user_id+'/stations?api_key='+api_key, data=json.dumps({'artist_ids':artist_id}), headers=headers)
            except  requests.exceptions.ReadTimeout as e:
                errors.append('senzari reading timeout!')
            except  requests.exceptions.ConnectTimeout as e:
                errors.append('senzari connect timeout!')
            except Exception as e:
                #check if doing mocking development, and if so just return some mock objects
                #r = None  
                pass
            print 'the new station is created after deleting the old one, r:', r.json()  
            #update the db
            ustation.station_id = r.json()['data']['station_id']
            ustation.station_session_id = r.json()['data']['station_session_id']
            count = User_Station.objects.filter(client_name='rokid', user_id=user_id).count()
            print 'before saving, number of stations for this user:', count
            ustation.save()
            count = User_Station.objects.filter(client_name='rokid', user_id=user_id).count()
            print 'number of stations for this user:', count
            payload = {'action':'first'}    

        try:    
            r = requests.get(senzari_url+'/station/'+ustation.station_id+'/'+ustation.station_session_id+'?api_key='+api_key, params=payload, headers=headers)
        except  requests.exceptions.ReadTimeout as e:
            errors.append('senzari reading timeout!')
        except  requests.exceptions.ConnectTimeout as e:
            errors.append('senzari connect timeout!')
        except Exception as e:
            #check if doing mocking development, and if so just return some mock objects
            #r = None  
            pass
        print 'after getting the recommended song, r:', r.json()
        data = r.json()['data']
        track_id = data['id'] 
        ustation.last_track_id = track_id
        ustation.save()


    data = cleanup_data(data)  
    
    return HttpResponse(json.dumps(data), content_type="application/json")



def feedback(request):
    pass    


def decades(request):
    pass


def genres(request):
    pass  


def countries(request):
    pass
        


