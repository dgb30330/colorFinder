# colorFinder
This module can be used to find the most commonly occurring color in an image.

Use:

You'd pass either a local file address or a web url of an image to either the **getImageLocal(fileLoc)** or **getImageWeb(url)** functions respectively.
These return Image objects (created by the PIL library). You would then have to pass the image object to the **findColor(image)** function which will return an rgb tuple for the color value. An **rgbToHex(color)** function for hex conversion is included as a utility.
