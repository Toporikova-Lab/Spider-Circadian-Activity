# Analysis of Circadian Rhythm in Spiders through Activity Onset
<p align="center">
  <img src="https://user-images.githubusercontent.com/106093318/180052222-47c1f831-58cb-4902-8a60-eb0a2b15ef9b.png" width="600" height="400" />
</p>
<p align = "center">
<em>Gasteracantha cancriformis</em>
</p>


## About My Project
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;While most organisms have internal clocks of around 24 hours to match the earth's day, spiders have been shown to have internal clocks that are anywhere from 15 to 30 hours. Because it has previously been shown that a clock that greatly differs from 24 hours can reduce an organism's fitness, it is our lab's intent to investigate how spiders are able to survive on earth. With the overarching goal of creating a model of spider activity to possibly tease out the biological mechanisms allowing altered clock spiders to thrive, I aim to determine the average time each species starts activity at night as an aspect of this model.
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In this project, I aim to analyze the average onset of activity every night for multiple days across multiple spiders. I define "activity onset" as being the first time each night where the mean of the individual's nightly activity is crossed. An example of a graph showing activity onsets is shown below. 
 <img width="1074" alt="Screen Shot 2022-07-25 at 10 25 27 AM" src="https://user-images.githubusercontent.com/106093318/180800679-157eeca7-99e1-4c68-ac85-ec9b5e976b7d.png">
 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In the above figure, the red dotted line represents the calculated activity onset. The area shaded in red represents the data used to calculate the first activity onset. Hopefully, with these calculations, we will be able to see a relationship between spider species and activity onset, and eventually use this data to create a model of spider activity.


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
  1. A file containing activity data in 12:12 light/dark conditions over multiple days
  2. File specifications:
  *    Must be in .csv format
  *    Must contain a light column in binary (Ex: 1 = Lights on, 0 = Lights off)
  *    Must contain a column with DateTime-like values for each datapoint in the style YYYY-MM-DD hh:mm:ss OR DateTime values of type pandas._libs.tslibs.timestamps.Timestamp
  *    Must contain multiple columns of activity data, with each column representing a single spider.
  *    Must contain only datetime, light, and activity columns. Any other columns will cause problems with the code.
  
  3. This file must be placed in the same folder/subfolder as the Jupyter Notebook document
  
  The file should look something like this:
<img width="1383" alt="Screen Shot 2022-07-20 at 2 20 57 PM" src="https://user-images.githubusercontent.com/106093318/180054569-d18dfa13-ef5d-45f1-9d62-f47d0dfce9ad.png">

## Usage <a name="Usage"></a>
  Upon opening my jupyter notebook, you should see this at the top of the document.
<img width="1407" alt="Screen Shot 2022-07-25 at 10 35 05 AM" src="https://user-images.githubusercontent.com/106093318/180802838-b31bfc07-ce3f-4d21-ba5a-fbc2989f7801.png">
In the first code cell, replace 'Metazygia wittfeldae Monitor 1 Updated_LD' with the name of your file. You must remove the .csv extension from the name, as this is built into the code. Once you have changed the file name, run the first code cell.
  
  
## Acknowledgements <a name="Acknowledgements"></a>
