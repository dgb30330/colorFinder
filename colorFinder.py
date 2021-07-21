from PIL import Image
import requests

class Bucket:
    def __init__(self,rmin,rmax,gmin,gmax,bmin,bmax):
        self.rmin = rmin
        self.rmax = rmax
        self.gmin = gmin
        self.gmax = gmax
        self.bmin = bmin
        self.bmax = bmax
        self.count = 0
        self.pixels = []

    def eval(self,pixelTuple):
        if pixelTuple[0] >= self.rmin and pixelTuple[0] <= self.rmax:
            if pixelTuple[1] >= self.gmin and pixelTuple[1] <= self.gmax:
                if pixelTuple[2] >= self.bmin and pixelTuple[2] <= self.bmax:
                    self.count += 1
                    self.pixels.append(pixelTuple)
        
    
    def getAverage(self):
        rTotal = 0
        gTotal = 0
        bTotal = 0
        for pix in self.pixels:
            rTotal += pix[0]
            gTotal += pix[1]
            bTotal += pix[2]
        r = int(rTotal / len(self.pixels))
        g = int(gTotal / len(self.pixels))
        b = int(bTotal / len(self.pixels))
        return (r,g,b)

def createBuckets():
    allBuckets = []
    rmin = 0
    rmax = 15
    gmin = 0
    gmax = 15
    bmin = 0
    bmax = 15

    interval = 15

    while rmax <= 255:
        while gmax <= 255:
            while bmax <= 255:
                newBucket = Bucket(rmin,rmax,gmin,gmax,bmin,bmax)
                allBuckets.append(newBucket)
                bmax += interval
                bmin += interval
            bmin = 0
            bmax = 15
            gmax+=interval
            gmin+=interval
        gmin = 0
        gmax = 15
        rmax+=interval
        rmin+=interval
    #print(len(allBuckets))
    return allBuckets

def getImageWeb(url):
    rawData = requests.get(url, stream=True).raw
    image = Image.open(rawData)
    return image
    

def getImageLocal(fileLoc):
    image = Image.open(fileLoc)
    return image

def findColor(image):
    pixels = getPixelSample(image)
    allBuckets = createBuckets()

    for p in pixels:
        for b in allBuckets:
            b.eval(p)

    maxBucket = allBuckets[0]
    for b in allBuckets:
        """
        if b.count > 0:
            print("Count: "+str(b.count)+" "+str(b.rmin)+","+str(b.gmin)+","+str(b.bmin))
        """
        if b.count > maxBucket.count:
            maxBucket = b

    return maxBucket.getAverage()

def getPixelSample(image):
    # pass Image.open() object
    width, height = image.size

    #print(str(width) + " x " + str(height))
    pixelGrid = image.load()
    pixels = []
    x = 0
    y = 0
    sampleRate = int((height*width)/5000)
    #print(sampleRate)
    sampleControl = 0
    while x < width:
        while y < height:
            sampleControl+=1
            if sampleControl == sampleRate:
                pixels.append(pixelGrid[x,y])
                sampleControl = 0
            y+=1
        x+=1
        y=0
    #print(len(pixels))
    return pixels

def rgbToHex(pixelTuple):
    return '#{:02x}{:02x}{:02x}'.format(pixelTuple[0],pixelTuple[1],pixelTuple[2])

#TEST ZONE
"""

url ='https://upload.wikimedia.org/wikipedia/en/8/8f/Steely_Dan_-_Gaucho.jpg'
url2 = 'https://upload.wikimedia.org/wikipedia/en/d/da/Black_Sabbath_debut_album.jpg'

image = getImageWeb(url)
color = findColor(image)
print(color)
print(rgbToHex(color))


"""
