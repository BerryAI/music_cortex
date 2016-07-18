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
feature_dir = '/home/share/MillionSongSubset/features/'
output_dir = '/home/chrishu/MSD/'
#get existing list and echonest list
name_list = obtain_mp3_name(song_dir)
song_dict = obtain_exist_song_ID(index_file)
match_dict = {}
i= 0

for name in name_list:
    if name in song_dict.keys():
        data = sio.loadmat(os.path.join(feature_dir, name+'.mat'))
        outfile = os.path.join(output_dir,name+'.mat')
        if True or not os.path.isfile(outfile):
            sio.savemat(outfile,data)
            print i
            i+=1


