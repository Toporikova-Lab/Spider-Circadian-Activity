# Spider Run Simulation

The goal is to be able to simulate an artificial spider's movements. Our first objective is to find run duration, which we define as a bout of uninterrupted movement. That is, when a spider moves with no stopping for a period of time. We then find the distribution of these run durations to visualize the counts of various run duration lengths using a histogram. 

## Table of Contents

- [Required Files](https://github.com/Toporikova-Lab/Spider-Circadian-Activity/blob/main/Spider%20runs%20simulation/README.md#required-files)
- [Calculating Spider Run Duration](https://github.com/Toporikova-Lab/Spider-Circadian-Activity/blob/main/Spider%20runs%20simulation/README.md#calculating-spider-run-duration)
- [Resampling Data](https://github.com/Toporikova-Lab/Spider-Circadian-Activity/blob/main/Spider%20runs%20simulation/README.md#resampling-data)
- [Creating Normalized Histograms](https://github.com/Toporikova-Lab/Spider-Circadian-Activity/blob/main/Spider%20runs%20simulation/README.md#creating-normalized-histograms)

## Required Files

- A .csv file of your data with columns for every spider labeled s1, s2, s3... etc. 
- Rows are times and dates when data is recorded. 
- Cells are filled with the number of times the spider moved by crossing an infrared beam. 
- Must contain a column with DateTime-like values for each datapoint in the style YYYY-MM-DD hh:mm:ss OR DateTime values of type pandas._libs.tslibs.timestamps.Timestamp. 
Below is an example of how the .csv file could look like:

<img width="494" alt="Screen Shot 2022-07-22 at 10 16 07 AM" src="https://user-images.githubusercontent.com/67922568/180458344-f9b3f88d-b477-416b-aa1e-5417a946537f.png">

All Python code is written in Jupyter Notebook. To install:
  1. Navigate to the [Anaconda website](https://www.anaconda.com/products/distribution)
  2. Download the correct distribution for your operating system
  3. Once downloaded, select Anaconda Navigator in your applications folder
  4. Select launch under the Jupyter Notebook symbol
  
All files must be placed in the same folder/subfolder as the Jupyter Notebook document

## Calculating Spider Run Duration

<img width="176" alt="Screen Shot 2022-07-22 at 10 13 21 AM" src="https://user-images.githubusercontent.com/67922568/180457786-8d81a053-c50f-40f2-90b2-d4c60d172dbf.png">

To calculate how long a spider has been moving, we binarized the data and found the start and end indices of movement. By subtracting the start and end indices, we can get the duration of uninterrupted run. This new data is made into a new .csv file.

We have also resampled the data by finding the sum of every two rows and making that a new .csv file.

<img width="157" alt="Screen Shot 2022-07-22 at 10 04 33 AM" src="https://user-images.githubusercontent.com/67922568/180456106-624c9501-5d8b-4062-8b18-93e777452920.png">

Using this new file, we have also ran the same run duration code to investigate if there was any change in the distribution of run durations from resampling.

## Creating Normalized Histograms

Using run duration data and resampled run duration data, we created a histogram to visualize the distribution.

<img width="573" alt="Screen Shot 2022-07-22 at 10 31 49 AM" src="https://user-images.githubusercontent.com/67922568/180461554-91dda34d-6656-43cb-908a-ad1282487db5.png">

We also normalized both histograms to compare if the distributions differed after resampling.

<img width="573" alt="Screen Shot 2022-07-22 at 10 32 19 AM" src="https://user-images.githubusercontent.com/67922568/180461677-1df6f653-d6a3-40ef-abd4-d8b371fc5512.png">
