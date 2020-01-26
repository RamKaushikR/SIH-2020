import sksound.sounds as sk
import numpy as np
import matplotlib.pyplot as plt
import os
import scipy as sp
from scipy import fftpack
import warnings
import time


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
