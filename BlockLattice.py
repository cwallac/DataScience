import pickle
import modified_pygmaps as pygmaps
import pandas
import matplotlib as mat
import numpy 
import math

class BlockLattice(object):

	def __init__(self,block_source="Data/pickle_convert.p"):
		self.read(block_source)

	def read(self,source):
		the_file=open(source,"rb")
		self.inner_rep=pickle.load(the_file)

	def map_lattice(self,output):
		mymap = pygmaps.maps(42.3, -71.1, 16)
		for block_info in self.inner_rep:
			path=block_info[1]
			mymap.addpath(path,"#000000")
		mymap.draw(output)

	def add_overlay(self,overlay):
		self.over_data=overlay.data

	def color_choose(self,num,max_num):
		return mat.colors.rgb2hex(mat.colors.hsv_to_rgb((((1-(num/max_num))*.5),1,1)))
	

	def map_overlay(self,output):
		if (self.over_data==None):
			self.map_lattice(output)
		else:
			mymap = pygmaps.maps(42.3, -71.1, 16)
			for block_info in self.inner_rep:
				path=block_info[1]
				over_val=self.over_data[int(block_info[0])]
				# mymap.add_point(path[0][0],path[0][1], "#0000FF",str(over_val))
				mymap.addpolygon(path,color=self.color_choose(over_val,2672))
			mymap.draw(output)

class Overlay(object):
	def __init__(self,data_source):
		self.data={}
	
	#read data is required to take a source and compute a 
	#dictionary of string geoid to num value
	def read_data(self,source):
		raise UnimplementedMethodException()	

class PopOverlay(Overlay):
	def __init__(self,data_source):
		# super.__init__(self,data_source)
		self.read_data(data_source)

	def read_data(self,source):
		df=pandas.DataFrame.from_csv(source)
		self.fix_pop(df)
		self.data=df.set_index("GEOID")["FIXPOP"].to_dict()

	def fix_pop(self,df):
		num_pop_list=[]
		for i in df["POP"]:
			try:
				num_pop=int(i)
				num_pop_list.append(num_pop)
			except:
				num_pop_list.append(int(i.split("(")[0]))
		df["FIXPOP"]=num_pop_list
		return df

class HousingOverlay(Overlay):
	def __init__(self,data_source):
		self.read_data(data_source)

	def initial_read(self,source):
		df=pandas.DataFrame.from_csv(source)
		df=df[["Location","AV_TOTAL"]]
		return df

	#seperates a string of the form '('72','-41')' into list of form ['72','-41']
	#returns a tuple of the form (72,-41)
	def seperate(self,latlonstr):
		lat_lon = latlonstr.strip("()").split(",")
		try: 
			to_return=(float(lat_lon[0]),float(lat_lon[1]))
		except:
			to_return=(0,0)
			print("Failed on: ("+lat_lon[0]+","+lat_lon[1]+")")
		return to_return

	def handle_loc(self,df):
		df["LAT"], df["LON"] = zip(*df["Location"].map(self.seperate))
		return df

	def point_in_path(self,x,y,path):
		mat_path = mat.path.Path(path)
		return mat_path.contains_point((x,y))

	def locate(self,lat,lon,geoid,path):
		if self.point_in_path(lat,lon,path):
			return geoid

	def which_block(self,lat,lon,val,shapes_df):
		non_null=shapes_df.reset_index().apply(lambda row:self.locate(lat,lon,row["GEOID"],row["PATH"]),axis=1).dropna()
		# pandas.set_option('display.max_rows', 8842)
		
		# non_null=temp.dropna()
		if len(non_null)>0:
			b_id=non_null.iget(0)
			
			if shapes_df.loc[b_id,"Val"]==None:
				shapes_df.loc[b_id,"Val"]=[val]
				# print(shapes_df.loc[b_id,"Val"])
			else:
				shapes_df.loc[b_id,"Val"]+=[val]

				# print(shapes_df.loc[b_id,"Val"])
		# return shapes_df

	def which_block2(self,lat,lon,val,shapes_df):
		for index,row in shapes_df.iterrows():
			geoid=index
			path=row["PATH"]
			if self.point_in_path(lat,lon,path):
				if shapes_df.loc[geoid,"Val"]==None:
					shapes_df.loc[geoid,"Val"]=[val]
				else:
					shapes_df.loc[geoid,"Val"]+=[val]
				# print(shapes_df.head())
				return 

	def which_block3(self,lat,lon,val,shapes_df,a):
		for geoid,row in shapes_df.iterrows():
			path=row["PATH"]
			if self.point_in_path(lat,lon,path):
				if geoid in a:
					a[geoid].append(val)
				else:
					a[geoid]=[val]
				return


			# shapes_df=self.locate(row["LAT"],row["LON"],row["AV_TOTAL"],shapes_df)


	def bin(self,df,bin_source):
		the_file=open(bin_source,"rb")
		shapes=pickle.load(the_file)
		shapes_df=pandas.DataFrame(shapes,columns=["GEOID","PATH"])
		shapes_df["Val"]=None
		shapes_df=shapes_df.set_index("GEOID")	
		a={}	
		# self.which_block2(42.340297,-71.166757,1680000,shapes_df)
		# self.which_block2(42.340297,-71.166757,10000,shapes_df)

		# self.which_block3(42.340297,-71.166757,10000,shapes_df,a)
		# self.which_block3(42.342947999704634, -71.10303999955583,1000,shapes_df,a)
		# print(a)

		# self.which_block2(42.342947999704634, -71.10303999955583,1000,shapes_df)
		# print(shapes_df.head())
		# self.which_block(42.340297,-71.166757,10000,shapes_df)

		# print(shapes_df[shapes_df["Val"]!=None])
		

		#250250003022011
		# i=0
		# print(0)
		# for index,row in df.iterrows():
		# 	if (i%10==0):
		# 		print(i)
		# 	i+=1
		# 	self.which_block3(row["LAT"],row["LON"],row["AV_TOTAL"],shapes_df,a)
		# print(len(a))

		print(df.head().apply(lambda row: self.which_block(row["LAT"],row["LON"],row["AV_TOTAL"],shapes_df),axis=1))

		# tie=[(0,0),(3,0),(0,4),(3,4)]

		# print(self.point_in_path(1,3.5,tie))
		# print(self.point_in_path(1,.5,tie))
		# print(self.point_in_path(.5,2,tie))
		# print(self.point_in_path(2,2,tie))
		# print(self.point_in_path(3.5,2,tie))
		# print(self.point_in_path(1,0,tie))
		# print(self.point_in_path(1.5,2,tie))
		# print(self.point_in_path(.0000001,.0000001,tie))

		# print(self.point_in_poly(3,4,[(0,0),(3,3),(0,3),(3,0)]))
		#print (type(shapes[0][1]))
		#df=pandas.DataFrame.from_items(shapes[0:1],columns=["GEOID","PATH"])
		# df=pandas.DataFrame.from_items([("a",2),("b",3)],orient="index")
		# print(df)

	def read_data(self,source):
		df=self.initial_read(source)
		df=self.handle_loc(df)
		self.bin(df,"Data/pickle_convert.p")



def make_lattice_map():
	boston_blocks=BlockLattice()
	boston_blocks.map_lattice("Plots/BlockLattice.html")

def make_pop_map():
	boston_blocks=BlockLattice()
	pop_over=PopOverlay("Data/Census_Condensed.csv")
	boston_blocks.add_overlay(pop_over)
	boston_blocks.map_overlay("Plots/PopHeatMap.html")

# make_pop_map()
ho=HousingOverlay("Property_Assessment_2014_O.csv")