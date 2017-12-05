from PIL import Image
import random


SMALL_TILE_SIZE = 20
BIG_TILE_SIZE = 300

SMALL_TILE_NUMBER = 20
BIG_TILE_NUMBER = 10

FINAL_SIZE = 200


def averagePixels(a):
    pixel = [0, 0, 0]

    for i in a:
        pixel[0] += i[0]
        pixel[1] += i[1]
        pixel[2] += i[2]

    pixel[0] = pixel[0] // len(a)
    pixel[1] = pixel[1] // len(a)
    pixel[2] = pixel[2] // len(a)

    return tuple(pixel)

def modusPixels(a, threshold = 32):
    pixel = {}

    for i in a:
        reducedColor = [((i[0]+1) // threshold) * threshold, ((i[1]+1) // threshold) * threshold, ((i[2]+1) // threshold) * threshold]
        reducedColor[0] += threshold // 2
        reducedColor[1] += threshold // 2
        reducedColor[2] += threshold // 2
        reducedColor = tuple(reducedColor)

        if reducedColor not in pixel.keys():
            pixel[reducedColor] = 1
        else:
            pixel[reducedColor] += 1

    return max(pixel.items(), key = lambda x: x[1])[0]

images = [Image.open("environments/desert/desert1.jpg"),
          Image.open("environments/desert/desert2.jpg"),
          Image.open("environments/desert/desert3.jpg"),
          Image.open("environments/ceskeSvycarsko/forest1.jpg"),
          Image.open("environments/ceskeSvycarsko/forest2.jpg"),
          Image.open("environments/ceskeSvycarsko/forest3.jpg")]


tiles = []
for im in images:
    for i in range(0, SMALL_TILE_NUMBER):
        x = random.randint(0, im.size[0] - SMALL_TILE_SIZE)
        y = random.randint(0, im.size[1] - SMALL_TILE_SIZE)
        tile = im.crop((x, y, x + SMALL_TILE_SIZE, y + SMALL_TILE_SIZE))
        tile = tile.resize((FINAL_SIZE, FINAL_SIZE))
        tiles.append(list(tile.getdata()))

for im in images:
    for i in range(0, BIG_TILE_NUMBER):
        x = random.randint(0, im.size[0] - BIG_TILE_SIZE)
        y = random.randint(0, im.size[1] - BIG_TILE_SIZE)
        tile = im.crop((x, y, x + BIG_TILE_SIZE, y + BIG_TILE_SIZE))
        tile = tile.resize((FINAL_SIZE, FINAL_SIZE))
        tiles.append(list(tile.getdata()))
"""
for im in images:
    for x in range(0, im.size[0] - TILE_SIZE, TILE_SIZE):
        for y in range(0, im.size[1] - TILE_SIZE, TILE_SIZE):
            tiles.append(list(im.crop((x, y, x + TILE_SIZE, y + TILE_SIZE)).getdata()))"""

tiles = list(zip(*tiles))
tilesAverage = [modusPixels(x) for x in tiles]

im2 = Image.new("RGB", (FINAL_SIZE, FINAL_SIZE))
im2.putdata(tilesAverage)

im2.save("camos/modpatTest.png")
