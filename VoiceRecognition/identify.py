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

class Denoise:
    """
    denoises the input voice signal using frequency component anlysis
    """
    def __init__(self, inData = None,keep_fraction = 0.3):
        self.data = inData
        self.keep_fraction = keep_fraction
    def fftdenoise(self):
        """
        The function transfroms the time domain signal to a frequency domain and retains a fraction of  frequency                           		specified.Returns the denoised time domain signal.
        Parameters:
        :exclude_fraction the fraction of frequency to be excluded 
        Return Value: return np.unit16 value of the time domain signal
        """
        s = np.fft.fft(self.data)
        m = np.mean(s)

        exclude = 0.01
        im_fft2 = s.copy()
        r = len(im_fft2)

        im_fft2[int(r * self.keep_fraction): int(r * (1 - self.keep_fraction))] = 0
        im_new = np.fft.ifft(im_fft2).real
        return np.int16(im_new)


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
    
        
    def identify_speaker(self, speaker):
        """
        Identifies a given speaker from an audio sample
        """
        try:
            files = os.listdir(self.source)

            for file in files:
                print(file)
                rate, audio = read(self.source + file)
                denoise = Denoise(inData = audio.copy(), keep_fraction = 0.3)
                audio = denoise.fftdenoise()

                mfcc = MFCC()
                mfcc_feature = mfcc.mfcc_features(audio, rate)
                log = np.zeros(len(self.models))

                
                def get_index(a,k):
                    p = 0
                    for i in range(len(a)):
                        if(a[i]==k):
                            return i
                    return -1
                
                for i in range(len(self.models)):
                    gmm = self.models[i]
                    score = np.array(gmm.score(mfcc_feature))
                    log[i] = score / len(mfcc_feature)

                #log = preprocessing.scale(log)
                os.remove(self.source + file)
                print('Log: ', log)
                log1 = np.sort(-1*log)
                max1 = -1*log1[0]
                max2 = -1*log1[1]
                #print(max1,max2)
                max1index = get_index(log,max1)
                max2index = get_index(log,max2)

                if speaker == self.speakers[max1index] or speaker == self.speakers[max2index]:
                    return 1
                return 0
                
                """
                _ = np.argmax(log)
                speaker_ = self.speakers[_]
                print('Log: ', log)
                """

                """
                total = 0.0
                for i in log:
                    total += (log[_] - i) ** 2
                total = math.sqrt(total) * len(self.speakers)

                print(self.speakers)
                print('Total: ', total)
                """
                """
                if log[_] > 1 and speaker == speaker_:
                    return 1
                return 0
                """

        except:
            return -1


if __name__ == '__main__':
    speaker = Voice_Identify()
    speaker.identify_speaker()
