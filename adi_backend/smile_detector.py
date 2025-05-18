""" TODOs:
tune smile and face classifiers individually, it isnt quite right.

play with object detection preprocessors
"""

from math import sqrt
from cv2 import data as classifier_data
from cv2 import (
    COLOR_BGR2GRAY,
    CascadeClassifier,
    cvtColor,
    rectangle,
)

class SmileDetector():
    face_classifier = CascadeClassifier(classifier_data.haarcascades + "haarcascade_frontalface_default.xml")
    smile_classifier = CascadeClassifier(classifier_data.haarcascades + "haarcascade_smile.xml")
    smiles=[]

    def rectangles_to_coordinates(self, rectangles):
        coordinates = []
        for rectangle in rectangles:
            s_x, s_y, s_w, s_h = rectangle
            x = s_x + (s_w/2)
            y = s_y + (s_h/2)
            coordinates.append((x, y))
        return coordinates

    def is_smile_in_face(self, candidate_smile, candidate_face):
        """ Helper function to check if a candidate smile fits within the lower half of a face.
        """

        # Get smile coordinates
        s_x, s_y = self.rectangles_to_coordinates([candidate_smile])[0] 

        # Get face coordinates
        f_x, f_y = self.rectangles_to_coordinates([candidate_face])[0]
        
        # Estimate face diameter
        f_l, f_b, f_w, f_h = candidate_face
        f_d = f_w + f_h /2

        # Naively assuming a face is a circle, check the smile is in the lower half.
        is_lower_half = f_y <= s_y
        coord_diff = sqrt((s_x - f_x)**2 + (s_y - f_y)**2)
        is_in_face = f_d >= coord_diff

        return is_in_face and is_lower_half

    def find_smiles(self, image):
        """ Function to find and return the coordinates of all smiles in an image. To reduce false positives,
        find the set of "faces" and "smiles" in an image using haarcascad classifiers. Then filter for the set
        of smiles fully contained within a face.

        args:
            image: opencv image
        returns:
            rectangles: list of tuples in form (x, y, w, h)
        """

        # Preprocess grayscale image.
        image_gray = cvtColor(image, COLOR_BGR2GRAY)

        # Preprocess set of potential faces and smiles.
        maybe_faces = self.face_classifier.detectMultiScale(image_gray, 1.3, 10)
        maybe_smiles = self.smile_classifier.detectMultiScale(image_gray, 1.8, 25)

        # Define set of smiles found within the bounds of the set of faces.
        smiles=list()
        for face in maybe_faces:
            for smile in maybe_smiles:
                if not self.is_smile_in_face(smile, face):
                    continue
                smiles.append(smile)
                
        return smiles

    def overlay_rectangles(self, image, rectangles):
        for (x, y, w, h) in rectangles: 
            rectangle(image, (x, y), ((x + w), (y + h)), (0, 0, 255), 2) 
        return image

    def get_smile_coords(self):
        coords = self.rectangles_to_coordinates(self.smiles)
        return coords

    def process_frame(self, image):
        self.smiles = self.find_smiles(image)
        processed_frame = self.overlay_rectangles(image, self.smiles)
        return processed_frame