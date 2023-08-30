# ImageJ_FlakeAnalysis

Repo for the development and implementation of a python script to determine layer thickness using imageJ

This program aims to allow you to find how many layers of a TMD you have by looking at the difference in contrast. 
It allows batches of images to be processed. 

REQUIREMENTS:

Have all the images you want to analyse be saved in one folder. I recommend the "INPUT images" folder under my name in the OneDrive. 

Contrast values can change drastically with exposure time, white balance, ect.  To ensure consistent lighting conditions, you should use a 100x magnification image with Mostafa's specified measurement parameters. 


Then just run the program. 

It will ask you to draw on a line selection and then name your file before saving. Remember the name you give to the batch of files and re-enter when prompted by the terminal. 
The program will then analyse each file (with the root filename you just saved) using the contrast difference method. 
Then save them to the dataframe. 
