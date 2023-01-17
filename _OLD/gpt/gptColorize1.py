from PIL import Image

# Open the image
imageToOpen = input("What is the path to the image?: ")
im = Image.open(imageToOpen)

# Define the color to use for the image
color = (255, 0, 0)  # red

# Create a new image with the same mode and size, but filled with the color
im = Image.new("RGB", im.size, color)

# Save the new image
im.save("colorized_image.jpg")
