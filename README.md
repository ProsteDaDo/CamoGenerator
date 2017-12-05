# CamoGenerator
Program for generating camouflage patterns from photos

## Introduction

Here are my experiments with generating camouflage patterns from photos. These are just scripts I thought would work (some didn't).

### Scripts

#### Genetic
* genetic.py
* attempt to use genetic algorithm
* evaluation function was sum of color differences with photos at random positions
* absolute failure

#### Average
* averageModus.py
* script takes n random big cutouts and m random small cutouts of photos and averages color of pixels at same coordinates
* fairly good

#### Modus
* averageModus.py
* similar to Average, but takes most common color at same coordinates
* reduces number of colors using threshold
  * new_R = R - R mod threshold + threshold/2, where R is brightness of pixel in red channel
  * same for blue and green
* best resuts so far

## TODO

* add example images
* genetic.py and averageModus.py need a lot of refactoring
  * separate averageModus.py in two
* make some "main" function that take some config file and runs particular script with set parameters
* create GUI with preview and settings and stuff
