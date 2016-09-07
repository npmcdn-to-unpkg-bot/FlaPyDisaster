import gdal


def list_to_raster(val_list, file_uri):
    cols = len(val_list[0])
    rows = len(val_list)

    driver = gdal.GetDriverByName('PNG')
    outraster = driver.Create(file_uri, cols, rows, 1, gdal.GDT_Int32)
    outband = outraster.GetRasterBand(1)
    outband.WriteArray(val_list)
    outband.FlushCache()

