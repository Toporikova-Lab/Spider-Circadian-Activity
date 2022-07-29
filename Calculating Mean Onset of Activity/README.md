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
<img width="847" alt="Screen Shot 2022-07-25 at 2 18 20 PM" src="https://user-images.githubusercontent.com/106093318/180846535-4b73473b-af39-4061-80c7-1910995b4265.png">

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In the above figure, the red dotted line represents the calculated activity onset. The area shaded in red represents the data used to calculate the first activity onset. Hopefully, with these calculations, we will be able to see a relationship between spider species and activity onset, and eventually use this data to create a model of spider activity.
<br />
<br /> 

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#Installation">Installation</a></li>
    <li><a href="#Getting-Started">Getting Started</a></li>
    <li><a href="#Usage">Usage</a></li>
    <li><a href="#Acknowledgements">Acknowledgements</a></li>
</details>
<br />
<br /> 

## Installation <a name="Installation"></a>
##### Installing Jupyter Notebook
  1. Navigate to the [Anaconda website](https://www.anaconda.com/products/distribution)
  2. Download the correct distribution for your operating system
  3. Once downloaded, select Anaconda Navigator in your applications folder
  4. Select launch under the Jupyter Notebook symbol
  
##### Using my Jupyter Notebook
  1. Download the Calculating Activity Onset Final Code file
  2. Upload it to your Jupyter Notebook
 
## Getting Started <a name="Getting-Started"></a>
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
<p align="center">
  <img src="https://user-images.githubusercontent.com/106093318/180846913-342af985-f456-4099-9055-8fef7b78d23f.png" width="559" />
</p>


## Usage <a name="Usage"></a>

  
### To Begin:
  Upon opening my jupyter notebook, you should see this at the top of the document.
<img width="1389" alt="Screen Shot 2022-07-25 at 12 16 55 PM" src="https://user-images.githubusercontent.com/106093318/180826889-4a3fb115-7a3b-4a6f-a3ee-857f9c07976f.png">
  
  Step 1: Change the filename to the name of your activity file.
  
  Step 2: Determine what time you would like to consider too late for activity onset to be accurate. I recommend 12:00AM as this has worked best with our data.
  
  Step 3: Run all code cells. 
<br />
<br /> 
<br />
<br />
### Calculating Activity Onset:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Once all code cells are run, the last two cells should produce an output. The second to last code cell should produce a .csv file containing the daily activity onset values for each spider. The threshold for each activity onset is defined in the code as the first time the mean of activity for the night is crossed after the lights turn off. This threshold can be manipulated to include standard deviation or SEM if you would like. The .csv file will be to saved to the location of your jupyter notebook. An example of what the output should look like is shown below.
<p align="center">
  <img src="https://user-images.githubusercontent.com/106093318/180848734-f02c4ace-0b11-481a-a5d7-d07bf977b4a3.png" />
</p>
  
  NOTE: Depending on the defined time for accurate activity onset, 'NaN' values may be in some of the cells. This is expected. 
  
  NOTE: The values in each of the cells represent activity onset in the number of minutes after the lights turn off. This is done to normalize data between datasets that might have different lights on/off times.
<br />
<br /> 
<br />
<br />

### Visualizing Activity Onset in Raster Plots
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In the final code cell, the output should be multiple raster plots, depending on the number of spiders being analyzed. Each figure will be saved separately in the same location as your jupyter notebook. The figures should look similar to the image shown below. It is important to validate the accuracy of every activity onset calculation using the raster plots, as there may be situations where the filters in the code may miss certain anomalies. 
<p align="center">
 <img src="https://user-images.githubusercontent.com/106093318/180849840-183b0bdf-8970-4c27-a7a0-f2ad806dfc10.png" width="500" height="600" />
</p>
  NOTE: If the activity threshold was not crossed, or if it was crossed after the defined threshold time, no activity onset will be plotted on the figure (For example, the second day for this individual).

  
  
## Acknowledgements <a name="Acknowledgements"></a>
