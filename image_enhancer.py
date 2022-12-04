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
import argparse

# TODO 
# - argparse 
# - isolate two methods [functional, domain]
# - pip freeze
# - reference algo 2 ni sir digimap
# - default { functional: 3, domain: 1 }
# - default values for bright sharp contrast
# - add save location, default would be current folder

def main():
    
    parser = argparse.ArgumentParser()

    parser.add_argument("--location", type=str, default=os.getcwd(), help="Directory on where the images that will be enhanced are")
    parser.add_argument("--enhance_time", type=float, default=5.0, help="How long the program will run")
    parser.add_argument("--brightness", type=float, default=1.0, help="Brightness of the image")
    parser.add_argument("--sharpness", type=float, default=1.0, help="Sharpness of the image")
    parser.add_argument("--contrast", type=float, default=1.0, help="Contrast of the image")
    parser.add_argument("--nthreads", type=int, default=1, help="How many threads to use")
    parser.add_argument("--save_loc", type=str, default=os.getcwd(), help="Directory on where to save the image that were enhanced")

    args = parser.parse_args()

    for images in listdir(args.location):
        # check if the image ends with png or jpg or jpeg
        if (images.endswith(".png") or images.endswith(".jpg") or images.endswith(".jpeg") or images.endswith(".gif")):
            # display
            curr = Image.open(args.location + '/' + images)
            curr.show()
            new_image = img_enhance(args.brightness, args.sharpness, args.contrast, curr)
            new_image.show()
            print(images)

if __name__ == "__main__":
    main()