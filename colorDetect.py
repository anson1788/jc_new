import cv2
import numpy as np

lower_red = np.array([0,0,200], dtype = "uint8") 

upper_red= np.array([100,120,250], dtype = "uint8")

image = cv2.imread('bjGame/image.png') 
ROI = image[490:490+50, 240:240+50]


mask = cv2.inRange(ROI, lower_red, upper_red)
detected_output = cv2.bitwise_and(ROI, ROI, mask =  mask) 
pixels = cv2.countNonZero(mask)
if pixels > 0:
    print("green exist")
else: 
    print("not found")

cv2.imshow("red color detection", detected_output) 
cv2.waitKey(0) 
