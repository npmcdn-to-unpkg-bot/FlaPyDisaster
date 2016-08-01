from general.general_objects import BoundingBox
import geojson

# class to mirror javascript leaflet layer server side
class leaflet_layer:
    def __init__(self, **kwargs):
        
        geojson = []

        return super().__init__(**kwargs)

# Class to mirror javascript leaflet map server side
class leaflet_map:
    def __init__(self, **kwargs):

        center_latlng = (0,0)
        zoom = 13
        layers = {}
        return super().__init__(**kwargs)
    
class geojson_geometry:
    """
    Container enum-like class containing the different GeoJSON geometry types
    """
    point = 'point'
    multipoint = 'multipoint'
    line = 'line'
    multiline = 'multiline'
    polygon = 'polygon'
    multipolygon = 'multipolygon'
    geo_feature = 'feature'
    geo_featurecollection = 'featurecollection'

    def get_geometry_names():
        return [point, multipoint, line, multiline, polygon, multipolygon, geo_feature, geo_featurecollection]

def create_feature(geometry, geo_type, val, id = None, color = (255, 0,0), weight = 10, opacity = 1.0):
    """
    :param geometry: Geometry struture that creates geojson string.  Options are:
                     Point: (lng, lat) as tuple
                     MultiPoint: [Point, Point] as array of points
                     Line(string): [Point, Point, Point] as array of points
                     Multiline(string): [Line, Line] as array of lines
                     Polygon without holes: [Point1, Point, Point, Point1] as array of points,
                        first and last point in array are the same point (example makes a triangle).
                    Polygon with hole: [[Point1, Point, Point, Point1], [Point2, Point, Point, Point2]] as array of polygons,
                        second polygon is the hole.
                    Multipolygon: [Polygon, Polygon] as array of polygons (must confirm...?)
    :param geo_type: string indicating the geometry type, must match id strings from class geojson_geometry
    :param val: value to put into properties.value for mapping and style color matching
    :param id - optional: id for the geojson string
    :param color: a 3 value tuple containing an rgb value
    :param weight: for lines/polygons, line width; for points, point size
    :param opacity: opacity of layer in leaflet, 1.0 = 100%, 0 = 0%
    :returns: dictionary with geojson feature string and a leaflet style created from input parameters
    """

    geo = None
    try:
        if (geo_type == geojson_geometry.point):
            geo = geojson.Point(geometry)
        elif (geo_type == geojson_geometry.multipoint):
            geo = geojson.MultiPoint(geometry)
        elif (geo_type == geojson_geometry.line):
            geo = geojson.LineString(geometry)
        elif (geo_type == geojson_geometry.multiline):
            geo = geojson.MultiLineString(geometry)
        elif (geo_type == geojson_geometry.polygon):
            geo = geojson.Polygon(geometry)
        elif (geo_type == geojson_geometry.multipolygon):
            geo = geojson.MultiPolygon(geometry)
        else:
            print ("Unsupported geometry type: " + geo_type)
            return
    except Exception as e:
        print (e + "\n probably wrong input data structure for " + geo_type)
        return
    
    style = None # leaflet_style_creator()
    geo = geojson.Feature(id = id, geometry = geo, properties = {"value":val})

    ret = {}
    ret['geojson'] = geo
    ret['style'] = style

    return ret
