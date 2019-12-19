
## Parsing the file

 * Assuming uncompressed (we can look at compression later, but should be irrelevant from a display/parsing perspective)
 * If the file is 16958 bytes, we will require 16958*2 squares
 * That's 33916
 * Assume a 1200x800 canvas - that's 960,000 squares
 * If we assume squares of 4x4 pixels, that means we can show 60,000 squares on that canvas. 5x5 pixels, that's 38400
 * We need to think about paging at some point!
 * From a boundary perspective, we could have the user input the file length
 * We need to create a palette - e.g. 16bit


## Palette

 * The smaller the palette, the less likely RDP/VNC compression will mess things up. If we had a 256bit palette that would greatly speed things up, but it probably won't be as accurate
 * RGB is composed of 3 channels, each having a value up to 255
 * To map a hexadecimal digiti to a colour, the 'unit' is of value 51 (255*3/15 = 51 - 0 being our 16th)
 * decimal(hexvalue) *  51
 * I wonder if it'd make more sense for the palette to increae the R component by 51 first, followed by G, followed by B etc... so e.g. 3 would be (51,51,51) vs (153,0,0) as it is now - if anything there'd be more differentiation between each byte - otherwise everything looks kind of red! but it might make it harder to decode as we'd need to check each component (vs summing everything up)

## Parsing the image!

 * We can take a screenshot of the active window - that's easy enough (used Greenshot, but I'm sure we can do this programmatically)
 * OpenCV does a great job at finding the bounding rectangle of the region we'll be displaying data on - but it's unscaled!
   * That is, it finds a 1802x1202 - because my display is set to 150% (1800/1200 is 1.5)
 * Once we have the x,y,w,h coordinates, it means we can extract the correct region from all subsequent screenshots
 * Ref code taken from https://gist.github.com/bigsnarfdude/d811e31ee17495f82f10db12651ae82d
 * Maybe we should apply weighting to the pixels - so the ones in the center contribute more than the ones at the edges - we can use that to smooth things out if required

## Misc

 * Firefox can take screenshots! https://stackoverflow.com/questions/25332458/firefox-addon-api-for-taking-screenshot#25359866
 * Only useful on the client though
 * But could be used to 'download' binaries onto the client whilst bypassing some restrictions

## Taking screenshots

 * This will be OS-dependent
 * For Windows it looks like we can use Powershell: https://gallery.technet.microsoft.com/scriptcenter/eeff544a-f690-4f6b-a586-11eea6fc5eb8
   * We can hook this up to a timer - it can take a number of 'pages' as an argument
 * The parsing script can be updated to take a directory and parse each screenshot alphabetically
 * The script above didn't work - but it looks like user32.dll exposes everything we need
   * https://stackoverflow.com/questions/5878963/getting-active-window-coordinates-and-height-width-in-c-sharp
   * https://docs.microsoft.com/en-us/dotnet/api/system.drawing.graphics.copyfromscreen?view=netframework-4.8
   * There's some here too, which leverages PrintScr essentially: https://powershell.org/2013/01/powershell-screen-shots/

## TODO:
 * stop using print statements and set some proper logging!
 outside pixels and higher weight to the inner ones
 * add type annotations!
  * take a screenshot of the screen programatically
 * clean up the paging - it's ugly...
 * DONE: deal with paging on the client side for larger files
 * DONE: migrate to argparse for Python - need to pass in the number of bytes too
 * DONE: work out the scaling as we attribute a lower weight to the 
 * DONE: merge bytes in the final array! otherwise we always represent the lower portion
 * DONE: create a 'proper' project - complete with requirements.txt - c.f. https://docs.python.org/3/tutorial/venv.html
   * DONE: and arguable something separate for js too (we can extract some of the functionality into separate modules, imported by the client)!
 * DONE: log the SHA256 digest of the file 
 * DONE: create test method to identify blocks on the roi (for debugging)
 * DONE: merge client/client_test code (c.f. point below)
 * DONE: take some new screenshots now that the scale has changed...
 * DONE: given x,y,w,h, extract the image data into pixels & colours
 * DONE: run it through openCV to find the bounding rectangle
 * DONE: map each hex character to an equally space colour in the RGB spectrum
 * DONE: iterate through a file and draw 'em squares