import numpy as np
from sklearn import preprocessing
import python_speech_features
import sys
import os
import pickle
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture
import warnings
from Denoiser import Denoiser as denoise

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


class Speakers:
    """
    Creates a speakers object, to add and update speaker models
    Parameters:
    :source: The source path for the audio files, default speakers/
    :models: The file where the speaker voice models are stored, default voice_models.dat
    """
    def __init__(self, source = 'speakers/', models = 'voice_models.dat'):
        self.source = source
        self.models = models
        self.features = np.asarray(())
        
    def get_features(self, file):
        """
        Computes the MFCC features
        Return Value: A numpy array containing the features
        """
        features = np.asarray(())
        
        print('GET FEATURES ' + file)
        rate, audio = read(self.source + file)
        rmnoise = denoise(inData = audio.copy(), keep_fraction = 0.3)
        audio = rmnoise.fftdenoise()   
        mfcc = MFCC()
        mfcc_feature = mfcc.mfcc_features(audio, rate)
        features = mfcc_feature
        try:
            os.remove(self.source + file)
        except:
            pass
            
        return features
        
    def add_speaker(self, name):
        """
        Adds a new speaker's voice model
        Parameters:
        :name: The name of the speaker
        """
                
        gmm = GaussianMixture(n_components = 6, max_iter = 200, covariance_type = 'diag', n_init = 3)
        files = os.listdir(self.source)
        files.sort()
        
        for file in files:
            self.features = self.get_features(file)
            gmm.fit(self.features)

        if self.models in os.listdir('./'):
            model = pickle.load(open(self.models, 'rb'))
        else:
            model = {}

        model[name] = gmm
        pickle.dump(model, open(self.models, 'wb'))
        print('Model developed for ' + name)
            
    def update_speaker(self, name):#, components = False):
        """
        Updates an existing speaker's voice model
        Parameters:
        :name: The name of the speaker
        :components: Boolean value to change the n_components of a speaker's voice model, default False
        """
        file = os.listdir(self.source)[0]
        self.features = self.get_features(file)
                
        model = pickle.load(open(self.models, 'rb'))
        gmm = model[name]

        #if components:
        #    gmm.n_components += 1

        gmm.fit(self.features)
        
        model[name] = gmm
        pickle.dump(model, open(self.models, 'wb'))
        print('Model updated for ' + name)

    def remove_speaker(self, name):
        """
        Removes an existing speaker's voice model
        Parameters:
        :name: The name of the speaker
        """
        model = pickle.load(open(self.models, 'rb'))
        _ = model.pop(name)

        print('Removed ' + name)

        pickle.dump(model, open(self.models, 'wb'))


if __name__ == '__main__':
    speaker = Speakers()
    choice = int(sys.argv[2])

    if choice == 1:
        speaker.add_speaker(sys.argv[1])
    elif choice == 2:
        speaker.update_speaker(sys.argv[1])
    else:
        speaker.remove_speaker(sys.argv[1])
