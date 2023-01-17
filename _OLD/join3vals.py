import os

# --- Function to colorize image
def colorizeImage(origImage,pathToImg,extensionType):
    img_path = f"{pathToImg}{origImage}{extensionType}"
    imagePath = os.path.join(pathToImg, origImage, extensionType)
    print(f"String concat: {img_path}")
    print(f"Join Concat: {imagePath}")


colorizeImage('imageName',"/path/",'.jpg')