
# iSpex spectral analyser

This is a short python program for turning a picture taken on an iPhone with
the iSpex spectrograph addon into a spectral plot.

## Usage

Take a jpg image using an iPhone with the iSpex device. The script is currently
hard-coded to use the 2448x3264 resolution of the iPhone 4S camera. This means
the pictures must be taken in vertical mode, or rotated afterwards.

Run `python iSpex_spectrum.py image.jpg` to produce the spectral plot.

The code requires NumPy, Matplotlib and the Python Imaging Library PIL (or its
more recent fork, Pillow).

## Calibration

The wavelength calibration is based on photos taken of a fluorescent lamp. It
seems rather unstable, different photos taken of the same lamp produce spectra
with shifts up to tens of nanometres. If you have a better calibration source,
you can try to measure better calibration coefficients (make a pull request if
you do!).

The spectrum is computed simply by integrating pixel values in the image. Since
the iSpex produces a spectrum of colours on the iPhone camera sensor, the
spectra produced by this code are affected by the spectral sensitivity of the
iPhone camera. There is no correction for Bayer filtering etc. either.


## Disclaimer

This code is written only to demonstrate simple principles of spectrometry and
does not produce results precise or accurate enough for scientific or any other
work. If you need a true spectrum, buy a proper spectrometer.
