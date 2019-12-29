import cv2
import json
from operator import itemgetter
import sys
import argparse

def extract(src, dest, coords):
    print(f'processing {src}')
    img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
    with open(coords, 'r') as f:
        coords = json.load(f)
    x, y, w, h = itemgetter('x','y','w','h')(coords)
    roi = img[y:y+h, x:x+w]
    print(f'writing roi to {dest}')
    cv2.imwrite(dest, roi)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image',
        action='store',
        default='ss_browser_window_with_data.png',
        type=str,
        help='path to image containing the region of interest')
    parser.add_argument('--out',
        action='store',
        default='roi.png',
        help='out path for the region of interest')
    parser.add_argument('--coords',
        action='store',
        default='coords.json',
        help='path of the file containing the position of the region of interest')
    args = parser.parse_args()
    extract(src=args.image, dest=args.out, coords=args.coords)