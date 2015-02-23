import pandas
import thinkstats2
import thinkplot
import modified_pygmaps as pygmaps
import matplotlib as mat

#Takes a number, returns normalized 
#number along a color gradient along Hue from 180 down to 0 in hex
def color_choose(num,max_num):
	return mat.colors.rgb2hex(mat.colors.hsv_to_rgb(((num/max_num)*.5,1,1)))
	
def color_choose_2(num,cdf):
	return mat.colors.rgb2hex(mat.colors.hsv_to_rgb((cdf.Prob(num)*.5,1,1)))

def color_choose_3(num,cdf):
	return mat.colors.rgb2hex((cdf.Prob(num),0,0))

def color_choose_4(num,cdf):
	return mat.colors.rgb2hex(mat.colors.hsv_to_rgb((.7,cdf.Prob(num),1)))


def geo_plot(the_map,lat,lon,pop,cdf):
	# mymap.addradpoint(37.429, -122.145, 95, "#FF0000")
	color=color_choose_4(pop,cdf)
	the_map.addradpoint(lat, lon,50, color)

def plot_pop(df):
	num_pop_list=[]
	for i in df["POP"]:
		try:
			num_pop=int(i)
			num_pop_list.append(num_pop)
		except:
			num_pop_list.append(int(i.split("(")[0]))
	df["FIXPOP"]=num_pop_list

	max_pop=max(df["FIXPOP"])
	habited_dist=thinkstats2.Cdf(df["FIXPOP"])

	mymap = pygmaps.maps(42.3, -71.1, 16)
	df.apply(lambda row: geo_plot(mymap,row["LAT"],row["LON"],row["FIXPOP"],habited_dist),axis=1)
	mymap.draw('Plots/PopMap.html')


	# mymap.addpoint(lat, lon, "#0000FF")
	# 
	# habited_dist=thinkstats2.Cdf(num_pop_list)
	# thinkplot.Cdf(habited_dist)
	# thinkplot.Show()

df=pandas.DataFrame.from_csv("Data/Census_Condensed.csv")
plot_pop(df)
