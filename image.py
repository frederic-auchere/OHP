import os
import inout
from astropy.io import fits


class Image:

    def __init__(self, file):

        self.header = inout.get_headers(file)

        # FITS files
        extension = os.path.splitext(file)[1].upper()
        if extension in ['.FTS', '.FITS', '.FIT']:
            self.data = fits.getdata(file)
        # DSLR files
        elif extension in ['.CR2', '.NEF']:
            self.data = inout.read_raw_dslr(str(file))
        else:
            raise ValueError(f'Unsupported extension: {extension}')
