import io
from sys import platform
import rawpy
from exiftool import ExifToolHelper
from astropy.io import fits
import os
import time
import subprocess
from PIL import Image
import numpy as np


if platform.startswith('win'):
    STRINGS_ENCODING = 'ansi'
elif platform.startswith('linux'):
    STRINGS_ENCODING = 'utf-8'
else:
    STRINGS_ENCODING = 'utf-8'

FITS_EXTENSIONS = ['.FITS', '.FTS', '.FIT']
RAW_EXTENSIONS = ['.CR2', '.CR3', '.ARW', '.NEF', '.RW2', '.DNG']


def get_headers(files):

    fits_extensions = FITS_EXTENSIONS

    if type(files) == str:
        f = files
        files = [files]
    else:
        f = files[0]
    _, extension = os.path.splitext(f)
    extension = extension.upper()

    if extension in RAW_EXTENSIONS:
        exif_data = get_exif_data(files)
        headers = exif2fitshead(exif_data)
    elif extension in fits_extensions:
        headers = [fits.getheader(f) for f in files]
    else:
        raise ValueError('get_headers: unknown extension: ' + extension)

    return headers


def exif2fitshead(exifdata):

    if type(exifdata) == dict:
        exifdata = [exifdata]

    headers = []
    for exif_tags in exifdata:
        header = fits.Header()

        # For EOS6D, 'EXIF:DateTimeOriginal' contains start of exposure, i.e.
        # after the mirror holding time (tested with 30 seconds hold before
        # 30 seconds exposure)
        if 'EXIF:DateTimeOriginal' in exif_tags:
            isodate = exif_tags['EXIF:DateTimeOriginal'] + '.'
            if 'EXIF:SubSecTimeOriginal' in exif_tags:
                isodate += '{:02}'.format(int(exif_tags['EXIF:SubSecTimeOriginal']))
                isodate = isodate.replace(':', '-', 2)
            header['DATE-OBS'] = (isodate, 'Date and time of image start')

        # For EOS6D, 'EXIF:ExposureTime' contains the exposure time not
        # including the mirror holding time (tested with 30 seconds hold before
        # 30 seconds exposure)
        if 'EXIF:ExposureTime' in exif_tags:
            header['EXPTIME'] = (exif_tags['EXIF:ExposureTime'], 'Exposure Time')
        if 'EXIF:ISO' in exif_tags:
            header['ISO'] = (exif_tags['EXIF:ISO'], 'ISO number')
        if 'MakerNotes:CameraTemperature' in exif_tags:
            if 'MakerNotes:CameraTemperature' in exif_tags:
                header['TEMP'] = (exif_tags['MakerNotes:CameraTemperature'], 'DIGIC processor temperature')
        if 'MakerNotes:CameraOrientation' in exif_tags:
            header['CAMORIEN'] = (exif_tags['MakerNotes:CameraOrientation'], 'Camera orientation')

        headers.append(header)

    if len(headers) == 1:
        headers = headers[0]

    return headers


def get_exif_data(files, exif=None):

    """
    Reads EXIF data using the exiftool utility
    """

    if exif is None:
        exifprocess = ExifToolHelper()
        exifprocess.run()
    else:
        if not exif.running:
            raise RuntimeError('io.get_exif_data: exif process not running')
        exifprocess = exif

    tags = exifprocess.get_metadata(files)

    if exif is None:
        exifprocess.terminate()

    return tags


def read_raw_dslr(file,
                  verbose=False,
                  use_libraw=True,
                  roi=None,
                  dtype=np.uint16):

    """
    Reads RAW (e.g .CR2) files using libraw or dcraw
    """

    if verbose:
        t0 = time.time()

    if os.path.isfile(file) and os.access(file, os.R_OK):

        if use_libraw:

            with rawpy.imread(file) as data:

                if roi is None:
                    y0 = data.sizes.top_margin
                    y1 = y0 + data.sizes.raw_height
                    x0 = data.sizes.left_margin
                    x1 = x0 + data.sizes.raw_width
                else:
                    y0 = data.sizes.top_margin + roi[0]
                    y1 = y0 + (roi[1] - roi[0] + 1)
                    x0 = data.sizes.left_margin + roi[2]
                    x1 = x0 + (roi[3] - roi[2] + 1)

                # # This makes a copy of the array (astype), even if from int to int
                # # otherwise the reference to full_frame is lost after lib.close()
                frame = data.raw_image[y0:y1, x0:x1].astype(dtype)

            return frame

        else:
            p = subprocess.Popen(["dcraw",
                                  "-c",  # Write image data to standard output
                                  "-T",  # Writes TIFF instead of PPM
                                  "-D",  # Document mode without scaling (totally raw)
                                  "-4",  # Linear 16 bits, same as "-6 -W -g 1 1"
                                  file],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

            try:
                outs, errs = p.communicate(timeout=15)
            except TimeoutError:
                p.kill()
                outs, errs = p.communicate()

            p.wait()

            raw = np.array(Image.open(io.BytesIO(outs)))

            return raw.astype(dtype)

    else:

        raise FileNotFoundError('read_raw_dslr: ' + file + ' not found')


def save_calibration_frame(filename, data, dictionary):
    header = fits.Header()
    header.update(dictionary)
    fits.writeto(filename, data, header, overwrite=True)
