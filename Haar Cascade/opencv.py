import numpy as np
import cv2 as cv
biopsy_cascade = cv.CascadeClassifier(r'C:\Users\banso\Documents\Dev\Project\Back End\biopsy_cascade.xml')
img = cv.imread(r'C:\Users\banso\Documents\Dev\Project\Back End\images\7.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

slides = biopsy_cascade.detectMultiScale(gray, 1.3, 5)
print(slides)
for (x,y,w,h) in slides:
    cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
cv.imshow('img',img)
cv.waitKey(0)
cv.destroyAllWindows()