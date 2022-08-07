import argparse
from PIL import Image
import numpy as np

# Argument Parsing
parser = argparse.ArgumentParser()
parser.add_argument('mode', help='encode or decode')
args, remaining = parser.parse_known_args()

if args.mode == 'encode':
  parser.add_argument('original_image', help='Image that you want to embed to')
  parser.add_argument('stega_image', help='Output')
elif args.mode == 'decode':
  parser.add_argument('stega_image', help='Image with embedded information')
else:
  print("Argument must be either 'encode' or 'decode'!")
  exit(-1)
  
args = parser.parse_args()

original_image = args.original_image if args.mode == 'encode' else None
stega_image = args.stega_image
mode = args.mode

# Reading in the image
def img_to_arr(dir, color_mode='RGBA'):
    img = Image.open(dir)
    img = img.convert(color_mode)
    img = np.array(img)
    return img
  
if mode == 'encode':
    img = img_to_arr(original_image)
elif mode == 'decode':
    img = img_to_arr(stega_image)

# Main algorithim

if mode == 'encode':
    pixel_num = 0
    cur_bit = 7
  
    message = input("Enter message: ")
    assert len(message) * 8 + 32 < (img.shape[0] * img.shape[1] * img.shape[2])  # each ascii char is 8 bits
  
    def add_len():
      global pixel_num, cur_bit, img, message
      
      message_len = len(message)
      
      for y in range(img.shape[0]):
        for x in range(img.shape[1]):
          for c in range(img.shape[2]):
            if pixel_num%8 == 0:
              cur_bit = 7
            img[y][x][c] |= (message_len >> cur_bit) & 1
            pixel_num += 1
            cur_bit -= 1
            if pixel_num == 32:
              return
    add_len()

    pixel_num = 0
    cur_bit = 7
  
    def add_message():
      global pixel_num, cur_bit, img, message
      
      char_iter = iter(message)
      pre_pixel_num = 0
      
      for y in range(img.shape[0]):
          for x in range(img.shape[1]):
              for c in range(img.shape[2]):
                  if pre_pixel_num != 32:
                    pre_pixel_num += 1
                  else:
                    if pixel_num%8 == 0:
                        cur_bit = 7
                        cur_char = next(char_iter)
                    img[y][x][c] |= (ord(cur_char) >> cur_bit) & 1
                    pixel_num += 1
                    cur_bit -= 1
                    if pixel_num == (len(message) * 8):
                        result = Image.fromarray(img)
                        result.save(stega_image)
                        return
    add_message()            
elif mode == 'decode':
  
    pixel_num = 0
    cur_bit = 7
  
    def read_len():
      global pixel_num, cur_bit, img
      length = 0
      for y in range(img.shape[0]):
        for x in range(img.shape[1]):
          for c in range(img.shape[2]):
            if pixel_num%8 == 0:
              cur_bit = 7
            length |= (img[y][x][c]&1)<<cur_bit
            pixel_num += 1
            cur_bit -= 1
            if pixel_num == 32:
              return length
              
    message_length = read_len()
  
    pixel_num = 0
    cur_bit = 7
  
    def read_message(): 
      global pixel_num, cur_bit, img
      pre_pixel_num = 0
      char_bin = 0
      res = ""
      for y in range(img.shape[0]):
          for x in range(img.shape[1]):
              for c in range(img.shape[2]):
                  if pre_pixel_num != 32:
                    pre_pixel_num += 1
                  else:
                    if pixel_num % 8 == 0:
                        cur_bit = 7
                        res += chr(char_bin)
                        char_bin = 0
                      
                    char_bin |= (img[y][x][c] & 1) << cur_bit
    
                    pixel_num += 1
                    cur_bit -= 1
                    if pixel_num == message_length*8+1:
                        return res
                      
    print(read_message())