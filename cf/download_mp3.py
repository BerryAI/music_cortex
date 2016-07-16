import io
import urllib
import urllib2
import json
import os

def download_spotify(save_as, artist_name, song_title, directory='', skip_exist=True):
    """ Get the preview audio file (I only see mp3 so far) from Spotify with given
        artist name and song name. 
        Save the file as $save_as.mp3
        :param save_as filename to save at local (no extention)
    """
    print "-"*80
    print "Want:", song_title, "-", artist_name

    save_file = os.path.join(directory, save_as + ".mp3")
    if skip_exist and os.path.isfile(save_file):
        print "File existed already."
        return True

    # Get a list of similar song titles
    try:
        base_url = "http://berry-music-cortex.appspot.com/api/search?"
        query_param = {"type":"track","q":song_title}
        url = base_url + urllib.urlencode(query_param)
        response = urllib2.urlopen(url)
        data = json.load(response)
        for item in data["tracks"]["items"]:
            # Exact match the artist name to make sure it's the intended songs
            # The song title is allowed to be a bit fuzzy
            if  item["artists"][0]["name"] == artist_name:
                print "Found:", item["name"]
                if "preview_url" in item:
                    preview_url = item["preview_url"]
                    with io.open(save_file, 'wb') as fp:
                        preview = urllib2.urlopen(preview_url)
                        fp.write(preview.read())
                    return True
                else:
                    print "No Preview"
                    return False
    except Exception:
        pass

    print "Not found"
    return False


def download_per_song(unique_tracks_file, directory):
    """ Download one audio file per unique song name (de-duplicate tracks)
    """
    # De-duplicate song titles from the file
    unique_songs = dict()
    with io.open(unique_tracks_file, 'r') as fp:
        for line in fp:
            contents = line.rstrip('\n').split("<SEP>")
            song_ID = contents[1]
            artist_name = contents[2]
            song_title = contents[3]
            if song_ID not in unique_songs:
                unique_songs[song_ID] = (artist_name, song_title)

    print "# Unique songs:", len(unique_songs)

    for key in unique_songs:
        value = unique_songs[key]
        artist_name = value[0]
        song_title = value[1]
        download_spotify(key, artist_name, song_title, directory)



subset_tracks_file = "subset_unique_tracks.txt"

download_per_song(subset_tracks_file, "download");
