""" Analyze the presence of points colocalizing with myelin in a stack
by Étienne Labrie-Dion, Douglas Hospital Research Center, 2017 """


iterations = 2 #dilate/erode cycles
noise = 750 #Noise tolerance for maxima detection
median = 3 #Radius of median filter
myelinCH = 2 #Channel containing myelin pictures
pointsCH = 3 #Channel containing the points


from ij import IJ
from ij.measure import ResultsTable

#Set the variables
image = IJ.getImage()
title = image.getTitle()
n_slices = image.getDimensions()[3]

#Prepare measurements
IJ.run("Set Measurements...", "area integrated display redirect=None decimal=3")
IJ.run("Clear Results")
IJ.run("Split Channels")
myelin = "C" + str(myelinCH) + "-" + title
points = "C" + str(pointsCH) + "-" + title
rt = ResultsTable.getResultsTable() #This object allows us to change the labels in the results table

#Threshold the myelin stack
IJ.selectWindow(myelin)
IJ.run("Convert to Mask", "method=Default background=Dark calculate")
IJ.run("Median...", "radius=%s stack" % median)
IJ.run("Fill Holes", "stack")
IJ.run("Close-", "stack")
for i in range(iterations):
	IJ.run("Dilate", "stack")
	IJ.run("Erode", "stack")

#Process all planes
for index in range(1, n_slices+1):

	#Find all the points
	IJ.selectWindow(points)
	IJ.setSlice(index)
	IJ.run("Find Maxima...", "noise=%s output=[Single Points]" % noise)
	IJ.run("Subtract...", "value=254") #so RawIntDen equals the number of points

	#Count all the points
	IJ.run("Measure")
	IJ.run("Close")	#simpler to close the image than to keep it open and select it again
	rt.setLabel("%s:  All #%03d" % (title,index), index*2-2)
	rt.show('Results')
	
	#Counts the dots located on myelin and the area of myelin
	IJ.selectWindow(myelin)
	IJ.setSlice(index)
	IJ.run("Create Selection")
	
	#generate the dots again and apply the selection
	IJ.selectWindow(points)
	IJ.setSlice(index)
	IJ.run("Find Maxima...", "noise=%s output=[Single Points]" % noise)
	IJ.run("Subtract...", "value=254")
	IJ.run("Restore Selection")
	IJ.run("Measure")
	IJ.run("Close")
	rt.setLabel("%s:  Myelin #%03d" % (title,index), index*2-1)
	rt.show('Results')