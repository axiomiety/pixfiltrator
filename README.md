[![Build Status](https://travis-ci.org/axiomiety/pixfiltrator.svg?branch=master)](https://travis-ci.org/axiomiety/pixfiltrator) [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](code-of-conduct.md)

# pixfiltrator

Using pixels to exfiltrate data - and we're not talking base64+OCR!

## TL;DR

In a nutshell, `pixfiltrator` allows you to transfer (binary) files using pixels - a bit like QR codes on steroids. 

A file on a guest computer (e.g. Citrix, RDP, VNC, ...) is broken down into 'pages' which roughly represent how many bytes can be displayed on a single screen. The host takes a screenshot of each of those pages and then processes them to recover the original file - but don't worry, all of that is pretty well automated.

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
 * Assuming all the computed SHA1 of each block match the extracted SHA1 from the metadata, you're good to perform the below:
   * `cat block_* > foo.bin` - the resulting file will be a perfect match to the original on the client, without ever leaving the network

## Details please!

The process is composed of 2 parts - one that decomposes a file (runs on the client), and one that re-assembles the parts (runs on the host).

### Client

A pixel is made of 3 components - one red, one blue, one green (RGB - technically there's alpha too in this, but let's ignore that for now). That gives us a range of `255x3` values. We divide this in a scale of 16 items, one for each half-byte - `0x0` to `0xf`. This allows us to handle compression somewhat as a particular colour on the guest may not be represented exactly the same on the host.

The file is read and each byte is divided into 2 half-bytes, or nimbles. So `0x4c` is divided in `0x4` and `0xc`. Each get a square of their own respective colour. The below is a sample that cycles through all bytes from `0x00` to `0xff`:

![sample all bytes](https://github.com/axiomiety/pixfiltrator/blob/master/docs/sample_all_bytes.png "Sample")

The last row contains meta-data about the file and the block. It consists of the current page number, the total number of pages, the SHA1 of the data on the pagea along with a fixed value (`0xdeadc0de`).

### Host

The first part is the calibration - by having a black canvas, we are able to identify the region on screen which will contain the data.

Once that region is identified, the PowerShell script takes periodic screenshots. After that the Python script extracts data from the region from each screenshot and parses each 'square' back into its corresponding value. 

![reassembly](https://github.com/axiomiety/pixfiltrator/blob/master/docs/reassembly1.png "Reassembly")

Note how we handle identical captures by simply overwriding the outputfile. Once all screenshots have been processed, the file is re-assembled by `cat`'ing each piece together.

## Any limitations?

Some remote desktop protocols might apply so much compression that the default block width of 5 pixels is not sufficient. If that's the case you'll need to increase the block width accordingy. This will require tweaking the the settings on both the client and host.

If you're scaling your resolution on the host (e.g. 150%), you may need to tweak the arguments to `find_bounding_rect` too.

## Can I contribute?

Absolutely! Please try to keep things consistent - if you have some thoughts on how to tackle certain aspects differently, do reach out first so we can discuss.

## Shout-out

 * @breaktoprotect for his presentation at BSidesSG - without which I probably wouldn't have had the motivation to see this through.