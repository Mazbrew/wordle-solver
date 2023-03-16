import cv2
import PIL
import numpy as np
from PIL import ImageGrab as IG

#using PIL to grab the sccreen
screen_image = IG.grab(bbox= None)

#converting the PIL image to an openCV compatible image
img = np.array(screen_image) 
img = img[:, :, ::-1].copy() 

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret,thresh = cv2.threshold(gray,50,50,0)
contours,hierarchy = cv2.findContours(thresh, 1, 2)
print("Number of contours detected:", len(contours))

for cnt in contours:
   x1,y1 = cnt[0][0]
   approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
   if len(approx) == 4:
      x, y, w, h = cv2.boundingRect(cnt)
      ratio = float(w)/h
      if ratio >= 0.9 and ratio <= 1.1:
         img = cv2.drawContours(img, [cnt], -1, (0,255,0), 3)

font = cv2.FONT_HERSHEY_SIMPLEX
text = "CLICK THE TOP LEFT BOX"
thickness = 2
text_size = cv2.getTextSize(text, font, 1, thickness)[0]
white = (255,255,255)

textX = int((img.shape[1] - text_size[0]) / 2)
textY = int((img.shape[0]/4 + text_size[1]) / 2)

org = (textX, textY)
img = cv2.putText(img,"CLICK THE TOP LEFT BOX", org, font, 1, white, thickness)

cv2.imshow("Shapes", img)
cv2.waitKey(0)
cv2.destroyAllWindows()