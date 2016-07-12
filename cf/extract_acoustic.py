import librosa
import numpy as np

def extract_acoustic(input_file,number_mels=128,frequency_max=8000):
    """ Load the music file
        Extract Mel Frequency Cepstrum Coefficient
        :
    """
    #load music from librosa example
    try:
        y,sr = librosa.load(input_file)
    except:
        print("File loading error")
        return 0

    #feature extraction(mfcc)
    librosa.feature.mfcc(y=y, sr=sr)

    #log-power Mel spectrogram
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
    feature = librosa.feature.mfcc(S=librosa.logamplitude(S))

    return feature
