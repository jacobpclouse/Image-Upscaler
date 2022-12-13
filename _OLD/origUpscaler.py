# https://towardsdatascience.com/deep-learning-based-super-resolution-with-opencv-4fd736678066

import cv2
from cv2 import dnn_superres

# Create an SR object
sr = dnn_superres.DnnSuperResImpl_create()

# Read image
image = cv2.imread('./input.png')

# Read the desired model
path = "EDSR_x3.pb"
sr.readModel(path)

# Set the desired model and scale to get correct pre- and post-processing
sr.setModel("edsr", 3)

# Upscale the image
result = sr.upsample(image)

# Save the image
cv2.imwrite("./upscaled.png", result)