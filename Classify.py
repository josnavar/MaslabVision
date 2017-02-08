import numpy as np
import math
import cv2
import os
import pickle
import time

from scipy.spatial import ConvexHull
imageDirectory="/home/pepe/PycharmProjects/maslab/blueee11.png"
#Must be padded, tricolor image (no inbetweens), specify channel for color (0->2)
def makePerimeter(colorMatrix,channel):

    NorthWest=1.0*colorMatrix[:-1,:-1,channel]-1.0*colorMatrix[1:,1:,channel]

    NorthEast=1.0*colorMatrix[:-1,1:,channel]-1.0*colorMatrix[1:,:-1,channel]

    booleanPositiveNorthWest=np.greater(NorthWest,0)

    booleanNegativeNorthWest=np.less(NorthWest,0)

    booleanPositiveSouthEast=np.greater(NorthEast,0)
    booleanNegativeSouthEast=np.less(NorthEast,0)

    ##Need to add padding to the sides
    positiveNW=np.insert(np.insert(booleanPositiveNorthWest,639,False,axis=1),479,False,axis=0)

    #Correct
    negativeNW=np.insert(np.insert(booleanNegativeNorthWest,0,False,axis=0),0,False,axis=1)

    positiveSE=np.insert(np.insert(booleanPositiveSouthEast,0,False,axis=1),479,False,axis=0)
    negativeSE=np.insert(np.insert(booleanNegativeSouthEast,0,False,axis=0),639,False,axis=1)
    diagonal=positiveNW+negativeNW+positiveSE+negativeSE
    ##############################################
    # horizontalRedDiff = np.diff(colorMatrix[:, :, channel])
    # verticalRedDiff = np.diff(colorMatrix[:, :, channel], axis=0)
    horizontalRedDiff=1.0*colorMatrix[:-1,:,channel]-1.0*colorMatrix[1:,:,channel]
    verticalRedDiff=1.0*colorMatrix[:,:-1,channel]-1.0*colorMatrix[:,1:,channel]
    # Reconstruct the perimeter from hori and verti
    booleanPositiveHorizontal = np.greater(horizontalRedDiff, 0)
    booleanNegativeHorizontal = np.less(horizontalRedDiff, 0)

    booleanPositiveVertical = np.greater(verticalRedDiff, 0)
    booleanNegativeVertical = np.less(verticalRedDiff, 0)

    booleanHorizontal = np.insert(booleanNegativeHorizontal, 0, False, axis=0) + np.insert(booleanPositiveHorizontal,
                                                                                           479, False, axis=0)
    booleanVertical = np.insert(booleanNegativeVertical, 0, False, axis=1) + np.insert(booleanPositiveVertical,
                                                                                       639,
                                                                                       False, axis=1)
    booleanMatrix = booleanHorizontal + booleanVertical+diagonal
    #booleanMatrix=positiveNW
    return booleanMatrix
def homies(currentTile):
    North = (currentTile[0] - 1, currentTile[1])
    #NorthEast = (currentTile[0] - 1, currentTile[1] + 1)
    East = (currentTile[0], currentTile[1] + 1)
    #SouthEast = (currentTile[0] + 1, currentTile[1] + 1)
    South = (currentTile[0] + 1, currentTile[1])
    #SouthWest = (currentTile[0] + 1, currentTile[1] - 1)
    West = (currentTile[0], currentTile[1] - 1)
    #NorthWest = (currentTile[0] - 1, currentTile[1] - 1)
    neighbors = [North, East, South, West]
    return neighbors
#Perims is the dictionary (id->(x,y)) and to-DO is the processed numpy where for the perimeter
#If toDo is empty it will not do any changes to perims
def populatePerimeterDictionary(perims,toDo):
    #Internal inverse mapping
    if (len(toDo)>0):
        counterId=0
        while (len(toDo)>0):
            perims[counterId]=[]
            DFS(toDo.popitem()[0],toDo,counterId,perims)
            counterId+=1


    return perims

#Perims with id entry should have at least empty list
def DFS(start,toDo,id,perims):
    perims[id].append(start)
    #print id
    #skip[start]=0
    for elt in homies(start):
        # if elt in skip:
        #     print "got here"
        #     continue
        if elt in toDo:
            DFS(toDo.pop(elt),toDo,id,perims)
        # else:
        #     skip[elt]=0
    #print "out of stuff"


#Specify the perimeter dictionary and then the color of interest (0->2)
def filterPerimeters(perims,channel):

    result=[]
    for elt in perims:
        try:
            if (len(perims[elt]) >= 140):
                a = np.asarray(perims[elt])
                average = np.average(a, axis=0)
                hull=ConvexHull(a)

                if (hull.__dict__["volume"]>1400):
                    print len(perims[elt])
                    print average
                    print hull.__dict__["volume"]
                    result.append(average[1]-320)
                    result.append(480-average[0])
                    result.append(len(perims[elt]))
        except:
            # Chill, if ConvexHull returns garbage, we didn't want that object anyway
            pass

    return result


    return result
# def processGreen():
#     perims={}
#     image = cv2.imread(imageDirectory)
#     greenBlobBoolean = np.logical_and(np.equal(image[:, :, 0], 0), np.equal(image[:, :, 1], 255))
#     greenBlobBoolean = np.logical_and(greenBlobBoolean, np.equal(image[:, :, 2], 0))
#     imageMatrix = np.copy(image)
#     imageMatrix[:, :, 0] = 0
#     imageMatrix[:, :, 1] = 0
#     imageMatrix[:, :, 2] = 0
#
#     imageMatrix[:,:,0]=image[:,:,0]*greenBlobBoolean
#     imageMatrix[:,:,1]=image[:,:,1]*greenBlobBoolean
#     imageMatrix[:,:,2]=image[:,:,2]*greenBlobBoolean
#
#     ##Need to add a 1 pixel width frame around the image (black)
#
#     xDim = imageMatrix[:, :, 0].shape[0]
#     yDim = imageMatrix[:, :, 0].shape[1]
#     imageMatrix = imageMatrix.astype(dtype=np.int32)
#     paddedMatrix = np.zeros((xDim + 2, yDim + 2, 3), dtype=np.int32)
#     paddedMatrix[1:xDim + 1, 1:yDim + 1, :] = imageMatrix
#
#     booleanMatrix = makePerimeter(paddedMatrix, 1)
#
#     # Convert the formatting to something easier for python in keyword
#     whereMatrix = np.where(booleanMatrix)
#     toDo = {}
#     for elt in range(0, whereMatrix[0].size):
#         toDo[(whereMatrix[0][elt], whereMatrix[1][elt])]=(whereMatrix[0][elt], whereMatrix[1][elt])
#
#     perims = populatePerimeterDictionary(perims, toDo)
#     print filterPerimeters(perims, 1)
#
#     paddedMatrix[:, :, 1] = paddedMatrix[:, :, 1] * booleanMatrix
#
#     paddedMatrix = paddedMatrix.astype(dtype=np.uint8)
#
#     cv2.imwrite("katon.png",paddedMatrix)
#     # while (True):
#     #     cv2.imshow('frame', paddedMatrix)
#     #     if cv2.waitKey(1) & 0xFF == ord('q'):
#     #         break
#
#
#
# def processRed():
#     perims={}
#     image = cv2.imread(imageDirectory)
#     redBlobBoolean = np.logical_and(np.equal(image[:, :, 0], 0), np.equal(image[:, :, 1], 0))
#     redBlobBoolean = np.logical_and(redBlobBoolean, np.equal(image[:, :, 2], 255))
#     imageMatrix = np.copy(image)
#     imageMatrix[:, :, 0] = 0
#     imageMatrix[:, :, 1] = 0
#     imageMatrix[:, :, 2] = 0
#
#     imageMatrix[:, :, 0] = image[:, :, 0] * redBlobBoolean
#     imageMatrix[:, :, 1] = image[:, :, 1] * redBlobBoolean
#     imageMatrix[:, :, 2] = image[:, :, 2] * redBlobBoolean
#
#
#
#     ##Need to add a 1 pixel width frame around the image (black)
#
#     xDim = imageMatrix[:, :, 0].shape[0]
#     yDim = imageMatrix[:, :, 0].shape[1]
#     imageMatrix = imageMatrix.astype(dtype=np.int32)
#     paddedMatrix = np.zeros((xDim + 2, yDim + 2, 3), dtype=np.int32)
#     paddedMatrix[1:xDim + 1, 1:yDim + 1, :] = imageMatrix
#
#     booleanMatrix = makePerimeter(paddedMatrix, 2)
#
#     # Convert the formatting to something easier for python in keyword
#     whereMatrix = np.where(booleanMatrix)
#     toDo = []
#     for elt in range(0, whereMatrix[0].size):
#         toDo.append((whereMatrix[0][elt], whereMatrix[1][elt]))
#
#     perims = populatePerimeterDictionary(perims, toDo)
#     filterPerimeters(perims, 2)
#
#     paddedMatrix[:, :, 2] = paddedMatrix[:, :, 2] * booleanMatrix
#     paddedMatrix = paddedMatrix.astype(dtype=np.uint8)
#processGreen()
def processGreen(new_array):
    start=time.time()
    perims = {}

    image = new_array

    greenBlobBoolean = np.logical_and(np.equal(image[:, :, 0], 0), np.equal(image[:, :, 1], 255))
    greenBlobBoolean = np.logical_and(greenBlobBoolean, np.equal(image[:, :, 2], 0))
    imageMatrix = np.copy(image)
    imageMatrix[:, :, 0] = 0
    imageMatrix[:, :, 1] = 0
    imageMatrix[:, :, 2] = 0

    imageMatrix[:, :, 0] = image[:, :, 0] * greenBlobBoolean
    imageMatrix[:, :, 1] = image[:, :, 1] * greenBlobBoolean
    imageMatrix[:, :, 2] = image[:, :, 2] * greenBlobBoolean

    ##Need to add a 1 pixel width frame around the image (black)

    # xDim = imageMatrix[:, :, 0].shape[0]
    # yDim = imageMatrix[:, :, 0].shape[1]
    # imageMatrix = imageMatrix.astype(dtype=np.int32)
    # paddedMatrix = np.zeros((xDim + 2, yDim + 2, 3), dtype=np.int32)
    # paddedMatrix[1:xDim + 1, 1:yDim + 1, :] = imageMatrix


    booleanMatrix = makePerimeter(imageMatrix, 1)

    # Convert the formatting to something easier for python in keyword
    whereMatrix = np.where(booleanMatrix)
    toDo = {}
    for elt in range(0, whereMatrix[0].size):
        toDo[(whereMatrix[0][elt], whereMatrix[1][elt])] = (whereMatrix[0][elt], whereMatrix[1][elt])
    #start=time.time()
    perims = populatePerimeterDictionary(perims, toDo)
    #end=time.time()
    #print (end-start)
    result=filterPerimeters(perims, 1)

    return result


def processRed(new_array):
    perims = {}

    image = new_array

    redBlobBoolean = np.logical_and(np.equal(image[:, :, 0], 0), np.equal(image[:, :, 1], 0))
    redBlobBoolean = np.logical_and(redBlobBoolean, np.equal(image[:, :, 2], 255))
    imageMatrix = np.copy(image)
    imageMatrix[:, :, 0] = 0
    imageMatrix[:, :, 1] = 0
    imageMatrix[:, :, 2] = 0

    imageMatrix[:, :, 0] = image[:, :, 0] * redBlobBoolean
    imageMatrix[:, :, 1] = image[:, :, 1] * redBlobBoolean
    imageMatrix[:, :, 2] = image[:, :, 2] * redBlobBoolean

    ##Need to add a 1 pixel width frame around the image (black)

    xDim = imageMatrix[:, :, 0].shape[0]
    yDim = imageMatrix[:, :, 0].shape[1]
    imageMatrix = imageMatrix.astype(dtype=np.int32)
    paddedMatrix = np.zeros((xDim + 2, yDim + 2, 3), dtype=np.int32)
    paddedMatrix[1:xDim + 1, 1:yDim + 1, :] = imageMatrix

    booleanMatrix = makePerimeter(paddedMatrix, 2)

    # Convert the formatting to something easier for python in keyword
    whereMatrix = np.where(booleanMatrix)
    toDo = {}
    for elt in range(0, whereMatrix[0].size):
        toDo[(whereMatrix[0][elt], whereMatrix[1][elt])] = (whereMatrix[0][elt], whereMatrix[1][elt])

    perims = populatePerimeterDictionary(perims, toDo)
    return filterPerimeters(perims, 2)

image = cv2.imread(imageDirectory)
#
# greenBlobBoolean = np.logical_and(np.equal(image[:, :, 0], 0), np.equal(image[:, :, 1], 255))
# greenBlobBoolean = np.logical_and(greenBlobBoolean, np.equal(image[:, :, 2], 0))
# imageMatrix = np.copy(image)
#
# imageMatrix[:, :, 0] = 0
# imageMatrix[:, :, 1] = 0
# imageMatrix[:, :, 2] = 0
#
# imageMatrix[:, :, 0] = image[:, :, 0] * greenBlobBoolean
# imageMatrix[:, :, 1] = image[:, :, 1] * greenBlobBoolean
# imageMatrix[:, :, 2] = image[:, :, 2] * greenBlobBoolean
#
# stuff=makePerimeter(imageMatrix,1)
#
# imageMatrix[:, :, 0] = imageMatrix[:,:,0] * stuff
# imageMatrix[:, :, 1] = imageMatrix[:,:,1] * stuff
# imageMatrix[:, :, 2] = imageMatrix[:,:,2]* stuff

#Need to add a 1 pixel width frame around the image (black)
#cv2.imwrite("fastMom3.png",imageMatrix)
print processRed(cv2.imread(imageDirectory))
# resultingDictionary={}
# calibrationDirectory="/home/pepe/PycharmProjects/maslab/Calibration2/"
# for elt in os.listdir(calibrationDirectory):
#     current=elt.split(".png")[0].split("_")
#     currentX=int(current[0])-9.5
#     currentY=int(current[1])-0.5+3
#     degreeFromCenter=math.atan2(currentX,currentY)*180.0/math.pi
#     distanceFromCenter=math.sqrt(currentX**2+currentY**2)
#     processed=processRed(cv2.imread(calibrationDirectory+elt))
#     if len(processed)>0:
#         print (processed[0],processed[1])
#         print degreeFromCenter
#         print elt
#         resultingDictionary[(processed[0], processed[1])] = (degreeFromCenter, distanceFromCenter)
#np.save("dic",resultingDictionary,allow_pickle=False)

# with open("dic.pickle","wb") as handle:
#     pickle.dump(resultingDictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)
# with open('dic.pickle', 'rb') as handle:
#     b = pickle.load(handle)
# print b==resultingDictionary
#image = cv2.imread(imageDirectory)





