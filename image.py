import os
import inout
from astropy.io import fits


class Image:

    def __init__(self, file, use_libraw=True):

        self.header = inout.get_headers(file)

        # FITS files
        extension = os.path.splitext(file)[1].upper()
        if extension in ['.FTS', '.FITS', '.FIT']:
            self.data = fits.getdata(file)
        # DSLR files
        elif extension in inout.RAW_EXTENSIONS:
            self.data = inout.read_raw_dslr(str(file), use_libraw=use_libraw)
        else:
            raise ValueError(f'Unsupported extension: {extension}')
