
# predict_tumor.py
from tensorflow.keras.models import load_model
import cv2 as cv
import imutils
import numpy as np

try:
    model = load_model('brain_tumor_detector.h5')
except Exception as e:
    print(f"Error: Failed to load model 'brain_tumor_detector.h5': {str(e)}")
    raise

def predictTumor(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (5, 5), 0)
    thresh = cv.threshold(gray, 45, 255, cv.THRESH_BINARY)[1]
    thresh = cv.erode(thresh, None, iterations=2)
    thresh = cv.dilate(thresh, None, iterations=2)
    cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if not cnts:  # Handle case where no contours are found
        raise ValueError("No contours found in the image. Ensure the input is a valid MRI scan.")
    c = max(cnts, key=cv.contourArea)
    extLeft = tuple(c[c[:, :, 0].argmin()][0])
    extRight = tuple(c[c[:, :, 0].argmax()][0])
    extTop = tuple(c[c[:, :, 1].argmin()][0])
    extBot = tuple(c[c[:, :, 1].argmax()][0])
    new_image = image[extTop[1]:extBot[1], extLeft[0]:extRight[0]]
    new_image = cv.resize(new_image, dsize=(240, 240), interpolation=cv.INTER_CUBIC)
    new_image = new_image / 255.0
    new_image = new_image.reshape((1, 240, 240, 3))
    res = model.predict(new_image)
    return res[0][0]