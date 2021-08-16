from PIL import Image
import requests
import time

from requests.models import RequestEncodingMixin

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

    def weightedCount(self):
        blackSum = 150
        wCount = self.count
        if (self.bmax + self.gmax + self.rmax) < blackSum:
            wCount *= ((self.bmax + self.gmax + self.rmax)/blackSum)

        whiteSum = 650
        if (self.bmax + self.gmax + self.rmax) > whiteSum:
            wCount *= (whiteSum/(self.bmax + self.gmax + self.rmax))
        

        return wCount
        
    
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
    time.sleep(1)
    image = Image.open(rawData)
    return image
    

def getImageLocal(fileLoc):
    image = Image.open(fileLoc)
    return image

def analyseImage(image,res = 100):
    width, height = image.size
    pixelCount = int((width*height)/30)
    print(pixelCount)
    pixels = getPixelSample(image,pixelCount)
    allBuckets = createBuckets()

    for p in pixels:
        for b in allBuckets:
            b.eval(p)
    
    total = 0
    activeBuckets = []
    for b in allBuckets:
        if b.count > 0:
            total += b.count
            activeBuckets.append(b)

    for b in activeBuckets:
        print("Percent: "+str(100.0*(b.count/total))+"% Count: "+str(b.count)+" "+str(b.rmin)+","+str(b.gmin)+","+str(b.bmin))

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
        #if b.count > maxBucket.count: 
        if b.weightedCount() > maxBucket.weightedCount():
            maxBucket = b

    return maxBucket.getAverage()

def colorSum(colorTuple):
    return colorTuple[0]+colorTuple[1]+colorTuple[2]

def findSecondary(image, primaryTuple):
    pixels = getPixelSample(image)
    allBuckets = createBuckets()
    maxSum = 255*3
    primarySum = colorSum(primaryTuple)
    neededDiv = 100*((2.6*maxSum)/(maxSum + primarySum))
    #print(neededDiv)
    rangeControl = 4
    rangeLimit = (primarySum/30) + rangeControl + 1
    #print("range limit "+str(rangeLimit))
    passed = False
    while not passed:
        blackoutRange = int(maxSum/rangeControl)
        blackoutMin = primarySum - blackoutRange
        blackoutMax = primarySum + blackoutRange
        rMin = primaryTuple[0] - blackoutRange/2
        rMax = primaryTuple[0] + blackoutRange/2
        gMin = primaryTuple[1] - blackoutRange/2
        gMax = primaryTuple[1] + blackoutRange/2
        bMin = primaryTuple[2] - blackoutRange/2
        bMax = primaryTuple[2] + blackoutRange/2
        #print("prime:"+str(primarySum)+" max:"+str(blackoutMax)+" min:"+str(blackoutMin))

        for p in pixels:
            for b in allBuckets:
                bColor = (b.rmax,b.gmax,b.bmax)
                bSum = colorSum(bColor)
                if (not ((bSum > blackoutMin) and (bSum < blackoutMax))) or \
                    ((not ((b.rmax > rMin) and (b.rmax < rMax))))or\
                        ((not ((b.gmax > gMin) and (b.gmax < gMax))))or\
                            ((not ((b.bmax > bMin) and (b.bmax < bMax)))):
                    b.eval(p)

        maxBucket = allBuckets[0]
        for b in allBuckets:
            if b.weightedCount() > maxBucket.weightedCount():
                maxBucket = b
        if maxBucket.count >= (len(pixels)/neededDiv):
            passed = True
            #print(maxBucket.count)
            secondaryColor = maxBucket.getAverage()
        rangeControl += 1
        if rangeControl > rangeLimit:
            secondaryColor = defaultSecondary(primaryTuple)
            passed = True
    
    return secondaryColor
    

def defaultSecondary(colorTuple):
    if colorSum(colorTuple) > 650: 
        default = (200, 200, 200)
    elif colorSum(colorTuple) < 150:
        default = (90, 90, 90)
    else:
        default = (255, 255, 255)
    return default


def getPixelSample(image,sampleSize = 5000):
    # pass Image.open() object
    width, height = image.size
    
    #print(str(width) + " x " + str(height))
    #print(image.mode)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    pixelGrid = image.load()
    
    #print(pixelGrid[0,0])
    pixels = []
    x = 0
    y = 0
    sampleRate = int((height*width)/sampleSize)
    print(sampleRate)
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

