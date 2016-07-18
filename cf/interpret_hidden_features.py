import io
import numpy as np
import scipy.io as sio
import sys
import codecs

def load_song_index(index_file):
    song_index = dict()
    with io.open(index_file, 'r') as fp:
        for line in fp:
            contents = line.rstrip('\n').split("<SEP>")
            index = int(contents[0])
            artist_name = contents[1]
            song_title = contents[2]
            song_index[index] = (artist_name, song_title)

    return song_index

def find_top_bottom_songs(hidden_features, song_index, limit):
    """
    For each feature, do a full sort for all songs and get the top
    and bottom songs
    """
    num_features = len(hidden_features[0])
    top_bottom_songs = []

    for f in range(0, num_features):
        values = hidden_features[:, f]
        sorted_index = np.argsort(values)
        top_index = sorted_index[-limit:]
        bottom_index = sorted_index[0:limit]
        top_songs = [song_index[i] for i in top_index]
        top_scores = values[top_index]
        bottom_songs = [song_index[i] for i in bottom_index]
        bottom_scores = values[bottom_index]
        top_bottom_songs.append({"top":top_songs, "bottom":bottom_songs, "top_scores": top_scores, "bottom_scores": bottom_scores})

    return top_bottom_songs

def pretty_print(top_bottom_songs):
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    for i in range(0, len(top_bottom_songs)):
        print "[Feature %d]"%(i+1)
        print "==Top=="
        for top in zip(top_bottom_songs[i]['top'], top_bottom_songs[i]['top_scores']):
            print top[0][0], "-", top[0][1], "-", top[1] 
        print "==Bottom=="
        for bottom in zip(top_bottom_songs[i]['bottom'], top_bottom_songs[i]['bottom_scores']):
            print bottom[0][0], "-", bottom[0][1], "-", bottom[1]
        print "="*80

song_index_file = 'index_file.txt'
hidden_features_mat = 'hidden_features.mat'
song_index = load_song_index(song_index_file)
hidden_features = sio.loadmat(hidden_features_mat)['hidden_features']
top_bottom_songs = find_top_bottom_songs(hidden_features, song_index, 10)
pretty_print(top_bottom_songs)
