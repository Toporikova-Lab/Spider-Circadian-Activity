# Analysis of Circadian Rhythm in Spiders through Activity Onset
<p align="center">
  <img src="https://user-images.githubusercontent.com/106093318/180052222-47c1f831-58cb-4902-8a60-eb0a2b15ef9b.png" width="600" height="400" />
</p>
<p align = "center">
<em>Gasteracantha cancriformis</em>
</p>


## About My Project
  In this project, I aim to analyze the average onset of activity every night for multiple days across multiple spiders. Because previous research has shown a difference in free running period (FRP) across species, I was interested in analyzing if the same holds true for mean activity onset. We hypothesized that a species with a longer FRP would not be as ready to move when lights turn off as a spider with a short FRP, and therefore long FRP spiders would generally have a longer mean activity onset. 

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#Installation">Installation</a></li>
    <li><a href="#Getting-Started">Getting Started</a></li>
    <li><a href="#Usage">Usage</a></li>
    <li><a href="#Acknowledgements">Acknowledgements</a></li>
</details>

## Installation <a name="Installation"></a>
##### Installing Jupyter Notebook
  1. Navigate to the [Anaconda website](https://www.anaconda.com/products/distribution)
  2. Download the correct distribution for your operating system
  3. Once downloaded, select Anaconda Navigator in your applications folder
  4. Select launch under the Jupyter Notebook symbol
  
##### Using my Jupyter Notebook
  1. Download the Calculating Activity Onset Final Code file
  2. Upload it to your Jupyter Notebook
 
## Getting Started <a name="Getting_Started"></a>
##### Necessary Files
  1. A file containing activity data in light/dark conditions over multiple days
  2. File specifications:
  *    Must be in .csv format
  *    Must contain a light column in binary (Ex: 1 = Lights on, 0 = Lights off)
  *    Must contain a column with DateTime-like values for each datapoint in the style YYYY-MM-DD hh:mm:ss OR DateTime values of type pandas._libs.tslibs.timestamps.Timestamp
  *    Must contain only datetime, light, and activity columns.
  
  3. This file must be placed in the same folder/subfolder as the Jupyter Notebook document
  
  The file should look something like this:
<img width="1122" alt="Screen Shot 2022-07-19 at 2 22 14 PM" src="https://user-images.githubusercontent.com/106093318/179821764-3ffdfc18-f075-4c28-99bd-7f905280f6cb.png">

## Usage <a name="Usage"></a>

## Acknowledgements <a name="Acknowledgements"></a>
