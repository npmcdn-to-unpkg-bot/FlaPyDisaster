import gdal
import numpy as np
import os


def list_to_raster(val_array, file_uri, overwrite=False, bands=1):
    if overwrite and os.path.isfile(file_uri):
        os.remove(file_uri)

    cols = val_array.shape[1]
    rows = val_array.shape[0]

    # Create memory raster
    mem_driver = gdal.GetDriverByName('MEM')
    mem_raster = mem_driver.Create('', cols, rows, 4, gdal.GDT_Byte)

    # Write array to memory raster
    outband = mem_raster.GetRasterBand(1)
    outband.WriteArray(val_array)

    # write alpha as 255 if making a 4-band array
    if bands == 4:
        a_band_array = np.full((val_array.shape[0], val_array.shape[1]), 255, dtype=int)
        a_band = mem_raster.GetRasterBand(4)
        a_band.WriteArray(a_band_array)

    # make physical png raster from memory raster
    png_driver = gdal.GetDriverByName('PNG')
    out_raster = png_driver.CreateCopy(file_uri, mem_raster, 0)

    # Explicitly close rasters and bands, might not be necessary
    mem_raster.FlushCache()
    outband.FlushCache()
    out_raster.FlushCache()

