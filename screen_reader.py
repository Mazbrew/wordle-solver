import cv2
import PIL
import numpy as np
import math
from PIL import ImageGrab as IG
from pynput import keyboard

#finds all the relevant points on the wordle board
#relevant points are the points in which the tile status can be read without being obstructed by the letters
#returns all the relevant points
def findPoints(make_image, mode):
   #using PIL to grab the sccreen
   screen_image = IG.grab(bbox= None)

   #converting the PIL image to an openCV compatible image
   img = np.array(screen_image) 
   img = img[:, :, ::-1].copy() 

   #creation of a grayscale image
   gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

   #applying a threshold, if the image rgb value is above a certain threshold set the pixel value to 1 else 0
   #55 70 for nytimes
   #150 150 for mazdle
   #defaults to mazdle if mode is invalid
   if(mode == "ny"):
      ret,thresh = cv2.threshold(gray,55,70,0)
   elif(mode == "maz"):
      ret,thresh = cv2.threshold(gray,150,150,0)
   else:
      ret,thresh = cv2.threshold(gray,150,150,0)
   
   #obtaining all the contour points
   contours,hierarchy = cv2.findContours(thresh, 1, 2)

   points =[]

   #iterating through all the contour points
   for cnt in contours:
      x1,y1 = cnt[0][0]
      approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)

      #if the contour point is a square
      if len(approx) == 4:
         x, y, w, h = cv2.boundingRect(cnt)
         ratio = float(w)/h
         if ratio >= 0.9 and ratio <= 1.1 and w >= 25:
            #detecting if the contour point is a duplicate
            duplicate = False
            for dupes in range(len(points)):
               if(x+3 == points[dupes][0] and y+3 == points[dupes][1]) or (x+3 in range(points[dupes][0]- int(points[dupes][0]*0.05), points[dupes][0]+ int(points[dupes][0]*0.05)) and y+3 in range(points[dupes][1]- int(points[dupes][1]*0.05), points[dupes][1]+ int(points[dupes][1]*0.05))):
                  duplicate = True

            #only append if the contour point is not a duplicate
            if(duplicate == False):
               points.append([x+3, y+3])

            if(make_image == True and duplicate == False):
               #drawing out the relevant points
               img = cv2.drawContours(img, [cnt], -1, (0,255,0), 1)
               img = cv2.circle(img, [x+3,y+3], 2, (0,0,255), -1)
               img = cv2.putText(img,str(x+3)+ " "+ str(y+3),[x+3,y+3],fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale= 0.50, color=(255,0,255), thickness=1)

   #reversing the tuple for ease of use in the main code
   points.reverse()

   if(len(points) != 30):
      print("[WORDLE BOARD NOT DETECTED]")
      exit(0)

   #segmenting the tuples for ease of use in the main code
   temp_points = []
   for i in range(6):
      temp = []
      for j in range(5):
         temp.append([points[5*i+j][0],points[5*i+j][1]])

      temp_points.append(temp)

   points = temp_points

   #sorting the array to ensure that all of the relevant points are in the right order
   for z in range(6):
      for i in range(6):
         for j in range(4):
            if(points[i][j][0] > points[i][j+1][0]):
               temp = points[i][j][0]
               points[i][j][0] = points[i][j+1][0]
               points[i][j+1][0] = temp

   #display the image holding the relevant points if the function is set to True
   if(make_image == True):
      cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
      cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
      cv2.imshow("window", img)
      cv2.waitKey(0)
      cv2.destroyAllWindows()

   return points

def getPixelCode(point):
   r_base_green = 43
   g_base_green = 83
   b_base_green = 41

   r_base_yellow = 255
   g_base_yellow = 211
   b_base_yellow = 0

   #using PIL to grab the sccreen
   screen_image = IG.grab(bbox= None)

   #converting the PIL image to an openCV compatible image
   img = np.array(screen_image) 
   img = img[:, :, ::-1].copy() 

   b,g,r =(img[point[1],point[0]])

   #detecting if the color is gray
   #gray colors normally have similar values in all three color channels
   #as such if all all 3 values are within a certain threshold of one another, it will be considered as grey
   if (r in range(g- 2, g + 2)) and (r in range(b- 2, b + 2)):
      return "0"

   #detecting if color is green or yellow
   #color similarity can be computed by the euclidian distances of the rgb values
   #if the color's rgb values is closer to green, it is most likely green than it is yellow and vice versa
   if(math.sqrt(math.pow(r-r_base_green,2) + math.pow(g-g_base_green,2) + math.pow(b-b_base_green,2)) < math.sqrt(math.pow(r-r_base_yellow,2) + math.pow(g-g_base_yellow,2) + math.pow(b-b_base_yellow,2))):
      return "2"
   else:
      return "1"
