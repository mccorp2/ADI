""" TODOs:
tune smile and face classifiers individually, it isnt quite right.

play with object detection preprocessors
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

    def is_smile_in_face(self, candidate_smile, candidate_face):
        """ Helper function to check if a candidate smile fits within the bounds of a face.
        
        args: 
            candidate_rect: tuple in form (x, y, w, h)
            bounding_rect: tuple in form (x, y, w, h)
        return:
            result: boolean
        """
        s_x, s_y, s_w, s_h = candidate_smile
        f_x, f_y, f_w, f_h = candidate_face

        return (
            s_x >= f_x and
            s_x + s_w  <= f_x + f_w and
            s_y >= f_y and
            s_y + s_h <= f_y + f_h
        )

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
        maybe_smiles = self.smile_classifier.detectMultiScale(image_gray, 1.3, 14)

        # Define set of smiles found within the bounds of the set of faces.
        smiles=list()
        for smile in maybe_smiles:
            smile_in_face = False
            for face in maybe_faces:
                if self.is_smile_in_face(smile, face):
                    smile_in_face = True
            if smile_in_face:
                smiles.append(smile)
        
        return smiles
