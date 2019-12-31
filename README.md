[![Build Status](https://travis-ci.org/axiomiety/pixfiltrator.svg?branch=master)](https://travis-ci.org/axiomiety/pixfiltrator)

# pixfiltrator

Using pixels to exfiltrate data - and we're not talking base64+OCR!

## TL;DR

In a nutshell, `pixfiltrator` allows you to transfer (binary) files using pixels - a bit like QR codes on steroids. 

A file is broken down into 'pages' which roughly represent how many bytes can be displayed on a single screen. The host takes a screenshot of each of those pages and then processes them to recover the original file - but don't worry, all of that is pretty well automated.

Sample: ![paging animation](https://github.com/axiomiety/pixfiltrator/blob/master/docs/paging1.gif "Paging")


## Instructions

There's a bit of set-up involved the first time around:

 * Open up the client page on the guest
 * Kick off the `Capture-Images.ps1` PowerShell script
 * Select the file on the client and press Play
 * Once all the pages have cycled through, stop the PowerShell script
 * Run `python3 find_bounding_rect.py --image <path_to_image_with_calibration_rectangle>`
   * That's usually the first screenshot
 * Once done, remove the calibration captures - they're no longer required 
 * Call `python3 batch.py` and watch magic happen
 * Assuming all the computed SHA1 of each block match the exracted SHA1 from the metadata, you're good to perform the below:
   * `cat block_* > foo.bin` - the resulting file will be a perfect match to the original on the client, without ever leaving the network

## Details please!

Coming soon!

## Any limitations?

Some remote desktop protocols might apply so much compression that the default block width of 5 pixels is not sufficient. If that's the case you'll need to increase the block width accordingy. This will require tweaking the code a little.

If you're scaling your resolution (e.g. 150%), you may need to tweak the arguments to `find_bounding_rect`.

## Can I contribute?

Absolutely! Please try to keep things consistent - if you have some thoughts on how to tackle certain aspects differently, do reach out first so we can discuss.

## Shout-out

 * @breaktoprotect for his presentation at BSidesSG - without which I probably wouldn't have had the motivation to see this through.