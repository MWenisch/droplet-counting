import csv
import cv2
import matplotlib.pyplot as plt
from scipy.ndimage import binary_fill_holes
from skimage.morphology import flood_fill
from skimage.feature import peak_local_max
from skimage.segmentation import watershed
from scipy import ndimage
import numpy as np
import imutils

def droplet_counting(image, lower_boundary_threshold,minimal_droplet_size_in_pixel , show_mask_plot=False):
    imgOriginal = image
    blurred_img = cv2.GaussianBlur(imgOriginal, (5, 5), 0)
    blurredGray = cv2.cvtColor(blurred_img, cv2.COLOR_BGR2GRAY)

    ret2,thresh = cv2.threshold(blurredGray,lower_boundary_threshold,255,cv2.THRESH_BINARY)

    # Deep copy for results:
    inputImageCopy = imgOriginal.copy()

    # Find the contours on the binary image:
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Store bounding rectangles and object id here:
    objectData = []
    drop_radius = []
    drop_area = []
    drop_circularity = []

    # ObjectCounter:
    objectCounter = 0

    # Look for the outer bounding boxes (no children):
    for _, c in enumerate(contours):
        # draw a circle enclosing the object
        ((x, y), r) = cv2.minEnclosingCircle(c)

        if r < minimal_droplet_size_in_pixel:
            continue
        # Increment object counter
        objectCounter += 1
        drop_radius.append(r)

        # get the perimeter of the droplet and calculate the circularity of that droplet
        perimeter = cv2.arcLength(c, True)
        area = cv2.contourArea(c)
        if perimeter == 0:
            break
        circularity = (4 * math.pi * area) / (perimeter * perimeter)

        drop_circularity.append(circularity)

        # Counting the pixel Size of the droplets
        empty_image = np.zeros_like(inputImageCopy)
        only_one_shape = cv2.drawContours(empty_image, [c], -1, (255, 255, 255), thickness=cv2.FILLED)
        droplet_area_in_pixel = np.sum(only_one_shape/255/3)
        drop_area.append(droplet_area_in_pixel)

        # Store in list:
        objectData.append((objectCounter, {"x":x,"y":y,"r":r}))

        cv2.circle(blurred_img, (int(x), int(y)), int(r), (0, 255, 0), 2)
        cv2.putText(blurred_img, "{}".format(objectCounter), (int(x) - 10, int(y)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)
    
    #calculate the mean circularity of one frame
    if len(drop_circularity)>1:
        
        mean_circ = statistics.mean(drop_circularity)
     # calculate the deviation circularity
        deviation_circ = statistics.stdev(drop_circularity)
    elif len(drop_circularity) == 1:
        mean_circ = drop_circularity[0]
        deviation_circ = 0
    else:
        mean_circ = 0
        deviation_circ = 0 
        
    # plot results
    if show_mask_plot:
        fig, axes = plt.subplots(ncols=3, figsize=(12, 6), sharex=True, sharey=True)
        ax = axes.ravel()

        ax[0].imshow(imgOriginal, cmap=plt.cm.nipy_spectral)
        ax[0].set_title('Original Image')
        ax[1].imshow(thresh, cmap=plt.cm.gray)
        ax[1].set_title('Binary Mask')
        ax[2].imshow(blurred_img, cmap=plt.cm.nipy_spectral)
        ax[2].set_title('Overlay blurred+Image')

        for a in ax:
            a.set_axis_off()

        fig.tight_layout()
        plt.show()

    return objectCounter, drop_radius, drop_area, mean_circ, deviation_circ
