"""
    collaborative_filter.py
    ~~~
    This module construct the basic structure of collaborative filtering

    :auther: Alexander Z Wang
"""

import io
import operator
import os.path
import time
import math
import sqlite3


def read_tracks_database(filename):
    """Read all tracks information from Million Song Dataset

    :param filename: filename of the track information file.
    :return unique_tracks_info_dict: MSD tracks information.
    :rtype: dictionary
    """
    unique_tracks_info_dict = dict()
    unique_tracks_info_dict_reverse = dict()
    i = 0
    with io.open(filename,'r',encoding='utf8') as fp:
        for line in fp:
            contents = line.rstrip('\n').split("<SEP>")
            track_info = contents[2] + "<SEP>" + contents[3]
            if track_info not in unique_tracks_info_dict:
                unique_tracks_info_dict[track_info] = i
                i = i+1
            if (i-1) not in unique_tracks_info_dict_reverse:
                unique_tracks_info_dict_reverse[i-1] = track_info

    return unique_tracks_info_dict, unique_tracks_info_dict_reverse

def read_intersect_user_log(filename, unique_tracks_info_dict):
    """Read User Listening Logs intercept MSD

    :param filename: filename of the user listening log contains only MSD tracks.
    :param unique_tracks_info_dict: MSD tracks information dictionary
    :return user_log_MSD: each user play history of MSD tracks.
    :return user_track_timestamp_MSD: timestamp information of each track been played
    :rtype: dictionary
    """
    user_log_MSD = dict()
    user_track_timestamp_MSD = dict()
    count = 0
    with io.open(filename,'r',encoding='utf8') as fp:
        for line in fp:
            contents = line.rstrip('\n').rstrip('\r').split("\t")
            if len(contents) < 6:
                continue
            track_info = contents[3] + "<SEP>" + contents[5]
            if contents[0] in user_log_MSD:
                user_log_MSD[contents[0]].append(unique_tracks_info_dict[track_info])
            else:
                user_log_MSD[contents[0]] = [unique_tracks_info_dict[track_info]]
            if contents[0] in user_track_timestamp_MSD:
                if unique_tracks_info_dict[track_info] in user_track_timestamp_MSD[contents[0]]:
                    user_track_timestamp_MSD[contents[0]][unique_tracks_info_dict[track_info]].append(contents[1])
                else:
                    user_track_timestamp_MSD[contents[0]][unique_tracks_info_dict[track_info]] = [contents[1]]
            else:
                track_timestamp_tmp = dict()
                track_timestamp_tmp[unique_tracks_info_dict[track_info]] = [contents[1]]
                user_track_timestamp_MSD[contents[0]] = track_timestamp_tmp

    # Remove duplicated in user history
    for user in user_log_MSD:
        user_log_MSD[user] = list(set(user_log_MSD[user]))

    return user_log_MSD, user_track_timestamp_MSD

def get_track_rating_from_history(user_track_timestamp_MSD):
    """Calculating rates from users' listening history

    :param user_track_timestamp_MSD: timestamp information of each track been played
    :return user_rate_dict: each user's rating score
    :rtype: dictionary
    """
    time_format = "%Y-%m-%dT%H:%M:%SZ"
    user_rate_dict = dict()
    for user in user_track_timestamp_MSD:
        user_rate_dict[user] = dict()
        for key in user_track_timestamp_MSD[user]:
            length = len(user_track_timestamp_MSD[user][key])
            if length == 1:
                user_rate_dict[user][key] = 3
                continue

            # if a track played more than 10 times, 5 star rating
            if length > 10:
                user_rate_dict[user][key] = 5
                continue

            if length > 1:
                user_rate_dict[user][key] = 4

                # if a track played more than once in a single day, 5 star rating
                for i in range(0, length-1):
                    diff_time = abs(time.mktime(time.strptime(user_track_timestamp_MSD[user][key][i], time_format)) \
                     - time.mktime(time.strptime(user_track_timestamp_MSD[user][key][i+1], time_format))) /3600
                    if diff_time < 24:
                        user_rate_dict[user][key] = 5
                        break
                if user_rate_dict[user][key] == 5:
                    continue

                # if a track played more than 4 times per month, 5 star rating
                if length > 4:
                    for i in range(0, length-4):
                        diff_time = abs(time.mktime(time.strptime(user_track_timestamp_MSD[user][key][i], time_format)) \
                         - time.mktime(time.strptime(user_track_timestamp_MSD[user][key][i+3], time_format))) /3600/24
                        if diff_time < 30:
                            user_rate_dict[user][key] = 5
                            break
                if user_rate_dict[user][key] == 5:
                    continue

    return user_rate_dict

# Set the most basic mean votes
def get_mean_vote_dict(user_rate_dict):
    """Calculating mean rates from users' listening history

    :param user_rate_dict: each user's rating score
    :return user_mean_votes_dict: each user's mean rating score
    :rtype: dictionary
    """

    user_mean_votes_dict = dict()
    for user in user_rate_dict:
        value = 0
        for key in user_rate_dict[user]:
            value += user_rate_dict[user][key]
        user_mean_votes_dict[user] = float(value) / float(len(user_rate_dict[user]))

    return user_mean_votes_dict

def read_full_user_log(filename):
    """Read full listening history

    :param filename: filename of user listening logs.
    :return user_play_his_dict: each user's listening history
    :rtype: dictionary
    """
    song_dictionary = dict()
    user_play_his_dict = dict()
    count = 0
    with io.open(filename,'r',encoding='utf8') as fp:
        for line in fp:
            contents = line.rstrip('\n').rstrip('\r').split("\t")
            if len(contents) < 6:
                continue
            track_info = contents[3] + "<SEP>" + contents[5]
            if track_info not in song_dictionary:
                song_dictionary[track_info] = count
                count = count + 1
            if contents[0] in user_play_his_dict:
                user_play_his_dict[contents[0]].append(song_dictionary[track_info])
            else:
                user_play_his_dict[contents[0]] = [song_dictionary[track_info]]

    for user in user_play_his_dict:
         user_play_his_dict[user] = list(set(user_play_his_dict[user]))

    return user_play_his_dict


def get_knn_dict(full_user_his_dict, k):
    """Get user's other most k similar neighbours

    :param full_user_his_dict: dictionary of full user listening history
    :param k: number of similar users
    :return user_knn_dict: each user's k most similar neighbours
    :rtype: dictionary
    """
    user_knn_dict = dict()
    for user in full_user_his_dict:
        user_knn_dict[user] = []
        user_tmp_dict = dict()
        for another_user in full_user_his_dict:
            if user is another_user:
                continue
            user_tmp_dict[another_user] = len(set(full_user_his_dict[user]) & \
                                        set(full_user_his_dict[another_user]))

        sorted_user_tmp_dict = sorted(user_tmp_dict.items(), key=operator.itemgetter(1))
        sorted_user_tmp_dict.reverse()
        boundary = 0
        for keys in sorted_user_tmp_dict:
            if boundary < k:
                user_knn_dict[user].append(keys)
                boundary = boundary + 1
            else:
                break
        print user_knn_dict[user]

    return user_knn_dict

def get_two_user_similarity(user_log_MSD, user_rate_dict, user_mean_votes_dict, user_1, user_2):
    """Get two users' similarity by pearson correlation

    :param user_log_MSD: all user's full MSD playing history
    :param user_rate_dict: all user's rating score
    :param user_mean_votes_dict: all user's average rating
    :param user_1: user 1
    :param user_2: user 2
    :return user_pearson_similarity: similarity between any two users
    :rtype: float
    """

    user_pearson_similarity_dict = 0
    user_1_ave = user_mean_votes_dict[user_1]
    user_2_ave = user_mean_votes_dict[user_2]
    user_1_tmp_rate = user_rate_dict[user_1]
    user_2_tmp_rate = user_rate_dict[user_2]

    tmp_play_his = list(set(user_log_MSD[user_1]) & set(user_log_MSD[user_2]))
    value_1 = 0
    value_2 = 0
    value_3 = 0
    for value in tmp_play_his:
        value_1 += (user_1_tmp_rate[value]-user_1_ave) * (user_2_tmp_rate[value]-user_2_ave)
        value_2 += (user_1_tmp_rate[value]-user_1_ave) * (user_1_tmp_rate[value]-user_1_ave)
        value_3 += (user_2_tmp_rate[value]-user_2_ave) * (user_2_tmp_rate[value]-user_2_ave)

    user_pearson_similarity_dict = value_1/math.sqrt(value_2)/math.sqrt(value_3)
    return user_pearson_similarity_dict

def get_all_user_similarity_dict(user_log_MSD, user_rate_dict, user_mean_votes_dict):
    """Get all users' similarity by pearson correlation

    :param user_log_MSD: all user's full MSD playing history
    :param user_rate_dict: all user's rating score
    :param user_mean_votes_dict: all user's average rating
    :return all_user_pearson_similarity: similarity between any two users
    :rtype: dictionary
    """
    all_user_similarity_dict = dict()
    for user in user_rate_dict:
        for other_user in user_rate_dict:
            if other_user is user:
                continue
            if user in all_user_similarity_dict[other_user]:
                all_user_similarity_dict[user][other_user] = all_user_similarity_dict[other_user][user]
            else:
                all_user_similarity_dict[user][other_user] = get_two_user_similarity(user_log_MSD,
                            user_rate_dict, user_mean_votes_dict, user, other_user)

    return all_user_similarity_dict


def write_neighbours(user_knn_dict, filename):
    """Write all neighbours information to disk

    :param user_knn_dict: dictionary of each user's k most similar neighbours
    :param filename: filename of neighbours' information
    """
    f = io.open(filename, "w")
    for user in user_knn_dict:
        tmp = user + "<SEP>"
        for other_user_value in user_knn_dict[user]:
            value = other_user_value[0] + ',' +  str(other_user_value[1])
            tmp  = tmp + value + "<SEP>"
        tmp.rstrip("<SEP>")
        tmp += "\n"
        f.write(tmp)

    f.close()

def get_write_knn(full_user_his, k, similar_weight_user_filename, max_k):
    """Get user's other most k similar neighbours and write to file

    :param full_user_his_dict: dictionary of full user listening history
    :param k: number of similar users
    :param similar_weight_user_filename: filename of neighbours information
    :param max_k: maximum number of neighbours could get, max_k > k
    :return user_knn_dict: each user's k most similar neighbours
    :rtype: dictionary
    """

    user_knn_dict = get_knn_dict(full_user_his, max_k)
    write_neighbours(user_knn_dict, similar_weight_user_filename)
    for user in user_knn_dict:
        user_knn_dict[user] = user_knn_dict[user][0:k]
    return user_knn_dict

def read_neighbours(filename, k):
    """Read user's most k similar neighbours from file

    :param filename: filename of neighbours' information
    :param k: number of similar users
    :return user_knn_dict: each user's k most similar neighbours
    :rtype: dictionary
    """

    user_knn_dict = dict()
    with io.open(filename,'r') as fp:
        for line in fp:
            contents = line.rstrip("\n").split("<SEP>")
            tmp = []
            for i in range(0,k):
                values = contents[i+1].split(',')
                weight_and_neighbour = (values[0], float(values[1]))
                tmp.append(weight_and_neighbour)
            user_knn_dict[contents[0]] = tmp

    return user_knn_dict

def collaborative_filtering_pearson_single_user(user, user_log_MSD, user_rate_dict,
                                user_mean_votes_dict, initial_recommendation,
                                all_user_similarity_dict, num):
    """Basic memory based collaboative filtering methods

    :param user: the ID of user
    :param user_log_MSD: each user's playing history of MSD tracks.
    :param user_rate_dict: each user's rating score
    :param user_mean_votes_dict: mean rating score of each user
    :param initial_recommendation: initial recommendation list to be refined
    :param all_user_similarity_dict: similarity dictionary of any two users
    :param num: number of tracks to be recommended
    :return user_predict_list: recommendation for each user based on MSD
    :rtype: list
    """

    user_predict_list = []
    weight = 0
    final_tmp = []
    for track in initial_recommendation:
        if track in user_log_MSD[user]:
            continue
        total_weight = 0
        value = 0
        for other_user in user_log_MSD:
            if user is other_user:
                continue
            if track in user_log_MSD[other_user]:
                value += all_user_similarity_dict[user][other_user] * \
                    (user_rate_dict[track] - user_mean_votes_dict[other_user])
                total_weight += math.abs(all_user_similarity_dict[user][other_user])

        predict_value_track = user_mean_votes_dict[user] + value/total_weight
        if predict_value_track >= 4:
            final_tmp.append((track,predict_value_track))

    final_num = min(num, len(final_tmp))
    user_predict_list = sorted(final_tmp, key=operator.itemgetter(1), reverse=True)[0:final_num]
    #user_predict_list = sorted(final_tmp, reverse=True)[0:final_num]

    return user_predict_list


def collaborative_filtering_user_based(user_knn_dict, user_log_MSD, user_rate_dict, user_mean_votes_dict):
    """Basic memory based collaboative filtering methods

    :param user_knn_dict: each user's k most similar neighbours
    :param user_log_MSD: each user's playing history of MSD tracks.
    :param user_rate_dict: each user's rating score
    :param user_mean_votes_dict: mean rating score of each user
    :param num: number of tracks to be recommended
    :return predict_dict: recommendation for each user based on MSD
    :rtype: dictionary
    """

    predict_dict = dict()
    for user in user_knn_dict:
        predict_dict[user] = []
        track_temp = []
        user_mean_tmp = user_mean_votes_dict[user]

        # combine all the tracks played by similar users
        for other_user in user_knn_dict[user]:
            track_temp += user_log_MSD[other_user[0]]
        track_temp = list(set(track_temp) - set(user_log_MSD[user]))

        # find values of each song and predict
        final_tmp = []
        for track in track_temp:
            value = 0
            weight = 0
            for other_user in user_knn_dict[user]:
                value += (user_rate_dict[other_user[0]].get(track, user_mean_votes_dict[other_user[0]]) \
                            - user_mean_votes_dict[other_user[0]]) *float(other_user[1])
                weight += float(other_user[1])
            value = value / weight
            if value >= 4-user_mean_tmp:
                final_tmp.append(track)
        final_num = min(num, len(final_tmp))
        predict_dict[user] = sorted(final_tmp, reverse=True)[0:final_num]


    return predict_dict

def collaborative_filtering_knn_single_user(user, user_knn_dict, user_log_MSD, user_rate_dict, user_mean_votes_dict, num):
    """Basic memory based collaboative filtering methods

    :param user: the ID of user
    :param user_knn_dict: each user's k most similar neighbours
    :param user_log_MSD: each user's playing history of MSD tracks.
    :param user_rate_dict: each user's rating score
    :param user_mean_votes_dict: mean rating score of each user
    :param num: number of tracks to be recommended
    :return user_predict_list: recommendation for each user based on MSD
    :rtype: list
    """

    track_temp = []
    user_mean_tmp = user_mean_votes_dict[user]

    # combine all the tracks played by similar users
    for other_user in user_knn_dict[user]:
        track_temp += user_log_MSD[other_user[0]]
    track_temp = list(set(track_temp) - set(user_log_MSD[user]))

    # find values of each song and predict
    final_tmp = []
    for track in track_temp:
        value = 0
        weight = 0
        for other_user in user_knn_dict[user]:
            value += (user_rate_dict[other_user[0]].get(track, user_mean_votes_dict[other_user[0]]) \
                        - user_mean_votes_dict[other_user[0]]) *float(other_user[1])
            weight += float(other_user[1])
        value = value / weight
        if value >= 4-user_mean_tmp:
            final_tmp.append((track,value))

    final_num = min(num, len(final_tmp))
    user_predict_list = sorted(final_tmp, key=operator.itemgetter(1), reverse=True)[0:final_num]
    #user_predict_list = sorted(final_tmp, reverse=True)[0:final_num]

    return user_predict_list

def get_user_final_prediction(knn_predict, pearson_predict, knn_weight, pearson_weight, num):
    """Get final recommendation by adding two results

    :param knn_predict: knn method recommendation
    :param pearson_predict: pearson method recommendation
    :param knn_weight: weights on knn method
    :param pearson_weight: weights on pearson methods
    :param num: number of tracks to be recommended
    :return final_user_predict_list: recommendation for each user based on MSD
    :rtype: list
    """
    final_dict = dict()
    if (knn_weight + pearson_weight) == 0:
        print "wrong weights coefficients"
        return
    if (knn_weight + pearson_weight) != 1:
        knn_weight = knn_weight / (knn_weight + pearson_weight)
        pearson_weight = pearson_weight / (knn_weight + pearson_weight)
    knn_dict = dict(knn_predict)
    pearson_dict = dict(pearson_predict)
    for key in knn_dict:
        final_dict[key] = knn_weight*knn_dict[key] + pearson_dict(key)
    final_tmp = sorted(final_dict.items(), key=operator.itemgetter(1), reverse=True)

    final_user_predict_list = [x[0] for x in final_tmp][0:num]

    return final_user_predict_list




def get_predict_list_with_name(user_predict_list, unique_tracks_info_dict_reverse):
    """Get full names of recommendation list

    :param user_predict_list: user prediction list
    :param unique_tracks_info_dict_reverse: track information with index, reverse
    :return user_predict_list: recommendation for each user based on MSD
    :rtype: list
    """

    user_predict_list_with_name = []
    for value in user_predict_list:
        user_predict_list_with_name.append(unique_tracks_info_dict_reverse[value])

    return user_predict_list_with_name



def get_track_tags(track):
    """Get track taste from Last.FM api database
    :return user_rate: tuples of track taste
    :rtype: list of tuples
    """

    dbfile = "lastfm_tags.db"

    conn = sqlite3.connect(dbfile)
    sql = "SELECT tags.tag, tid_tag.val FROM tid_tag, tids, tags WHERE tags.ROWID=tid_tag.tag AND tid_tag.tid=tids.ROWID and tids.tid='%s'" % track
    res = conn.execute(sql)
    data = res.fetchall()
    conn.close()
    return data
