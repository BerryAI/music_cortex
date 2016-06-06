import numpy
import urllib
import urllib2
import json

def get_track_lastfm_tags_by_track_info(track_info, k):
    """Get track tags from front end api

    :param track_ID: Track ID
    :return tags_list: list of tag tuples, (tag, counting)
    :rtype: list of tuples
    """
    tags_list = []

    base_url = "http://ws.audioscrobbler.com/2.0/?"
    method = "track.gettoptags"
    artist = track_info[0]
    track = track_info[1]
    if artist == "" or track == "" :
        return tags_list
    api_key = "c5e3f10d5180158b1e2b9a634bb83738"
    query_param = {"method": method, "artist": artist, "track": track, "api_key": api_key, "format": "json"}
    url = base_url + urllib.urlencode(query_param,'utf-8')
    #print url
    response = urllib2.urlopen(url)
    data = json.load(response)

    if "error" in data:
        return tags_list

    if data is not []:
        for value in data["toptags"]["tag"]:
            #tmp = (value["name"], value["count"])
            tmp = value["name"]
            tags_list.append(tmp)
            if len(tags_list) > k:
                return tags_list

    return tags_list

import numpy

def get_track_lastfm_tags_by_track_info(track_info, k):
    """Get track tags from front end api

    :param track_ID: Track ID
    :return tags_list: list of tag tuples, (tag, counting)
    :rtype: list of tuples
    """
    tags_list = []

    base_url = "http://ws.audioscrobbler.com/2.0/?"
    method = "track.gettoptags"
    artist = track_info[0]
    track = track_info[1]
    if artist == "" or track == "" :
        return tags_list
    api_key = "c5e3f10d5180158b1e2b9a634bb83738"
    query_param = {"method": method, "artist": artist, "track": track, "api_key": api_key, "format": "json"}
    url = base_url + urllib.urlencode(query_param,'utf-8')
    response = urllib2.urlopen(url)
    data = json.load(response)

    if "error" in data:
        return tags_list

    if data is not []:
        for value in data["toptags"]["tag"]:
            tmp = value["name"]
            tags_list.append(tmp)
            if len(tags_list) > k:
                return tags_list

    return tags_list

def get_user_play_history(filename_user_history, user_ID):
    """Get user played history from 1k User data

    :param filename_user_history: filename for user listening history
    :param track_ID: Track ID
    :param list_of_tracks: List of tracks user has been played
    :return list_of_tracks: list of played tracks
    :rtype: list
    """

    list_of_tracks = []
    with io.open(filename_user_history,'r',encoding='utf8') as fp:
        for line in fp:
            contents = line.rstrip('\n').rstrip('\r').split("\t")
            if contents[0] == user_ID:
                tmp = ""
                if len(contents) < 6:
                    continue
                track_name = contents[3] + "<SEP>" + contents[5]
                if track_name not in list_of_tracks:
                    list_of_tracks.append(track_name)

    return list_of_tracks

def write_user_track_tags(filename_written_tags, user_ID, list_of_tracks):
    """Write track tags for one user, in case of Last.fm API limits

    :param filename_written_tags: filename for written tags
    :param track_ID: Track ID
    :param list_of_tracks: List of tracks user has been played
    """

    list_of_tags = []

    f = io.open(filename_written_tags, "w")
    for value in list_of_tracks:
        tmp_track_info = value.split("<SEP>")
        tmp = value + "<SEP>"
        data = get_track_lastfm_tags_by_track_info(tmp_track_info,10)
        time.sleep(0.25)
        for value in data:
            tmp += value + "<SEP>"
        tmp += '\n'
        f.write(tmp)
    f.close()

def get_user_most_played_tags(filename_written_tags, percentage):
    """get most played tags with index with given percentage

    :param filename_written_tags: filename for written tags
    :param percentage: percentage of top tags been defined
    :return top_tag_index: the index dictionary of top tags
    :rtype: dictionary
    """

    tag_dictionary = dict()
    top_tag_index = dict()

    with io.open(filename_written_tags,'r', encoding='utf8') as fp:
        for line in fp:
            contents = line.rstrip('\n').split("<SEP>")
            for i in range(2, len(contents)-1):
                if contents[i] not in tag_dictionary:
                    tag_dictionary[contents[i]] = 1
                else:
                    tag_dictionary[contents[i]] += 1
    sorted_tag_dictionary = sorted(tag_dictionary.items(), key=operator.itemgetter(1), reverse=True)

    tag_size = int(len(sorted_tag_dictionary)*percentage)
    for i in range(0, tag_size):
        top_tag_index[sorted_tag_dictionary[i][0]] = i

    return top_tag_index

def get_user_tag_matrix(filename_written_tags, top_tag_index):
    """get user tag full matrix for regression

    :param filename_written_tags: filename for written tags
    :param top_tag_index: the index dictionary of top tags
    :return full_matrix: full matrix of tags with tracks
    :rtype: numpy matrix
    """

    full_matrix = []
    row_length = len(top_tag_index)
    unpoplar_count = 0
    song_with_tag_count = 0
    song_without_tag_count = 0
    with io.open(filename_written_tags,'r', encoding='utf8') as fp:
        for line in fp:
            contents = line.rstrip('\n').split("<SEP>")
            if len(contents) == 3:
                song_without_tag_count += 1
                continue
            row_tmp = [0] * row_length
            song_with_tag_count += 1
            for i in range(2, len(contents)-1):
                if contents[i] in top_tag_index:
                    row_tmp[top_tag_index[contents[i]]] = 1

            if 1 in row_tmp:
                full_matrix.append(row_tmp)
            else:
                unpoplar_count += 1

    # print "number of unpopar song is: ", unpoplar_count
    # print "number of song with tag is: ", song_with_tag_count
    # print "number of song without tag is: ", song_without_tag_count
    full_matrix = numpy.array(full_matrix)

    return full_matrix

def taste_regression(user_ID, filename_written_tags, filename_user_history, percentage):
    """Build regression methods upon user tastes

    :param user_ID: user ID
    :param filename_written_tags: filename for written tags
    :param filename_user_history: filename for user listening history
    :param percentage: percentage of top tags
    :return solution: weights of each top tag for prediction
    :rtype: numpy array
    :return top_tag_index: the index dictionary of top tags
    :rtype: dictionary
    """


    if os.path.exists(filename_written_tags) is False:
        list_of_tracks = get_user_play_history(filename_written_tags, user_ID)
        write_user_track_tags(filename_written_tags, user_ID, list_of_tracks)

    top_tag_index = get_user_most_played_tags(filename_written_tags, percentage)
    full_matrix = get_user_tag_matrix(filename_written_tags, top_tag_index)
    inverse_matrix = numpy.linalg.pinv(full_matrix)
    rhs_vector = numpy.array([1]*len(full_matrix))
    solution = inverse_matrix.dot(numpy.transpose(rhs_vector))

    l2_error = numpy.linalg.norm(numpy.array(rhs_vector) - full_matrix.dot(solution)) / float(len(full_matrix))

    error = numpy.absolute(numpy.array(rhs_vector) - full_matrix.dot(solution)).tolist()
    # count = 0
    # for value in error:
    #     if value > 0.2:
    #         count += 1
    # print count, len(error)
    # print l2_error


    return solution, top_tag_index

def song_prediction(track_info, solution, top_tag_index):
    """Build regression methods upon user tastes

    :param track_info: track information
    :param solution: weights of each top tag for prediction
    :param top_tag_index: the index dictionary of top tags
    :return prediction: if a song will be recommended
    :rtype: boolean
    """

    tag_data = get_track_lastfm_tags_by_track_info(track_info,10)
    tag_row = [0]*len(top_tag_index)
    for value in tag_data:
        if value in top_tag_index:
            tag_row[top_tag_index[value]] = 1

    result = solution.dot(tag_row)
    if abs(result-1) < 0.2:
        return True
    else:
        return False
