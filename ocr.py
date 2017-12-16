# import the necessary packages
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import geocoder
import time
import requests
import re
import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def send_request(name, lat, lng):
  # Request (3)
  # POST http://boiling-taiga-24096.herokuapp.com/locations

  try:
    response = requests.post(
        url="http://boiling-taiga-24096.herokuapp.com/api/locations",
        headers={
          # "Cookie": "laravel_session=eyJpdiI6IkgzdGVjdUFwOFpBQ3B0VnBFK3kxZkE9PSIsInZhbHVlIjoiK2VjV3NNdmVDTkd6VnNjRkEzeEpzRVpuT2hYcDUxa0xGTXZFbzlxQjdOWTNqNWdmbWNxVDE4cWs4RVNjWVJmSnkxbWZZMEQxYldDZHJxMmhSUFdxV0E9PSIsIm1hYyI6ImEyNzIyMmY0NzcwMWJhMzRhYmIwNjNiNjY3ODJiN2M1YzhlMzA2MDY0MGUxZWJhMTYzNGUxMTFiYWMyZGFkNDQifQ%3D%3D",
          "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        },
        data={
          "name": name,
          "longitude": lng,
          "latitude": lat
        },
    )
    
    return response
    # print('Response HTTP Status Code: {status_code}'.format(
    #   status_code=response.status_code))
    # print('Response HTTP Response Body: {content}'.format(
    #   content=response.content))
  except requests.exceptions.RequestException:
      print('HTTP Request failed')

def send_request_ticket(signature, description, dep_name, dep_lat, dep_lng, dest_name, dest_lat, dest_lng, ocr_text, dep_id, dest_id, image):
  # Request (3)
  # POST http://boiling-taiga-24096.herokuapp.com/locations

  try:
    print("POST ticket")
    print(dep_id)
    print(dest_id)
    response = requests.post(
        url="http://boiling-taiga-24096.herokuapp.com/tickets",
        headers={
          # "Cookie": "laravel_session=eyJpdiI6IkgzdGVjdUFwOFpBQ3B0VnBFK3kxZkE9PSIsInZhbHVlIjoiK2VjV3NNdmVDTkd6VnNjRkEzeEpzRVpuT2hYcDUxa0xGTXZFbzlxQjdOWTNqNWdmbWNxVDE4cWs4RVNjWVJmSnkxbWZZMEQxYldDZHJxMmhSUFdxV0E9PSIsIm1hYyI6ImEyNzIyMmY0NzcwMWJhMzRhYmIwNjNiNjY3ODJiN2M1YzhlMzA2MDY0MGUxZWJhMTYzNGUxMTFiYWMyZGFkNDQifQ%3D%3D",
          # "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        },
        data={
          "signature": signature,
          "description": description,
          "ocr_text": ocr_text,
          "point_of_departure_id": dep_id,
          "destination_id": dest_id
          # "image": (signature, open(image, 'rb'))
        },
        files={
          "image": (signature, open(image, 'rb'))
        }  
    )
    print('Response HTTP Status Code: {status_code}'.format(status_code=response.status_code))
    print('Response HTTP Response Body: {content}'.format(content=response.content))
  except requests.exceptions.RequestException:
      print('HTTP Request failed')

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=False,help="path to input image to be OCR'd")
ap.add_argument("-p", "--path", required=False,help="path containing images")
args = vars(ap.parse_args())

path = "./dbhack/III.5.09-30/"
if args["path"]:
  path = args["path"]
  pass
 
dirs = os.listdir( path )

for file in dirs:
  print(file)
  imagePath = path + file
  image = cv2.imread(path + file)
  filename = "{}.jpg".format(os.getpid())

  cv2.imwrite(filename, image)
  text = pytesseract.image_to_string(Image.open(filename), lang='deu')
  os.remove(filename)
  print(text)
  words = text.splitlines()
  print(words)
  
  pattern = re.compile('([^\W\d])+')
 
  word_results = []
  destination_longitude = 0
  destination_latitude = 0
  destination_name = ""
  departure_longitude = 0
  departure_latitude = 0
  departure_name = ""
  departure_id = 0
  destination_id = 0

  for word in words:
    for m in re.finditer(pattern, word):
      word_results.append(m.group(0))
      if len(m.group(0)) > 3:
        with requests.Session() as session:
          searchString = m.group(0)
          print("Geocode: " + searchString)
          g = geocoder.arcgis(searchString, session=session)
          print(g.json)
          if not g.ok:
            pass
          else:
            lat = 0
            lng = 0
            name =""
            for result in g:
              lat = result.lat
              lng = result.lng
              name = result.address
              pass
            if lng > 36.6 or lng < -9.2 or lat > 58.5 or lat < 33.2:
              pass
            else:
              response = send_request(name, lat, lng)
              locationId = (json.loads(response.text)['id'])
              locationName = (json.loads(response.text)['name'])
              # print(locationName)
              print(fuzz.partial_ratio(name, searchString))
              if fuzz.partial_ratio(name, searchString) > 75:
                if departure_id == 0:
                  departure_id = locationId
                  pass
                elif destination_id == 0:
                  destination_id = locationId
                  pass
                pass
            pass
          time.sleep(1)
        pass
  sig = os.path.splitext(file)[0]
  send_request_ticket(sig, "", "", "", "", "", "", "", json.dumps(word_results), departure_id, destination_id, path+file),
  print("NEXT FILE")

