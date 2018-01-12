# DL-Art4Transparency: Deep Learning Art Transfer for Transparent PNGs (by muntisa)
# 
# based on fchollet's AI script
# Note: generated images (outputs) will have composed names as [content_name]_[style_name]_[iterations].jpg

# Use: python DL-Art4Transparency.py
# It will use all default parameters = default folders for contents, styles, outputs, resized and corrected images, 10 iterations (for a fast test)

import os, time, argparse
from PngResizeTransparency import *
from PngTransfTransparency import *

# set starting time
start_time = time.time()

print """
*********************************************************************************
DL-Art4Transparency: Deep Learning Art Transfer for Transparent PNGs (by muntisa)
*********************************************************************************
* Based on fchollet's AI:
https://github.com/keras-team/keras/blob/master/examples/neural_style_transfer.py
*********************************************************************************
"""

# ====================================================
# PARAMETERS
# ====================================================
# Setup to receive command line arguments
parser = argparse.ArgumentParser(description='DL-Art4Transparency: Deep Learning Art Transfer for Transparent PNGs (by muntisa)')
parser.add_argument('--content_folder', metavar='content_folder', type=str, help='Folder with content images to transform.', default='contents')
parser.add_argument('--style_folder',   metavar='style_folder',   type=str, help='Folder with style images to use.', default='styles')
parser.add_argument('--output_folder',  metavar='output_folder',  type=str, help='Folder to store the generated image without correction.', default='outputs')
parser.add_argument('--resized_folder', metavar='resized_folder', type=str, help='Folder to store the resized content images.', default='contents_resized')
parser.add_argument('--corrected_folder', metavar='corrected_folder', type=str, help='Folder to store final corrected generated images.', default='outputs_corrected')
parser.add_argument('--iterations', help='Set the number of iterations to run the optimizer.', type=int, default=10)

# Parse command line arguments
args = parser.parse_args()
ContentFolder = args.content_folder
StyleFolder = args.style_folder
GeneratedFolder = args.output_folder
ResizedFolder   = args.resized_folder
CorrectedFolder = args.corrected_folder

# number of iterations for all the AI scripts (1000 = default for anishathalye's AI)
iter = args.iterations
# -------------------------------------------------------

# Set the lists with files (default will get all the files in the folders!)
ContentFileList  = os.listdir(ContentFolder) # get all files in content folder
# ContentFileList = ["dog.jpg","dome.jpg","lion.jpg","london.jpg","puppy.jpg"] # use a specific list
StyleFileList    = os.listdir(StyleFolder)   # get all files in style folder
# StyleFileList = ["dora-maar-picasso.jpg","rain-princess-aframov.jpg","starry-night-van-gogh.jpg"] # use a specific list
# ====================================================

print "Content Folder   =", ContentFolder
print "Style Folder     =", StyleFolder
print "Output Folder    =", GeneratedFolder
print "Resized Folder   =", ResizedFolder
print "Corrected Folder =", CorrectedFolder

# for each image to modify use each style image to generate a new image
i = 0 # curent number of generated images
n = len(ContentFileList)*len(StyleFileList) # total number of generated files
for iContentFile in ContentFileList:
	sContentFile = os.path.join(ContentFolder, iContentFile) # join path with filename for content
	for iStyleFile in StyleFileList:
		print "\n\n==> ", "Content = ", iContentFile, "| Style = ", iStyleFile
		sStyleFile   = os.path.join(StyleFolder, iStyleFile) # join path with filename for style
				
		# Run fchollet's AI (https://github.com/keras-team/keras/blob/master/examples/neural_style_transfer.py)
		sOutputFile  = os.path.join(GeneratedFolder, iContentFile[:-4]+"_"+iStyleFile[:-4]+"_fchollet_"+str(iter)+".png") # join path with filename for style
		sCmd = "python fchollet_neural_style_transfer.py "+sContentFile+" "+sStyleFile+" "+sOutputFile+" --iter "+str(iter)
		i+=1
		print "\n\n---> Running Art Transfer - ", i, "from", n, ":"
		print sCmd
		time_AI = time.time()
		#os.system(sCmd) !!!!!!!!!!!!!!!! ENABLE THIS LINE !!!!!!!!!!!!!!!!!!!

		# Correct the PNG
		# (1) Resize the input content to the same size of the output
		sResizedPNG = (os.path.join(ResizedFolder, iContentFile))[:-4]+'_resized.png'
		print "---> Resizing content image for transparency tranfer ..."
		PNG_ResizeKeepTransparency(sContentFile, sResizedPNG, RefFile = sOutputFile)

		# (2) Transfer the transparency from resized content file to output file
		sCorrectedPNG = (os.path.join(CorrectedFolder, iContentFile[:-4]+"_"+iStyleFile[:-4]+"_fchollet_"+str(iter)+".png"))[:-4] + '_corr.png'
		print "---> Correct the generated image by transfer of the resized content transparency ..."
		PngTransfTransparency(sResizedPNG,sOutputFile,sCorrectedPNG)
		
		print(".......... Execution time: %s seconds" % (time.time() - time_AI))
		
print ("\nPlease find the corrected generated images in %s.") % (CorrectedFolder)
print("Total Execution time of DL-Art4Transparency: %s seconds" % (time.time() - start_time))
