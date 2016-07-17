import librosa
import numpy as np
import os.path
import scipy.io as sio
from extract_acoustic_feature import *
from obtain_name import *

'''extract features from all song previews
   :
   :
   :
   :Author: Chris Hu
'''
input_dir = '/home/share/MillionSongSubset/download/'
output_dir = '/home/share/MillionSongSubset/features/'
name_list = obtain_mp3_name(input_dir)
i = 1
for name in name_list:
    outfile = os.path.join(output_dir,name+'.mat')
    if True or not os.path.isfile(outfile):
    	feature = extract_acoustic_feature(os.path.join(input_dir, name+'.mp3'))
    	sio.savemat(outfile,{'x':feature})
    print i
    i+=1    
#print feature
