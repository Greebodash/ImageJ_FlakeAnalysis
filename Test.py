import numpy as np
import imagej
import scyjava

scyjava.config.add_options('-Xmx6g')
ij=imagej.init('/home/greebo/Desktop/Apps/Fiji.app')
print(ij.getApp().getInfo(True))
array = np.random.rand(5,4,3)
dataset = ij.py.to_java(array)

print(dataset.shape)
