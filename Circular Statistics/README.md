# Analysis of Circadian Rhythm in Spiders through Circular Statistics

In this project, we use circular statistics to analyze the circadian rhythm in spiders. For circular statistics, the main procedure is to find the mean vector which indicates the directional bias in circular data. Geometrically, the mean vector is the normalized vector sum of vectors in all the directions. We want to find the mean vector for each spider and see if there is any pattern in terms of the activity for the specific spider species.

## Getting Started

### Necessary Files

1. A file containing activity data in 12:12 light/dark condition for several days
2. A file containing activity data in constant darkness condition for several days
3. File specifications:
    - Must in .csv format
    - Must contain a column indicating light condition in binary (e.g. 1 for lights on and 0 for lights off)
    - The first column must contain the DateTime information of each data (e.g. YYYY-MM-DD hh:mm:ss)
    - Must contain multiple columns of activity data where each column represents a single spider and the first row should clearly indicates the spider index (e.g. s1, s2, and s3)
    - Data file must be placed under the same folder as the Jupyter Notebook document

## Usage

+ **Step 1:** Open the `LS_Period` Jupyter Notebook and modify the datafile base according to your activity files for LD and DD period.  
+ **Step 2:** Run all the code cells in `LS_Period` and a .csv file containing the circadian period for each spider calculated by Lomb-Scargle Periodogram would be generated under the same folder (e.g. `Para_LD_Stats.csv` and `Para_DD_Stats.csv`). Do not move the file.  
+ **Step 3:** Open the `Circular_Statistics` Jupyter Notebook and modify the filename under `LD Period` and `DD Period` sections according to your activity files. You can also modify the output data filename under the saving sections according to your needs.  
+ **Step 4:** Run all the code cells in `Circular_Statistics` and two files containing the circular statistics for each spider (mean direction and mean length) would be generated (e.g. `Mean_Para_LD.csv` and `Mean_Para_DD.csv`). A graph with raster plot on the left and circular plot on the right would also be generated inside the Jupyter Notebook for each spider.  

## Documentation

0. `README.md`: readme file giving basic instructions on how to operate and perform your own analysis using circular statistics.

1. Data files
    + `Para_LD.csv`: dataset containing spider activity for Parasteatoda in LD period. Including a DateTime column, a light column, and 32 spider activity columns.
    + `Para_DD.csv`: dataset containing spider activity for Parasteatoda in DD period. Including a DateTime column, a light column, and 32 spider activity columns.
    + `Rhythm.csv`: dataset containing information on whether each spider is rhythmic in LD and DD repsectively. Indicated by binary variable (1 for rhythmic and 0 otherwise).

2. Jupyter Notebook
    + `LS_Period.ipynb`: Jupyter Notebook document calculating the circadian period for each spider using Lomb-Scargle Periodogram.  
    + `Circular_Statistics.ipynb`: Jupyter Notebook document performing all procedures to calculate circular statistics. 
    + `Circular_Parasteatoda_Example.ipynb`: Jupyter Notebook document demonstrating the process of circadian rhythm analysis using circular statistics. Including some summary visualizations. You can use this file as an example.
    
3. Output files
    + `Para_LD_Stats.csv`: output file of `LS_Period.ipynb` containing the circadian period for each spider in LD period and corresponding p-value.
    + `Para_DD_Stats.csv`: output file of `LS_Period.ipynb` containing the circadian period for each spider in DD period and corresponding p-value. 
    + `Mean_Para_LD.csv`: output file of `Circular_Statistics.ipynb` containing the resulting mean direction and mean length for each spider in LD period.  
    + `Mean_Para_DD.csv`: output file of `Circular_Statistics.ipynb` containing the resulting mean direction and mean length for each spider in DD period.  
    

# Circular Analysis

After calculating circular statistics for several species, we can do some circular analysis based on the circular statistics we have for these species. In our analysis, we have circular statistics for four spider species--P. tepidariorum, L. mactans, A. studiosus and M. wittfeldae. We analyze the distribution of their circular stats through creating different graphs--circular plot, boxplot, ECDF (empirical cumulative distribution function), and histogram, and performing t-test and bootstrapping for the stats.

## Usage

+ **Step 1:** Open the `Circular_Analysis` Jupyter Notebook and modify the list containing circular stats (mean length and mean direction) for LD and DD period for each species.  
+ **Step 2:** Run all the code cells in `Circular_Analysis` and images containing different graphs would be generated and saved under the same directory as the Jupyter Notebook. The result of t-test and bootstrapping for confidence interval would be generated inside the Jupyter Notebook.  

## Documentation

1. Jupyter Notebook
    + `Circular_Analysis.ipynb`: Jupyter Notebook document performing circular analysis including generating graphs (circular plot, boxplot, ECDF, and histogram) and doing t-test and bootstrapping.  
    
2. Output files
    + `CircularPlot_4species.png`: output file of `Circular_Analysis.ipynb` containing the picture of circular plot for the four species  
    + `Boxplot_4species_angle.png`: output file of `Circular_Analysis.ipynb` containing the picture of boxplot of the distribution of mean direction in LD and DD period for the four species  
    + `Boxplot_4species_length.png`: output file of `Circular_Analysis.ipynb` containing the picture of boxplot of the distribution of mean length in LD and DD period for the four species  
    + `ECDF_4species.png`: output file of `Circular_Analysis.ipynb` containing the picture of ECDF of mean direction for the four species  
    + `Histogram_4species.png`: output file of `Circular_Analysis.ipynb` containing the picture of histogram of mean direction for the four species  