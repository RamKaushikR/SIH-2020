import numpy as np
import python_speech_features
import math
import os
import pickle
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture
from sklearn import preprocessing
from sklearn.utils.extmath import softmax
#from mfcc import MFCC
import warnings
import time


warnings.filterwarnings('ignore')


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


class Voice_Identify:
    """
    Creates an identify object, to identify a speaker from an audio sample
    Parameters:
    :source: The source path for the audio files, default identify/
    :models: The file where the speaker voice models are stored, default voice_models.dat
    """
    def __init__(self, source = 'identify/', models = 'voice_models.dat'):
        self.source = source
        self.gmm_model = pickle.load(open(models, 'rb'))
        self.models = list(self.gmm_model.values())
        self.speakers = list(self.gmm_model.keys())
    
        
    def identify_speaker(self):
        """
        Identifies a given speaker from an audio sample
        """
        files = os.listdir(self.source)
        
        for file in files:
            print(file)
            rate, audio = read(self.source + file)

            mfcc = MFCC()
            mfcc_feature = mfcc.mfcc_features(audio, rate)
            log = np.zeros(len(self.models))
            
            for i in range(len(self.models)):
                gmm = self.models[i]
                score = np.array(gmm.score(mfcc_feature))
                log[i] = score / len(mfcc_feature) #1 / (1 + math.exp(-1 * score / len(mfcc_feature)))
                
            #log = preprocessing.scale(log)
            #print(log)
            _ = np.argmax(log)
            os.remove(self.source + file)

            total = 0.0
            for i in log:
                total += (log[_] - i) ** 2
            total = math.sqrt(total) * len(self.speakers)

            print(self.speakers)
            print('Log: ', log)
            print('Total: ', total)

            if total > 0.5:
                speaker = self.speakers[_]
                return speaker#print('Speaker is ' + speaker + '\n')
            else:
                return 'Not found'#print('Speaker not found\n')


if __name__ == '__main__':
    speaker = Voice_Identify()
    speaker.identify_speaker()
