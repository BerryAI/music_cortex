import librosa
import numpy as np
from extract_acoustic_feature import *
from obtain_mp3_name import *


'''extract features from 520 song previews
   :
   :
   :
   :Author: Chris Hu
'''
name_list = obtain_mp3_name('/home/share/MillionSongSubset/download/')
feature = []
for name in name_list:
    feature_temp = extract_acoustic_feature(name)
    feature.append(feature_temp)
    
#print feature
