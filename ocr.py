# import the necessary packages
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import geocoder
import time
import requests
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,help="path to input image to be OCR'd")
ap.add_argument("-p", "--preprocess", type=str, default="thresh",help="type of preprocessing to be done")
args = vars(ap.parse_args())

path = "./dbhack/III.5.09-30/"
dirs = os.listdir( path )

for file in dirs:
  print(file)
  image = cv2.imread(path + file)
  filename = "{}.jpg".format(os.getpid())
  # image = cv2.imread(path+file)
  # originalFile = path + file
  cv2.imwrite(filename, image)
  text = pytesseract.image_to_string(Image.open(filename), lang='deu')
  os.remove(filename)
  print(text)
  words = text.splitlines()
  print(words)

  for word in words:
	  with requests.Session() as session:
		  print("Geocode: " + word)
		  searchString = word.replace(" ", "")
		  g = geocoder.arcgis(searchString, session=session)
		  print(g.json)
	  time.sleep(3)
	  pass
  print("NEXT FILE")



# load the example image and convert it to grayscale
# image = cv2.imread(args["image"])
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# check to see if we should apply thresholding to preprocess the
# image
# if args["preprocess"] == "thresh": gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# make a check to see if median blurring should be done to remove
# noise
# elif args["preprocess"] == "blur": gray = cv2.medianBlur(gray, 3)

# elif args["preprocess"] == "gauss": gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 12)

# elif args["preprocess"] == "mean": gray = cv2.adaptiveThreshold(gray,180,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,9,12)

# elif args["preprocess"] == "canny": gray =cv2.Canny(gray, 100, 125)

# write the grayscale image to disk as a temporary file so we can
# apply OCR to it
# filename = "{}.png".format(os.getpid())
# cv2.imwrite(filename, image)

# load the image as a PIL/Pillow image, apply OCR, and then delete
# the temporary file
# text = pytesseract.image_to_string(Image.open(filename), lang='deu')
# os.remove(filename)
# print(text)

# words = text.splitlines()
# print(words)

# for word in words:
# 	with requests.Session() as session:
# 		print("Geocode: " + word)
# 		searchString = word.replace(" ", "")
# 		g = geocoder.arcgis(searchString, session=session)
# 		print(g.json)
# 	time.sleep(3)
# 	pass

# show the output images
# cv2.imshow("Image", image)
# cv2.imshow("Output", gray)
# cv2.imwrite("test.png", gray)
# cv2.waitKey(0)