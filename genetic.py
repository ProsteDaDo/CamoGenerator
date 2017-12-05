from PIL import Image
import random
import math
import copy

SmallImageSize = 20
BigImageSize = 200

def evaluate(camoIm, envIm, envW, envH, num = 1):
    results = []

    camoData = camoIm.getdata()

    for i in range(0, num):
        #randX, randY = random.randint(0, envW - BigImageSize), random.randint(0, envH - BigImageSize)
        randX, randY = 500, 500
        randCrop = envIm.crop((randX, randY, randX + BigImageSize, randY + BigImageSize))

        randCropData = randCrop.getdata()
        average = list(map(lambda a, b: math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2), randCropData, camoData))

        results.append(sum(average)/len(average))

    return sum(results)/len(results)


def loadEnvironment(name):
    image = Image.open("environments/" + name)
    image = image.convert("RGB")
    x, y = image.size
    return image, x, y


def randomImage():
    im = Image.new("RGB", (SmallImageSize, SmallImageSize))

    data = []
    for i in range(0, SmallImageSize**2):
        data.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    im.putdata(data)
    im.resize((BigImageSize, BigImageSize), Image.NEAREST)
    return im

def whiteImage():
    return Image.new("RGB", (50, 50), "white")

def updatePattern(im, updateNum, updateAmount):
    imSmall = im.resize((SmallImageSize, SmallImageSize), Image.NEAREST)
    data = list(imSmall.getdata())

    colorShift = (random.randint(-updateAmount, updateAmount), random.randint(-updateAmount, updateAmount), random.randint(-updateAmount, updateAmount))

    for i in range(0, updateNum):
        pixel = random.randint(0, SmallImageSize**2 - 1)
        newPixel = list(data[pixel])

        newPixel[0] += colorShift[0]
        newPixel[0] = max(min(newPixel[0], 255), 0)

        newPixel[1] += colorShift[1]
        newPixel[1] = max(min(newPixel[1], 255), 0)

        newPixel[2] += colorShift[2]
        newPixel[2] = max(min(newPixel[2], 255), 0)

        data[pixel] = tuple(newPixel)


    imSmall.putdata(data)
    im = imSmall.resize((BigImageSize, BigImageSize), Image.NEAREST)
    return im

def geneticPattern(envName, generationNum, patternNum = 100, updateNum = 20, updateAmount = 50):
    patterns = [randomImage() for i in range(0, patternNum)]

    envIm, envW, envH = loadEnvironment(envName)

    for i in range(0, generationNum):
        print("Generation", i)
        patterns.sort(key = lambda x: evaluate(x, envIm, envW, envH, num = 1))

        print(evaluate(patterns[0], envIm, envW, envH, num = 1))

        temp = patterns[0].convert("RGB")
        temp.save("camos/gen" + str(i) + ".png", "PNG")

        patterns = patterns[0:patternNum//2] + copy.deepcopy(patterns[0:patternNum//2])

        for i in range(0, patternNum//2):
            patterns[i] = updatePattern(patterns[i], updateNum, updateAmount)

geneticPattern("forest1.jpg", 1000)

#envIm, envW, envH = loadEnvironment("forest1.jpg")
#camoIm = Image.open("camos/gen0.png")

#print(evaluate(camoIm, envIm, envW, envH, num = 1))
