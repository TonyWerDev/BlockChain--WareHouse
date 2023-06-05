##########  Librerias  ##########
import cv2
import numpy as np
from time import sleep
import paho.mqtt.client as mqtt
import datetime;
from math import atan, atan2, cos, sin, sqrt, pi, acos
import numpy as np

#cap = cv2.VideoCapture('rtsp://admin:Camera01_@10.50.70.178:554')
#cap = cv2.VideoCapture('rtsp://admin:Camera02_@10.50.70.75:554')
#cap = cv2.VideoCapture('rtsp://admin:Camera03_@10.50.70.11:554') #--
#cap = cv2.VideoCapture('rtsp://admin:Camera04_@10.50.70.89:554')
cap = cv2.VideoCapture('rtsp://admin:Camera05_@10.50.70.68:554')

font = cv2.FONT_HERSHEY_SIMPLEX

def drawAxis(img, p_, q_, color, scale):
  p = list(p_)
  q = list(q_)
 
  ## [visualization1]
  angle = atan2(p[1] - q[1], p[0] - q[0]) # angle in radians
  hypotenuse = sqrt((p[1] - q[1]) * (p[1] - q[1]) + (p[0] - q[0]) * (p[0] - q[0]))
 
  # Here we lengthen the arrow by a factor of scale
  q[0] = p[0] - scale * hypotenuse * cos(angle)
  q[1] = p[1] - scale * hypotenuse * sin(angle)
  cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)
 
  # create the arrow hooks
  p[0] = q[0] + 9 * cos(angle + pi / 4)
  p[1] = q[1] + 9 * sin(angle + pi / 4)
  cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)
 
  p[0] = q[0] + 9 * cos(angle - pi / 4)
  p[1] = q[1] + 9 * sin(angle - pi / 4)
  cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)
  ## [visualization1]

def getOrientation(pts, img):
  ## [pca]
  # Construct a buffer used by the pca analysis
  sz = len(pts)
  data_pts = np.empty((sz, 2), dtype=np.float64)
  for i in range(data_pts.shape[0]):
    data_pts[i,0] = pts[i,0,0]
    data_pts[i,1] = pts[i,0,1]
 
  # Perform PCA analysis
  mean = np.empty((0))
  mean, eigenvectors, eigenvalues = cv2.PCACompute2(data_pts, mean)
 
  # Store the center of the object
  cntr = (int(mean[0,0]), int(mean[0,1]))
 
  ## [visualization]
  # Draw the principal components
  cv2.circle(img, cntr, 3, (255, 0, 255), 2)
  p1 = (cntr[0] + 0.02 * eigenvectors[0,0] * eigenvalues[0,0], cntr[1] + 0.02 * eigenvectors[0,1] * eigenvalues[0,0])
  p2 = (cntr[0] - 0.02 * eigenvectors[1,0] * eigenvalues[1,0], cntr[1] - 0.02 * eigenvectors[1,1] * eigenvalues[1,0])
  drawAxis(img, cntr, p1, (255, 255, 0), 1)
  drawAxis(img, cntr, p2, (0, 0, 255), 5)

  angle_prev = np.rad2deg(atan2(eigenvectors[0,1], eigenvectors[0,0])) # orientation in radians
  if (angle_prev <= -0.1 and angle_prev >= -45):
      angle = -int(angle_prev)
  elif (angle_prev <= 135 and angle_prev > 0.1):
      angle = 180-int(angle_prev)
  else:
      angle = 0    

 
  M = cv2.moments(pts)
  if(M["m00"]==0):
    M["m00"]==1
  y=int(M["m10"]/M["m00"])
  x=int(M["m01"]/M["m00"])
  contorno2=cv2.convexHull(contour)
  cv2.circle(frame,(y,x),7,(0,255,0),-1)
  cv2.putText(frame,'{},{}'.format(y,x),(y,x+10), font, 0.75,(0,130,255),1,cv2.LINE_AA)
  
  # Label with the rotation angle
  label = "Px:" + str(x) + ", Py:" + str(y) + ", Angle:" + str(angle)   
  textbox = cv2.rectangle(img, (cntr[0], cntr[1]-25), (cntr[0] + 250, cntr[1] + 10), (255,255,255), -1)
  cv2.putText(img, label, (cntr[0], cntr[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)

  return angle

x=0
y=0
angle=0

##pieza 1
while x <= 2:
    for i in range(0,50):
        succes, img = cap.read()

        a= 600  
        b= 850  
        c= 680  
        d= 1150

        if succes:    
            frame = img[a:b,c:d] 
            
            #Blur image
            blurred = cv2.blur(frame, (5, 5))

            # converting image into grayscale image
            gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

            # setting threshold of gray image
            _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

            #Cany img
            bordes = cv2.Canny(threshold,2.5,5)
        
            # using a findContours() function
            contours, _ = cv2.findContours(
                bordes, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
            i = 0
        
            # list for storing names of shapes
            for k, contour in enumerate(contours):

                #Calculo de area
                area = cv2.contourArea(contour)
                #print(area)

                if (area>3700):  
                    # here we are ignoring first counter because 
                    # findcontour function detects whole image as shape
                
                    if i == 0:
                        i = 1
                        continue
            
                    # cv2.approxPloyDP() function to approximate the shape
                    approx = cv2.approxPolyDP(
                        contour, 0.01 * cv2.arcLength(contour, True), True)
                
                    # using drawContours() function
                    if len(approx) == 3:
                        cv2.drawContours(frame, [contour], 0, (0, 0, 255), 5)
            
                    elif len(approx) == 4:
                        cv2.drawContours(frame, [contour], 0, (0, 0, 255), 5)

                    angle = getOrientation(contour, frame)

                    # finding center point of shape
                    M = cv2.moments(contour)
                    if M['m00'] != 0.0:
                        x = int(M['m10']/M['m00'])
                        y = int(M['m01']/M['m00'])

                else:
                    continue
            
            # displaying the image after drawing contours
            cv2.imshow('Pieza', frame)

            if cv2.waitKey(2) & 0xFF == ord('s'):
                    break
            
        
print(x, ", ", y, ", ", angle)