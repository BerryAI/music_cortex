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
match_file = '/home/chrishu/music_cortex/cnn/match_index.mat'
mat_file = '/home/chrishu/music_cortex/cnn/log/filter160802022951.mat'
output_file = '/home/chrishu/music_cortex/cnn/log/top.txt'

data = sio.loadmat(mat_file)
index = sio.loadmat(match_file)
output = io.open(output_file, "w", encoding='utf-8')

track_dict = dict()

with io.open(index_file, 'r') as fp:
    for line in fp:
        contents = line.rstrip('\n').split("<SEP>")
        song_num = contents[0]
        track_info = "<Artist>" + contents[1] + "<Name>" + contents[2]
        track_dict[contents[0]] = track_info
print track_dict
counter = 1
for i in range(32):
    response = data['x'][:,i].tolist()
    toplist = [response.index(i) for i in sorted(response, reverse=True)][:10]
    output.write(u"Filter #%d:\n" % counter)
    counter += 1
    for k in toplist:
        a = index['index'][0,k]
        print a
        output.write(track_dict[str(a)]+'\n')

output.close()
    
