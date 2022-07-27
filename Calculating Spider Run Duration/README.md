# Spider Run Simulation

The objective is to find run duration, which we define as a bout of uninterrupted movement; that is, when a spider moves with no stopping for a period of time. We then find the distribution of these run durations to visualize the counts of various run duration lengths using a histogram. 

<img width="384" alt="Screen Shot 2022-07-27 at 12 01 58 PM" src="https://user-images.githubusercontent.com/67922568/181294762-613a510b-e7d1-492c-af42-9d28a808b365.png">
The red box represents run duration.

## Table of Contents

- [Required Files](https://github.com/Toporikova-Lab/Spider-Circadian-Activity/tree/main/Calculating%20Spider%20Run%20Duration#required-files)
- [Calculating Spider Run Duration](https://github.com/Toporikova-Lab/Spider-Circadian-Activity/tree/main/Calculating%20Spider%20Run%20Duration#calculating-spider-run-duration)
- [Creating Normalized Histograms](https://github.com/Toporikova-Lab/Spider-Circadian-Activity/tree/main/Calculating%20Spider%20Run%20Duration#creating-normalized-histograms)
- [Usage](https://github.com/Toporikova-Lab/Spider-Circadian-Activity/tree/main/Calculating%20Spider%20Run%20Duration#usage)

## Required Files

- A .csv file of your data with columns for every spider labeled s1, s2, s3... etc. 
- Rows are times and dates when data is recorded. 
- Cells are filled with the number of times the spider moved by crossing an infrared beam. 
- Must contain a column with DateTime-like values for each datapoint in the style YYYY-MM-DD hh:mm:ss OR DateTime values of type pandas._libs.tslibs.timestamps.Timestamp. 

Below is an example of what the .csv file could look like:

<img width="475" alt="Screen Shot 2022-07-22 at 1 30 36 PM" src="https://user-images.githubusercontent.com/67922568/180493070-9f2ec4d8-cb4a-4343-9b69-ad7d9dd147c3.png">

All Python code is written in Jupyter Notebook. To install:
  1. Navigate to the [Anaconda website](https://www.anaconda.com/products/distribution)
  2. Download the correct distribution for your operating system
  3. Once downloaded, select Anaconda Navigator in your applications folder
  4. Select launch under the Jupyter Notebook symbol
  
All files must be placed in the same folder/subfolder as the Jupyter Notebook document

## Calculating Spider Run Duration

To calculate how long a spider has been moving, we binarized the data and found the start and end indices of movement. By subtracting the start and end indices, we can get the duration of uninterrupted run. This new data is made into a new .csv file.

<img width="176" alt="Screen Shot 2022-07-22 at 10 13 21 AM" src="https://user-images.githubusercontent.com/67922568/180457786-8d81a053-c50f-40f2-90b2-d4c60d172dbf.png">



## Creating Normalized Histograms

Using run duration data and resampled run duration data, we created a histogram to visualize the distribution. The histograms were normalized, meaning that the area under the histogram is equal to 1 and the frequencies of run duration counts are relative to each other. 

<img width="221" alt="Screen Shot 2022-07-25 at 9 21 59 AM" src="https://user-images.githubusercontent.com/67922568/180787371-933d4aee-5a3a-4978-b6c5-8894177c4863.png">

## Usage

For those who want to visualize and investigate the duration of movement through histograms.
