# Folder location of images 
#  Folder location of enhanced images 
#  Enhancing time in minutes 
#  Brightness enhancement factor 
#  Sharpness enhancement factor 
#  Contrast enhancement factor

from PIL import Image
from PIL import ImageEnhance
from os import listdir
import argparse

# TODO 
# - argparse 
# - isolate two methods [functional, domain]
# - pip freeze
# - reference algo 2 ni sir digimap
# - default { functional: 3, domain: 1 }
# - default values for bright sharp contrast
# - add save location, default would be current folder
def img_enhance(bright, sharp, contrast, img):
    curr_image = ImageEnhance.Brightness(img)
    new_image = curr_image.enhance(bright)

    #sharpness
    curr_image = ImageEnhance.Sharpness(new_image)
    new_image = curr_image.enhance(sharp)

    #contrast
    curr_image = ImageEnhance.Contrast(new_image)
    new_image = curr_image.enhance(contrast)

    return new_image

def main():
    
    # location = input("Input location of images: ")
    location = "C:/Users/leana/Documents/DISCM/project/images"
    enhancing_time = float(input("How long will the program run? "))
    brightness = float(input("Brightness: "))
    sharpness = float(input("Sharpness: "))
    contrast = float(input("Contrast: "))

    for images in listdir(location):
        # check if the image ends with png or jpg or jpeg
        if (images.endswith(".png") or images.endswith(".jpg") or images.endswith(".jpeg") or images.endswith(".gif")):
            # display
            curr = Image.open(location + '/' + images)
            curr.show()
            new_image = img_enhance(brightness, sharpness, contrast, curr)
            new_image.show()
            print(images)

if __name__ == "__main__":
    main()