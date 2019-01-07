import os
from glob import glob
from auditok import ADSFactory, AudioEnergyValidator, StreamTokenizer, player_for, dataset
from pydub import AudioSegment
import soundfile as sf


#This code uses sound file to check if audio duration min 3s, 
#else uses pydub convert wav files to mono, 
#auditok to identify regions of interest in a sound file and 
#pydub again to split them into separate wav files in a specified subdirectory
#Both libraries are based on miliseconds
#Finally the source audio file is deleted.

#Specify foldername to iterate through
#car horn, door, glass break, music, speech, water
sndfdr='car horn'

#Change directory to folder of interest    
os.chdir("Sound Library/Clipped/"+sndfdr)

def read_split_dir(file):
     f = sf.SoundFile(file)
     #duration of file in seconds
     duration = len(f) / f.samplerate
     
     if duration <= 4:
          print(file, 'untouched')
     else:
          #Get original filename
          name = os.path.splitext(file)[0]

          tempsound = AudioSegment.from_wav(file)
          tempsound = tempsound.set_channels(1)
          tempsound.export('0wavtmp_'+file, format="wav")
          tmpfile = '0wavtmp_'+file


          # We set the `record` argument to True so that we can rewind the source
          asource = ADSFactory.ads(filename=tmpfile, record=True)

          validator = AudioEnergyValidator(sample_width=asource.get_sample_width(), energy_threshold=50)

          # Default analysis window is 10 ms (float(asource.get_block_size()) / asource.get_sampling_rate())
          # min_length=20 : minimum length of a valid audio activity is 20 * 10 == 200 ms
          # max_length=4000 :  maximum length of a valid audio activity is 400 * 10 == 4000 ms == 4 seconds
          # max_continuous_silence=30 : maximum length of a tolerated  silence within a valid audio activity is 30 * 30 == 300 ms
          tokenizer = StreamTokenizer(validator=validator, min_length=500, max_length=4000, max_continuous_silence=100)

          asource.open()
          tokens = tokenizer.tokenize(asource)
        

          for index,t in enumerate(tokens):
               #print("Token starts at {0} and ends at {1}".format(t[1], t[2]))
               newAudio = AudioSegment.from_wav(file)
               newAudio = newAudio[t[1]:t[2]] 
               
               chunk_name = "{}_clip{}.wav".format(name,index)
               print("Generating", chunk_name)
               newAudio.export(chunk_name, format="wav") #Exports to a wav file in the current path.
          
          #Remove the temporary file we made earlier
          os.remove(tmpfile)
          #Remove the original file to avoid confusion
          os.remove(file)

          
for file in list(glob('*.wav')):                                       
     print('processing', file)
     try: 
          read_split_dir(file) 
     except:
          pass

print('Done')