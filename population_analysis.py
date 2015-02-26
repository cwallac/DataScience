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

def opac_choose(num,max_num):
	return num/max_num

def geo_plot(the_map,lat,lon,pop,cdf):
	color=color_choose_4(pop,cdf)
	if (pop==0):
		opac=0
		size=10
	else:
		opac=.5
		size=50
	the_map.addradpoint(lat, lon,size, color,opac)

def geo_plot_uni(the_map,lat,lon,pop,cdf):
	color=color_choose_4(pop,cdf)
	if (pop==0):
		opac=0
		size=10
	else:
		opac=opac_choose(pop,2671)
		size=50
	
	the_map.addradpoint(lat, lon,size, color,opac)

def fix_pop(df):
	num_pop_list=[]
	for i in df["POP"]:
		try:
			num_pop=int(i)
			num_pop_list.append(num_pop)
		except:
			num_pop_list.append(int(i.split("(")[0]))
	df["FIXPOP"]=num_pop_list
	return df

def map_pop(df):
	max_pop=max(df["FIXPOP"])
	habited_dist=thinkstats2.Cdf(df["FIXPOP"])

	mymap = pygmaps.maps(42.3, -71.1, 16)
	df.apply(lambda row: geo_plot(mymap,row["LAT"],row["LON"],row["FIXPOP"],habited_dist),axis=1)
	mymap.draw('Plots/PopMap.html')

def map_unipop(df):
	max_pop=max(df["UNIPOP"])
	#This is on po\urpose to plot using same colors are regular population
	habited_dist=thinkstats2.Cdf(df["FIXPOP"])

	mymap = pygmaps.maps(42.3, -71.1, 16)
	df.apply(lambda row: geo_plot_uni(mymap,row["LAT"],row["LON"],row["UNIPOP"],habited_dist),axis=1)
	mymap.draw('Plots/UniPopMap.html')

def consistancy_check(df):
	impossible=df[df["UNIPOP"]>df["FIXPOP"]]

	if (len(impossible)>0):
		print("INCONSISTENCY")
		print(1/0)

def non_unipop(df):
	df["NONUNIPOP"]=df["FIXPOP"]-df["UNIPOP"]
	return df

def plot_pop(df):
	habited_dist=thinkstats2.Cdf(df["FIXPOP"])
	thinkplot.Cdf(habited_dist)
	thinkplot.Show()

def plot_unipop(df):
	unipop_dist=thinkstats2.Cdf(df["UNIPOP"])
	habited=df[df["UNIPOP"]!=0]
	habited_uni=thinkstats2.Cdf(habited["UNIPOP"])
	thinkplot.Cdf(unipop_dist,label="University Population")
	thinkplot.Cdf(habited_uni,label="Habited University Population")
	thinkplot.Save("Plots/UniPopulation",formats=["png"],legend=True,xlabel="People",ylabel="Cumulative Probability",title="Cumulative Probability of University Population per census block")

def plot_both(df):
	pop_dist=thinkstats2.Cdf(df["FIXPOP"])
	unipop_dist=thinkstats2.Cdf(df["UNIPOP"])
	thinkplot.Cdf(unipop_dist,label="University Population")
	thinkplot.Cdf(pop_dist,label="Total Population")
	thinkplot.Save("Plots/Population",formats=["png"],legend=True,xlabel="People",ylabel="Cumulative Probability",title="Cumulative Probability of Boston Population per census block")


df=pandas.DataFrame.from_csv("Data/Census_Condensed.csv")
fix_pop(df)
consistancy_check(df)
# plot_both(df)
# map_unipop(df)
# plot_unipop(df)
# plot_both(df)
# map_pop(df)

