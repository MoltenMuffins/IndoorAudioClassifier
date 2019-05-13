# Indoor Audio Classifier for EDGE-X + SCALE @ NTU
## 1. Problem Case
For this EDGE-X deep learning project, the task assigned was to create and train a machine learning model to classify sound input within the context of an indoor setting.

This was part of an overarching project where a microphone placed in a location would utilise a real-time machine learning inference engine to classify input audio and raise an alert for certain target classes. Instructions would then be sent to a camera to point at and zoom in on the direction of the sounds of interest for further validation. 

As such, the following classes were highlighted for training and testing the machine learning model: speech, music, water running, door sounds, car horn, glass breaking. A dataset for the aforementioned classes would be generated from various sources as well for which to train the model on.

This project lasted about 11 weeks, from October to January and concluded with two presentations, one to the team at Singtel Cognitive and Artificial Intelligence Lab for Enterprises (SCALE @ NTU), and one to the Career Affairs Office Team that organized this project.

## 2. Proposed Solution
### Dataset Generation
According to the project briefing, the requirements for the sound data set are as follows:
Each sound file must consist of one distinct sound event and have the following file format - 44.1 kHz, PCM 16 bit, Mono, with constant sampling rate. There should also be ideally 10 minutes of worth of sound data for each class.

Several websites offering open source sound databases were highlighted during the project briefing, however it was found that navigating the different websites to individually download sound files was extremely time consuming and tenuous. Furthermore, not all sounds that met the search criteria could be immediately used and some had to be cut up into smaller clips containing each distinct sound event. It was found that Freesound.org has an API in Python for querying and downloading audio files.

A script in Python `query_sound_download.py` was written to send a query to the Freesound server via API which would then return a list of audio files that matched a query. The script then iterated through the list, sending a request to retrieve the files. 

The Freesound API requires OAuth2 authentication in order to download 44.1kHz sound files (otherwise the files would be a low resolution sample file used for previewing the sound file on their website). A second script `get_access_token.py`was written to pass the following keys: client_id, client_secret  to the Freesound server, which then required the user to log into the Freesound website to authorise the use of the client. An access token would be obtained which only had one use. This access token was then submitted to the Freesound server once again, finally producing an OAuth2 token which was valid for 24 hours and had a limit of 2000 requests per day (ie. 2000 downloads a day).

Using these scripts, a raw database of about 1.6GB for the six classes was generated, consisting about 200mb worth of sound files per each class. Less files for the car horn, door and glass breaking classes that met our requirements were available, and hence the number of files downloaded for the music, speech and door classes were suppressed to try to keep the dataset balanced. 

As some of the sound files were exceedingly long, or contained more than one sound event per file, a third script `split_audio_files.py` was written. This script parses the file using the Auditok and PyDub and SoundFile Python libraries, converts the files to mono channel audio and splits up the sound files into smaller clips (illustrated below) based on several parameters that are user defined such as minimum audio event length, maximum audio event length, maximum silence duration and silence threshold. For our classes, it was found that the following values gave the best results:

```
minimum audio event length = 500
maximum audio event length = 4000
maximum silence duration = 100
silence threshold = 50
```

[image:6FBEDB5C-2DA1-478F-8ECB-49FF14DFE6FB-20451-0000F6BE23BC96BD/AD24AA96-C4FE-4E0D-A0DA-6037ACB5D5A9.png]

As a result of the sound splitting, much of the dataset was truncated, leaving us with 263mb of data for all six classes. In particular, the car horn class suffered the most with 17.4mb of usable data left after processing.

The creation of the scripts and mainly studying the mechanisms of the Freesound API took about two months with gaps in the working progress due to examinations and submissions for school.

### Approach for Model Building
The following models were researched and tested over the span of the remaining month of the project:
* Basic Neural Network 
* VGG16
* Transfer Learning on InceptionV3 with Imagenet weights
* Transfer Learning on VGG16 with Imagenet weights
* Transfer Learning VGGish (VGG16 slightly modified for audio input)

In particular, the transfer learning approaches were of interest given the relatively small dataset we had to work with.

## 3. Techniques or Pre-processing Algorithms used
As the database consisted of audio files of varying length, they were preprocessed spectrograms of 64 by 32. This method of preprocessing was chosen because of the intention of utilising transfer learning on models trained on the Imagenet dataset.  A working theory was that the lower level embeddings generated by the image recognition models would be useful in identifying the spectrogram shapes, eliminating the need for manual feature engineering via MFCCs. 

A script `audio_to_stamp_img.py` was written to process the sound files into .png images which are called stamps within the context of the project  as the small images produced resemble stamps.

[image:F5D4F831-DA88-4C14-BCB8-53D17711CB6B-20451-0000F83CD3B2D871/glass.png] [image:6F10AC5A-3A61-4279-BC54-D7B7FB3E5CC0-20451-0000F83ED0DB9C64/horn.png] [image:F861D1E9-1E94-4047-BB42-4CBEC75A9BA4-20451-0000F841702C70A2/music.png] [image:6E21ADFE-722C-4E5D-846B-825DDAA8D2ED-20451-0000F8439618F3DF/door.png] [image:032BDF95-A226-494B-AC9E-E609A6D33D58-20451-0000F84536F1F870/water.png] 
These stamps were then placed in folders according to their classes.

## 4. Results
The dataset was uploaded into Google Colabs and were shuffled into training and validation splits. Each Neural Net was trained for 5 epochs through the data before further action was taken.

The final accuracy of each network is as follows:
*VGGish is omitted as there were problems loading our custom dataset to train.*

> * **Basic Neural Network** `acc: 0.3365 - val_acc: 0.2781`
> * **VGG16** `acc: 0.8900 - val_acc: 0.5809`
> * **Transfer Learning on InceptionV3 with Imagenet weights** `acc 0.2064 - val_acc: 0.2017`
> * **Transfer Learning on VGG16 with Imagenet weights** `acc: 0.2603 - val_acc: 0.2503`

As the VGG16 model with no weights seemed promising, it was trained further for 30 epochs.

> **VGG16** `loss: 0.0246 - acc: 0.9990 - val_loss: 1.7021 - val_acc: 0.6359`

However, despite the high accuracy reported by the model, it is likely overfitting given the disparity between the training accuracy and the validation accuracy. This is exemplified that adhoc testing of individual files gives results biased towards the music class.

The approach of converting sound files directly to images seems to not work well. Alternatively the dataset may not be clean enough for which to produce good results. Unfortunately due to the lack of time, I could not explore other options for the project.

## 5. Conclusion
The two main challenges encountered in the project can be attributed to the two main tasks in the project, namely the database creation and the model creation. As I am not someone well versed with the subject of programming, much time was spent trying to understand the tools at my disposal, much less put them to use in the way intended. Furthermore, the field of deep learning is extremely broad and this was my first foray into building neural networks. If more time was available to create a larger dataset or try other models, a better trained model could be obtained.
