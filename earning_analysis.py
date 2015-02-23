import pandas
import thinkstats2
import matplotlib.pyplot as plt
import collections
import thinkplot

def plotDepart(hist):
	hist=hist.GetDict()
	sort_hist=collections.OrderedDict(sorted(hist.items(),key=lambda t:t[1],reverse=True))
	plt.figure(figsize=(18, 7.195), dpi=100)
	plt.bar(range(len(sort_hist)),sort_hist.values(),align="center",log=True)
	plt.xticks(range(len(sort_hist)),list(sort_hist.keys()),rotation="vertical")
	plt.subplots_adjust(bottom=0.5)
	plt.xlabel("Department")
	plt.ylabel("Number of Employees")
	plt.title("Number of Employees by Department")

	plt.savefig("Plots/EmployeeTypes.png",format="png", dpi=72)
def create_depart_chart(df):
	depart_hist=thinkstats2.Hist(df["DEPARTMENT"])
	plotDepart(depart_hist)

def moneyToNum(money_series):
	new_monies=[]
	for el in money_series:
		if el[0]=="$":
			new_el=el[1:]
			new_monies.append(int(float(new_el)))
		else:
			print("Malformed: "+el)
	return new_monies

def make_cdf_from_dep(dep_string):
	dep_data=df[df["DEPARTMENT"]==dep_string]
	monies=dep_data["TOTAL EARNINGS"]
	recoded_monies=moneyToNum(monies)
	return thinkstats2.Cdf(recoded_monies)

def create_school_earn_chart(df):
	schools=make_cdf_from_dep("Boston Public Schools")
	fire=make_cdf_from_dep("Boston Fire Department")
	police=make_cdf_from_dep("Boston Police Department")

	thinkplot.Cdf(schools,label="Public Schools",color="#000000")
	thinkplot.Cdf(fire,label="Fire Department",color="#FF0000")
	thinkplot.Cdf(police,label="Police Department")
	thinkplot.Save("Plots/EmployeeEarnings2013",formats=["png"],legend=True,xlabel="Total Earnings",ylabel="Cumulative Probability",title="Cumulative Probability of Boston Employee Earnings 2013")

	#thinkplot.Show(legend=True,xlabel="Total Earnings",ylabel="Cumulative Probability",title="Cumulative Probability of Boston Employee Earnings 2013")

def estimate_school_earn(df):
	school=make_cdf_from_dep("Boston Public Schools")
	actual_mean=school.Mean()
	means=[]
	for i in range(200):
		sample=school.Sample(2000)
		mean=thinkstats2.Mean(sample)
		means.append(mean)

	sample_dist=thinkstats2.Cdf(means)

	#How accurate is my estimate of the statistic
	#How big is the range I am likely to see my statistic fall in

	print("standard error: "+str(thinkstats2.Std(means)))
	print("mean of mean: "+str(thinkstats2.Mean(means)))
	print("actual mean: "+str(actual_mean))
	print("90 CI: "+str(sample_dist.CredibleInterval()))

	thinkplot.Cdf(sample_dist)
	#thinkplot.Cdf(sample_dist,label="sampled")
	thinkplot.Show(legend=True)



df=pandas.DataFrame.from_csv("Data/Employee_Earnings_Report_2013.csv")
# create_depart_chart(df)
# create_school_earn_chart(df)
estimate_school_earn(df)