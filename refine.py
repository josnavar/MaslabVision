import numpy as np
import cv2


def runCamera():
    # calibrationDirectory="/home/pepe/PycharmProjects/maslab/Calibration/"
    # writeDirectory="/home/pepe/PycharmProjects/maslab/results/"
    # dataDirectory="/home/pepe/PycharmProjects/maslab/Samples/"
    god = [0.04064465, 0.02110231, 0.01545663]
    godHelper = 0.258985056198
    god = np.asarray(god)
    # the input to VideoCapture can vary between 0-1, try them both to find the correct setting
    camera=cv2.VideoCapture(1)
    frame=0
    while(True):
        #frame+=1
        ret, BGRframe=camera.read()
        #BGRframe=cv2.imread("/home/pepe/PycharmProjects/maslab/bluee11.png")
        #BGRframe = cv2.imread("/home/pepe/PycharmProjects/maslab/bluee4.png")
        # Convert the frame to an HSV matrix.
        HSVframe = cv2.cvtColor(BGRframe, cv2.COLOR_BGR2HSV)

        greenMatrix = np.copy(HSVframe)
        redMatrix = np.copy(HSVframe)
        blueMatrix=np.copy(HSVframe)
        greenMatrix[:, :, 0] = 60
        greenMatrix[:, :, 1] = 255
        greenMatrix[:, :, 2] = 255
        redMatrix[:, :, 0] = 0
        redMatrix[:, :, 1] = 255
        redMatrix[:, :, 2] = 255
        blueMatrix[:,:,0]=120
        blueMatrix[:,:,1]=255
        blueMatrix[:,:,2]=255



        presenceMatrix = np.copy(HSVframe)

        # DotMatrix = presenceMatrix[:, :, 0] * god[0] + presenceMatrix[:, :, 1] * god[1] + presenceMatrix[:, :, 2] * god[
        #     2] + godHelper
        #
        # redRatio1Matrix=1.0*BGRframe[:,:,2]/(BGRframe[:,:,1]+0.001)
        # redRatio2Matrix=1.0*BGRframe[:,:,2]/(BGRframe[:,:,0]+0.001)
        #
        # greenRatio1Matrix=1.0*BGRframe[:,:,1]/(BGRframe[:,:,2]+0.001)
        # greenRatio2Matrix=1.0*BGRframe[:,:,1]/(BGRframe[:,:,0]+0.001)
        # greenDiffMatrix=np.fabs(1.0*HSVframe[:,:,0]-90)
        #
        # blueRatio1Matrix=1.0*BGRframe[:,:,0]/(BGRframe[:,:,1]+0.001)
        # blueRatio2Matrix=1.0*BGRframe[:,:,0]/(BGRframe[:,:,2]+0.001)
        # blueRatio3Matrix=1.0*BGRframe[:,:,2]/(BGRframe[:,:,1]+0.001)
        # blueRatio4Matrix=1.0*BGRframe[:,:,2]/(BGRframe[:,:,0]+0.001)
        #
        # blueDiffMatrix=np.fabs(1.0*HSVframe[:,:,0]-110.0)
        #
        #
        # Diff1Matrix = 1.0 * BGRframe[:, :, 0] / (1.0 * BGRframe[:, :, 1] + 0.001)
        # Diff2Matrix = 1.0 * BGRframe[:, :, 0] / (1.0 * BGRframe[:, :, 2] + 0.001)
        # Diff3Matrix = 1.0 * BGRframe[:, :, 1] / (1.0 * BGRframe[:, :, 2] + 0.001)
        #
        #
        #
        # redBooleanDotMatrix = np.logical_and(np.less_equal(DotMatrix, 13 + 2), np.greater_equal(DotMatrix, 13 - 1.1))
        # redBooleanDot1Matrix=np.logical_and(np.greater(redRatio1Matrix,1.5),np.greater(redRatio2Matrix,1.5))
        # redBooleanDot1Matrix=np.logical_and(redBooleanDot1Matrix,np.greater(BGRframe[:,:,2]),120)
        # redBooleanDotMatrix=np.logical_or(redBooleanDotMatrix,redBooleanDot1Matrix)
        #
        # blueBooleanDotMatrix=np.logical_and(np.greater(blueRatio1Matrix,1.55),np.greater(blueRatio2Matrix,2))
        # blueBooleanDotMatrix=np.logical_and(blueBooleanDotMatrix,np.less(blueDiffMatrix,5))
        # blueBoolean2DotMatrix=np.logical_and(np.less(blueRatio3Matrix,1.07),np.greater(blueRatio4Matrix,1.35))
        # blueBoolean2DotMatrix=np.logical_and(blueBoolean2DotMatrix, np.greater(BGRframe[:,:,2],125))
        # blueBooleanDotMatrix=np.logical_or(blueBooleanDotMatrix,blueBoolean2DotMatrix)
        #
        # greenBooleanDot1Matrix = np.logical_and(np.less_equal(DotMatrix, 7.5 + 2), np.greater_equal(DotMatrix, 7.5 - 1))
        # greenBooleanDot1Matrix = np.logical_and(greenBooleanDot1Matrix, np.less(redRatio1Matrix, 1.5))
        # greenBooleanDot1Matrix=np.logical_and(greenBooleanDot1Matrix,np.less(HSVframe[:,:,1],200))
        # #Green Circle
        # greenBooleanDot2Matrix=np.logical_and(np.less_equal(DotMatrix,12),np.greater_equal(DotMatrix,9.6))
        # greenBooleanDot2Matrix=np.logical_and(greenBooleanDot2Matrix,np.less(greenDiffMatrix,12))
        #
        # greenBooleanDotMatrix = np.logical_and(np.greater(greenRatio1Matrix, 1.08), np.greater(greenRatio2Matrix, 1.05))
        #
        # greenBooleanDotMatrix = np.logical_or(greenBooleanDot1Matrix, greenBooleanDotMatrix)
        # greenBooleanDotMatrix=np.logical_or(greenBooleanDotMatrix,greenBooleanDot2Matrix)
        # greenBooleanDotMatrix = np.logical_and(greenBooleanDotMatrix, np.greater(BGRframe[:, :, 1], 15))
        # greenBooleanDotMatrix=np.logical_and(greenBooleanDotMatrix,np.logical_not(blueBooleanDotMatrix))
        #
        DotMatrix = presenceMatrix[:, :, 0] * god[0] + presenceMatrix[:, :, 1] * god[1] + presenceMatrix[:, :, 2] * god[
            2] + godHelper

        array1 = BGRframe[:, :, 1] + 0.001
        array2 = BGRframe[:, :, 0] + 0.001
        array3 = BGRframe[:, :, 2] + 0.001

        redRatio1Matrix = BGRframe[:, :, 2] / (array1)
        redRatio2Matrix = BGRframe[:, :, 2] / (array2)

        greenRatio1Matrix = BGRframe[:, :, 1] / (array3)
        greenRatio2Matrix = BGRframe[:, :, 1] / (array2)
        greenDiffMatrix = np.fabs(1.0 * BGRframe[:, :, 1] -25)

        blueRatio1Matrix = BGRframe[:, :, 0] / (array1)
        blueRatio2Matrix = BGRframe[:, :, 0] / (array3)
        blueRatio3Matrix = redRatio1Matrix
        blueRatio4Matrix = redRatio2Matrix

        blueDiffMatrix = np.fabs(1.0 * HSVframe[:, :, 0] - 110.0)

        Diff1Matrix = blueRatio1Matrix
        Diff2Matrix = blueRatio2Matrix
        Diff3Matrix = greenRatio1Matrix

        redBooleanDotMatrix = np.logical_and(np.less_equal(DotMatrix, 13 + 2), np.greater_equal(DotMatrix, 13 - 1.1))
        redBooleanDot1Matrix = np.logical_and(np.greater(redRatio1Matrix, 1.5), np.greater(redRatio2Matrix, 1.5))
        redBooleanDot1Matrix = np.logical_and(redBooleanDot1Matrix, np.greater(BGRframe[:, :, 2], 45))
        redBooleanDotMatrix = np.logical_or(redBooleanDotMatrix, redBooleanDot1Matrix)

        blueBooleanDotMatrix = np.logical_and(np.greater(blueRatio1Matrix, 1.55), np.greater(blueRatio2Matrix, 2))
        blueBooleanDotMatrix = np.logical_and(blueBooleanDotMatrix, np.less(blueDiffMatrix, 5))

        blueBoolean2DotMatrix = np.logical_and(np.less(blueRatio3Matrix, 1.07), np.greater(blueRatio4Matrix, 1.35))
        blueBoolean2DotMatrix = np.logical_and(blueBoolean2DotMatrix, np.greater(BGRframe[:, :, 2], 125))
        blueBoolean2DotMatrix=np.logical_and(blueBoolean2DotMatrix,np.less(HSVframe[:,:,0],30))
        blueBooleanDotMatrix = np.logical_or(blueBooleanDotMatrix, blueBoolean2DotMatrix)


        greenBooleanDot1Matrix = np.logical_and(np.less_equal(DotMatrix, 7.5 + 2),
                                                np.greater_equal(DotMatrix, 7.5 - 1.5))
        greenBooleanDot1Matrix = np.logical_and(greenBooleanDot1Matrix, np.less(redRatio1Matrix, 1.5))
        greenBooleanDot1Matrix = np.logical_and(greenBooleanDot1Matrix, np.less(HSVframe[:, :, 1], 200))
        bad=np.logical_and(np.greater(BGRframe[:,:,2],190),np.less(redRatio1Matrix,1.15))
        greenBooleanDot1Matrix=np.logical_and(greenBooleanDot1Matrix,np.logical_not(bad))

        greenBooleanDot2Matrix = np.logical_and(np.less_equal(DotMatrix, 12.5), np.greater_equal(DotMatrix, 9.6))
        greenBooleanDot2Matrix = np.logical_and(greenBooleanDot2Matrix, np.less(greenDiffMatrix, 12))
        # greenBooleanDotMatrix = np.logical_and(np.greater(greenRatio1Matrix, 1.08), np.greater(greenRatio2Matrix, 1.05))
        # greenBooleanDotMatrix = np.logical_or(greenBooleanDot1Matrix, greenBooleanDotMatrix)
        greenBooleanDotMatrix = np.logical_or(greenBooleanDot1Matrix, greenBooleanDot2Matrix)
        greenBooleanDotMatrix = np.logical_and(greenBooleanDotMatrix, np.greater(BGRframe[:, :, 1], 15))
        greenBooleanDotMatrix = np.logical_and(greenBooleanDotMatrix, np.logical_not(blueBooleanDotMatrix))

        ##First filter for green and most shades.
        # greenBooleanDot1Matrix = np.logical_and(np.less_equal(DotMatrix, 6 + 2.2),
        #                                         np.greater_equal(DotMatrix, 6 - 2))
        # greenBooleanDot1Matrix = np.logical_and(greenBooleanDot1Matrix, np.less(HSVframe[:, :, 0], 100))
        # greenBooleanDot1Matrix=np.logical_and(greenBooleanDot1Matrix,np.greater(HSVframe[:,:,0],32))
        # ##Gets rid of noise but masks some green...
        # greenBooleanDot1Matrix=np.logical_and(greenBooleanDot1Matrix,np.greater(BGRframe[:,:,1],30))
        #
        # ##Fix for the above:
        # greenFix1=np.logical_and(np.greater_equal(greenRatio1Matrix,1.64),np.greater_equal(greenRatio2Matrix,1.15))
        # greenFix1=np.logical_and(greenFix1,np.less_equal(greenDiffMatrix,8))
        # greenBooleanDot1Matrix=np.logical_or(greenFix1,greenBooleanDot1Matrix)
        # greenBooleanDot2Matrix = np.logical_and(np.less_equal(HSVframe[:,:,0], 103),
        #                                         np.greater_equal(HSVframe[:,:,0], 92))#
        # greenBooleanDotMatrix=np.logical_or(greenBooleanDot1Matrix,greenBooleanDot2Matrix)
        # greenBooleanDotMatrix=np.logical_and(greenBooleanDotMatrix,np.logical_not(blueBooleanDotMatrix))




        diff1Boolean = np.logical_and(np.less_equal(Diff1Matrix, 1.3), np.greater_equal(Diff1Matrix, 0.8))
        diff2Boolean = np.logical_and(np.less_equal(Diff2Matrix, 1.3), np.greater_equal(Diff2Matrix, 0.8))
        diff3Boolean = np.logical_and(np.less_equal(Diff3Matrix, 1.2), np.greater_equal(Diff3Matrix, 0.8))
        diffBooleanMatrix = np.logical_and(diff1Boolean, diff2Boolean)
        diffBooleanMatrix = np.logical_and(diffBooleanMatrix, diff3Boolean)
        diffBooleanMatrix = np.logical_not(diffBooleanMatrix)

        presenceMatrix[:, :, 0] = greenMatrix[:, :, 0] * greenBooleanDotMatrix + redMatrix[:, :,
                                                                                 0] * redBooleanDotMatrix+blueMatrix[:,:,0]*blueBooleanDotMatrix
        presenceMatrix[:, :, 1] = greenMatrix[:, :, 1] * greenBooleanDotMatrix + redMatrix[:, :,
                                                                                 1] * redBooleanDotMatrix+blueMatrix[:,:,1]*blueBooleanDotMatrix
        presenceMatrix[:, :, 2] = greenMatrix[:, :, 2] * greenBooleanDotMatrix + redMatrix[:, :,
                                                                                 2] * redBooleanDotMatrix+blueMatrix[:,:,2]*blueBooleanDotMatrix

        presenceMatrix[:, :, 0] = presenceMatrix[:, :, 0] * diffBooleanMatrix
        presenceMatrix[:, :, 1] = presenceMatrix[:, :, 1] * diffBooleanMatrix
        presenceMatrix[:, :, 2] = presenceMatrix[:, :, 2] * diffBooleanMatrix

        processedFrame = cv2.cvtColor(presenceMatrix, cv2.COLOR_HSV2BGR)
        cv2.imshow("ty's tomato.png", processedFrame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        cv2.imwrite("/home/pepe/PycharmProjects/maslab/test100.png", processedFrame)
        cv2.imwrite("/home/pepe/PycharmProjects/maslab/test101.png", BGRframe)




runCamera()













