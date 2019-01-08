import os
from glob import glob
import soundfile as sf
import scipy
from scipy.misc import imsave
from scipy.misc import imresize
import numpy as np
import python_speech_features

sample_window_step = 0.01

#Specify foldername to iterate through
#car horn, door, glass break, music, speech, water
sndfdr='water'

#Change directory to folder of interest    
os.chdir("Sound Library/Train/"+sndfdr)

def get_sample_features(samples, sample_rate):
    features, energy = python_speech_features.fbank(samples, samplerate=sample_rate, 
                            winlen=0.025, winstep=sample_window_step, 
                            nfilt=32,nfft=512,
                            lowfreq=0,highfreq=None,preemph=0.25,
                            winfunc=lambda x:np.hamming( x ))
    return features, energy
    
def make_stamp(file):
    #Get original filename
    name = os.path.splitext(file)[0]
    samples, sample_rate = sf.read(file)

    sample_feat, energy = get_sample_features(samples, sample_rate)
    data = np.log(sample_feat)
    # Now normalize each vertical slice so that the minimum energy is ==0
    data_mins = np.min(data, axis=1)
    data_min0 = data - data_mins[:, np.newaxis]
    
    # Force the data into the 'stamp size' as an image (implicit range normalization occurs)
    stamp = scipy.misc.imresize(data_min0, (64, 32), 'bilinear') 
    imsave('{}.png'.format(name), stamp) 
    
    #Remove the original file to avoid confusion
    os.remove(file)

          
for file in list(glob('*.wav')):                                       
    print('processing', file)
    make_stamp(file) 

print('Done')