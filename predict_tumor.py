# predict_tumor.py

import cv2 as cv
import imutils
from tensorflow.keras.models import load_model

# load your trained model once
_model = load_model('brain_tumor_detector.h5')

def predict_tumor(image_bgr):
    """
    Takes a BGR numpy array, returns a float probability of tumor.
    """
    gray = cv.cvtColor(image_bgr, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (5, 5), 0)

    # Threshold + noise removal
    thresh = cv.threshold(gray, 45, 255, cv.THRESH_BINARY)[1]
    thresh = cv.erode(thresh, None, iterations=2)
    thresh = cv.dilate(thresh, None, iterations=2)

    # Find largest contour
    cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if not cnts:
        return 0.0
    c = max(cnts, key=cv.contourArea)

    # Crop to bounding box
    extLeft = tuple(c[c[:, :, 0].argmin()][0])
    extRight = tuple(c[c[:, :, 0].argmax()][0])
    extTop = tuple(c[c[:, :, 1].argmin()][0])
    extBot = tuple(c[c[:, :, 1].argmax()][0])
    crop = image_bgr[extTop[1]:extBot[1], extLeft[0]:extRight[0]]

    # Resize + normalize
    resized = cv.resize(crop, (240, 240), interpolation=cv.INTER_CUBIC)
    inp = resized.astype('float32') / 255.0
    inp = inp.reshape((1, 240, 240, 3))

    # Predict
    prob = float(_model.predict(inp)[0][0])
    return prob
