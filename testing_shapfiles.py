import shapefile as pyshp
import modified_pygmaps as pygmaps
import pyproj

def get_shapes():
	# the_shp=open("Data/Shapefiles/Bos_neighborhoods_new.shp","rb")
	# the_dbf=open("Data/Shapefiles/Bos_neighborhoods_new.dbf","rb")
	# the_shx=open("Data/Shapefiles/Bos_neighborhoods_new.shx","rb")
	# the_shp=open("Data/Shapefiles/CENSUS2010TRACTS_POLY.shp","rb")
	# the_dbf=open("Data/Shapefiles/CENSUS2010TRACTS_POLY.dbf","rb")
	# the_shx=open("Data/Shapefiles/CENSUS2010TRACTS_POLY.shx","rb")
	# the_shp=open("Data/Shapefiles/CENSUS2010BLOCKGROUPS_POLY.shp","rb")
	# the_dbf=open("Data/Shapefiles/CENSUS2010BLOCKGROUPS_POLY.dbf","rb")
	# the_shx=open("Data/Shapefiles/CENSUS2010BLOCKGROUPS_POLY.shx","rb")
	the_shp=open("Data/Shapefiles/CENSUS2010BLOCKS_POLY.shp","rb")
	the_dbf=open("Data/Shapefiles/CENSUS2010BLOCKS_POLY.dbf","rb")
	the_shx=open("Data/Shapefiles/CENSUS2010BLOCKS_POLY.shx","rb")
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

#x,y are in state projection
def convert(x=0,y=0,tup=()):
    if tup!=():
        x,y=tup
    p=pyproj.Proj(init="epsg:2805")
    return p(x,y,inverse=True)

def plot_shape(mymap,shape):
    new_points=[]
    for x,y in shape.points:
        lon,lat=convert(x,y)
        # lat,lon=convert(x,y)
        # print(lat,lon)
        new_points.append((lat,lon))
    mymap.addpath(new_points,"#000000")

def plot_shapes(shape_thing):
    mymap = pygmaps.maps(42.3, -71.1, 16)
    # points=shape_thing.shapes()[0].points
    # print(len(shape_thing.shapes()))
    # print(len(shape_thing.records()))
    print(shape_thing.records()[0])
    # print(shape_thing.records()[0][9])


# !!!TODO:take in geographic data, test to see if block is in boston by checking block is in geographic data file by id2.
# Should really write to file when done.

    # # for i in range(len(shape_thing.records())):
    # for i in range(1):
    # 	data=shape_thing.records()[i]
    # 	lat=float(data[9])
    # 	lon=float(data[10])
    # 	print (lat)
    # 	mymap.addradpoint(lat,lon,2000,"#000000")

    # for shape in shape_thing.shapes()[0:1]:
    #      plot_shape(mymap,shape)
    # mymap.draw('Plots/TestingShapes.html')

shapes=get_shapes()
plot_shapes(shapes)

# mymap = pygmaps.maps(42.3, -71.1, 16)
# mymap.addradpoint(42.3, lon,size, color,opac)