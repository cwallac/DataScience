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

def create_school_earn_chart(df):
	school_emps=df[df["DEPARTMENT"]=="Boston Public Schools"]
	fire_emps=df[df["DEPARTMENT"]=="Boston Fire Department"]
	police_emps=df[df["DEPARTMENT"]=="Boston Police Department"]
	
	monies=school_emps["TOTAL EARNINGS"]
	recoded_monies=moneyToNum(monies)
	money_cdf=thinkstats2.Cdf(recoded_monies)
	thinkplot.Cdf(money_cdf)
	thinkplot.Show(xlabel="Monies",ylabel="Cumulative Probability",title="Cumulative Probabiity of Boston Public School Employee Earnings 2013")


df=pandas.DataFrame.from_csv("Data/Employee_Earnings_Report_2013.csv")
# create_depart_chart(df)
create_school_earn_chart(df)