import numpy as np
import os
import cv2
absDirectory="/home/pepe/PycharmProjects/maslab/readySamples/"
redDirectory="/home/pepe/PycharmProjects/maslab/readySamples/RedAlone/"
greenDirectory="/home/pepe/PycharmProjects/maslab/readySamples/GreenAlone/"
#HSVframe=cv2.cvtColor(RGBframe,cv2.COLOR_BGR2HSV)

sample=[]
#Green is 1 and red is -1
labelSample=[]
for greenFile in os.listdir(greenDirectory):
    if greenFile.endswith(".png"):
        #print greenFile
        greenImage=cv2.imread(absDirectory+"GreenAlone/"+greenFile)
        #greenImage=cv2.cvtColor(greenImage,cv2.COLOR_BGR2HSV)
        #cv2.imshow('frame',greenImage)
        #print greenImage.shape
        for x in range(0,greenImage.shape[0]):
            for y in range(0,greenImage.shape[1]):

                sample.append((greenImage[x,y,0],greenImage[x,y,1],greenImage[x,y,2]))
                labelSample.append(1)
        print greenFile
        print greenImage[5,5,:]

for redFile in os.listdir(redDirectory):
    if redFile.endswith(".png"):
        #print redFile
        redImage=cv2.imread(absDirectory+"RedAlone/"+redFile)
        #redImage=cv2.cvtColor(redImage,cv2.COLOR_BGR2HSV)
        for x in range(0,redImage.shape[0]):
            for y in range(0,redImage.shape[1]):
                sample.append((redImage[x,y,0],redImage[x,y,1],redImage[x,y,2]))
                labelSample.append(-1)
        #print redImage.shape
        #cv2.imshow('frame', redImage)

sample=np.asarray(sample)
labelSample=np.asarray(labelSample)
# print sample
# print labelSample
# print sample.shape
# print labelSample.shape
np.save("sample",sample)
np.save("labelSample",labelSample)





