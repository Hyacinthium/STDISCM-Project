import image_enhancer
from PIL import ImageEnhance
from PIL import Image

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

def gif_enhancer(bright, sharp, contrast, img):
    new = []
    for frame in range(0,img.n_frames):
        img.seek(frame)
        new_frame = Image.new('RGBA', img.size)
        new_frame.paste(img)
        new_frame = img_enhance(bright, sharp, contrast, new_frame)
        new.append(new_frame)

    new[0].save('new.gif', append_images=new[1:], save_all=True, duration = img.info['duration'], loop= img.info['loop'])