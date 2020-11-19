import cv2
import numpy as np
from tone import createTone, pasteLayers, resizeToFitLongSide

# raw_file_name = 'kimikura.jpg'
raw_file_name ='thai_curry.jpg'

# thresholds = [50, 75, 100, 125, 150, 175, 200, 205, 215]
# tone_thresholds = [1.75, 2.00, 2.50, 3.50, 4.50, 5.00, 7.50, 20.00]
thresholds = [50, 75, 100, 125, 150, 175, 200, 215] # for ~1000px
tone_thresholds = [1.75, 2, 2.5, 3.25, 7.25, 10.50, 20.25] # for ~1000px

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
  file_path = 'out/' + file_name
  cv2.imwrite(file_path, img_bgra)
  return file_path

img = cv2.imread('raw/' + raw_file_name)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_gray = resizeToFitLongSide(img_gray, 1000) # 縮小
cv2.imwrite('out/gray.' + raw_file_name, img_gray)

# 下地画像をつくる
ret, img_bin = cv2.threshold(img_gray, thresholds[0], 255, cv2.THRESH_BINARY)
h, w = img_bin.shape
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
