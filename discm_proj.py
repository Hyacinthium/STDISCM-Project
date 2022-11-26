# Folder location of images 
#  Folder location of enhanced images 
#  Enhancing time in minutes 
#  Brightness enhancement factor 
#  Sharpness enhancement factor 
#  Contrast enhancement factor

from PIL import Image
from PIL import ImageEnhance
import os
from os import listdir


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
    
    
    location = "C:/Users/leana/Documents/DISCM/project/images"
    enhancing_time = int(input("How long will the program run? "))
    brightness = int(input("Brightness: "))
    sharpness = int(input("Sharpness: "))
    contrast = int(input("Contrast: "))

    for images in os.listdir(location):
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

# image_loc = input("Input folder location: ")
# enhancing_time = int(input("How long will the program run? "))
# brightness = int(input("Brightness: "))
# sharpness = int(input("Sharpness: "))
# contrast = int(input("Contrast: "))

# image_file = Image.open(image_loc)
# image_file.show()

# # brightness
# curr_image = ImageEnhance.Brightness(image_file)
# new_image = curr_image.enhance(brightness)

# #sharpness
# curr_image = ImageEnhance.Sharpness(new_image)
# new_image = curr_image.enhance(sharpness)

# #contrast
# curr_image = ImageEnhance.Contrast(new_image)
# new_image = curr_image.enhance(contrast)

# new_image.show()