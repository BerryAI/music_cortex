"""
    front_back_tunnel.py
    ~~~
    This module build retrieving function from front end servers

    :auther: Alexander Z Wang
"""



import urllib
import urllib2
import json

def get_track_info_by_trackID(track_ID):
    """Get artist name + track name from track_ID

    :param track_ID: Track ID
    :return track_info: artist name + track name
    :rtype: lsit of string
    """

    track_info = ["", ""]

    base_url = "http://berry-music-cortex.appspot.com/track/details?"
    query_param = {"trackId": track_ID}
    url = base_url + urllib.urlencode(query_param)
    response = urllib2.urlopen(url)
    data = json.load(response)

    if "error" not in data:
        track_info[0] = data["track"]["artist"]["name"]
        track_info[1] = data["track"]["title"]

    return track_info

def get_track_lastfm_tags(track_ID):
    """Get track tags from front end api

    :param track_ID: Track ID
    :return tags_list: list of tag tuples, (tag, counting)
    :rtype: list of tuples
    """
    tags_list = []

    track_info = get_track_info_by_trackID(track_ID)
    base_url = "http://ws.audioscrobbler.com/2.0/?"
    method = "track.gettoptags"
    artist = track_info[0]
    track = track_info[1]
    if artist == "" or track == "" :
        return tags_list
    api_key = "c5e3f10d5180158b1e2b9a634bb83738"
    query_param = {"method": method, "artist": artist, "track": track, "api_key": api_key, "format": "json"}
    url = base_url + urllib.urlencode(query_param)
    response = urllib2.urlopen(url)
    data = json.load(response)

    if data is not []:
        for value in data["toptags"]["tag"]:
            tmp = (value["name"], value["count"])
            tags_list.append(tmp)

    return tags_list

def get_user_played_list_with_events(user_ID, **args):
    """Get user played list with events(like, disliked, etc)

    :param user_ID: user ID
    :param **args: arguments for calling api
        eventType: any values of [WTF, NotMyTaste, OK, Nice, LoveIt].
                   Leaving this value blank will get a history of played tracks.
        page: Page number of the result. Default to 1.
        pageSize: Number of results to be returned from each page. Default to 20.
        timestamp_from: UTC timestamp of the oldest records to be returned.
                   Default to [1 hour ago]. This parameter should be always
                   provided to avoid time difference between host servers.
        timestamp_to: UTC timestamp of the newest record. Default to [now].
    :return user_play_list: played list with events
    :rtype: list
    """

    user_play_list = []
    query_param = dict()
    if args.has_key("eventType"):
        if args["eventType"] not in ["WTF", "NotMyTaste", "OK", "Nice", "LoveIt"]:
            return user_play_list
        query_param["eventType"] = args["eventType"]
    if args.has_key("page"):
        query_param["page"] = args["page"]
    if args.has_key("pageSize"):
        query_param["pageSize"] = args["pageSize"]
    if args.has_key("timestamp_from"):
        query_param["timestamp_from"] = args["timestamp_from"]
    if args.has_key("timestamp_to"):
        query_param["timestamp_to"] = args["timestamp_to"]
    query_param["user_id"] = user_ID

    base_url = "http://berry-acai.appspot.com/api/activities/?"
    url = base_url + urllib.urlencode(query_param)
    response = urllib.urlopen(url)
    data = json.loads(response.read())

    if "status" in data:
        if data["status"] == "failed" or data["status"] =="error":
            return user_play_list

    for value in data["track_ids"]:
        user_play_list.append(value["track_id"])

    return user_play_list


def get_user_rate_front_end(user_ID):
    """Get user rate for each track ever listened from front end

    :param user_ID: user ID
    :return user_rate: rating score of each track ever listened
    :rtype: dictionary
    """

    user_rate = dict()

    user_play_list_wtf = get_user_played_list_with_events(user_ID, eventType = "WTF")
    for track in user_play_list_wtf:
        user_rate[track] = 1

    user_play_list_nmt = get_user_played_list_with_events(user_ID, eventType = "NotMyTaste")
    for track in user_play_list_nmt:
        user_rate[track] = 2

    user_play_list_okay = get_user_played_list_with_events(user_ID, eventType = "OK")
    for track in user_play_list_okay:
        user_rate[track] = 3

    user_play_list_nice = get_user_played_list_with_events(user_ID, eventType = "Nice")
    for track in user_play_list_nice:
        user_rate[track] = 4

    user_play_list_love = get_user_played_list_with_events(user_ID, eventType = "LoveIt")
    for track in user_play_list_love:
        user_rate[track] = 5

    user_play_list = get_user_played_list_with_events(user_ID)
    for track in user_play_list:
        if track not in user_rate:
            user_rate[track] = 3

    return user_rate
