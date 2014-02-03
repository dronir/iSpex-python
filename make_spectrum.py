#!/usr/bin/env python
#coding: utf8

import numpy as np
import matplotlib.pyplot as plot
import Image
from sys import argv


def spectrum_from_file(filename):
    raw = raw_from_file(filename)
    return spectrum_from_raw(raw)

def curve(x,a=0.00015,b=-120):
    return a*(x+b)**2

def calibration(i):
    a,b = 3.04956866e-01, 3.82033291e+02
    return a*i + b

def reverse_calibration(x):
    a,b = 3.27772287, -1251.98408954
    return int(a*x + b)

def spectrum_from_raw(data):
    height,width = data.shape
    a,b = (0.00015, -120)
    cmax = max(curve(data.shape[1], a, b), curve(0, a, b))
    skip = int(cmax)+1
    N = height-skip
    output = np.zeros(N)
    for i in xrange(N):
        for j in xrange(width):
            di = int(round(curve(j,a,b)))
            output[i] += data[i-di, j]
    idx550 = reverse_calibration(550.0)
    return output / output[idx550]

def raw_from_file(filename):
    box = (1050, 1800, 1400, 2750)
    image = Image.open("test_image.jpg")
    subimage = image.crop(box)
    data = np.asarray(subimage)
    data = data.sum(2)
    return data

def plot_raw(data, spectrum=None):
    if spectrum==None:
        spectrum = spectrum_from_raw(data)

    plot.figure()
    plot.title("Raw data with summation lines")
    plot.imshow(data)
    plot.gray()
    X = np.linspace(0,data.shape[1],1000)
    a,b = (0.00015, -120)
    for i in xrange(10):
        Y = a*(X+b)**2 + 100*i+50
        plot.plot(X,Y.round(),color="blue")
    plot.xlim(0,data.shape[1])
    plot.ylim(0,data.shape[0])
    
    plot.figure()
    plot.title("Spectrum normalized to 550nm")
    plot.xlabel("Wavelength (nm)")
    plot.ylabel("Normalized intensity")
    X = np.arange(len(spectrum))
    X = calibration(X)
    plot.plot(X,spectrum, linewidth=2, color="black")
    plot.xlim(X.min(), X.max())
    plot.show()

def main(filename):
    data = raw_from_file(filename)
    spectrum = spectrum_from_raw(data)
    print "Integral: {}".format(spectrum.sum())
    print "Max peak {} at index {}".format(spectrum.max(), spectrum.argmax())
    plot_raw(data, spectrum)

if __name__=="__main__":
    if len(argv) < 2:
        filename = "test_image.jpg"
    else:
        filename = argv[1]
    main(filename)
    