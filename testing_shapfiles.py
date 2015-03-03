import shapefile as pyshp
import modified_pygmaps as pygmaps
import pyproj

def get_shapes():
	# the_shp=open("Data/Shapefiles/Bos_neighborhoods_new.shp","rb")
	# the_dbf=open("Data/Shapefiles/Bos_neighborhoods_new.dbf","rb")
	# the_shx=open("Data/Shapefiles/Bos_neighborhoods_new.shx","rb")
	the_shp=open("Data/Shapefiles/CENSUS2010TRACTS_POLY.shp","rb")
	the_dbf=open("Data/Shapefiles/CENSUS2010TRACTS_POLY.dbf","rb")
	the_shx=open("Data/Shapefiles/CENSUS2010TRACTS_POLY.shx","rb")
	r= pyshp.Reader(shp=the_shp,dbf=the_dbf,shx=the_shx)
	return r	

def point_in_poly(x,y,poly):

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

#x,y are in 
def convert(x,y):
    p=pyproj.Proj(init="epsg:2805")
    return p(x,y,inverse=True)



def plot_shapes(shape_thing):
    points=shape_thing.shapes()[0].points
    converted_points=[]

    for x,y in points:
        converted_points.append(convert(x,y))
    print(converted_points)

shapes=get_shapes()
plot_shapes(shapes)

# mymap = pygmaps.maps(42.3, -71.1, 16)
# mymap.addradpoint(42.3, lon,size, color,opac)