import sksound as sound
import numpy as np
import os
from scipy.io.wavfile import write
import warnings


warnings.filterwarnings('ignore')

class Noise:
    def __init__(self, source = 'speaker/', dest = 'speaker/'):
        """
        Modifies the audio file by adding random noise and modifying the frequency
        Parameters:
        :source: The source directory from which the files must be read, default add_speakers/
        :dest: The destination directory to store the modified files, default add_speakers/
        """
        self.source = source
        self.dest = dest
        self.files = os.listdir(self.source)
        self.files.sort()
        self.count = 1
        
    def add_noise(self):
        """
        Adds the random noise to the audio files
        """
        for file in self.files:
            audio = sound.sounds.Sound(self.source + file)
            data = audio.data
            rate = audio.rate
            
            if self.count % 3 != 0:
                data = data + np.random.normal(0, 1, data.shape) * np.random.randint(30, 100)
                _ = np.random.randint(70, 110) // 80
                rate = rate * _
                
                write(self.dest + file, rate, data)
                
            self.count += 1
        
        print('Noise has been added to the audio samples')


if __name__ == '__main__':
    noise = Noise()
    noise.add_noise()
