import numpy as np
import os.path
import scipy.io as sio
from obtain_name import *

'''
   :
   :
   :
   :Author: Chris Hu
'''
index_file = '/home/chrishu/music_cortex/cnn/index_file.txt'
song_dir = '/home/share/MillionSongSubset/download/'

#get existing list and echonest list
name_list = obtain_mp3_name(song_dir)
song_dict = obtain_exist_song_ID(index_file)
match_dict = {}
match_name = []
match_index = []

for name in name_list:
    if name in song_dict.keys():
        match_dict.update({name:int(song_dict[name])})
        match_name.append(name)
        match_index.append(int(song_dict[name]))

#print match_dict
#print len(match_dict)
sio.savemat('match_dict',match_dict)
sio.savemat('match_index',{'index':match_index})
sio.savemat('match_name',{'name':match_name})
