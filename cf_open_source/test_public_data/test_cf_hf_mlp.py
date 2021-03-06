"""
    test_cf_hd_svd.py
    ~~~
    This module contains testing function of SVD method to discover hidden
    features in collaborative filtering method

    In this tesing file, we generate rating matrix for 1k user playing history
    of songs in Million Song Dataset. Because there are large amount of miss
    match in two data source, we only generate rate matrix of tracks in MSD
    which are played by 1k user dataset. Then we user SVD method to discover
    the hidden features in the CF methods.

    :auther: Alexander Z Wang
"""

import sys
sys.path.append('../cf')
sys.path.append('../read_public_data')
sys.path.append('../../apis')
import msd
import cf_hidden_feature as ch
import cf_mlp as cm
import user_api as ua


# filename of all track information of subset of Million Song Dataset(MSD)
filename_subset = "../../../data/subset_unique_tracks.txt"
# filename of 1k user play history intersect MSD
user_log_intersection_filename = "../../../data/full_log.txt"
# filename of json of hidden feature matrix
json_file_hidden_feature = "../../../data/hf.json"
# number of hidden features
k = 50
lean_rate = 0.00001
lambda_rate = 0.02
max_iter = 5000
GD_method = 1
test_username = "user_000530"

print "Reading MSD and 1k user data..."
# get MSD track dictionary
(unique_tracks_info_dict,
    unique_tracks_info_dict_reverse) = msd.read_tracks_database(
        filename_subset)
# get user play history within MSD
user_log_MSD, user_track_timestamp_MSD = msd.read_intersect_user_log(
    user_log_intersection_filename, unique_tracks_info_dict)
# get user rating dictionary
user_rate_dict = msd.get_track_rating_from_history(user_track_timestamp_MSD)

# get user profile
# if you want to test the function, please uncomment next three line

# user_profile = ch.get_user_profile(
#     user_rate_dict, k, lean_rate, lambda_rate, max_iter, GD_method)
# print user_profile

print "Calculating Hidden Features..."

# get hidden feature matrix
(user_weight, hidden_feature, res_norm, user_index,
    song_index) = ch.get_hidden_feature_matrix_GD(
        user_rate_dict, k, lean_rate, lambda_rate, max_iter, GD_method)

track_hidden_features, user_ratings = cm.get_user_training_data(
    hidden_feature, user_rate_dict, song_index, test_username)
user_model = ua.train_user_taste_model(track_hidden_features, user_ratings)
user_predict = ua.predict_rating(user_model, hidden_feature)

print "Prediction for user_000530 is:"
print user_predict

# write json file to disk
ch.write_hidden_feature_to_file(
    json_file_hidden_feature, hidden_feature, song_index)

# get pridiction matrix
predict_matrix = cm.get_predict_matrix_MLP_hidden_feature(
    hidden_feature, user_rate_dict, user_index, song_index)

print predict_matrix
