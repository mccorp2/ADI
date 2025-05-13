from cv2 import data as classifier_data
from cv2 import (
    COLOR_BGR2GRAY,
    CascadeClassifier,
    cvtColor,
    rectangle,
)

def detect_objects(image, classifier="haarcascade_smile.xml"):
    image_gray = cvtColor(image, COLOR_BGR2GRAY)
    object_classifier = CascadeClassifier(classifier_data.haarcascades + classifier)
    
    # TO DO: tune paramaterization
    objects = object_classifier.detectMultiScale(image_gray, 2, 35)
    return objects

def overlay_rectangles(image, rectangles):
    for (x, y, w, h) in rectangles: 
        rectangle(image, (x, y), ((x + w), (y + h)), (0, 0, 255), 2) 
    return image
