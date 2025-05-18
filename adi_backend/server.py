import time
import json
import signal

from smile_detector import SmileDetector
from video_steamer import VideoStreamer, log
from cv2 import imencode
from flask import Flask, render_template, Response
from flask_cors import CORS

# Initalize streamer and classifier objects.
streamer = VideoStreamer()
smile_detector = SmileDetector()

# Dictionary structure for stored smiles.
detected_smiles = {
    "image": {
        "width": streamer.frame_width,
        "height": streamer.frame_height,
    },
    "smiles": {
    },
}

# Initialize flask app.
# https://github.com/corydolphin/flask-cors
app = Flask(__name__)
CORS(app)

def process_coords(coords):
    """ Helper function to translate a list of coodinates into a dictionary.
    Args:
    - coords: list of integer tuples in form (x, y)
    
    Return:
    - dictionary of coords in form: {id: (x, y), ...}
    """

    coords_str = [f"({str(x)}, {str(y)})" for x, y in coords]
    coords_dict = {f"{index}:": value for index, value in enumerate(coords_str)}
    return coords_dict

def proccess_stream(streamer):
    """ Helper function to continiously encode video capture as jpegs.
    Args:
    - VideoStreamer object

    Yeild:
    - sequentiall returns encoded jpeg frames
    """
    while True:
        frame = streamer.get_frame()
        processed_frame = smile_detector.process_frame(frame)
        ret, buffer = imencode('.jpg', processed_frame)
        frame_bytes = buffer.tobytes()

        smiles_in_frame = smile_detector.get_smile_coords()
        if len(smiles_in_frame) > 0:
            detected_smiles["smiles"][str(time.time())] = process_coords(smiles_in_frame)
        # https://wiki.tcl-lang.org/page/multipart%2Fx-mixed-replace
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    """ Endpoint to grab a stream of jpegs bound as frames.
    """
    # https://wiki.tcl-lang.org/page/multipart%2Fx-mixed-replace
    return Response(proccess_stream(streamer), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/smiles')
def upload_smiles():
    """ Endpoint to grab image/smile metadata. Returns a json object.
    
    Keys:
    - image: width, height
    - simles: index, coordinates
    """

    # Get image metadata
    image_metadata_dict = {"image": (streamer.frame_width, streamer.frame_height)}

    # Get smile data
    smile_coords = smile_detector.get_smile_coords()
    smile_dict = {"smiles": process_coords(smile_coords)}

    return json.dumps(image_metadata_dict | smile_dict)

def save_detected_faces(sig, frame):
    """ Helper function to store detected faces incase of server interrupt.
    """
    file_name = "detected_smiles.json"
    log("flask_server", f"Saving detected smiles to {file_name}")
    with open(file_name, "w") as file:
        json.dump(detected_smiles, file, indent=4)
    exit(0)

signal.signal(signal.SIGINT, save_detected_faces)

if __name__ == '__main__':
    app.run(port=8081, threaded=True, use_reloader=False)
