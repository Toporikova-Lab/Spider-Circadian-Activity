# Spider Run Simulation

The goal is to be able to simulate a spider's movements.

## Table of Contents

- [Required Files](https://github.com/Toporikova-Lab/Spider-Circadian-Activity/blob/main/Spider%20runs%20simulation/README.md#required-files)
- [Calculating Spider Run Duration](https://github.com/Toporikova-Lab/Spider-Circadian-Activity/blob/main/Spider%20runs%20simulation/README.md#calculating-spider-run-duration)
- [Resampling Data](https://github.com/Toporikova-Lab/Spider-Circadian-Activity/blob/main/Spider%20runs%20simulation/README.md#resampling-data)
- [Creating Normalized Histograms](https://github.com/Toporikova-Lab/Spider-Circadian-Activity/blob/main/Spider%20runs%20simulation/README.md#creating-normalized-histograms)

## Required Files

A .csv file of your data with columns for every spider labeled s1, s2, s3... etc. Rows are times and dates when data is recorded. Cells are filled with the number of times the spider moved by crossing an infrared beam. 

All Python code is written in Jupyter Notebook.

## Calculating Spider Run Duration

To calculate how long a spider has been moving, we binarized the data and found the start and end indices of movement. By subtracting the start and end indices, we can get the duration of uninterrupted run. This new data is made into a new .csv file.

## Resampling Data

We also resampled the data by finding the sum of movements in 2 minute intervals. This was done to reduce "noise."

## Creating Normalized Histograms
