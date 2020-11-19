from PIL import Image
import os, math, cv2
import numpy as np

# グレースケールのみ対応
def pil2cv (image):
  newImage = np.array(image, dtype=np.uint8)
  return newImage

def createTone (srcPath, outWidth, outHeight):
  print(srcPath)
  im = Image.open(srcPath)
  # 台紙を作成
  toneSize = 500
  scale = math.ceil(max(outWidth, outHeight) / float(toneSize))
  dstSize = int(toneSize * scale)
  imDst = Image.new(mode='L', size=(dstSize, dstSize), color=0)
  for i in range(0, dstSize, toneSize):
    for j in range(0, dstSize, toneSize):
      imDst.paste(im, (i, j))
  # 切り抜く
  imOut = imDst.crop(box=(0, 0, outWidth, outHeight))
  return pil2cv(imOut)

def pasteLayers (imgBase, layerPaths, outFileName='a.png'):
  outFileName = '.'.join(outFileName.split('.')[:-1]) + '.png'
  outFilePath = 'out/' + outFileName
  try:
    os.remove(outFilePath)
  except:
    pass
  print(layerPaths)

  h, w = imgBase.shape
  imDst = Image.new(mode='RGBA', size=(w, h), color=(255, 255, 255, 255)) # (0, 0, 0, 0)
  for layerPath in layerPaths:
    im = Image.open(layerPath)
    imDst.paste(im, (0, 0), im)
  cv2.imwrite(outFilePath, pil2cv(imDst))

def resizeToFitLongSide (imgBase, size=1000):
  h, w = imgBase.shape
  # if max(h, w) <= size:
    # return imgBase
  if w >= h:
    h = int(size * (h / w))
    w = size
  else:
    w = int(size * (w / h))
    h = size
  return cv2.resize(imgBase, (w, h))
