from msd_extract import *
from content_filter import *

import os.path

def get_tag_vector(filename_written_tags, top_tag_index):
    """get user tag full vector

    :param filename_written_tags: filename for written tags
    :param top_tag_index: the index dictionary of top tags
    :return tag_vector: full vector of tags with tracks
    :rtype: list
    """

    row_length = len(top_tag_index)
    with io.open(filename_written_tags,'r') as fp:
        for line in fp:
            contents = line.rstrip('\n').split("<SEP>")
            tag_vector = [0] * row_length
            for i in range(2, len(contents)-1):
                if contents[i] in top_tag_index:
                    tag_vector[top_tag_index[contents[i]]] = 1

    return tag_vector

def get_user_CNN_training_data(user_ID):
    """Get CNN training data by user ID

    :param user_ID: user ID
    :return data: training data
    :rtype: list
    """

    MSD_user_filename = "full_log.txt"
    MSD_track_filename = "unique_tracks.txt"
    filename_written_tags = user_ID + "_tags.txt"
    base_url = ""
    percentage = 0.2

    user_play_list = get_MSD_user_history(MSD_user_filename, user_ID)
    MSD_track_ID_dict = get_MSD_track_id_dictionary(MSD_track_filename)

    if os.path.exists(filename_written_tags) is False:
        write_user_track_tags(filename_written_tags, user_ID, user_play_list)

    top_tag_index = get_user_most_played_tags(filename_written_tags, percentage)
    track_index = dict()
    count = 0;
    for value in user_play_list:
        track_index[value] = count
        count += 1

    data = [None] * len(user_play_list)
    for value in user_play_list:
        data[track_index[value]] = []
        MSD_track_ID = MSD_track_ID_dict[value]
        segments_start = extract_segments_start(base_dir, MSD_track_ID)
        segments_pitches = extract_segments_pitches(base_dir, MSD_track_ID)
        segments_timbre = extract_segments_timbre(base_dir, MSD_track_ID)
        tag_vector = get_tag_vector(filename_written_tags, top_tag_index)
        data[track_index[value]].append([segments_start, segments_pitches, segments_timbre, tag_vector])

    return data

def get_acoustic_data(filename, base_dir):
    """Get acoustic data for CNN training

    :param filename: filename for unique MSD tracks
    :param base_dir: base directory for data
    :return data: training data
    :rtype: list
    """

    MSD_track_ID_dict = get_MSD_track_ID_index(filename)
    data = [None] * len(MSD_track_ID_dict)
    for key in MSD_track_ID_dict:

        data[MSD_track_ID_dict[key]] = []
        segments_start = extract_segments_start(base_dir, key)
        segments_pitches = extract_segments_pitches(base_dir, key)
        segments_timbre = extract_segments_timbre(base_dir, key)
        data[MSD_track_ID_dict[key]].append([segments_start, segments_pitches, segments_timbre])

    return data
