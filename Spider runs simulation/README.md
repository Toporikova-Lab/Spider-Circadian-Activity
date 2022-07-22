# Spider Run Simulation

The goal is to be able to simulate a spider's movements. Our first objective 

## Table of Contents

- [Required Files](https://github.com/Toporikova-Lab/Spider-Circadian-Activity/blob/main/Spider%20runs%20simulation/README.md#required-files)
- [Calculating Spider Run Duration](https://github.com/Toporikova-Lab/Spider-Circadian-Activity/blob/main/Spider%20runs%20simulation/README.md#calculating-spider-run-duration)
- [Resampling Data](https://github.com/Toporikova-Lab/Spider-Circadian-Activity/blob/main/Spider%20runs%20simulation/README.md#resampling-data)
- [Creating Normalized Histograms](https://github.com/Toporikova-Lab/Spider-Circadian-Activity/blob/main/Spider%20runs%20simulation/README.md#creating-normalized-histograms)

## Required Files

A .csv file of your data with columns for every spider labeled s1, s2, s3... etc. Rows are times and dates when data is recorded. Cells are filled with the number of times the spider moved by crossing an infrared beam. 

All Python code is written in Jupyter Notebook. To install:
  1. Navigate to the [Anaconda website](https://www.anaconda.com/products/distribution)
  2. Download the correct distribution for your operating system
  3. Once downloaded, select Anaconda Navigator in your applications folder
  4. Select launch under the Jupyter Notebook symbol
  
All files must be placed in the same folder/subfolder as the Jupyter Notebook document

## Calculating Spider Run Duration

Binarized Data <img width="64" alt="Screen Shot 2022-07-22 at 9 40 59 AM" src="https://user-images.githubusercontent.com/67922568/180451473-83b735c4-d976-48b0-bd84-493bea6fb846.png"> Run Duration Data <img width="46" alt="Screen Shot 2022-07-22 at 9 33 59 AM" src="https://user-images.githubusercontent.com/67922568/180450129-7ec07599-ec4c-4765-899d-1c68f52f2bd5.png">

To calculate how long a spider has been moving, we binarized the data and found the start and end indices of movement. By subtracting the start and end indices, we can get the duration of uninterrupted run. This new data is made into a new .csv file.

## Creating Normalized Histograms
