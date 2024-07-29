# Welcome to the Circadian Pipeline! (v.1.0c)
### In this tutorial, we will walk through the easiest way to use this pipeline.
Currently, the pipeline processes spider circadian activity data and generates raster plots, Lomb-Scargle periodograms, and Lomb-Scargle information.
### This version of the pipeline runs on the *command line*. 
**To run the file,** the command should be in the format `python3 pipeline.py <filename> <binarized> <ls_result>`. As the pipeline is running, it will print out the numbers of the spiders as they are processed so the user can follow along. 
<img width="724" alt="Screenshot 2024-07-28 at 7 08 34 PM" src="https://github.com/user-attachments/assets/41a7dbfe-cb00-4bfc-90ac-3d39af5baa69">

**File name**: This input should be the name of the .txt or.csv file that needs to be processed. The file name **MUST** be in the format 
<spider group> <light condition> <start date> - <end date> - <year> .txt/.csv. For example, the file MsD DD 0718 - 0722 - 2024.txt where:
*MsD* is the group name - Metazygia group D
*DD* is the light conditions the spiders were subjected to - constant darkness
*0718* is the start date, MMDD
*0722* is the end date, MMDD
*2024* is the year of the experiment, YYYY
The pipeline will look for data in the **Data folder** inside **circadian pipeline**.

**Binarized**: This input either takes the word True, if you would prefer the data to be binarized, or False, if you would like the data to be processed as is. 

**Ls_Result**: This input tells the Lomb-Scargle processing code what you would like to generate. One of the following words should come after the binarized input:

*value*: This will tell the code to only write the Lomb-Scargle information to a text file and not generate any periodograms. In our example, the name of the file generated was "MsD_0718 _LS_info.txt". If the file already exists, it will be **overwritten**.
<img width="575" alt="Screenshot 2024-07-28 at 7 09 18 PM" src="https://github.com/user-attachments/assets/b834df8d-ae04-4d5e-ab0c-ff9ce1c2e77f">

*display*: This will tell the code to write the information to the text file and also display the periodograms on the command line, if that is supported on your machine. 

*save*: This will tell the code to save the periodograms to a folder as .png files. In our example, the name of the folder was "LS_MsD_DD_0718".
<img width="225" alt="Screenshot 2024-07-28 at 7 09 55 PM" src="https://github.com/user-attachments/assets/7c61c525-9e24-420e-ae25-417239dacfc7"> 

*dis+save*: This option saves the periodograms and displays them.

### Raster Plots
The pipeline will generate raster plots for every spider and save them in a folder named similarly to "MsD_DD_0718 _raster_plots". When the light sensor detects light, the raster plot will automatically be colored yellow to indicate this. The division of days is automatic. Whether a raster plot based on the raw data or a binarized version is generated is determined by the **"binarized"** input. 

![MsD_01_0718 _raster_plot](https://github.com/user-attachments/assets/adfe2235-a8ce-45b9-9d87-3259e16a87b7)

### Lomb-Scargle
The pipeline will generate the following information:
- The top 3 periods under local maxima frequencies
- The best period approximation
- The false alarm probability for that period approximation
- Periodograms (if desired by the user) that graph the results, with periods ranging from 12 to 48 hours. The best power and period is denoted by a red dot, and the scale of the y-axis is dynamically determined by the max power value.

The raw numbers will be written to a text file as elaborated above, and the periodograms will be saved to a folder. 
![LS_MsD_05_0718 ](https://github.com/user-attachments/assets/d62e0b7b-8482-4d11-9b98-512731fe0230)
