#!/usr/bin/env python
#coding: utf8

import numpy as np
import matplotlib.pyplot as plot
import Image
from sys import argv

CURVE_A_MIN = 0.00009
CURVE_A_MAX = 0.00010
CURVE_B = 175

def spectrum_from_file(filename):
    raw = raw_from_file(filename)
    return spectrum_from_raw(raw)

def curve(x,a,b):
    return a*(x-b)**2

def calibration(i):
    a,b = 3.04956866e-01, 3.82033291e+02
    return a*i + b

def reverse_calibration(x):
    a,b = 3.27772287, -1251.98408954
    return int(a*x + b)

def spectrum_from_raw(data):
    print "Generating spectrum."
    height,width = data.shape
    a,b = (CURVE_A_MAX, CURVE_B)
    cmax = curve(np.arange(width), a, b).max()
    print cmax
    skip = int(cmax)+1
    N = height-skip
    output = np.zeros((N,2))
    A = np.linspace(CURVE_A_MIN, CURVE_A_MAX, height)
    for i in xrange(N):
        a = A[i]
        for j in xrange(390):
            di = int(round(curve(j,a,b)))
            output[i,0] += data[i+di, j]
        for j in xrange(390,width):
            di = int(round(curve(j,a,b)))
            output[i,1] += data[i+di, j]
    idx550 = reverse_calibration(550.0)
    output[:,0] /= output[idx550,0]
    output[:,1] /= output[idx550,1]
    return output

def raw_from_file(filename):
    print "Loading raw data from {}.".format(filename)
    box = (1050, 1800, 1800, 2850)
    image = Image.open(filename)
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
    b = CURVE_B
    A = np.linspace(CURVE_A_MIN, CURVE_A_MAX, data.shape[0])
    for y in xrange(0, data.shape[0], 50):
        a = A[y]
        Y = a*(X-b)**2 + y
        plot.plot(X,Y.round(),color="white")
    plot.xlim(0,data.shape[1])
    plot.ylim(0,data.shape[0])
    plot.axvline(390)
    
    plot.figure()
    plot.title("Spectrum normalized to 550nm")
    plot.xlabel("Wavelength (nm)")
    plot.ylabel("Normalized intensity")
    X = np.arange(len(spectrum))
    X = calibration(X)
    plot.plot(X,spectrum[:,0], "-", linewidth=2, color="black", label="Wide slit")
    plot.plot(X,spectrum[:,1], ":", linewidth=2, color="black", label="Narrow slit")
    plot.xlim(X.min(), X.max())
    plot.legend()
#    plot.axvline(435.8)
#    plot.axvline(611.6)
#    plot.axvline(487)
    plot.show()

def main(filename):
    data = raw_from_file(filename)
    spectrum = spectrum_from_raw(data)
    print "Integral: {}".format(spectrum.sum())
    print "Max peak {} at index {}".format(spectrum.max(), spectrum.argmax())
    plot_raw(data, spectrum)

if __name__=="__main__":
    if len(argv) < 2:
        filename = "test3.jpg"
    else:
        filename = argv[1]
    main(filename)
    