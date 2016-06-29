import io
import time
import numpy
from hdf5_getters import *
from msd_extract import *

def read_tracks_database(filename):
    """Read all tracks information from Million Song Dataset

    :param filename: filename of the track information file.
    :return unique_tracks_info_dict: MSD tracks information.
    :rtype: dictionary
    """
    unique_tracks_info_dict = dict()
    i = 0
    with io.open(filename,'r',encoding='utf8') as fp:
        for line in fp:
            contents = line.rstrip('\n').split("<SEP>")
            track_info = contents[2] + "<SEP>" + contents[3]
            if track_info not in unique_tracks_info_dict:
                unique_tracks_info_dict[track_info] = i
                i = i+1
    return unique_tracks_info_dict

def get_MSD_track_id_dictionary(MSD_track_filename, user_play_list):
    """Get track info and MSD ID dictionary

    :param MSD_track_filename: filename of MSD unique tracks
    :return MSD_track_ID_dict: track ID dictionary
    :rtype: dictionary
    """

    MSD_track_ID_dict = dict()
    with io.open(MSD_track_filename,'r',encoding='utf8') as fp:
        for line in fp:
            contents = line.rstrip('\n').split("<SEP>")
            track_info = contents[2] + "<SEP>" + contents[3]
            if track_info in user_play_list:
                if track_info not in MSD_track_ID_dict:
                    MSD_track_ID_dict[track_info] = contents[0]

    return MSD_track_ID_dict

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
            if track_info not in unique_tracks_info_dict:
                continue
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

def full_rating_matrix_with_index(user_rate_dict):
    """Get full rating matrix with song index at each row

    :param user_rate_dict: user rate score dictionary (sparse)
    :return rating_matrix: full matrix of rating scores
    :rtype: dictionary
    """

    user_index = dict()
    song_index = dict()

    user_count = 0
    song_count = 0
    for user in user_rate_dict:
        if user not in user_index:
            user_index[user] = user_count
            user_count += 1
        for track_key in user_rate_dict[user]:
            if track_key not in song_index:
                song_index[track_key] = song_count
                song_count += 1

    rating_matrix = [None]*len(user_index)

    for user in user_rate_dict:
        rating_vector = [0.0] * len(song_index)
        for track_key in user_rate_dict[user]:
            rating_vector[song_index[track_key]] = user_rate_dict[user][track_key]
        rating_matrix[user_index[user]] = rating_vector

    rating_matrix = numpy.array(rating_matrix)
    matrix_update_by_song_mean_rate(rating_matrix)
    return user_index, song_index, rating_matrix

def matrix_update_by_song_neighbours(rating_matrix, user_rate_dict, user_index, song_index):
    """Update rating score with nearest neighbours

    :param rating_matrix: full matrix of rating scores
    """
    filename = "similar_user_weight.txt"
    user_knn_dict = read_neighbours(similar_weight_user_filename, 3)
    user_rate_pred_dict = dict()

    for user in user_rate_dict:
        user_rate_pred_dict[user] = []
        user_play_list = [x[0] for x in user_rate_pred_dict[user]]
        user_mean_rate = numpy.mean([x[1] for x in user_rate_pred_dict[user]])
        overall_weight = 0
        for value in user_knn_dict[user]:
            other_user = value[0]
            weight = value[1]
            overall_weight += weight
            for pair in user_rate_dict[other_user]:
                pass


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

def matrix_update_by_song_mean_rate(rating_matrix):
    """Update rating score with average score

    :param rating_matrix: full matrix of rating scores
    """

    for i in range(0, len(rating_matrix[0])):
        index = rating_matrix[:,i] > 0
        ave_score = float(numpy.sum(rating_matrix[:,i])) / float(numpy.sum(index))
        for j in range(0, len(rating_matrix)):
            if rating_matrix[j][i] == 0.0:
                rating_matrix[j][i] = ave_score

def get_hidden_feature_matrix(user_log_intersection_filename, tracks_filename, base_dir, k):
    """Get CNN training data by user ID

    :param filename: filename of unique MSD tracks
    :param tracks_filename: filename of all unique tracks
    :param base_dir: base directory of data
    :return data: hidden feature dataset
    :rtype: ndarray
    """

    unique_tracks_info_dict = read_tracks_database(tracks_filename)
    inv_unique_tracks_info_dict = {v: k for k, v in unique_tracks_info_dict.items()}
    MSD_track_ID_dict = get_MSD_track_id_dictionary(tracks_filename, unique_tracks_info_dict)

    user_log_MSD, user_track_timestamp_MSD = read_intersect_user_log(user_log_intersection_filename, unique_tracks_info_dict)
    user_rate_dict = get_track_rating_from_history(user_track_timestamp_MSD)
    user_index, song_index, rating_matrix = full_rating_matrix_with_index(user_rate_dict)

    U, s, V = numpy.linalg.svd(rating_matrix, full_matrices=True)

    V_bar = V[0:k]
    for i in range(0,k):
        V_bar[i] = numpy.sqrt(s[i])* V_bar[i]

    return V_bar.T

def get_acoustic_data_with_rate_matrix(user_log_intersection_filename, tracks_filename, base_dir):
    """Get CNN training data by user ID

    :param filename: filename of unique MSD tracks
    :param tracks_filename: filename of all unique tracks
    :param base_dir: base directory of data
    :return data: training data
    :rtype: list
    """

    unique_tracks_info_dict = read_tracks_database(tracks_filename)
    inv_unique_tracks_info_dict = {v: k for k, v in unique_tracks_info_dict.items()}
    MSD_track_ID_dict = get_MSD_track_id_dictionary(tracks_filename, unique_tracks_info_dict)

    user_log_MSD, user_track_timestamp_MSD = read_intersect_user_log(user_log_intersection_filename, unique_tracks_info_dict)
    user_rate_dict = get_track_rating_from_history(user_track_timestamp_MSD)
    user_index, song_index, rating_matrix = full_rating_matrix_with_index(user_rate_dict)

    U, s, V = numpy.linalg.svd(rating_matrix, full_matrices=True)

    k = int(len(s) * 0.1)
    V_bar = V[0:k]
    for i in range(0,k):
        V_bar[i] = numpy.sqrt(s[i])* V_bar[i]

    data = [None] * len(song_index)

    f = open('datafile.dat','w')
    f.write(str(len(song_index))+"\n")

    for key in song_index:
        track_info = inv_unique_tracks_info_dict[key]
        data[song_index[key]] = []
        MSD_track_ID = MSD_track_ID_dict[track_info]
        segments_start = extract_segments_start(base_dir, MSD_track_ID)
        segments_pitches = extract_segments_pitches(base_dir, MSD_track_ID)
        segments_timbre = extract_segments_timbre(base_dir, MSD_track_ID)
        hidden_feature = V_bar.T[song_index[key]]
        message_line = str(segments_start.shape[0]) + " " + str(segments_pitches.shape[0]) + " " + \
            str(segments_pitches.shape[1]) + " " + str(segments_timbre.shape[0]) + " " + \
            str(segments_timbre.shape[1]) + " " + str(k) + "\n"
        f.write(message_line)
        for i in range(0, segments_start.shape[0]):
            line = str(segments_start[i]) + "\n"
            f.write(line)
        for i in range(0, segments_pitches.shape[0]):
            for j in range(0, segments_pitches.shape[1]):
                line = str(segments_pitches[i][j]) + "\n"
                f.write(line)
        for i in range(0, segments_timbre.shape[0]):
            for j in range(0, segments_timbre.shape[1]):
                line = str(segments_timbre[i][j]) + "\n"
                f.write(line)
        for i in range(0, k):
            line = str(hidden_feature[i]) + "\n"
            f.write(line)

        data[song_index[key]].append([segments_start, segments_pitches, segments_timbre, hidden_feature])

    f.close()

    return data, song_index

def get_user_prediction_SVD(user_IDs):
    """Get user prdiction by SVD

    :param user_ID: user ID
    :return prediction: prediction track list
    :rtype: list
    """

    filename_subset = "subset_unique_tracks.txt"
    user_log_intersection_filename = "full_log.txt"
    base_dir = "../data"

    prediction = dict()
    history = dict()
    user = dict()

    unique_tracks_info_dict = read_tracks_database(filename_subset)
    inv_unique_tracks_info_dict = {v: k for k, v in unique_tracks_info_dict.items()}
    MSD_track_ID_dict = get_MSD_track_id_dictionary(filename_subset, unique_tracks_info_dict)

    user_log_MSD, user_track_timestamp_MSD = read_intersect_user_log(user_log_intersection_filename, unique_tracks_info_dict)
    user_rate_dict = get_track_rating_from_history(user_track_timestamp_MSD)
    user_index, song_index, rating_matrix = full_rating_matrix_with_index(user_rate_dict)
    inv_song_index_dict = {v: k for k, v in song_index.items()}

    U, s, V = numpy.linalg.svd(rating_matrix, full_matrices=True)

    k = int(len(s) * 0.1)
    V_bar = V[0:k]
    U_bar = U[:,0:k]
    for i in range(0,k):
        V_bar[i] = numpy.sqrt(s[i])* V_bar[i]
        U_bar[:,i] = numpy.sqrt(s[i])* U_bar[:,i]

    if isinstance(user_IDs, list) is False:
        user_IDs = [user_IDs]

    for user_ID in user_IDs:
        user[user_ID] = dict()
        user_his = []
        user_pred = []
        output_vector = U_bar.dot(V_bar)[user_index[user_ID]].tolist()
        index = sorted(range(len(output_vector)), key=output_vector.__getitem__, reverse=True)
        count = 0
        for value in index:
            track_index = inv_song_index_dict[index[value]]
            if track_index in user_log_MSD[user_ID]:
                continue
            user_pred.append(inv_unique_tracks_info_dict[track_index])
            count += 1
            if count > 9:
                break
        for value in user_log_MSD[user_ID]:
            user_his.append(inv_unique_tracks_info_dict[value])

        user[user_ID]["recommendation"] = user_pred
        user[user_ID]["history"] = user_his


    return user

filename_subset = "subset_unique_tracks.txt"
tracks_filename = "full_log.txt"
base_dir = "../data"
# Hidden feature number k
k = 5
hidden_feature = get_hidden_feature_matrix(tracks_filename, filename_subset, base_dir, k)

hist, bin_edges = numpy.histogram(hidden_feature, bins=20)
print hist
print bin_edges
