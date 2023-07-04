import numpy as np
import imagej
import scyjava
import os

ini_dir= os.getcwd()

scyjava.config.add_options('-Xmx6g') #assings 6G of memory to Java
ij=imagej.init('/home/greebo/Desktop/Apps/Fiji.app') #Initilisation

print(os.getcwd())  #Prints Current Directory
os.chdir(ini_dir)


dataset = ij.io().open('sample-data/test_image.tif')
ij.py.show(dataset)

print(dataset.shape)
