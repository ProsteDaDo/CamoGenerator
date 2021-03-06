from PIL import Image
import random
import math
import copy


SMALL_IMAGE_SIZE = 20
BIG_IMAGE_SIZE = 200

def evaluate(camoIm, envIm, envW, envH, num=1):
    results = []

    camoData = camoIm.getdata()

    for i in range(0, num):
        #randX, randY = random.randint(0, envW - BigImageSize), random.randint(0, envH - BigImageSize)
        randX, randY = 500, 500
        randCrop = envIm.crop((randX, randY, randX + BIG_IMAGE_SIZE, randY + BIG_IMAGE_SIZE))

        randCropData = randCrop.getdata()
        average = list(map(lambda a, b: math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2), randCropData, camoData))

        results.append(sum(average)/len(average))

    return sum(results)/len(results)


def load_environment(name):
    image = Image.open("environments/" + name)
    image = image.convert("RGB")
    x, y = image.size
    return image, x, y


def random_image():
    im = Image.new("RGB", (SMALL_IMAGE_SIZE, SMALL_IMAGE_SIZE))

    data = []
    for i in range(0, SMALL_IMAGE_SIZE**2):
        data.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    im.putdata(data)
    im.resize((BIG_IMAGE_SIZE, BIG_IMAGE_SIZE), Image.NEAREST)
    return im

def white_image():
    return Image.new("RGB", (50, 50), "white")

def update_pattern(im, updateNum, updateAmount):
    imSmall = im.resize((SMALL_IMAGE_SIZE, SMALL_IMAGE_SIZE), Image.NEAREST)
    data = list(imSmall.getdata())

    colorShift = (random.randint(-updateAmount, updateAmount), random.randint(-updateAmount, updateAmount), random.randint(-updateAmount, updateAmount))

    for i in range(0, updateNum):
        pixel = random.randint(0, SMALL_IMAGE_SIZE ** 2 - 1)
        newPixel = list(data[pixel])

        newPixel[0] += colorShift[0]
        newPixel[0] = max(min(newPixel[0], 255), 0)

        newPixel[1] += colorShift[1]
        newPixel[1] = max(min(newPixel[1], 255), 0)

        newPixel[2] += colorShift[2]
        newPixel[2] = max(min(newPixel[2], 255), 0)

        data[pixel] = tuple(newPixel)


    imSmall.putdata(data)
    im = imSmall.resize((BIG_IMAGE_SIZE, BIG_IMAGE_SIZE), Image.NEAREST)
    return im

def genetic_pattern(envName, generationNum, patternNum = 100, updateNum = 20, updateAmount = 50):
    patterns = [random_image() for i in range(0, patternNum)]

    envIm, envW, envH = load_environment(envName)

    for i in range(0, generationNum):
        print("Generation", i)
        patterns.sort(key=lambda x: evaluate(x, envIm, envW, envH, num=1))

        print(evaluate(patterns[0], envIm, envW, envH, num=1))

        temp = patterns[0].convert("RGB")
        temp.save("camos/gen" + str(i) + ".png", "PNG")

        patterns = patterns[0:patternNum//2] + copy.deepcopy(patterns[0:patternNum//2])

        for i in range(0, patternNum//2):
            patterns[i] = update_pattern(patterns[i], updateNum, updateAmount)

genetic_pattern("forest1.jpg", 1000)

#envIm, envW, envH = loadEnvironment("forest1.jpg")
#camoIm = Image.open("camos/gen0.png")

#print(evaluate(camoIm, envIm, envW, envH, num = 1))
