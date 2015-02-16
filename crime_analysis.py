import pandas
import thinkplot
import thinkstats2
import collections
import numpy
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

df=pandas.DataFrame.from_csv("Data/Crime_Incident_Reports.csv")
# createMonthlyCrime(df)
createCrimeType(df)