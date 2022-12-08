import argparse

import domain_enhancer
import functional_enhancer

# Folder location of images 
# Folder location of enhanced images 
# Enhancing time in minutes 
# Brightness enhancement factor 
# Sharpness enhancement factor 
# Contrast enhancement factor

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--location", type=str, default='./images', help="Directory on where the images that will be enhanced are")
  parser.add_argument("--save_loc", type=str, default='./enhanced', help="Directory on where to save the image that were enhanced")
  parser.add_argument("--nthreads", type=int, default=1, help="How many threads to use")
  parser.add_argument("--enhance_time", type=float, default=0.05, help="How long the program will run")
  parser.add_argument("--brightness", type=float, default=1.0, help="Brightness of the image")
  parser.add_argument("--sharpness", type=float, default=1.0, help="Sharpness of the image")
  parser.add_argument("--contrast", type=float, default=1.0, help="Contrast of the image")
  parser.add_argument("--method", type=str, default='domain', help="options: domain | functional")

  args = (parser.parse_args())

  enhancer = domain_enhancer if args.method == 'domain' else functional_enhancer
  enhancer.image_enhance(vars(args)) 