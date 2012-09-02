#!/usr/bin/env python
import argparse
from pyPdf import PdfFileWriter, PdfFileReader

parser = argparse.ArgumentParser(description='convert an N pages pdf whit M internal pages in a N*M PDF')
parser.add_argument("inPDF", help="the PDF input")
parser.add_argument("horizontalPages", help="how many internal pages are in a row of an external page",type=int)
parser.add_argument("verticalPages", help="how many internal pages are in a column of an external page",type=int)
parser.add_argument("leftBorder", help="distance (in points) between left border of the external page and left border of first internal page",type=int)
parser.add_argument("rightBorder", help="distance (in points) between left border of the external page and right border of first internal page",type=int)
parser.add_argument("upBorder", help="distance (in points) between up border of the external page and up border of first internal page",type=int)
parser.add_argument("downBorder", help="distance (in points) between up border of the external page and down border of first internal page",type=int)
parser.add_argument("horizontalDelta", help="horizontal distance (in points) between two internal pages (from left border to left border)",type=int)
parser.add_argument("verticalDelta", help="vertical distance (in points) between two internal pages (from top border to top border)",type=int)
parser.add_argument("outPDF", help="the PDF output")
args = parser.parse_args()

output = PdfFileWriter()
inputs = [[PdfFileReader(file(args.inPDF, "rb")) for col in range(args.verticalPages)] for row in range(args.horizontalPages)]

for page in range(inputs[0][0].getNumPages()):
	#for all rows
	for row in range(args.horizontalPages):
		#for all columns (inside the row)
		for column in range(args.verticalPages):
			page1=inputs[row][column].getPage(page)
			(high,width) = (page1.mediaBox.getUpperRight_y(),page1.mediaBox.getUpperRight_x())
			page1.mediaBox.upperRight = (args.horizontalDelta*column+args.rightBorder,high-args.verticalDelta*row-args.upBorder)
			page1.mediaBox.lowerLeft = (args.horizontalDelta*column+args.leftBorder,high-args.verticalDelta*row-args.downBorder)
			output.addPage(page1)

outputStream = file(args.outPDF, "wb")
output.write(outputStream)
outputStream.close()
