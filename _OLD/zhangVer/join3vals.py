import os
from colorizers import *
import matplotlib.pyplot as plt
import zipfile

colorizeZipFileName = 'zipboi'
doesColorizedExist = 'false'

# --- Function to colorize image
# NOTE: this was made possible due to the wonderful colorizing library at: https://github.com/richzhang/colorization
def colorizeImage(origImage,pathToImg,extensionType):
    img_path = f"{pathToImg}{origImage}{extensionType}"
    print(f"Location of Target Image: {img_path}")

    # load colorizers
    colorizer_eccv16 = eccv16(pretrained=True).eval()
    colorizer_siggraph17 = siggraph17(pretrained=True).eval()

    # default size to process images is 256x256
    # grab L channel in both original ("orig") and resized ("rs") resolutions
    img = load_img(img_path)
    (tens_l_orig, tens_l_rs) = preprocess_img(img, HW=(256,256))

    # colorizer outputs 256x256 ab map
    # resize and concatenate to original L channel
    img_bw = postprocess_tens(tens_l_orig, torch.cat((0*tens_l_orig,0*tens_l_orig),dim=1))
    out_img_eccv16 = postprocess_tens(tens_l_orig, colorizer_eccv16(tens_l_rs).cpu())
    out_img_siggraph17 = postprocess_tens(tens_l_orig, colorizer_siggraph17(tens_l_rs).cpu())


    colorizedImageName1 = f'colorized_{origImage}1.{extensionType}'
    colorizedImageName2 = f'colorized_{origImage}2.{extensionType}'

    plt.imsave(colorizedImageName1, out_img_eccv16)
    plt.imsave(colorizedImageName2, out_img_siggraph17)





colorizeImage('imageName',"/path/",'.jpg')