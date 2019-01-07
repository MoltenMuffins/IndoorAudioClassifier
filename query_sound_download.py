#This file uses the freesound api to download sounds based on the results of a text search

import os
import sys
import json
import freesound as fs
import requests

#Enter what sounds you are searching for. The sounds will be downloaded in the appropriate folder
query='speech'

#enter access token obtained from 'get_access_token.py' as a string ie 'uicC99kzXG9rTwLdqASpY4Bk4OaIRa'
os.environ['FREESOUND_ACCESS_TOKEN'] = 'uicC99kzXG9rTwLdqASpY4Bk4OaIRa'
#This token lasts 24 hours, after which you would have to request a new token or use the refresh_token

access_token = os.getenv('FREESOUND_ACCESS_TOKEN', None)
if access_token is None:
    print("You need to set your ACCESS TOKEN as an evironment variable",)
    print("named FREESOUND_ACCESS_TOKEN")
    sys.exit(-1)

print(access_token)

path_name = os.path.join(os.getcwd(), 'Sound Library/Unsorted/'+query)
try:
    os.mkdir(path_name)
except:
    pass

freesound_client = fs.FreesoundClient()
freesound_client.set_token(access_token, "oauth")

#Results forms an array of filenames,ids and usernames of the sound files that match our query
sound_results_pager = freesound_client.text_search(query=query, fields="name,id,username,license", 
filter="samplerate:44100 type:wav bitdepth:16 channels:1")

print('The sound files will be downloaded in {}'.format(path_name))

#Issue 1: Couldn't get code to write filenames to text file for proper attribution
#f = open('freesoundsources.txt', 'a+')

#We use a while loop with for and if not to iterate through the pages of the results
while True:
    for sound in sound_results_pager:
        #We add .wav to the files that are incomplete (no filetype)
        if ".wav" not in sound.name:
            xtra=".wav"
        else:
            xtra= ""
            
        #We download the sound files stored in the results array
        sound.retrieve(path_name,sound.name+xtra)
        
        print("File:",sound.name, "ID:", sound.id, "by", sound.username, sound.license)
        #Issue 1: f.write('{} by {}, {}'.format(sound.id,sound.username,sound.license))

    if not sound_results_pager.next:
                break
    sound_results_pager = sound_results_pager.next_page()

print('Queries Expended')
#Issue 1: f.close()
        