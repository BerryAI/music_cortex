from os import listdir

def obtain_mp3_name(filepath):
    '''use os.dirlist() to read all mp3 file names
       :param filename: filename of the song preview file
       :return namelist: all mp3 file name
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
