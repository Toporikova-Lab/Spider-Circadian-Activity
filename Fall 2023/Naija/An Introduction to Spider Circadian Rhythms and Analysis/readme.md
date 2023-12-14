# An Introduction to Spider Circadian Rhythms and Analysis
## Fall 2023 Research Experience in the Toporikova Lab, Washington & Lee University
*Naija Barakat ('24), Neuroscience Department*

## About the Project
This semester I worked under Dr. Natalia Toporikova. Her lab's current focus is novel work involving measuring, analyzing, and understanding the circadian rhythms of spiders, namely *Parasteadoda*, common house spider, and *Steatoda*, false Black Widow. 

During my time in the lab, I: 
- learned about circadian rhythms of *Drosophilia melanogaster* and spiders, including current gaps in research
- learned how circadian research is conducted and data is produced
- completed first-pass processing and visualization of circadian rhythm data

## Background on Circadian Rhythms
A circadian rhythm is a biological cycle comprised of synchronized biochemical, physiological, and behavioral changes throughout a roughly 24-hour period. This cycle allows organisms with circadian rhythms to remain in sync with its environment and respond to environmental changes, such as temperature and light. Circadian rhythms are thought to be highly conserved and nearly ubiquitous across eukaryotes, demonstrative of the advantage circadian rhythms provide to the organism and its biological fitness. 
  
Despite the importance of biological synchronization with the environment, some species of spiders have been found to have much shorter circadian rhythms, as short as 18.7 h (Mah et al., 2020), while not suffering from any apparent losses in fitness or suitability to their environment. Research on spider circadian rhythms remains limited in number, leaving questions about mutability of typical length of the circadian clock and the plasticity of shorter or longer circadian clocks, unanswered. 

## Circadian Rhythm Research & Data
Circadian rhythms can be studied by analyizing biochemical changes, such as changes in gene expression or hormone levels, or by studying behavior. In behavioral examination of circadian rhythms, reproduction, feeding, social activities, or locomotion can be observed and analyzed to determine normal rhythms or how these behaviors can be entrained. Entrainment is synchronization of the endogenous circadian rhythm with environmental cues. In the Toporikova lab, the entrainment to red light of *Parasteadoda* and *Steatoda*, is studied through measuring locomotion. 

Locomotion data is collected using a Locomotor Activity Monitor (LAM). The spiders are placed in glass tubes by themselves and the tubes are inserted into the LAM array. The array sends infrared (IR) beams of light through the tubes and an data point is collected each time the IR beam is broken by the spider. The LAM monitor also collects data about the light conditions the spiders are in and record light presence in a simple binary, where 1 means light, and 0 means darkness. This set up allows data from multiple spiders, under the same light conditions to be collected at once.

![Locomotor Activity Monitor](https://github.com/Toporikova-Lab/Spider-Circadian-Activity/assets/148475054/d80e59d3-9c4b-4b12-a40f-9fd625dfd4dd)

*A Locomotor Activity Monitor by TriKinetics*

### Files and Materials Utilized
* Juypter Notebook, which can be installed by navigating to the [Anaconda website](https://www.anaconda.com/download)
* a .csv file with locomotor activity, with the following column in order
  1. date (YYYY-MM-DD) and time (hh:mm:ss) information,
  2. light data in a binary where: light = 1 and darkness = 0
  3. locomotor activity counts of a single spider is a spider
* ensure that .csv file is in same folder as the notebook you are working in
![Example .csv file structure](https://github.com/Toporikova-Lab/Spider-Circadian-Activity/blob/main/Fall%202023/Naija/An%20Introduction%20to%20Spider%20Circadian%20Rhythms%20and%20Analysis/2Capture.PNG)

### First-pass Processing
* Upload data into dataframe and clean by removing empty or unnecessary cells
* Convert date and time data to readable and manipulatable format using Python's datetime package
* Find average activity for each time point to analyze population of spider
* Create rolling frame to find rolling average - this smooths your data, limits the influence of outliers on the visualization, and helps you identify potential entrainment, cycles, or other features of note
  - the length of the rolling frame depends on your data, once you plot your data, you can experiment with the frame length

### Visualization of Average Activity Data
* Create plot (and subplot if analyzing more than one population)
* Plot rolling average date and light data on the same plot, in different colors
* Label axes
