import shapely.geometry


def geojson2shp(geojson):
    """Convert geometry of any geojson to a shapely object."""
    if geojson['type'] == 'Feature':
        return geojson2shp(geojson["geometry"])
    elif geojson['type'] == 'FeatureCollection':
        geometries = [geojson2shp(geom) for geom in geojson['features']]
        return shapely.geometry.GeometryCollection(geometries)
    elif geojson['type'] == 'Point':
        return shapely.geometry.Point(geojson['coordinates'])
    elif geojson['type'] == 'MultiPoint':
        points = [
            geojson2shp(dict(type='Point', coordinates=poly))
            for poly in geojson['coordinates']
        ]
        return shapely.geometry.MultiPoint(points)
    elif geojson['type'] == 'LineString':
        return shapely.geometry.LineString(geojson['coordinates'])
    elif geojson['type'] == 'MultiLineString':
        linestrings = [
            geojson2shp(dict(type='LineString', coordinates=poly))
            for poly in geojson['coordinates']
        ]
        return shapely.geometry.MultiLineString(linestrings)
    elif geojson['type'] == 'Polygon':
        return shapely.geometry.Polygon(geojson['coordinates'][0])
    elif geojson['type'] == 'MultiPolygon':
        polygons = [
            geojson2shp(dict(type='Polygon', coordinates=poly))
            for poly in geojson['coordinates']
        ]
        return shapely.geometry.MultiPolygon(polygons)
    elif geojson['type'] == 'GeometryCollection':
        geometries = [geojson2shp(geom) for geom in geojson['geometries']]
        return shapely.geometry.GeometryCollection(geometries)
    else:
        raise Exception('Unknown geojson type: %s' % geojson)
