from PIL import Image

imageToOpen = input("What is the path to the image?: ")

# Open the image
im = Image.open(imageToOpen).convert('LA')

# Define the color to use for the image
color = (255, 0, 0)  # red

# Create a new image with the same mode and size, but filled with the color
im = Image.new("RGB", im.size, color)

# Create a mask for the image
mask = Image.new("L", im.size, 0)

# Apply the mask to the image
im.putalpha(mask)

# Save the new image
im.save("colorized_image.png")
