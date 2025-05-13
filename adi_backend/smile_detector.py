""" TODOs:
tune smile and face classifiers individually, it isnt quite right.
"""

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

    def detect_objects(self, image, classifier):
        image_gray = cvtColor(image, COLOR_BGR2GRAY)
        objects = classifier.detectMultiScale(image_gray, 1.3, 15)
        return objects

    def is_rectangle_in_rectangle(self, candidate_rect, bounding_rect):
        c_left, c_bottom, c_width, c_height = candidate_rect
        b_left, b_bottom, b_width, b_height = bounding_rect

        c_right = c_left + c_width
        c_top = c_bottom + c_height
        b_right = b_left + b_width
        b_top = b_bottom + b_height

        return (
            c_left >= b_left and
            c_bottom >= b_bottom and
            c_right <= b_right and
            c_top <= b_top
        )

    def find_smiles(self, image):
        """ Function to find and return the coordinates of all smiles in an image. To reduce false positives,
        find the set of "faces" and "smiles" in image using haarcascad classifiers. Then filter for the set of
        smiles fully contained within a face.

        args:
            image: opencv image
        returns:
            rectangles: list of tuples, where the tuple is in form (x, y, w, h)

        """

        # Preprocess set of potential faces and smiles.
        maybe_faces = self.detect_objects(image, self.face_classifier)
        maybe_smiles = self.detect_objects(image, self.smile_classifier)

        # Define set of smiles found within the bounds of the set of faces.
        smiles=list()
        for smile in maybe_smiles:
            smile_in_face = False
            for face in maybe_faces:
                if self.is_rectangle_in_rectangle(smile, face):
                    smile_in_face = True
            if smile_in_face:
                smiles.append(smile)
        
        return smiles
