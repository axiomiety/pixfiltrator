[![Build Status](https://travis-ci.org/axiomiety/pixfiltrator.svg?branch=master)](https://travis-ci.org/axiomiety/pixfiltrator)

# pixfiltrator
Using pixels to exfiltrate data - and we're not talking OCR!

## Instructions

 * Open up the client page on the guest
 * Take a screenshot containing the black calibration region
 * Extract the region's coordinates: `python3 find_bounding_rect.py --image images/calibration.png --region 1800x1200`
 * Open up the file on the guest and take a screenshot
 * Extract the region of interest: `python3 extract_roi.py --image images/ss.png --out images/roi1.png --coords coords.json`
 * Extract the data: `python3 extract_data.py --image images/roi1.png --out foo.bin`
 * Enjoy