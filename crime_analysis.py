import pandas
import thinkplot
import thinkstats2
import collections
import numpy
from ast import literal_eval as make_tuple
import pygmaps
import matplotlib.pyplot as plt
from datetime import datetime,date

#returns number of months since first date in dataset
def unformat2(date_string):
	dt=datetime.strptime(date_string,"%m/%d/%Y %I:%M:%S %p")

	first = datetime(2012, 12, 1)
	return (dt-first).total_seconds()

def createMonths(df):
	#years since 2012, the first year of dataset
	year_num=df["Year"]-2012

	#months where Jan=0
	month=df["Month"]-1

	df["MONTHDATE"]=month+(12*year_num)
	return df

def createMonthlyCrime(df):
	df=createMonths(df)
	crime_months=thinkstats2.Hist(df["MONTHDATE"])
	thinkplot.Hist(crime_months)
	thinkplot.Save("Plots/MonthlyCrime",formats=["png"],xlabel="Months since Jan 2012",ylabel="Number of crimes")

def plotCategorical(hist):
	hist=hist.GetDict()
	sort_hist=collections.OrderedDict(sorted(hist.items(),key=lambda t:t[1],reverse=True))
	plt.bar(range(len(sort_hist)),sort_hist.values())
	plt.xticks(range(len(sort_hist)),list(sort_hist.keys()),rotation="vertical")
	plt.show()

def createCrimeType(df):
	# nature=thinkstats2.Hist(df["INCIDENT_TYPE_DESCRIPTION"])
	# plotCategorical(nature)

	count=collections.Counter(df["INCIDENT_TYPE_DESCRIPTION"])
	sort_count=collections.OrderedDict(sorted(count.items(),key=lambda t:t[1],reverse=True))
	
	plt.figure(figsize=(18, 7.195), dpi=100)
	plt.bar(range(len(sort_count)),sort_count.values())
	plt.xticks(range(len(sort_count)),list(sort_count.keys()),rotation="vertical")
	plt.subplots_adjust(bottom=0.5)
	plt.xlabel("Type of Crime")
	plt.ylabel("Frequency of Crime")
	plt.title("Number of types of crime in Boston")
	plt.savefig("Plots/CrimeTypes.png",format="png", dpi=72)

def createDailyCrime(df):
	count=collections.Counter(df["DAY_WEEK"])
	sort_count=collections.OrderedDict(sorted(count.items(),key=lambda t:t[1],reverse=True))
	plt.bar(range(len(sort_count)),sort_count.values())
	plt.xticks(range(len(sort_count)),list(sort_count.keys()),rotation="vertical")
	plt.subplots_adjust(bottom=0.2)
	plt.xlabel("Day of Week")
	plt.ylabel("Number of Crimes")
	plt.title("Crime per Day")
	plt.savefig("Plots/DailyCrime.png",format="png", dpi=72)

def createGeograph(df):

	mymap = pygmaps.maps(42.3, -71.1, 16)

	locs=df["Location"]
	a=0
	for el in locs:
		if a%20==0:
			(lat,lon)=make_tuple(el)
			mymap.addpoint(lat, lon, "#0000FF")
		a+=1

	mymap.draw('Plots/CrimeMap.html')

def testPmf(df):
	crime_pmf=thinkstats2.Pmf(df["INCIDENT_TYPE_DESCRIPTION"])
	thinkplot.Pmf(crime_pmf, width=1)
	thinkplot.Show()



	# fname = 'boston.png'
	# image = Image.open(fname).convert("L")
	# arr = np.asarray(image)
	# plt.imshow(arr, cmap = cm.Greys_r)
	# plt.show()
	# thinkplot.Scatter(xs,ys)
	# thinkplot.Show()


df=pandas.DataFrame.from_csv("Data/Crime_Incident_Reports.csv")
# createMonthlyCrime(df)
# createCrimeType(df)
# createDailyCrime(df)
# createGeograph(df)
testPmf(df)