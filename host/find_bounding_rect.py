import cv2
import numpy as np
import json

img = cv2.imread('ss_browser_window_no_data.png', cv2.IMREAD_UNCHANGED)

ret, threshed_img = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),
                127, 255, cv2.THRESH_BINARY)

contours, hier = cv2.findContours(threshed_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# with each contour, draw boundingRect in green
# a minAreaRect in red and
# a minEnclosingCircle in blue
for c in contours:
    # get the bounding rect
    x, y, w, h = cv2.boundingRect(c)
    # draw a green rectangle to visualize the bounding rect
    
    if w > 500 and h > 600:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # get the min area rect
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        # convert all coordinates floating point values to int
        box = np.int0(box)
        # draw a red 'nghien' rectangle
        cv2.drawContours(img, [box], 0, (0, 0, 255))
        print(w,h)
        # we don't need to, but it's cool that we can extract the region of interest so easily!
        roi = img[y:y+h, x:x+w] 
        cv2.imwrite('roi.png', roi)
        coords = {'x':x, 'y': y, 'w': w, 'h': h}
        with open('coords.json', 'w') as outfile:
            json.dump(coords, outfile)

print(len(contours))
#cv2.drawContours(img, contours, -1, (255, 255, 0), 1)
#cv2.imshow("contours", img)
cv2.imshow("contours", img)

while True:
    key = cv2.waitKey(1)
    if key == 27: #ESC key to break
        break
cv2.destroyAllWindows()
