# colorFinder
This module can be used to find the most commonly occurring color in an image.

Use:

You'd pass either a local file address or a web url as of an image (as string) to either the **getImageLocal(fileLoc)** or **getImageWeb(url)** functions respectively.
These return Image objects (created by the PIL library). You would then have to pass the image object to the **findColor(image)** function which will return an rgb tuple for the determined color value. You can then apply a second function to the image along with the first result to obtain a secondary color that should not conflict with the first result in subsequent usage. (defaults are internally defined for monochromatic images) This function is **findSecondary(image,primaryTuple)** where primaryTuple is the rgb tuple for your first result. 

An **rgbToHex(color)** function for hex conversion is included as a utility.

Methodology:
The image is reduced to 5000 representative pixels that are then sorted according to the **Bucket** (Bucket(rmin,rmax,gmin,gmax,bmin,bmax)) objects, defining ~ 4000 color ranges. The bucket with the most numerous pixel occurances is then used to provide an average of the pixels sorted into that bucket. 

An additional **analyseImage(image,factor)** utility function will provide a terminal readout of the images composition by **Bucket**, displaying an absolute count of pixels from the sample for each bucket along with the percent share of the total. The factor arg allows for adjusting the sample size, 1 would analyze each pixel and 100 would analyze 1 of every 100, default factor is 50.

Example Result:
Feeding this image:
<br><img src="gaucho.jpg" width=200><br>
Provides this result:
rgb: (193, 197, 182)
hex: #c1c5b6
<br><img src="gauchoGrey.png" width=200><br>
Secondary Color:
rgb: (56, 127, 171)
hex: #387fab
<br><img src="gauchoBlue.png" width=200><br>
[Sample Analysis Output](https://github.com/dgb30330/colorFinder/blob/main/gauchoAnalysis.txt)



