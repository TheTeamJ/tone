from PIL import Image
import os, math, cv2
import numpy as np
from lib import base_dir

BASE_IMAGE_MODE_W = 'White'
BASE_IMAGE_MODE_T = 'Transparent'
BASE_IMAGE_MODE_C = 'Color' # 原画との合成

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

def pasteLayers (img_raw, img_base, layer_paths, out_file_name='out.webp', \
  save_format='webp', binarization_threshold=None, base_image_mode='White'):
  out_file_name = '.'.join(out_file_name.split('.')[:-1]) + '.' + save_format
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

  # 要求に応じて二値化する
  if binarization_threshold is not None:
    _, im_dst = cv2.threshold(im_dst, binarization_threshold, 255, cv2.THRESH_BINARY)
    # 背景色 (黒以外の箇所の色) の透過処理はこのタイミングで行う
    if base_image_mode in [BASE_IMAGE_MODE_T, BASE_IMAGE_MODE_C]:
      white = np.all(im_dst == [255, 255, 255, 255], axis=-1)
      im_dst[white, -1] = 0

  if base_image_mode == BASE_IMAGE_MODE_W:
    im_dst = cv2.cvtColor(im_dst, cv2.COLOR_BGRA2GRAY)
  elif base_image_mode == BASE_IMAGE_MODE_C:
    im_dst_raw = cv2.cvtColor(img_raw, cv2.COLOR_BGR2BGRA)
    print('###!!!!!', np.shape(im_dst_raw), np.shape(im_dst))
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
