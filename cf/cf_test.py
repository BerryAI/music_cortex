#import * from collaborative_filter
from front_back_tunnel import *
import sqlite3


filename = "unique_tracks.txt"
filename_subset = "subset_unique_tracks.txt"
filename_test = "test.txt"
user_log_filename_test = "user_log_test.txt"
user_log_filename = "userid-timestamp-artid-artname-traid-traname.tsv"
user_log_filename_small = "userid-timestamp-artid-artname-traid-traname_small.tsv"
user_log_final_filename_small = "final_log_small.txt"
user_log_intersection = "full_log.txt"
similar_user_filename = "similar_user.txt"
similar_weight_user_filename = "similar_user_weight.txt"
k = 5
max_k = 10
recommended_num = 100
time_format = "%Y-%m-%dT%H:%M:%SZ"

# data = get_track_info_by_trackID(29903689)
# print data
#
# data = get_track_tags_front_end(29903619)
# print data

user_1 = "5629499534213120"
data = get_user_played_list_with_events(user_1, eventType="NotMyTaste")
print data

# dbfile = "lastfm_tags.db"
#
# conn = sqlite3.connect(dbfile)
# print '************** DEMO 3 **************'
# tid = 'TRMMHIG128F4228C77'
# print 'We get all tags (with value) for track: %s' % tid
# sql = "SELECT tags.tag, tid_tag.val FROM tid_tag, tids, tags WHERE tags.ROWID=tid_tag.tag AND tid_tag.tid=tids.ROWID and tids.tid='%s'" % tid
# res = conn.execute(sql)
# data = res.fetchall()
# print data
# conn.close()


# unique_tracks_info_dict, unique_tracks_info_dict_reverse = read_tracks_database(filename)
#
#
# print "length of the tracks infomation : ", len(unique_tracks_info_dict)
#
# user_log_MSD, user_track_timestamp_MSD = read_intersect_user_log(user_log_intersection, unique_tracks_info_dict)
# user_rate_dict = get_track_rating_from_history(user_track_timestamp_MSD)
# user_mean_votes_dict = get_mean_vote_dict(user_rate_dict)
# test_user_name = "user_000691"
#
# print "length of the user log with MSD infomation : ", len(user_log_MSD)
# print "Length of test user MSD is : ", len(user_log_MSD[test_user_name])
# print "Length of test user rate is : ", len(user_rate_dict[test_user_name])
# print user_mean_votes_dict[test_user_name]
#
#
# # for user in user_log_MSD:
# #     for value in user_log_MSD[user]:
# #         if value not in user_track_weight_MSD[user]:
# #             print value, user
#
# # # for value in user_track_weight_MSD[test_user_na me]:
# # print user_log_MSD[test_user_name]
# # full_user_his = read_full_user_log(user_log_filename)
# #
# # print "length of the full user log infomation : ", len(full_user_his)
# # print "Length of test user dict is : ", len(full_user_his[test_user_name])
# #
# if os.path.isfile(similar_user_filename):
#     user_knn_dict = read_neighbours(similar_weight_user_filename, k)
# else:
#     user_knn_dict = get_write_knn(full_user_his, k, similar_weight_user_filename, max_k)
#     write_neighbours(user_knn_dict, similar_weight_user_filename)
#
# print "Length of user knn is : ", len(user_knn_dict)
# print "neighbours of the test user is : ", user_knn_dict[test_user_name]
#
# # predict_dict = collaborative_filtering_user_based(user_knn_dict, user_log_MSD,
# #                     user_rate_dict, user_mean_votes_dict, recommended_num)
#
# user_predict_list = collaborative_filtering_single_user(test_user_name, user_knn_dict, user_log_MSD,
#                      user_rate_dict, user_mean_votes_dict, recommended_num)
# print user_predict_list
# user_predict_list_with_name = get_predict_list_with_name(user_predict_list, unique_tracks_info_dict_reverse)
# print user_predict_list_with_name
# #print predict_dict[test_user_name]
#
# # print len(user_knn_dict)
# #
# # i = 0
# # for key in user_knn_dict:
# #     i += 1
# #     if i > 5:
# #         break
# #     print key, user_knn_dict[key]
# # print user_knn_dict[test_user_name]
