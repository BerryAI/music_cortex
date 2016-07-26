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

num_el = len(match_name['name'])

cnn_features = np.zeros((num_el,1,128,999))

for i in range(num_el):
    infile = os.path.join(input_dir,match_name['name'][i]+'.mat')
    features = sio.loadmat(infile)
    cnn_features[i, 0, :, :] = features['x'][:, :999]
    print i

sio.savemat('cnn_features',{'cnn_features':cnn_features})
