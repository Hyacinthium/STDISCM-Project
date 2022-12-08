import os, time, threading
from PIL import Image
from PIL import ImageEnhance

""" global variables """
buffer = []
enhanced_ctr = 0
save_ctr = 0

""" flags """
timeout_flag = False
done_flag = False

""" semaphores """
buffer_full = threading.Semaphore(0)
buffer_lock = threading.Semaphore()
enhanced_ctr_lock = threading.Semaphore()

def image_enhance(options):
  timer = threading.Thread(target=set_timeout_flag, args=(options['enhance_time'],))
  producer = threading.Thread(target=produce, args=(options['location'],))
  enhancer = threading.Thread(target=enhance, args=(
    options['brightness'], 
    options['sharpness'],
    options['contrast'],
    options['save_loc'],
  ))

  producer.start()
  enhancer.start()
  timer.start()

  producer.join()
  enhancer.join()
  timer.join()

  print(save_ctr)

  file = open('stats.txt', 'w+')
  file.write('# of enhanced images: ' + str(save_ctr))
  file.close()

def enhance(bright, sharp, contrast, save_loc):
  global enhanced_ctr
  global done_flag
  global save_ctr

  while not timeout_flag and not done_flag:
    with enhanced_ctr_lock:
      if enhanced_ctr == 0: 
        done_flag = True
      else: 
        enhanced_ctr -= 1

    if not done_flag:
      buffer_full.acquire()
      with buffer_lock:
        img = buffer.pop()

      # Brightness
      curr_image = ImageEnhance.Brightness(img)
      enhanced_image = curr_image.enhance(bright)

      # Sharpness
      curr_image = ImageEnhance.Sharpness(enhanced_image)
      enhanced_image = curr_image.enhance(sharp)

      # Contrast
      curr_image = ImageEnhance.Contrast(enhanced_image)
      enhanced_image = curr_image.enhance(contrast)

      if not timeout_flag:
        enhanced_image.save(f"{save_loc}/{img.filename.rsplit('/', 1)[-1]}")
        save_ctr += 1

def gif_enhance(bright, sharp, contrast, img):
  new = []
  for frame in range(0,img.n_frames):
    img.seek(frame)
    new_frame = Image.new('RGBA', img.size)
    new_frame.paste(img)
    new_frame = enhance(bright, sharp, contrast, new_frame)
    new.append(new_frame)

  new[0].save('new.gif', append_images=new[1:], save_all=True, duration = img.info['duration'], loop= img.info['loop'])

def produce(location):
  global enhanced_ctr
  
  with enhanced_ctr_lock:
    enhanced_ctr = len(os.listdir(location))

  for file in os.listdir(location):
    if (
        file.endswith(".png") or 
        file.endswith(".jpg") or 
        file.endswith(".jpeg") or 
        file.endswith(".gif")
    ):
      image = Image.open(location + '/' + file)
      with buffer_lock:
        buffer.append(image)
        buffer_full.release()

def set_timeout_flag(mins):
  global timeout_flag
  # time.sleep(mins*60)
  time.sleep(1)
  timeout_flag = True


