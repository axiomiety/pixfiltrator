import argparse
import binascii
import cv2
import json
import numpy as np
import sys

from collections import namedtuple
from itertools import chain

Metadata = namedtuple('Metadata', 'page_num num_pages num_bytes_on_page sha1')

# accessing a pixel is as easy as accessing the x-y coordinate: img[x,y]
# the array returned though is in BGR, not RGB

PALETTE_RGB_WIDTH = 47

def convertToPaletteScale(val):
    val_int = int(val)
    if val_int > 255*3:
        raise ValueError(f'cannot convert {val_int} as it is greater than 255*3')
    remainder = val_int % PALETTE_RGB_WIDTH
    quotient = val_int // PALETTE_RGB_WIDTH
    if remainder > PALETTE_RGB_WIDTH/2:
        # round up
        quotient = min(16, quotient+1)
    return quotient

def rescale(image, regionOnGuest):
    # is this the best way to scale it?
    # small = cv2.resize(image, (0,0), fx=2/3, fy=2/3) 
    w, h = [int(r) for r in regionOnGuest.split('x')]
    resized_image = cv2.resize(image, (w, h))
    return resized_image

def identifyBlock(img, r, c, w):
    # columns are x, rows are y
    x = c*w
    y = r*w
    print(f'drawing a green square at ({x},{y}) with width {w}')
    cv2.rectangle(img, (x, y), (x+w, y+w), (0, 255, 0), 2)
    cv2.namedWindow('output2', cv2.WINDOW_NORMAL)
    cv2.imshow('output2',img)
    cv2.waitKey(0)

def blockify(image, width, block_num=-1):
    """Converts the raw image into a list of blocks according to the given size

    E.g. if the image is of size 20x10 (width x height) and each block is of size
    5x5, this will return a list of 8 blocks, and each block will contain 25 elements
    representing the sum of the rgb components of each individual pixel
    """

    # we need to generate 'blocks' of pixels of width x width
    h, w, channels = image.shape # we don't use channels
    print(f'h: {h}, w: {w}')
    num_rows = h//width
    num_cols = w//width
    print(f'dividing the image in {num_rows} rows and {num_cols} columns')
    counter = 0
    scale = width*width
    #block_num = 0
    ret = []
    for r in range(num_rows):
        for c in range(num_cols):
            tally = []
            for ii, i in enumerate(image[r*width:(r+1)*width]):
                for jj, j in enumerate(i[c*width:(c+1)*width]):
                    # r,g,b are the first 3 components
                    # the 4th is alpha which we don't want
                    tally.append(np.sum(j[:3]))
            if counter == block_num:
                print(f'average pixel: {sum(tally)/scale}')
                identifyBlock(image, r, c, width)
            ret.append(tally)
            counter += 1
    return ret

def pyramid_weights(n):
    """Weighs inner values more than outer values according to the height of the pyramid

    We scale the weights to ensure their sum is equal to one
    """

    r = np.arange(n)
    d = np.minimum(r,r[::-1])
    p = np.minimum.outer(d,d)
    sum_weights = sum(p.reshape(n*n))
    return p/sum_weights
    
def weigh_blocks(vals, width, sum_values=False):
    """Gives more weight to inner values of a block compared to outer values

    This is only applicable if the size of a block is > than 2x2 - otherwise
    the original blocks will be returned.

    From size 3x3 and above, the values at the edges of each block are weighed at 0.
    """

    if width < 3:
        return vals

    p = pyramid_weights(width)
    num_elems = width*width
    
    ret = []
    for val in vals:
        res = np.multiply(np.array(val).reshape((width, width)), p).reshape(1, num_elems)
        if sum_values:
            ret.append(sum(sum(r) for r in res))
        else:
            ret.extend(res)
    return ret

def combine_half_bytes(arr):
    pairs = zip(arr[::2], arr[1::2])
    return [((a<<4) + b) for (a,b) in pairs]

def extract_meta_data(byte_array, meta_data_length):
    ret = {}
    byteorder = 'big'
    data = byte_array[-meta_data_length:]
    page_num = int.from_bytes(data[:2], byteorder=byteorder)
    num_of_pages = int.from_bytes(data[2:4], byteorder=byteorder)
    num_bytes_on_page = int.from_bytes(data[4:6], byteorder=byteorder)
    sha1 = binascii.hexlify(data[6:26]) # 20 bytes
    print(f'{page_num}/{num_of_pages} - {num_bytes_on_page} - {sha1}')
    return Metadata(page_num, num_of_pages, num_bytes_on_page, sha1)

def extract(image, sqWidth, regionOnGuest, outFile, verify):
    print(f'processing {image}')
    img = cv2.imread(image, cv2.IMREAD_UNCHANGED)
    rimg = rescale(img, regionOnGuest)
    
    blocks = blockify(rimg, sqWidth)
    extract = weigh_blocks(blocks, sqWidth, sum_values=True)
    ps = [convertToPaletteScale(ex) for ex in extract]
    int_array = combine_half_bytes(ps)
    byte_array_all = bytearray(int_array)
    w, h = [int(r) for r in regionOnGuest.split('x')]
    # e.g. 1200/5 = 240 squares, which is 120 bytes
    meta_data_length = w//sqWidth//2
    meta_data = extract_meta_data(byte_array_all, meta_data_length)
    byte_array = byte_array_all[:meta_data.num_bytes_on_page]

    if verify:
        import hashlib
        m = hashlib.sha1()
        m.update(byte_array)
        print(f'computed  sha1: {m.hexdigest()}')
        print(f'extracted sha1: {meta_data.sha1.decode("ascii")}')
    if outFile is None:
        import os
        bp = os.path.dirname(image)
        outFile = os.path.join(bp, f'block_{str(meta_data.page_num).zfill(5)}_{str(meta_data.num_pages).zfill(5)}_{meta_data.sha1.decode("ascii")}')
    with open(outFile, 'wb') as f:
        f.write(byte_array)
        print(f'wrote file to {outFile}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image',
        action='store',
        default='roi.png',
        type=str,
        help='path to image containing the data')
    parser.add_argument('--numBytes',
        action='store',
        default=1200*800,
        type=int,
        help='length (in bytes) of the file encoded in the image')
    parser.add_argument('--out',
        action='store',
        default='out.bin',
        help='out path for the decoded file')
    parser.add_argument('--verify',
        action='store_true',
        default=False,
        help='toggle computing the SHA1 of the decoded block and compares with what was extracted from the metadata')
    parser.add_argument('--blockSize',
        action='store',
        default=5,
        type=int,
        help='the width of a block in pixels')
    parser.add_argument('--regionOnGuest',
        action='store',
        default='1200x800',
        type=str,
        help='width x height area containing the data on the guest')
    args = parser.parse_args()
    extract(args.image, args.blockSize, args.regionOnGuest, args.out, args.verify)
    