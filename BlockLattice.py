import pickle
import modified_pygmaps as pygmaps
import pandas
import matplotlib as mat

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

class BlockOverlay(object):
	def __init__(self,data_source):
		self.data={}
	
	#read data is required to take a source and compute a 
	#dictionary of string geoid to num value
	def read_data(self,source):
		raise UnimplementedMethodException()	

class PopOverlay(BlockOverlay):
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

def make_lattice_map():
	boston_blocks=BlockLattice()
	boston_blocks.map_lattice("Plots/BlockLattice.html")

def make_pop_map():
	boston_blocks=BlockLattice()
	pop_over=PopOverlay("Data/Census_Condensed.csv")
	boston_blocks.add_overlay(pop_over)
	boston_blocks.map_overlay("Plots/PopHeatMap.html")

make_pop_map()