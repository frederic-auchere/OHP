# Paris-Saclay OHP Summer School 2023

## America / Pelican challenge

Our objective will be to build collectively images of the [NGC 7000](https://en.wikipedia.org/wiki/North_America_Nebula) / [IC 5070 / IC 5067](https://en.wikipedia.org/wiki/Pelican_Nebule) complex, *a.k.a.* the North America and Pelican nebulae. We will acquire and reduce the data necessary to produce an image in 'natural' RGB colors (similar to the one below, but at higher resolution) and in 'false color' narrow band (SII, H&#0945;, OII, similar to [this](https://en.wikipedia.org/wiki/North_America_Nebula#/media/File:NANeb3PS23_SCNR.jpg)).

**The challenge will be to collectively accumulate as many hours of exposure as possible to assemble the best final images**.  

![](ngc7000.jpg)
ESPRIT 100 ED / Canon EOS 6D / 10 hours

Beyond making pretty pictures, our objective will be to understand the data acquisition chain and the calibration process. This will be performed using a [refracting telescope](https://en.wikipedia.org/wiki/Refracting_telescope), a camera and filters, all commercially available. We will measure the physical properties of the [CMOS sensor](https://en.wikipedia.org/wiki/Active-pixel_sensor), understand the sources of noise in the data, and derive the optimum acquisition parameters. The principles and methods exposed are generic and applicable to amateur equipment and professional giant telescopes alike.

Using Python notebooks, we will

- Determine the optimal bias of the camera ([notebook](bias.ipynb))
- Measure the dark signal of the sensor ([notebook](darks.ipynb))
- Measure the flat field of the system ([notebook](flats.ipynb))
- Measure the read noise of the camera (in electrons) ([notebook](ptc.ipynb))
- Measure the gain of the camera (in electrons / DN) ([notebook](ptc.ipynb))
- Measure the sky background (in electrons) ([notebook](sky.ipynb))
- Determine the optimal exposure time ([notebook](exposure.ipynb))

Then, using ([Siril](https://www.siril.org/), [old website](https://free-astro.org/index.php?title=Siril)), we will
- Stack the individual frames 
- Composite the channels into color pictures

## 1. Equipment

### 1.1 Hardware

- Refracting telescope: [Skywatcher ESPRIT 100 ED
](https://inter-static.skywatcher.com/upfiles/en_download_caty01390352363.pdf)
- Equatorial mount: [Skywatcher AZ-EQ6](https://inter-static.skywatcher.com/upfiles/en_download_caty01353096919.pdf)
- Camera: [ZWO ASI 2600 MM Cool](https://i.zwoastro.com/zwo-website//manuals/ZWO_ASI_Cooled_Cameras_Quick_Guide.pdf)
- Filter wheel: [ZWO EFW](https://astronomy-imaging-camera.com/manuals/EFW%20QuickGuide.pdf)
- Filters: broad band [Luminance, Red, Green, Blue](https://www.baader-planetarium.com/en/filters/l-rgb-cmos-filters/baader-lrgb-filter-set-%E2%80%93-cmos-optimized.html) and narrow band (6 nm) [SII, H&#0945;, OIII](
https://www.baader-planetarium.com/en/filters/(ultra-)-narrowband-/-highspeed/baader-6.5nm-narrowband-filter-set-%E2%80%93-cmos-optimized-(h-alpha--o-iii--s-ii).html)
- Guide telescope: [EVO guide 50 mm](https://www.pierro-astro.com/materiel-astronomique/autoguidage/lunette-guide-50mm-evoguide-50ed-avec-support-queue-daronde-vixen-m%C3%A2le-sky-watcher_detail) with [field flattener](https://www.pierro-astro.com/materiel-astronomique/autoguidage/correcteur-de-champ-pour-lunette-sky-watcher-evoguide50-sky-watcher-7135_detail) and [ASI 178 MM](https://i.zwoastro.com/zwo-website/manuals/ZWO_Uncooled_Camera_Quick_Guide.pdf) camera 

### 1.2 Software

- Equatorial mount driver: [EQASCOM](https://eq-mod.sourceforge.net/eqaindex.html) 
- Sequencer: [Nightime Imaging 'n' Astronomy (NINA)](https://nighttime-imaging.eu/)

### 1.3 Notes on the acquisition setup

#### 1.3.1 Plate scale

Given the pixel size of 3.76 &#0956;m, and the [measured focal length](https://www.astrobin.com/forum/c/astrophotography/equipment/what-is-the-focal-length-of-my-esprit-100ed/) of the telescope is 555 mm (larger than the listed value by 1%), the plate scale of the setup is 

3600 * &#0960; atan( 0.00376 / 555 ) / 180 = 1.397" / pixel

#### 1.3.2 Angular resolution

The angular resolution is given by the diameter of the [Airy disk](https://en.wikipedia.org/wiki/Airy_disk)

r = 1.22 &#0955; / D

with D = 0.1 m the diameter of the objective lens. In the green (530 nm), this corresponds to about 1.3". However, the typical seeing (from atmospheric turbulence) is about 2" to 3" rms, which thus drives the resolution. In addition, the tracking errors of the equatorial mount are of the order of 1" rms. Taking the quadratic sum of the three contributors, we get the effective width of the [Point Spread Function](https://en.wikipedia.org/wiki/Point_spread_function) (PSF).

| Filter   | &#0955; [nm] | Optical r ["] | 2" seeing r ["] | 3" seeing r ["] |
|----------|--------------|---------------|-----------------|-----------------|
| B        | 460          | 1.16          | 2.52            | 3.37            |
| OIII     | 496 / 501    | 1.25 / 1.26   | 2.56 / 2.57     | 3.40 / 3.40     |
| G        | 530          | 1.33          | 2.60            | 3.43            |
| R        | 640          | 1.61          | 2.75            | 3.55            |
| H&#0945; | 656          | 1.65          | 2.78            | 3.57            |
| SII      | 672          | 1.69          | 2.80            | 3.59            |

While the optical resolution values differ by 45%, the effective resolution varies by 11% with 2" seeing and by 6% with 3". At 2" seeing, the system does not satisfy the
[Nyquist–Shannon sampling theorem](https://en.wikipedia.org/wiki/Nyquist%E2%80%93Shannon_sampling_theorem), which requires a sampling of 1.2" / pixel in the blue. 

#### 1.3.3 Tracking

The equatorial mount is tracking very accurately, with compensation of the periodic error down to ~2" rms. Without active guiding, long exposures would be affected by drift caused by polar alignment errors, refraction & mechanical deformations. The measured drift rate is typically 0.5" / minute. If we allow a total drift during an exposure to be 1/10th the PSF (so that the effect is negligible), the exposure time is limited to 30s with 2" seeing. Exposures of 90s induce a drift of ~1/3 PSF with 2" seeing, which can be marginally acceptable.

#### 1.3.4 Guiding

Active guiding is provided by a 50 mm diameter, F/4.8 guide telescope equipped with a field flattener and an AZI 178 mono camera. The guiding error is systematically < 1" rms, down to 0.6" rms in good conditions.

## 2. The acquisition chain

The signal S(**x**) measured in DN (Digital Number, *a.k.a.* ADU, Analog to Digital Unit) by the detector is equal to

S(**x**) = g(**x**) * [ t * ( Q(**x**, &#0955;) * I(**x**) + N(**x**, T) ) + R(**x**) ] + B(**x**)

where:
- **x** is the vector position on the detector.
- &#0955; is the wavelength.
- I(**x**) is the intensity incident on the detector, in photons per second.
- Q(**x**, &#0955;) is the [external quantum efficiency](https://en.wikipedia.org/wiki/Quantum_efficiency) (EQE), *i.e.* the number of photo-electrons created per incident photon.
- g(**x**) is the gain of the detector, *i.e.* the number of DN per photo-electron.
- N(**x**, T) is the thermal signal, function of the temperature T, in electrons per second.
- t is the exposure time, in seconds.
- R(**x**) is the read noise, in electrons.
- B(**x**) is the bias of the Analog to Digital Converter(s) (ADC), *i.e.* the output value that corresponds to zero incident intensity, in DN per electron. The bias is set to a positive value to avoid clipping of faint signals to zero.

It is important to note that for a given pixel, I(**x**), N(**x**, T) and R(**x**) are functions of time because of the statistical fluctuations of the photon and thermal signals, and because of the noise in the readout electronics. I, N and R must thus be understood as random variables. It is worth noting that thermal electrons cannot be distinguished from photo-electrons. They obey to the same [Poisson statistics](https://en.wikipedia.org/wiki/Poisson_distribution).

The above equation can be rewritten:

S(**x**) = g(**x**) * [ t * Q(**x**) * I(**x**) + R(**x**) ] + g(**x**) * t * N(**x**, T) + B(**x**)

The relevant quantity to compute the [shot noise](https://en.wikipedia.org/wiki/Shot_noise) in the image is E(**x**) = EQE(x) * I(x), *i.e.* the number of electrons, which is what is effectively counted by the sensor. We thus have 

S(**x**) = g(**x**) * [ t * E(**x**) + R(**x**) ] + g(**x**) * t * N(**x**, T) + B(**x**)

The objective of the calibration of the detector is to invert the above equation to be able to determine E(**x**) knowing the measured signal S(**x**). As mentioned above, N and R are random variables. As such, it is impossible to know the exact value taken by each one during a given data acquisition. All we can determine - and correct for - is the mean (denoted <>) of these random variables. In addition, we note that the read noise R(**x**) has zero mean. We can thus now write the calibration equation as 

E(**x**) = { S(**x**) - [ g(**x**) * t * < N >(**x**, T) + B(**x**) ] } / [ g(**x**) * t ]

or, with D(**x**) = g(**x**) * t * < N >(**x**, T) + B(**x**)

E(**x**) = [ S(**x**) - D(**x**) ] / [ g(**x**) * t ]


- D(**x**), sum of the thermal signal and [bias](bias.ipynb), can be measured by taking '[dark frames](darks.ipynb)', *i.e.* images taken without illuminating the detector.

- The gain g(**x**) and read noise R(**x**) can be measured simultaneously using a method called the [Photon Transfer Curve (PTC)](ptc.ipynb) analysis. Although the read noise does not appear in the calibration equation, it is an important quantity to determine to choose the optimal acquisitaion parameters and to reduce the data.  

- The PTC analysis will typically provide the mean value of the gain over the detector. The pixel-to-pixel variations of the gain g(**x**) are called the '[flat-field](flats.ipynb)' and can be measured using a uniform light source. By extension, the term flat-field is used to describe the combination of all the multiplicative terms that affect the spatial variations of the response of the instrument (*e.g.* the [vignetting](https://en.wikipedia.org/wiki/Vignetting)).  

## 3. Choosing the optimal acquisition parameters

### 3.1 Bias

The bias of the ADC needs to be chosen so that the values are not clipped due to random fluctuations of the signal around zero. This will be looked at in the [bias notebook](bias.ipynb). 

### 3.2 Gain

Looking at the characteristics of the [ZWO ASI 2600 MM Cool](https://astronomy-imaging-camera.com/manuals/ASI2600_Manual_EN.pdf), the 'gain' setting of 100 is a good compromise between dynamic range and read noise. Note that this 'gain' value of 100 is *not* the gain as defined above. It is a setting value in arbitrary units, to which corresponds a true gain (as expressed in DN / electron), as measured in the [ptc](ptc.ipynb) notebook.

### 3.3 Exposure time

Deep sky objects require long exposures, typically several hours. One could either take a single very long exposure, or take multiple shorter exposures and sum (or stack) them up to the same equivalent total exposure time:

- A single frame is in theory the best in terms of noise (see below), but requires perfect guiding and will be ruined by trails from planes and satellites, and possibly by clouds.
- Stacking multiple images will result in more noise (see below), but guiding does not have to be as good, and trails can easily be removed in post-processing.

As demonstrated in the [exposure time](exposure.ipynb) notebook, there is an objective way to determine the optimal exposure for individual frames in the stack.

### 3.4 Sensor temperature

The sensor temperature is chosen so that the thermal signal is negligible compared to that from the sky background. from the [ASI 2600 datasheet](https://astronomy-imaging-camera.com/manuals/ASI2600_Manual_EN.pdf), we choose to operate at -5°C, which corresponds to 0.001 electron / s, *i.e.* ~20 times lower than the [sky brightness](sky.ipynb) in narrowband images.
