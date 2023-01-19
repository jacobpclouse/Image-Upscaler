from PIL import Image




image = Image.open('./a.jpg')
image.thumbnail((23132, 2341))
image.save('image_thumbnail.jpg')
print(image.size) # Output: (400, 350)