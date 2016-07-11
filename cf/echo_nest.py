import io
import operator
import numpy
from hidden_feature_prediction import *

def get_song_ID_index(filename):

    song_index = dict()
    name_index = dict()

    with io.open(filename,'r') as fp:
        count = 0
        for line in fp:
            contents = line.rstrip('\n').split("<SEP>")
            track_ID = contents[1]
            if track_ID not in song_index:
                song_index[track_ID] = count
                if count not in name_index:
                    info = contents[2] + "<SEP>" + contents[3]
                    name_index[count] = info
                count += 1

    return song_index, name_index

def get_echo_nest_user_history(filename, song_index):

    echo_nest_user_history = dict()
    with io.open(filename,'r') as fp:
        for line in fp:
            contents = line.rstrip('\n').split("\t")
            if contents[1] not in song_index:
                continue
            if contents[0] not in echo_nest_user_history:
                echo_nest_user_history[contents[0]] = [(song_index[contents[1]], contents[2])]
            else:
                echo_nest_user_history[contents[0]].append((song_index[contents[1]], contents[2]))

    return echo_nest_user_history

def get_user_rating_from_history_echo_nest(echo_nest_user_history, song_index):

    user_rating_dict = dict()

    for user in echo_nest_user_history:
        user_rating_dict[user] = dict()
        for value in echo_nest_user_history[user]:
            score = 3
            play_times = int(value[1])
            if play_times > 4:
                score = 5
            if play_times < 5 and play_times > 1:
                score = 4
            index = value[0]
            if index not in user_rating_dict[user]:
                user_rating_dict[user][index] = score
            else:
                if user_rating_dict[user][index] < 5:
                    user_rating_dict[user][index] += 1

    return user_rating_dict

def get_hidden_feature_matrix(filename_echo_nest, filename_tracks, k):
    """Get CNN training data by user ID

    :param filename: filename of unique MSD tracks
    :param tracks_filename: filename of all unique tracks
    :param base_dir: base directory of data
    :return data: hidden feature dataset
    :rtype: ndarray
    """

    song_index, name_index = get_song_ID_index(filename_tracks)
    echo_nest_user_history = get_echo_nest_user_history(filename_echo_nest, song_index)
    user_rating_dict = get_user_rating_from_history_echo_nest(echo_nest_user_history, song_index)

    user_rating_length = dict()
    for user in user_rating_dict:
        user_rating_length[user] = len(user_rating_dict[user])

    sorted_user_rating_length = sorted(user_rating_length.items(), key=operator.itemgetter(1), reverse=True)

    top_user_rating_dict = dict()
    for value in sorted_user_rating_length[0:1000]:
        top_user_rating_dict[value[0]] = user_rating_dict[value[0]]
    user_index, song_index, rating_matrix = full_rating_matrix_with_index(top_user_rating_dict)

    U, s, V = numpy.linalg.svd(rating_matrix, full_matrices=True)

    V_bar = V[0:k]
    for i in range(0,k):
        V_bar[i] = numpy.sqrt(s[i])* V_bar[i]

    return V_bar.T

def write_song_index_file(song_index_rate, name_index, index_filename):

    inv_song_index_rate = {v: k for k, v in song_index_rate.items()}
    with io.open(index_filename,'w',encoding='utf8') as f:
        for key in inv_song_index_rate:
            info = str(key) + "<SEP>" + name_index[inv_song_index_rate[key]] + "\n"
            f.write(info)


def get_hidden_feature_matrix_SGD(filename_echo_nest, filename_tracks, k, lean_rate, lambda_rate, max_iter):
    """Get hidden feature matrix by stochastic gradient descent method

    :param filename: filename of unique MSD tracks
    :param tracks_filename: filename of all unique tracks
    :param base_dir: base directory of data
    :return data: hidden feature dataset
    :rtype: ndarray
    """

    song_index, name_index = get_song_ID_index(filename_tracks)
    echo_nest_user_history = get_echo_nest_user_history(filename_echo_nest, song_index)
    user_rating_dict = get_user_rating_from_history_echo_nest(echo_nest_user_history, song_index)

    user_rating_length = dict()
    for user in user_rating_dict:
        user_rating_length[user] = len(user_rating_dict[user])

    sorted_user_rating_length = sorted(user_rating_length.items(), key=operator.itemgetter(1), reverse=True)

    top_user_rating_dict = dict()
    for value in sorted_user_rating_length[0:1000]:
        top_user_rating_dict[value[0]] = user_rating_dict[value[0]]
    user_index, song_index_rate, rating_matrix = full_rating_matrix_with_index(top_user_rating_dict)

    write_song_index_file(song_index_rate, name_index, "index_file.txt")

    print "SGD starts"

    user_weight, hidden_feature = stochastic_GD(rating_matrix, lean_rate, lambda_rate, k, max_iter)

    return user_weight, hidden_feature

k = 5
lean_rate = 0.00001
lambda_rate = 0.00
max_iter = 5000

filename_tracks = "subset_unique_tracks.txt"
filename_echo_nest = "train_triplets.txt"
k = 5
user, hidden_feature_matrix = get_hidden_feature_matrix_SGD(filename_echo_nest, filename_tracks, k, lean_rate, lambda_rate, max_iter)

print hidden_feature_matrix[0:10,:]
hist, bin_edges = numpy.histogram(hidden_feature_matrix, bins=20)
print hist
print bin_edges
