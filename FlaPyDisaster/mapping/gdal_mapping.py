import gdal
import numpy
import os


def list_to_raster(val_list, file_uri, overwrite=False):
    if overwrite:
        os.remove(file_uri)

    val_array = numpy.array(val_list)
    cols = val_array.shape[1]
    rows = val_array.shape[0]

    driver = gdal.GetDriverByName('MEM')
    png_driver = gdal.GetDriverByName('PNG')
    temp_raster = driver.Create('', cols, rows, 1, gdal.GDT_Byte)

    outband = temp_raster.GetRasterBand(1)
    outband.WriteArray(val_array)
    out_raster = png_driver.CreateCopy(file_uri, temp_raster, 0)
    outband.FlushCache()
    out_raster.FlushCache()

