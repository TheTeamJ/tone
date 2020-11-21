import cv2
import numpy as np
from tone import createTone, pasteLayers, resizeToFitLongSide

raw_file_name = 'thai_curry.jpg'
# 矩形の長辺のピクセル数 (オリジナルサイズの場合はNone)
thumbnail_size = 1000
histogram_equalization = False
tone_base = 1.50

# 2枚の画像の差分を求めてみよう
def generateImgBinDiffs (img_gray):
  diffs = []
  for i in range(0, len(thresholds)):
    if i == len(thresholds) - 1: continue
    # 閾値50と閾値100の結果の着色領域(黒領域)の差分
    # 閾値が大きいほうが着色領域は広くなる
    ret, img_bin_0 = cv2.threshold(img_gray, thresholds[i], 255, cv2.THRESH_BINARY)
    ret, img_bin_1 = cv2.threshold(img_gray, thresholds[i + 1], 255, cv2.THRESH_BINARY)
    diffs.append(cv2.bitwise_not(cv2.absdiff(img_bin_0, img_bin_1)))
  return diffs

def convertToTransparent (img, file_name):
  img_bgr = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
  img_bgra = np.concatenate([img_bgr, np.full((h, w, 1), 255, dtype=np.uint8)], axis=-1)
  white = np.all(img_bgr == [255, 255, 255], axis=-1)
  img_bgra[white, -1] = 0
  file_path = 'tmp/' + file_name
  cv2.imwrite(file_path, img_bgra)
  return file_path

def getThresholds (width, height):
  size = max(width, height)
  if size > 1000:
    thresholds = [50, 75, 100, 125, 150, 175, 200, 205, 215]
    tone_thresholds = [1.75, 2.00, 2.50, 3.50, 4.50, 5.00, 7.50, 20.00]
  else:
    thresholds = [50, 75, 100, 125, 150, 175, 200, 215]
    tone_thresholds = [1.75, 2, 2.5, 3.25, 7.25, 10.50, 20.25]
  return (thresholds, tone_thresholds)

def loadRawImage (file_path):
  img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
  h, w, a = img.shape
  if a <= 3:
    return img
  transparent_mask = img[:, :, 3] == 0
  img[transparent_mask] = [255, 255, 255, 255]
  return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

if __name__ == '__main__':
  img = loadRawImage('raw/' + raw_file_name)
  img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  if thumbnail_size:
    img_gray = resizeToFitLongSide(img_gray, thumbnail_size)
  if histogram_equalization:
    cv2.imwrite('out/gray/raw.' + raw_file_name, img_gray)
    # Contrast Limited Adaptive Histogram Equalization
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img_gray = clahe.apply(img_gray)
  cv2.imwrite('out/gray/' + raw_file_name, img_gray)

  # 下地画像をつくる
  h, w = img_gray.shape
  thresholds, tone_thresholds = getThresholds(w, h)
  ret, img_bin = cv2.threshold(img_gray, thresholds[0], 255, cv2.THRESH_BINARY)
  img_tone = createTone('tone72/{:.2f}.png'.format(tone_base), w, h)
  masked = cv2.bitwise_or(img_bin, img_tone)
  layer_file_paths = []
  layer_file_paths.append(convertToTransparent(masked, 'base.masked.png'))

  # 密度の異なる点描パターンレイヤーを重ねていく
  img_bin_diffs = generateImgBinDiffs(img_gray)
  for i in range(0, len(thresholds) - 1):
    img_bin_diff = img_bin_diffs[i]
    h, w = img_bin_diff.shape
    img_tone = createTone('tone72/{:.2f}.png'.format(tone_thresholds[i]), w, h)
    # マスク処理にはbitwise_or関数を用いる
    masked = cv2.bitwise_or(img_bin_diff, img_tone)
    file_path = convertToTransparent(masked, str(thresholds[i]) + '.masked.png')
    layer_file_paths.append(file_path)

  pasteLayers(img_bin, layer_file_paths, raw_file_name)
