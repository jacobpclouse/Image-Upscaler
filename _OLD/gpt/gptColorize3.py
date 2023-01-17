import cv2

imageToOpen = input("What is the path to the image?: ")

# Load the grayscale image
gray_image = cv2.imread(imageToOpen, 0)

# Define the colorization parameters
radius = 3
edges_threshold = 0.1

# Apply the colorization algorithm
color_image = cv2.edgePreservingFilter(gray_image, flags=1, sigma_s=60, sigma_r=0.4)

# Save the colorized image
cv2.imwrite("colorized_image.jpg", color_image)