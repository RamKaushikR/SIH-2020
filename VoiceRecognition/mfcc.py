import numpy as np
from sklearn import preprocessing
import python_speech_features


class MFCC:
    """
    Computes the MFCC and delta MFCC features for an audio sample
    """
    def __init__(self):
        self.mfcc = None
        self.delta_mfcc = None
        self.mfcc_feature = None
        
    def mfcc_features(self, audio, rate, numcep = 20, nfft = 2000, N = 2):
        """
        Returns the MFCC and delta MFCC features of the given audio, stacked together horizontally
        Parameters:
        :audio: The audio file for which MFCC features must be computed
        :rate: The sample rate of the audio file
        :numcep: The number of cepstrum to return, default 20
        :nfft: The FFT size, default 2000
        :N: Calculate delta features based on preceding and following N frames, default 2
        Return Value: A numpy array which has the scaled MFCC and delta MFCC features, stacked horizontally
        """
        self.mfcc = python_speech_features.mfcc(audio, rate, numcep = numcep, nfft = nfft)
        #self.mfcc = preprocessing.scale(self.mfcc)
        
        self.delta_mfcc = python_speech_features.delta(self.mfcc, N)
        
        self.mfcc_feature = np.hstack((self.mfcc, self.delta_mfcc))
        
        return self.mfcc_feature
