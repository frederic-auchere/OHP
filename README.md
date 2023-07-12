# Paris-Saclay OHP Summer School 2023

## Equipment

### Hardware

- Telescope: [Skywatcher ESPRIT 100 ED
](https://inter-static.skywatcher.com/upfiles/en_download_caty01390352363.pdf)
- Equatorial mount: [Skywatcher AZ-EQ6](https://inter-static.skywatcher.com/upfiles/en_download_caty01353096919.pdf)
- Camera: [ZWO ASI 2600 MM Cool](https://astronomy-imaging-camera.com/manuals/ASI2600_Manual_EN.pdf)
- Filter wheel: [ZWO EFW](https://astronomy-imaging-camera.com/manuals/EFW%20QuickGuide.pdf)

### Software


## The acquisition chain

The signal S(**x**) measured in DN (Digital Number) by the detector is equal to

S(**x**) = g(**x**) * [ t * ( &#0951; * QE(**x**) * I(**x**) + N(**x**, T) ) + R(**x**) ] + B(**x**)

where:
- **x** is the vector position on the detector.
- I(**x**) is the intensity incident on the detector, in photons per second.
- &#0951; is the quantum yield, *i.e.* the number of photo-electrons created per interacting photon.
- QE(**x**) is the quantum efficiency, *i.e.* the fraction of incident photons interacting with the detector.
- g(**x**) is the gain of the detector, *i.e.* the number of DN per photo-electron.
- N(**x**, T) is the thermal signal, in electrons per second, function of the temperature T.
- t is the exposure time.
- R(**x**) is the read noise, in electrons.
- B(**x**) is the bias of the Analog to Digital Converter(s) (ADC), *i.e.* the output value that corresponds to zero incident intensity, in DN per electron. The bias is set to a positive value to avoid clipping of faint signals to zero.

The above equation can be rewritten:

S(**x**) = g(**x**) * [ t * &#0951; * QE(**x**) * I(**x**) + R(**x**) ] + g(**x**) * t * N(**x**, T) + B(**x**)

At visible wavelengths, the quantum yield &#0951; can be assumed to be equal to 1.

We do not have the capability here to measure the QE, but the relevant quantity for the statistics is I'(**x**) = QE(x) * I(x), *i.e.* the number of detected photons. We thus have 

S(**x**) = g(**x**) * [ t * I'(**x**) + R(**x**) ] + g(**x**) * t * N(**x**, T) + B(**x**)

The objective of the calibration of the detector is to be able to determine I'(**x**) knowing the measure signal S(**x**).

- The last two terms can be measured by taking '[dark frames](darks.ipynb)', *i.e.* images taken without illuminating the detector.

- The gain g(**x**) and read noise R(**x**) can be measured simultaneously using a method called the [Photon Transfer Curve (PTC)](ptc.ipynb) analysis.

- The PTC analysis will typically provide the mean value of the gain over the detector. The pixel-to-pixel variations of the gain are called the '[flat-field](flats.ipynb)' and can be measured using a uniform light source. By extension, the term flat-field is used to describe the combination of all the multiplicative terms that affect the spatial variations of the response of the instrument (*e.g.* the vignetting).  

It is worth noting that thermal electrons cannot be distinguished from photo-electrons. They obey to the same Poisson statistics. 

## Exposure time *vs.* number of images


## Targets

- Messier 31 (galaxy)
- NGC 7000 (emission nebula)
- Veil nebula (supernova remnant)
- Messier 13 (globular cluster).
