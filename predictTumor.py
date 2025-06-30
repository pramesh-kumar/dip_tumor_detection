# from tensorflow.keras.models import load_model
# import cv2 as cv
# import imutils

# model = load_model('brain_tumor_detector.h5')

## model.summary()

# # config=model.get_config()
# # print(config)

# # List weights for each layer
# # for layer in model.layers:
# #     weights = layer.get_weights()
# #     if weights:
# #         print(f"Layer: {layer.name}")
# #         print(f"Weights shape: {[w.shape for w in weights]}")



# import h5py

# with h5py.File('brain_tumor_detector.h5', 'r') as f:
#     print("Groups in HDF5 file:", list(f.keys()))
#     print("Model attributes:", list(f.attrs.keys()))

#     if 'model_weights' in f:
#         for layer_name in f['model_weights']:
#             print(f"Layer: {layer_name}")
#             for weight_name in f['model_weights'][layer_name]:
#                 item = f['model_weights'][layer_name][weight_name]
#                 if isinstance(item, h5py.Dataset):
#                     weight = item[:]
#                     print(f"  Weight: {weight_name}, Shape: {weight.shape}")
#                 elif isinstance(item, h5py.Group):
#                     print(f"  Subgroup: {weight_name}")
#                     for sub_weight_name in item:
#                         sub_item = item[sub_weight_name]
#                         if isinstance(sub_item, h5py.Dataset):
#                             sub_weight = sub_item[:]
#                             print(f"    Weight: {sub_weight_name}, Shape: {sub_weight.shape}")



# def predictTumor(image):
#     gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
#     gray = cv.GaussianBlur(gray, (5, 5), 0)

#     # Threshold the image, then perform a series of erosions +
#     # dilations to remove any small regions of noise
#     thresh = cv.threshold(gray, 45, 255, cv.THRESH_BINARY)[1]
#     thresh = cv.erode(thresh, None, iterations=2)
#     thresh = cv.dilate(thresh, None, iterations=2)

#     # Find contours in thresholded image, then grab the largest one
#     cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
#     cnts = imutils.grab_contours(cnts)
#     c = max(cnts, key=cv.contourArea)

#     # Find the extreme points
#     extLeft = tuple(c[c[:, :, 0].argmin()][0])
#     extRight = tuple(c[c[:, :, 0].argmax()][0])
#     extTop = tuple(c[c[:, :, 1].argmin()][0])
#     extBot = tuple(c[c[:, :, 1].argmax()][0])

#     # crop new image out of the original image using the four extreme points (left, right, top, bottom)
#     new_image = image[extTop[1]:extBot[1], extLeft[0]:extRight[0]]

#     image = cv.resize(new_image, dsize=(240, 240), interpolation=cv.INTER_CUBIC)
#     image = image / 255.

#     image = image.reshape((1, 240, 240, 3))

#     res = model.predict(image)

#     return res












from tensorflow.keras.models import load_model
import cv2 as cv
import imutils
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

model = load_model('brain_tumor_detector.h5')
logging.debug("Brain tumor detector model loaded")

model.summary()

config=model.get_config()
print(config)


import h5py

with h5py.File('brain_tumor_detector.h5', 'r') as f:
    print("Groups in HDF5 file:", list(f.keys()))
    print("Model attributes:", list(f.attrs.keys()))

    if 'model_weights' in f:
        for layer_name in f['model_weights']:
            print(f"Layer: {layer_name}")
            for weight_name in f['model_weights'][layer_name]:
                item = f['model_weights'][layer_name][weight_name]
                if isinstance(item, h5py.Dataset):
                    weight = item[:]
                    print(f"  Weight: {weight_name}, Shape: {weight.shape}")
                elif isinstance(item, h5py.Group):
                    print(f"  Subgroup: {weight_name}")
                    for sub_weight_name in item:
                        sub_item = item[sub_weight_name]
                        if isinstance(sub_item, h5py.Dataset):
                            sub_weight = sub_item[:]
                            print(f"    Weight: {sub_weight_name}, Shape: {sub_weight.shape}")





def predictTumor(image):
    logging.debug("predictTumor called")
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (5, 5), 0)

    # Threshold the image, then perform a series of erosions +
    # dilations to remove any small regions of noise
    thresh = cv.threshold(gray, 45, 255, cv.THRESH_BINARY)[1]
    thresh = cv.erode(thresh, None, iterations=2)
    thresh = cv.dilate(thresh, None, iterations=2)

    # Find contours in thresholded image, then grab the largest one
    cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    if not cnts:
        logging.error("No contours found in the image")
        raise ValueError("No contours found in the image. The image may be too noisy or lack distinct features.")

    c = max(cnts, key=cv.contourArea)

    # Find the extreme points
    extLeft = tuple(c[c[:, :, 0].argmin()][0])
    extRight = tuple(c[c[:, :, 0].argmax()][0])
    extTop = tuple(c[c[:, :, 1].argmin()][0])
    extBot = tuple(c[c[:, :, 1].argmax()][0])

    # Crop new image out of the original image using the four extreme points (left, right, top, bottom)
    new_image = image[extTop[1]:extBot[1], extLeft[0]:extRight[0]]

    image = cv.resize(new_image, dsize=(240, 240), interpolation=cv.INTER_CUBIC)
    image = image / 255.

    image = image.reshape((1, 240, 240, 3))

    res = model.predict(image)
    logging.debug(f"Prediction result: {res[0][0]}")
    return res[0][0]  # Return the scalar probability