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

input_dir = '/home/chrishu/MSD/'

#match_index = sio.loadmat('match_index.mat')
match_name = sio.loadmat('match_name.mat')

num_el = np.shape(match_name['name'])[1]


cnn_features = np.zeros((num_el,128,1294))



for i in range(num_el):
    infile = os.path.join(input_dir,match_name['name'][i]+'.mat')
    features = sio.loadmat(infile)
    cnn_features[i, :, :] = features['x']
    print i

sio.savemat('cnn_features',{'cnn_feature':cnn_features})
