import hdf5_getters
import os.path
import io

def extract_segments_start(base_dir, MSD_track_ID):
    """Get segments start list by MSD track ID

    :param base_dir: base directory of data file
    :param MSD_track_ID: MSD track ID
    :return segments_start: segments start time array
    :rtype: ndarry
    """

    base_dir = "../data/"
    filename = base_dir + MSD_track_ID[2] + "/" + MSD_track_ID[3] + "/" \
        + MSD_track_ID[4] + "/" + MSD_track_ID + ".h5"
    h5 = hdf5_getters.open_h5_file_read(filename)
    segments_start = hdf5_getters.get_segments_start(h5)
    h5.close()

    return segments_start

def extract_segments_pitches(base_dir, MSD_track_ID):
    """Get segments pitches matrix by MSD track ID

    :param base_dir: base directory of data file
    :param MSD_track_ID: MSD track ID
    :return segments_start: segments pitches array
    :rtype: ndarray
    """

    base_dir = "../data/"
    filename = base_dir + MSD_track_ID[2] + "/" + MSD_track_ID[3] + "/" \
        + MSD_track_ID[4] + "/" + MSD_track_ID + ".h5"
    h5 = hdf5_getters.open_h5_file_read(filename)
    segments_pitches = hdf5_getters.get_segments_pitches(h5)
    h5.close()

    return segments_pitches

def extract_segments_timbre(base_dir, MSD_track_ID):
    """Get segments timbre matrix by MSD track ID

    :param base_dir: base directory of data file
    :param MSD_track_ID: MSD track ID
    :return segments_start: segments timbre array
    :rtype: ndarray
    """

    base_dir = "../data/"
    filename = base_dir + MSD_track_ID[2] + "/" + MSD_track_ID[3] + "/" \
        + MSD_track_ID[4] + "/" + MSD_track_ID + ".h5"
    h5 = hdf5_getters.open_h5_file_read(filename)
    segments_timbre = hdf5_getters.get_segments_timbre(h5)
    h5.close()

    return segments_timbre

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

def get_MSD_user_history(MSD_user_filename, user_ID):
    """Get user play history of MSD tracks

    :param MSD_track_filename: filename of MSD unique tracks
    :return MSD_user_history: user play history of MSD tracks
    :rtype: list
    """

    MSD_user_history = []
    with io.open(MSD_user_filename,'r',encoding='utf8') as fp:
        for line in fp:
            contents = line.rstrip('\n').rstrip('\r').split("\t")
            if contents[0] is not user_ID:
                continue
            if len(contents) < 6:
                continue
            track_info = contents[3] + "<SEP>" + contents[5]
            if track_info not in MSD_user_history:
                MSD_user_history.append(track_info)

    return MSD_user_history

def get_MSD_track_ID_index(MSD_track_filename):
    """Get track ID and index dictionary

    :param MSD_track_filename: filename of MSD unique tracks
    :return MSD_track_ID_index: track ID index dictionary
    :rtype: dictionary
    """

    MSD_track_ID_index = dict()
    count = 0
    with io.open(MSD_track_filename,'r',encoding='utf8') as fp:
        for line in fp:
            contents = line.rstrip('\n').split("<SEP>")
            if contents[0] not in MSD_track_ID_index:
                MSD_track_ID_index[contents[0]] = count
                count += 1

    return MSD_track_ID_index
