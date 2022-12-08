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
enhancer_states = []

""" semaphores """
buffer_full = threading.Semaphore(0)
buffer_lock = threading.Semaphore()
enhanced_ctr_lock = threading.Semaphore()

def image_enhance(options):
  timer = threading.Thread(target=set_timeout_flag, args=(options['enhance_time'],))
  producer = threading.Thread(target=produce, args=(options['location'],))
  enhancers = [threading.Thread(target=enhance, args=(
    options['brightness'], 
    options['sharpness'],
    options['contrast'],
    options['save_loc'],
    i
  )) for i in range(options['nthreads'])]

  for enhancer in enhancers:
    enhancer_states.append(False)

  timer.start()
  producer.start()
  for enhancer in enhancers:
    enhancer.start()
  
  producer.join()
  for enhancer in enhancers:
    enhancer.join()
  timer.join()

  print(save_ctr)

  file = open('stats.txt', 'w+')
  file.write('# of enhanced images: ' + str(save_ctr))
  file.close()

def enhance(bright, sharp, contrast, save_loc, index):
  global enhanced_ctr
  global done_flag
  global save_ctr

  while not timeout_flag and not done_flag:
    with enhanced_ctr_lock:
      if enhanced_ctr == 0: 
        done_flag = True
        canAcquire = False
      else: 
        canAcquire = True
        enhanced_ctr -= 1
        
    if canAcquire:
      buffer_full.acquire()
      img, filename = buffer.pop()
        
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
        enhanced_image.save(f"{save_loc}/{filename}")
        save_ctr += 1
      else:
        with enhanced_ctr_lock:
          enhanced_ctr += 1

  print('thread', index, 'terminated')
  enhancer_states[index] = True

def produce(location):
  global enhanced_ctr
  
  with enhanced_ctr_lock:
    enhanced_ctr = len(os.listdir(location))

  for file in os.listdir(location):
    if timeout_flag and sum(enhancer_states) == len(enhancer_states):
      print('stop produce')
      break

    if (
        file.endswith(".png") or 
        file.endswith(".jpg") or 
        file.endswith(".jpeg") or 
        file.endswith(".gif")
    ):
      image = Image.open(location + '/' + file)
      filename = image.filename.rsplit('/', 1)[-1]
      image_copy = image.copy()
      image.close()

      buffer.append((image_copy, filename))
      buffer_full.release()

def set_timeout_flag(mins):
  global timeout_flag
  time.sleep(mins*60)
  timeout_flag = True