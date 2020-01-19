import numpy as np
import math
import os
import pickle
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture
from sklearn import preprocessing
from sklearn.utils.extmath import softmax
from mfcc import MFCC
import warnings
import time


warnings.filterwarnings('ignore')


class Identify:
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
    speaker = Identify()
    speaker.identify_speaker()
