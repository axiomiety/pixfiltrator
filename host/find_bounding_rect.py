import cv2
import numpy as np
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--image',
    action='store',
    default='ss_browser_window_no_data.png',
    type=str,
    help='path to image containing the calibration screenshot')
parser.add_argument('--region',
    action='store',
    default='1800x1200',
    type=str,
    help='approximate area of the bounding rectangle on the local host (so including scaling - e.g. if the guest has 1200x800 and the host uses 150% scaling, that would be 1800x1200)')
args = parser.parse_args()

img = cv2.imread(args.image, cv2.IMREAD_UNCHANGED)

ret, threshed_img = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),
                127, 255, cv2.THRESH_BINARY)

contours, hier = cv2.findContours(threshed_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# with each contour, draw boundingRect in green
# a minAreaRect in red and
# a minEnclosingCircle in blue

delta = 0.01
width, height = [int(r) for r in args.region.split('x')]

for c in contours:
    # get the bounding rect
    x, y, w, h = cv2.boundingRect(c)
    
    # TODO: this should be arguments with a given thr
    if width*(1+delta)> w > width*(1-delta) and height*(1+delta) > h > height*(1-delta):
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

#print(len(contours))
#cv2.drawContours(img, contours, -1, (255, 255, 0), 1)
#cv2.imshow("contours", img)

#while True:
#    key = cv2.waitKey(1)
#    if key == 27: #ESC key to break
#        break
#cv2.destroyAllWindows()
