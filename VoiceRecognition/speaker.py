import numpy as np
from sklearn import preprocessing
import python_speech_features
import sys
import os
import pickle
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture
import warnings


warnings.filterwarnings('ignore')

class Denoise:
    """
    denoises the input voice signal using frequency component anlysis
    """
    def __init__(self, inData = None, keep_fraction = 0.3):
        self.data = inData
        self.keep_fraction = keep_fraction

    def fftdenoise(self):
        """
        The function transfroms the time domain signal to a frequency domain and retains a fraction of  frequency                           		specified.Returns the denoised time domain signal.
        Parameters:
        :exclude_fraction the fraction of frequency to be excluded 
        Return Value: return np.uint16 value of the time domain signal
        """
        s = np.fft.fft(self.data)
        m = np.mean(s)

        exclude = 0.01
        im_fft2 = s
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
        

        rate, audio = read(self.source + file)
        denoise = Denoise(inData = audio, keep_fraction = 0.3)
        audio = denoise.fftdenoise()
 
        mfcc = MFCC()
        mfcc_feature = mfcc.mfcc_features(audio, rate)
        features = mfcc_feature

        os.remove(self.source + file)
        return features
        
    def add_speaker(self, name):
        """
        Adds a new speaker's voice model
        Parameters:
        :name: The name of the speaker
        """

        try:
            gmm = GaussianMixture(n_components = 6, max_iter = 200, covariance_type = 'diag', warm_start = True)
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
            return 'Added ' + name

        except:
            return 'Could not add ' + name
            
    def update_speaker(self, name):#, components = False):
        """
        Updates an existing speaker's voice model
        Parameters:
        :name: The name of the speaker
        :components: Boolean value to change the n_components of a speaker's voice model, default False
        """

        try:
            file = os.listdir(self.source)[0]
            self.features = self.get_features(file)
                
            model = pickle.load(open(self.models, 'rb'))
            gmm = model[name]

            #if components:
            #    gmm.n_components += 1

            gmm.fit(self.features)
    
            model[name] = gmm
            pickle.dump(model, open(self.models, 'wb'))
            return 'Updated ' + name

        except:
            return 'Could not update ' + name

    def remove_speaker(self, name):
        """
        Removes an existing speaker's voice model
        Parameters:
        :name: The name of the speaker
        """
        try:
            model = pickle.load(open(self.models, 'rb'))
            _ = model.pop(name)
            print(model.keys())

            if len(model.keys()) == 0:
                os.remove(self.models)
            else:
                pickle.dump(model, open(self.models, 'wb'))
            return 'Removed ' + name

        except:
            return 'Could not remove ' + name


if __name__ == '__main__':
    speaker = Speakers()
    choice = int(sys.argv[2])

    if choice == 1:
        speaker.add_speaker(sys.argv[1])
    elif choice == 2:
        speaker.update_speaker(sys.argv[1])
    else:
        speaker.remove_speaker(sys.argv[1])
