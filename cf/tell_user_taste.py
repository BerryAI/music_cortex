"""
    tell_user_taste.py
    ~~~
    This module calculates user taste by listening history

    :auther: Alexander Z Wang
"""
import json
import operator
from front_back_tunnel import *

def tell_user_taste(user_ID):
    """Get user taste from user listening listory

    :param user_ID: user id
    :return user_taste: description of user taste
    :rtype: JSON string
    """

    user_play_list = get_user_played_list_with_events(user_ID)
    if len(user_play_list) > 10:
        user_taste = tell_user_taste_later(user_ID)
    else:
        user_taste = tell_user_initial_taste(user_ID)

    return user_taste


def tell_user_initial_taste(user_ID):
    """Get user taste from first 10 songs

    :param user_ID: user id
    :return user_taste: description of user taste
    :rtype: JSON string
    """

    user_taste = dict()
    user_rate = get_user_rate_front_end(user_ID)

    user_tags_tmp = dict()

    user_taste["user"] = user_ID
    user_taste["taste"] = []

    tags_data_dict = get_initial_track_tags()
    for track in tags_data_dict:
        tags_data = tags_data_dict[track]
        for value in tags_data:
            if value[0] in user_tags_tmp:
                user_tags_tmp[value[0]] += (user_rate[track]-3) * value[1]
            else:
                user_tags_tmp[value[0]] = (user_rate[track]-3) * value[1]

    sorted_user_tags_tmp = sorted(user_tags_tmp.items(), key=operator.itemgetter(1), reverse=True)
    count = 0
    for value in sorted_user_tags_tmp:
        if value[1] > 0:
            count += 1
    weight = 0
    k = min(count, 5)
    for i in range(0,k):
        weight += sorted_user_tags_tmp[i][1]

    for i in range(0,k):
        taste_tag = dict()
        taste_tag["tag"] = sorted_user_tags_tmp[i][0]
        taste_tag["percent"] = str(int(sorted_user_tags_tmp[i][1] * 100.0 / weight)) + "%"
        user_taste["taste"].append(taste_tag)

    return json.dumps(user_taste)

def tell_user_taste_later(user_ID):
    """Get user taste from listening history

    :param user_ID: user id
    :return user_taste: description of user taste
    :rtype: JSON string
    """

    user_taste = dict()
    user_rate = get_user_rate_front_end(user_ID)

    user_tags_tmp = dict()

    user_taste["user"] = user_ID
    user_taste["taste"] = []


    for track in user_rate:
        print "track is: ", track
        tags_data = get_track_lastfm_tags(track)
        print tags_data
        for value in tags_data:
            if value[0] in user_tags_tmp:
                user_tags_tmp[value[0]] += (user_rate[track]-3) * value[1]
            else:
                user_tags_tmp[value[0]] = (user_rate[track]-3) * value[1]

    sorted_user_tags_tmp = sorted(user_tags_tmp.items(), key=operator.itemgetter(1))
    count = 0
    for value in sorted_user_tags_tmp:
        if value[1] > 0:
            count += 1
    weight = 0
    k = min(count, 5)
    for i in range(0,k):
        weight += sorted_user_tags_tmp[i][1]

    for i in range(0,k):
        taste_tag = dict()
        taste_tag["tag"] = sorted_user_tags_tmp[i][0]
        taste_tag["percent"] = str(int(sorted_user_tags_tmp[i][1] * 100.0 / weight)) + "%"
        user_taste["taste"].append(taste_tag)

    return json.dumps(user_taste)
