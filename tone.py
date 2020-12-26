from PIL import Image
import os, math, cv2
import numpy as np
from lib import base_dir

# グレースケールのみ対応
def pil2cv (image):
  return np.array(image, dtype=np.uint8)

def createTone (src_path, out_width, out_height):
  im = Image.open(src_path)
  # 台紙を作成
  unit_size = 500
  scale = math.ceil(max(out_width, out_height) / float(unit_size))
  dst_size = int(unit_size * scale)
  im_dst = Image.new(mode='L', size=(dst_size, dst_size), color=0)
  for i in range(0, dst_size, unit_size):
    for j in range(0, dst_size, unit_size):
      im_dst.paste(im, (i, j))
  # 切り抜く
  # XXX: 中央付近をcropしたほうがいいかも？
  im_out = im_dst.crop(box=(0, 0, out_width, out_height))
  return pil2cv(im_out)

def pasteLayers (img_base, layer_paths, out_file_name='out.webp'):
  out_file_name = '.'.join(out_file_name.split('.')[:-1]) + '.webp'
  out_file_path = base_dir + 'out/' + out_file_name
  try:
    os.remove(out_file_path)
  except Exception as e:
    print(e)
  print(out_file_path)

  h, w = img_base.shape
  im_dst = Image.new(mode='RGBA', size=(w, h), color=(255, 255, 255, 255))
  for layer_path in layer_paths:
    im = Image.open(layer_path)
    im_dst.paste(im, (0, 0), im)
  im_dst = pil2cv(im_dst)
  im_dst = cv2.cvtColor(im_dst, cv2.COLOR_BGRA2GRAY)
  cv2.imwrite(out_file_path, im_dst)
  return out_file_path

def resizeToFitLongSide (img_base, size=1000):
  h, w = img_base.shape
  if w >= h:
    h = int(size * (h / w))
    w = size
  else:
    w = int(size * (w / h))
    h = size
  return cv2.resize(img_base, (w, h))
