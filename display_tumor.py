# display_tumor.py

import numpy as np
import cv2 as cv

class DisplayTumor:
    def __init__(self):
        self.Img = None
        self.cur_mask = None
        self.kernel = np.ones((3, 3), np.uint8)

    def read(self, image_bgr):
        """Store original image and compute initial Otsu threshold mask."""
        self.Img = image_bgr.copy()
        gray = cv.cvtColor(image_bgr, cv.COLOR_BGR2GRAY)
        _, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
        # remove small noise
        self.cur_mask = cv.morphologyEx(thresh, cv.MORPH_OPEN, self.kernel, iterations=2)

    def get_mask(self):
        """Return the cleaned binary mask after morphological operations."""
        return self.cur_mask

    def segment(self):
        """Run watershed on the current mask, paint boundary red."""
        # sure background
        sure_bg = cv.dilate(self.cur_mask, self.kernel, iterations=3)
        # sure foreground via distance transform
        dist = cv.distanceTransform(self.cur_mask, cv.DIST_L2, 5)
        _, sure_fg = cv.threshold(dist, 0.7 * dist.max(), 255, 0)
        sure_fg = np.uint8(sure_fg)
        unknown = cv.subtract(sure_bg, sure_fg)

        # label markers
        _, markers = cv.connectedComponents(sure_fg)
        markers = markers + 1
        markers[unknown == 255] = 0

        # watershed
        markers = cv.watershed(self.Img, markers)
        # boundary pixels marked with -1
        self.Img[markers == -1] = [0, 0, 255]  # red boundary

    def get_result(self):
        """Return the BGR image with overlay."""
        return self.Img
