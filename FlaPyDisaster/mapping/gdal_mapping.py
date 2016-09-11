import gdal
import numpy
import os


def list_to_raster(val_array, file_uri, overwrite=False):
    if overwrite:
        os.remove(file_uri)

    cols = val_array.shape[1]
    rows = val_array.shape[0]

    # Create memory raster
    mem_driver = gdal.GetDriverByName('MEM')
    mem_raster = mem_driver.Create('', cols, rows, 1, gdal.GDT_Byte)

    # Write array to memory raster
    outband = mem_raster.GetRasterBand(1)
    outband.WriteArray(val_array)

    # make physical png raster from memory raster
    png_driver = gdal.GetDriverByName('PNG')
    out_raster = png_driver.CreateCopy(file_uri, mem_raster, 0)

    # Explicitly close rasters and bands, might not be necessary
    mem_raster.FlushCache()
    outband.FlushCache()
    out_raster.FlushCache()

