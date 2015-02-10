import numpy as np
import pandas as p 
import thinkstats2
import thinkplot
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


class AssessmentData(object):
	"""Class containing data and methods for hte proerty assessment dataset """
	def __init__(self):	
		print "CREATING INITIATION"
		self.initialized = False
		self.wholeDataFrame = None
		self.allLats = None
		self.allLongs = None
		self.imageFile = "Map.png"
		self.activeDataFrame = None
		self.activeLats = None
		self.activeLongs = None
		self.activeColumn = None
		self.XMesh = None
		self.YMesh = None
		self.ZMesh = None
		self.initalize()

	def initalize(self):
		""" Loads the data set, also puts teh latitudes and longitude as a usable format, 
		initalized active dataframe as whole dataframe"""
		print "RUNNING INITIALIZATION"
		self.wholeDataFrame = p.DataFrame.from_csv("Property_Assessment_2014_O.csv")
		self.activeDataFrame = p.DataFrame.from_csv("Property_Assessment_2014_O.csv")
		lats = [0] * len(self.activeDataFrame.Location.values)
		longs = [0] * len(self.activeDataFrame.Location.values)
		for i in range(len(self.activeDataFrame.Location.values)):
    		
			latLong = self.activeDataFrame.Location.values[i].strip("()").split(",")
			try:
				lats[i] = float(latLong[0])
				longs[i] = float(latLong[1])
			except: # Data error
				print i # This will be excel -2 shows error
				latLong = self.activeDataFrame.Location.values[i-1].strip("()").split(",")
        		lats[i] = float(latLong[0])
        		longs[i] = float(latLong[1])
		self.allLats = lats
		self.allLongs = longs
		self.activeLats = lats
		self.activeLongs = longs
		self.initialized = True

	def setActiveColumn(self,columnName):
		self.activeColumn = columnName
		self.generateMesh(columnName)
		self.geoPColorVisualization()



	def setActiveLatLongs(self):
		""" Sets active lat longs to the active data set values, called from setActiveVariable"""
		for i in range(len(self.activeDataFrame.Location.values)):
    		
			latLong = self.activeDataFrame.Location.values[i].strip("()").split(",")
			try:
				lats[i] = float(latLong[0])
				longs[i] = float(latLong[1])
			except: # Data error
				print i # This will be excel -2 shows error
				latLong = self.activeDataFrame.Location.values[i-1].strip("()").split(",")
				lats[i] = float(latLong[0])
				longs[i] = float(latLong[1])

		self.activeLats = lats
		self.activeLongs = longs

	def generateMesh(self, variable,resolution=50):
		"""Generates a mesh of the dataframe, should not be called, should only be called
		by setActiveVariable"""
		import bisect
		latLookup = np.linspace(min(self.activeLats),max(self.activeLats),resolution)
		longLookup = np.linspace(min(self.activeLongs),max(self.activeLongs),resolution)
		values = [[0 for _ in range(resolution)] for _ in range(resolution)]
		for i in range(len(self.activeLats)):
			val = float(self.activeDataFrame.iloc[[i]][variable].values)
			latIndex = bisect.bisect_left(latLookup,self.activeLats[i])
			longIndex = bisect.bisect_left(longLookup,self.activeLongs[i])
			values[longIndex][latIndex] += val

		X, Y = np.meshgrid(longLookup,latLookup)
		Z = np.array(values)
		self.XMesh = X
		self.YMesh = Y
		self.ZMesh = Z



	def showLocationVisualization(self):
		"""Shows on a map where the active dataframe points are located on teh map"""

		im=plt.imread('Map.png')
		plt.scatter(self.activeLongs,self.activeLats,alpha=.1)
		im = plt.imshow(im, extent=[-71.18568, -70.993521, 42.23038, 42.394968])
		plt.show()

	def geoPColorVisualization(self):
		plt.figure()
		plt.pcolor(self.XMesh, self.YMesh, self.ZMesh, cmap='RdBu')#, vmin=10000, vmax=z_max)
		#plt.pcolor(X, Y, Z, cmap='RdBu', norm=LogNorm(vmin=Z.min(), vmax=Z.max()))
		plt.axis([self.XMesh.min(), self.XMesh.max(),self.YMesh.min(), self.YMesh.max()])
		plt.colorbar()
		#plt.clabel(CS, inline=1, fontsize=10)
		plt.title('Visualization of ACtive DataColumn')
		plt.show()

	def run(self):
		self.setActiveColumn("AV_LAND")


