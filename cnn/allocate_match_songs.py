import librosa
import numpy as np
import os.path
import scipy.io as sio
from extract_acoustic_feature import *
from obtain_name import *

'''
   :
   :
   :
   :Author: Chris Hu
'''
index_file = '/home/chrishu/music_cortex/cnn/index_file.txt'
input_dir = '/home/share/MillionSongSubset/download/'
output_dir = '/home/share/MillionSongSubset/features/'
#get existing list and echonest list
name_list = obtain_mp3_name(input_dir)
song_dict = obtain_exist_song_ID(index_file)

#name_dict = dict(zip(name_list,name_list))

for name in name_list:
    if name in song_dict.keys():
        print song_dict[key]
