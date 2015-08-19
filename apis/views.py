
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
from mcx.settings import TOKEN, DOWNLOAD_DIR


omnifone_url = 'https://gateway-prod.core-aws.ribob03.net:443/api'
_authorization = 'b5ac9cdb:6c682f4ef33d3f04ed75c43de3bb6d56'



senzari_url = 'http://api.musicgraph.com/api/v2'
api_key = '1cd705639b7cb9846c9d1cda9c3a6324'
senzari_account_id = '2445581183408'

aivvy_url = 'http://lab.dj4.me'



#TODO:using decorator
def validate_token(request):
    #TODO:
    token = request.REQUEST.get('api_key', '')    
    return token == TOKEN or token == '1qufrn7tZKt693tlhbZL7ZmUXx4sbAdZddXXU1w0acqo9idiua983diuia378yid'
        
pop_fields = ['id',
 'spotify_id',
 'musicbrainz_id',
 'artist_ref_id',
 'musicbrainz_image_url',
 'album_artist_id',
 'album_ref_id',
 'track_artist_id',
 'track_spotify_id',
 'track_album_id',
 'track_musicbrainz_id',
 'track_album_ref_id',
 'track_artist_ref_id',
 'track_ref_id',
 'album_musicbrainz_id']

def cleanup_data(data, exclude=[]):
    popup_fields = pop_fields[:]
    for e in exclude:
        popup_fields.remove(e)
    new_data = []
    if type(data) == list:
        for d in data:
            for f in popup_fields:
                d.pop(f, None) 
                new_data.append(d)   
        return new_data        
    else:
        for f in popup_fields:
            data.pop(f, None) 
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
    
    # for d in data:
    #     t = None
    #     senzari_track_id = d.get('id')
    #     if Track.objects.filter(senzari_track_id=senzari_track_id).exists():
    #         t = Track.objects.get(senzari_track_id=senzari_track_id)
    #     else:
    #         #TODO:if no artist name, use performer name?
    #         t = Track(track_id=uuid.uuid4().hex, senzari_track_id=senzari_track_id, title=d['title'], singer=d['artist_name'])    
    #         t.save()
    #     d['id'] = t.track_id
    data = cleanup_data(data)
    #data = cleanup_data(data, exclude=['id'])
    return HttpResponse(json.dumps(data), content_type="application/json")


def recommend(request):
    if not validate_token(request):
        return HttpResponse(json.dumps({'msg':'Not Authorized!'}), content_type="application/json", status=401)
    
    errors = [] 
    start = request.GET.get('start', '')
    user_id = request.GET.get('device_id', '')
    headers = {'Content-type': 'application/json',  'Accept': 'application/json'}
    #check the token, and find the client for that token. For now, assume rokid. TODO:
    data = None
    ustation = None
    omnifone_track_id = None
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
                print 'senzari reading timeout!'
                errors.append('senzari reading timeout!')
            except  requests.exceptions.ConnectTimeout as e:
                print 'senzari connect timeout!'
                errors.append('senzari connect timeout!')
            except Exception as e:
                #check if doing mocking development, and if so just return some mock objects
                #r = None  
                print 'other errors happened'
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

    t = None
    senzari_track_id = data.get('id')
    if Track.objects.filter(senzari_track_id=senzari_track_id).exists():
        t = Track.objects.get(senzari_track_id=senzari_track_id)
    else:
        #TODO:if no artist name, use performer name?
        t = Track(track_id=uuid.uuid4().hex, senzari_track_id=senzari_track_id, title=data['title'], singer=data['artist_name'])    
        # try:    
        #     print 'requesting: ', aivvy_url+'/search_tracks/?query='+data['artist_name']+' '+data['title']
        #     r = requests.get(aivvy_url+'/search_tracks/?query='+data['artist_name']+' '+data['title'])
        # except  requests.exceptions.ReadTimeout as e:
        #     errors.append('senzari reading timeout!')
        # except  requests.exceptions.ConnectTimeout as e:
        #     errors.append('senzari connect timeout!')
        # except Exception as e:
        #     #check if doing mocking development, and if so just return some mock objects
        #     #r = None  
        #     pass

        payloados = {'_authorization':_authorization, 
               'country':'US',
               'searchAttributes':'combinedName',
               'distinct':'true',
               'index':'track',
               'right':'play',
               #'rights':'subscription_playlist_stream',
               'licenseeId':'demo',
               'limit':500
                   }
        payloados.update({'query':data['artist_name']+' '+data['title']})
        r = requests.get(omnifone_url+'/find/catalogues/demo/query.json', params=payloados, timeout=90)    
        rjson = r.json()  
        print 'rjson:', rjson 
        print 'result of getting omnifone id:', r.json()
        #again all the temporary things for the crapy catalogs we have now
        omnifone_track_id = None
        for trackId in r.json()['trackIds']:
            track_id = trackId['trackId']
            payloadom = {'_authorization':_authorization, 
              } 
            print 'the omnifone track id to check:', track_id  
            print 'requesting:', omnifone_url+'/license/licensees/demo/licenses/tracks/US/'+track_id+'.json'                            
            r = requests.get(omnifone_url+'/license/licensees/demo/licenses/tracks/US/'+track_id+'.json', params=payloadom, timeout=90)
            
            if r.status_code != 200:
                #TODO:return 404 for download url not found?
                print 'r.status_code:', r.status_code     
                print 'r.json():', r.json()   
                return ''
            rjson = r.json()    
            token = rjson.get(u'trackRights')[0]['token']    
            payloadom.update({'token':token,
                            'profileName':'320-mp3-mpeg-full',
                            'right':'play',
                            'userId':'demo:user1',
                            'country':'US'
                })
            r = requests.get(omnifone_url+'/contentUrl/audio/trusted/urls/'+track_id+'.json', params=payloadom, timeout=90)
            if r.status_code != 200:
                pass
            else:    
                download_url = r.json()['url']
                if download_url:
                    omnifone_track_id = track_id
                    break


        while not omnifone_track_id:
            payload = {'action':'skip'}    
            #if didn't get the omnifone track id, get another recommendation
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

            senzari_track_id = data.get('id')
            if Track.objects.filter(senzari_track_id=senzari_track_id).exists():
                t = Track.objects.get(senzari_track_id=senzari_track_id)
            else:
                t = Track(track_id=uuid.uuid4().hex, senzari_track_id=senzari_track_id, title=data['title'], singer=data['artist_name'])    
            
                try:    
                    print 'requesting: ', aivvy_url+'/search_tracks/?query='+data['artist_name']+' '+data['title']
                    r = requests.get(aivvy_url+'/search_tracks/?query='+data['artist_name']+' '+data['title'])
                except  requests.exceptions.ReadTimeout as e:
                    errors.append('senzari reading timeout!')
                except  requests.exceptions.ConnectTimeout as e:
                    errors.append('senzari connect timeout!')
                except Exception as e:
                    #check if doing mocking development, and if so just return some mock objects
                    #r = None  
                    pass
                print 'result of getting omnifone id:', r.json()
                #again all the temporary things for the crapy catalogs we have now
                omnifone_track_id = None
                for trackId in r.json()['trackIds']:
                    track_id = trackId['trackId']
                    payloadom = {'_authorization':_authorization, 
                      } 
                    print 'requesting:', omnifone_url+'/license/licensees/demo/licenses/tracks/US/'+track_id+'.json'                            
                    r = requests.get(omnifone_url+'/license/licensees/demo/licenses/tracks/US/'+track_id+'.json', params=payloadom, timeout=90)
                    
                    if r.status_code != 200:
                        #TODO:return 404 for download url not found?
                        print 'getting token, r.status_code:', r.status_code     
                        print 'r.json():', r.json()   
                        return ''
                    rjson = r.json()    
                    token = rjson.get(u'trackRights')[0]['token']    
                    payloadom.update({'token':token,
                                    'profileName':'320-mp3-mpeg-full',
                                    'right':'play',
                                    'userId':'demo:user1',
                                    'country':'US'
                        })
                    r = requests.get(omnifone_url+'/contentUrl/audio/trusted/urls/'+track_id+'.json', params=payloadom, timeout=90)
                    if r.status_code != 200:
                        pass
                    else:    
                        download_url = r.json()['url']
                        if download_url:
                            omnifone_track_id = track_id
                            break
        
        t.provider_track_id = omnifone_track_id
        t.save()

        
    data['id'] = t.track_id
    print 'data is:', data
    data = cleanup_data(data, exclude=['id'])  
    
    return HttpResponse(json.dumps(data), content_type="application/json")



def feedback(request):
    pass    


def decades(request):
    pass


def genres(request):
    pass  


def countries(request):
    pass
        


def download_track(request):
    if not validate_token(request):
        return HttpResponse(json.dumps({'msg':'Not Authorized!'}), content_type="application/json", status=401)
    
    #this track_id is our track_id, isntead of service provider's
    #temp, this track_id is now changed to senzari id. just find our id from it
    track_id = request.GET.get('track_id')
    #t = Track.objects.get(senzari_track_id=track_id)
    #track_id = t.track_id
    filename = download(track_id)
    if not filename:
        #TODO: status code and more detailed error msg
        return HttpResponse(json.dumps({'msg':'failed to download the track!'}), content_type="application/json", status=404) 
    response = HttpResponse(FileWrapper(open(filename)), content_type='audio/mpeg', status=206) #application/zip
    response['Content-Disposition'] = 'attachment; filename='+filename
    response['Accept-Ranges'] = 'bytes'
    print 'filename:', '/' + filename
    response['X-Accel-Redirect'] = '/' + filename
    response['X-Accel-Buffering'] = 'no'
    return response 





def download(track_id):
    print 'track_id to download:', track_id
    filename = DOWNLOAD_DIR+track_id+'.mp3'
    print 'filename:', filename
    #if it already downloaded previously, just return that file aname
    if os.path.isfile(filename):
        return filename
    #provider_track_id = Track.objects.get(track_id=track_id).provider_track_id
    download_url = get_download_url(track_id)
    if not download_url:
        return None
    print 'requesting to download the track...'
    r = requests.get(download_url, stream=True)
    print 'downloading request, r.status_code:', r.status_code
    chunk_size = 1024
    with open(filename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)
    return  filename




def get_download_url(track_id):
    payload = {'_authorization':_authorization, 
              }  
    #get the provider track_id
    t = Track.objects.get(track_id=track_id)  

    track_id = t.provider_track_id
    print 'requesting:', omnifone_url+'/license/licensees/demo/licenses/tracks/US/'+track_id+'.json'                            
    r = requests.get(omnifone_url+'/license/licensees/demo/licenses/tracks/US/'+track_id+'.json', params=payload, timeout=90)
    
    if r.status_code != 200:
        #TODO:return 404 for download url not found?
        print 'get_download_url r.status_code:', r.status_code     
        print 'r.json():', r.json()   
        return ''
    rjson = r.json()    
    token = rjson.get(u'trackRights')[0]['token']    
    payload.update({'token':token,
                    'profileName':'320-mp3-mpeg-full',
                    'right':'play',
                    'userId':'demo:user1',
                    'country':'US'
        })
    r = requests.get(omnifone_url+'/contentUrl/audio/trusted/urls/'+track_id+'.json', params=payload, timeout=90)
    if r.status_code != 200:
        return ''
    download_url = r.json()['url']
    print 'download_url:', download_url
    return download_url