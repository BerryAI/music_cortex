
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
    payload = {'api_key':api_key}
    errors = [] 
    start = request.GET.get('start', '')
    user_id = request.GET.get('user_id', '')
    #check the token, and find the client for that token. For now, assume rokid. TODO:
    if not User_Station.objects.filter(client_name='rokid', user_id=userid).exists():
        #no station created yet for this user_id. So create it
        #First check if a user profile existing in senzari for this user, if not, create one
        #payload.update({'user_id':user_id})
        try:    
            r = requests.get(senzari_url+'/user/'+senzari_account_id+':'+user_id, params=payload, timeout=90)
        except  requests.exceptions.ReadTimeout as e:
            errors.append('senzari reading timeout!')
        except  requests.exceptions.ConnectTimeout as e:
            errors.append('senzari connect timeout!')
        except Exception as e:
            #check if doing mocking development, and if so just return some mock objects
            #r = None  
            pass
        print 'r:', r
    data = {}
    return HttpResponse(json.dumps(data), content_type="application/json")

        


