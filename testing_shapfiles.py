import shapefile as pyshp
import modified_pygmaps as pygmaps
import pyproj
import pandas
import pickle

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
	print("Read shapefile")
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

def check_geoids(geoids,shape_file):
	records=shape_file.records()
	G_INDEX=4
	if shape_file.fields[G_INDEX+1][0]=='GEOID10':
		print("CHECK")
	else:
		print("INVALID")
#154621
#8841
	to_return=[]
	indexes=[]
	i=123204
	j=0
	print(shape_file.records()[123214][G_INDEX])
	for record in shape_file.records()[123204:134510]:
		if int(record[G_INDEX]) in geoids:
			indexes.append(i)
		i+=1

	# to_return.append(shape_file.shapes()[i])
		
	
	print("max "+str(max(indexes)))
	print("min "+str(min(indexes)))
	print(len(indexes))

	pickle_file=open("Data/pickle_shape.p","wb")
	shapes=shape_file.shapes()
	i=0
	for index in indexes:
		to_return.append((records[index][G_INDEX],shapes[index].points))
		i+=1
	pickle.dump(to_return,pickle_file)


	# print(shape_file.fields)
	# print(type(shape_file.records()[3][3]))
	# print(shape_file.records()[4])

def print_status(cur,total):
	print(str(cur/total))

def read_geo():
    df=pandas.DataFrame.from_csv("Data/Census_GEOID.csv")
    print("Read Geoid File")
    return df.index.get_values()

def plot_shapes(shape_thing):
    mymap = pygmaps.maps(42.3, -71.1, 16)

def convert_one(datum):
	points=datum[1]
	new_points=[]
	for pair in points:
		lat,lon=convert(pair[0],pair[1])
		new_points.append((lon,lat))
	return (datum[0],new_points)

def convert_pickle():
	pickle_file=open("Data/pickle_shape.p","rb")
	convert_file=open("Data/pickle_convert.p","wb")
	# pickle file is a list of tuples
	# each tuple contains geoid and a list of list state proj pairs . 
	boston_blocks=pickle.load(pickle_file)
	convert_blocks=[]
	for block in boston_blocks:
		convert_blocks.append(convert_one(block))
	pickle.dump(convert_blocks,convert_file)
	pickle_file.close()
	convert_file.close()


# shape_file=get_shapes()
# geoids=read_geo()
# check_geoids(geoids,shape_file)
convert_pickle()