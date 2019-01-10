import numpy as np
import cv2 as cv
brightnessThreshold = 100

img0 = cv.imread('arrow.jpg', cv.IMREAD_GRAYSCALE)
ret, thresh = cv.threshold(img0, brightnessThreshold, 255, 0)
x1, y1, x2, y2 = 200, 500, 500, 800
kernel = np.ones((3, 3), np.uint8)
erosion = cv.erode(thresh, kernel, iterations=5)
filtered = cv.bilateralFilter(erosion, 10, 1000, 1000)
img = filtered  # [x1:y1, x2:y2]
corners = cv.goodFeaturesToTrack(img, 3, 0.01, 10)
imgc = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
for corner in corners:
    x, y = corner.ravel()
    cv.circle(imgc, (x, y), 5, 255, -1)
    coord = corners.ravel()
        #print(coord)
    distList = []
for i in range(0, 5, 2):
    x, y = coord[i], coord[i + 1]
    dist = 0
    for j in range(0, 5, 2):
        if j != i:
            a, b = coord[j], coord[j + 1]
            dist += (x - a) * (x - a) + (y - b) * (y - b)
    distList.append(dist)
#print(distList)

frontX, frontY = coord[2 * distList.index(max(distList))], coord[2 * distList.index(max(distList)) + 1]
backPoints = []
for i in range(0, 5, 2):
    if i != 2 * distList.index(max(distList)):
        backPoints.append(coord[i])
        backPoints.append(coord[i + 1])

midX = (backPoints[0] + backPoints[2]) / 2
deltaX = frontX - midX
#cv.imwrite('processedImage.jpg',imgc)
cv.namedWindow('Display', cv.WINDOW_NORMAL)
cv.imshow('Display', imgc)
cv.waitKey(0)
cv.destroyAllWindows()
