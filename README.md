# colorFinder
This module can be used to find the most commonly occurring color in an image.

Use:

You'd pass either a local file address or a web url as of an image (as string) to either the **getImageLocal(fileLoc)** or **getImageWeb(url)** functions respectively.
These return Image objects (created by the PIL library). You would then have to pass the image object to the **findColor(image)** function which will return an rgb tuple for the determined color value. An **rgbToHex(color)** function for hex conversion is included as a utility.

Methodology:
The image is reduced to 5000 representative pixels that are then sorted according to the **Bucket** (Bucket(rmin,rmax,gmin,gmax,bmin,bmax)) objects, defining ~ 4000 color ranges. The bucket with the most numerous pixel occurances is then used to provide an average of the pixels sorted into that bucket. 

Example Result:
Feeding this image:
<br><img src="gaucho.jpg" width=200><br>
Provides this result:
rgb: (193, 197, 182)
hex: #c1c5b6
<br><img src="gauchoGrey.png" width=200><br>

Possible features:
Block return ranges. As of now, blacks/grays will frequently be returned for darker images, as would be expected. By creating a threshold for colors evaluated, a 'highlight color' could be determined.


