import matplotlib.pyplot as plt
import cv2
import numpy as np


def main():
	imgName = str(input()).rstrip()
	detectPlate(imgName)


'''
    Crops the image at the maximum and minimum values of the contour
'''
def cropImg(img, contour):
    img = np.copy(img)
    maxX = maxY = 0
    minX = minY = img.shape[0]
    for c in contour:
        c = c[0]
        if c[0] > maxX:
            maxX = c[0]
        elif c[0] < minX:
            minX = c[0]

        if c[1] > maxY:
            maxY = c[1]
        elif c[1] < minY:
            minY = c[1]

    crop_img = img[minY:maxY, minX:maxX]
    return crop_img


def applyBlurToImg(img, kernel=(5,5)):
    return cv2.GaussianBlur(img, kernel, 0)


def getBinaryImg(img, alpha = 1.0):
    mean = np.mean(img)
    _, binaryImg = cv2.threshold(img, mean*alpha, 255, 0)
    return binaryImg


def getBestContour(img, minVertex=0, maxVertex=15, maxArea=-1):
    # finds contours
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    imgSize = img.shape[0]*img.shape[1]
    largestC = -1

    # checks if there`s a threshold to how large the area should be
    if maxArea == -1:
        maxArea = imgSize
    
    largestAreaFound = 0
    for c in contours:
        # gets area and perimeter of contour
        perimeter = cv2.arcLength(c, True)
        area = cv2.contourArea(c)
        approxPolygon = cv2.approxPolyDP(c, 0.005 * perimeter, True)
#         if len(approxPolygon) > minVertex and len(approxPolygon) < maxVertex and area > largestAreaFound and area < 0.9*imgSize and area < 0.9*maxArea:
        if len(approxPolygon) > minVertex and len(approxPolygon) < maxVertex and area > largestAreaFound and area < 0.9*maxArea:
            largestC = c
            largestAreaFound = area
    
    return largestC


'''
    [not used anymore]
    Applies all contours into the image and returns it
'''
def getContouredImg(regularImg, grayImg, minVertex=0, maxVertex=15):
    contours, hierarchy = cv2.findContours(grayImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    regularImg = np.copy(regularImg)
    
    for c in contours:
        perimeter = cv2.arcLength(c, True)
        area = cv2.contourArea(c)
        approxPolygon = cv2.approxPolyDP(c, 0.005 * perimeter, True)
        if len(approxPolygon) > minVertex and len(approxPolygon) < maxVertex and area > 4000:
            cv2.drawContours(regularImg, [c], -1, (0, 255, 0), 2)
    return regularImg


'''
    Simply draws the contour into the image with green colour
'''
def applyDetectionToImg(regularImgAux, bestContour):
    regularImg = np.copy(regularImgAux)
    cv2.drawContours(regularImg, [bestContour], -1, (0, 255, 0), 2)
    return regularImg


'''
    Does all the Image Processing steps needed to detect a sign with text,
    except for checking the content of the crop
'''
def detectPlate(imgName, maxVertex=15,
                kernel=(5,5), printBinary=False,
                binarizationMode='adaptiveThreshold',
                maxArea=-1):
    
    regularImg = cv2.imread(imgName)
    blurredImg = applyBlurToImg(regularImg, kernel=kernel)
    grayImg = cv2.cvtColor(blurredImg, cv2.COLOR_BGR2GRAY);
    
    # sets binarization mode
    if binarizationMode == 'mean':
        binaryImg = getBinaryImg(grayImg)
    else:
        binaryImg = cv2.adaptiveThreshold(grayImg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 13, 2)
    
    bestContour = getBestContour(binaryImg, maxVertex=maxVertex, maxArea=maxArea)
    
    regularImgWithDetection = applyDetectionToImg(regularImg, bestContour)
    
    # plots binary or regular image
    if printBinary:
        plt.imshow(binaryImg, cmap='gray')
    else:
        plt.imshow(cv2.cvtColor(regularImgWithDetection, cv2.COLOR_BGR2RGB), cmap='gray')
    plt.axis('off');
    
    croppedImg = cropImg(regularImg, bestContour);
    cv2.imwrite("output.jpg", croppedImg)
    return croppedImg

if __name__ == "__main__":
    main()
