import io
import urllib
import urllib2
import json
from os import listdir

def obtain_mp3_name(filepath):
    '''use os.dirlist() to read all mp3 file names
       :param filename: filename of the song preview file
       :return name_list: all mp3 file name
       :rtype: list
       :Author: Chris Hu
    '''
    #read all file names in list m
    #filepath='/home/share/MillionSongSubset/download/'
    filename_list = listdir(filepath)
    name_list = []
    
    #check last 3 char to ensure mp3 files
    for filename in filename_list:
        if filename[-3:]=='mp3':
            name_list.append(filename[:-4])#add into list if mp3 file
            
    return name_list

def obtain_exist_song_ID(index_file):
    '''read all existing song ID
       :param filename: filename of the song preview file
       :return song_list: all existing song ID & row numbers
       :rtype: dict
       :Author: Chris Hu
    '''
    #
    song_list = {}
    
    with io.open(index_file, 'r') as fp:
        for line in fp:
            contents = line.rstrip('\n').split("<SEP>")
            song_num = contents[0]
            song_ID = contents[3]
            song_list.update({contents[3]:contents[0]})
    return song_list
