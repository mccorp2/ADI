### ADI Backend Smile Detector

#### server.py:
Flask server with two endpoints:
* video_feed: Sequentially uploads jpegs to mimick video.
* smiles: Returns image metadata, and smile coordinates.

#### smile_detector.py:
Class using opencv and existing classifiers to process images
and find faces and smiles then overlay rectangles about their positions.

To debug the paramaterization of these classifiers, use debug_stream
this can be found in video_streamer.py

#### video_streamer.py
Class using opencv to capture images from the hosts default camers.

Includes helper functions to debug classifiers in a local window.


### Potential Improvements:
* Store local host paramaters in a common .env file, and link both 
frontend and backend to these endpoints
* Unittests with unittest.mock
* Add static typing with mypy
* Add linter with pylint
* Enforce linting and static typing with pre-commit on git.
* Publish FPS metric and setup react to dynamically tune its interval from FPS.