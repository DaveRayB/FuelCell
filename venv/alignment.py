###################################
# This portion checks the top white ring for vertical alignment with the fuel cell
###################################

import numpy as np
from matplotlib import colors
import skimage
from skimage.color import rgb2gray
from skimage import io
import os
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt

gray_index = 0
gray_rect = 500
white_index = 0
white_rect = 0
gray_x_1 = 0
gray_x_2 = 0
white_x_1 = 0
white_x_2 = 0
gray_value_min = 0.3
gray_value_max = 0.5
white_value = 0.7
vertical_tolerance = 0.5
ptm = 264.5833
gray_x_offset = 130
gray_y_offset = 200
width = 300
height = 300

# Read in the cell image
filename = os.path.join(skimage.data_dir, 'misaligned_cell.jpg')
image = io.imread(filename)
cell = rgb2gray(image)

# Examine the position of the top ring relative to the fuel cell
for index, value in np.ndenumerate(cell):
    if white_x_1 > 0 and white_x_2 > 0:
        white_index = ((white_x_2 - white_x_1) / 2.0) + white_x_1
        break
    else:
        if value > white_value and white_x_1 == 0:
            white_x_1 = index[1]
        if white_x_1 > 0 and value < white_value:
            white_x_2 = index[1]
for index, value in np.ndenumerate(cell):
    if gray_x_1 > 0 and gray_x_2 > 0:
        gray_index = ((gray_x_2 - gray_x_1) / 2.0) + gray_x_1
        break
    else:
        if (gray_value_max >= value >= gray_value_min) and gray_x_1 == 0:
            gray_x_1 = index[1]
        if gray_x_1 > 0 and value < gray_value_min:
            gray_x_2 = index[1]

# Print the measurement error
error = abs(gray_index - white_index) * 1.0
if error > vertical_tolerance:
    print("ERROR: Top ring is out of alignment by " + str(error) + " microns")
else:
    print("Top ring is aligned correctly")

#Display the image
plt.imshow(cell)
# Get the current reference
ax = plt.gca()
# Create a Rectangle patch
rect = Rectangle((gray_index-gray_x_offset,gray_y_offset),width,height,linewidth=1,edgecolor='r',facecolor='none')
# Add the patch to the Axes
ax.add_patch(rect)
plt.show()