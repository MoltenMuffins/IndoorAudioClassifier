# Indoor Audio Classifier

The goal of this project is to create an indoor sound classifier for the following classes: Speech, Music, Water, Door Sounds, Car Horn, Glass Breaking. The model trained will then be loaded onto an arudino module to provided realtime sound classification.

<mark>Work-in-progress</mark>

**Approaches used:**

**Questions to solve:**
* Does the sampling rate of the sound dataset matter? Google AudioSet (Features extracted at 1Hz) vs self collated dataset via FreeSound API (44.1 kHz)
* Which approach is best given that the model has to fit on the limited space in the arduino module?
* Audio recognition speed.
