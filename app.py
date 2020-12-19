import validators
from flask import Flask, request, send_file
from download import download_image
from main import main
from lib import create_dirs

app = Flask(__name__)

def parse_thumbnail_size(request):
  size_range = [100, 2000]
  size = 1000 # default size
  try:
    size = min(int(request.args.get("size", "1000")), size_range[1])
    if size < size_range[0]:
      size = size_range[0]
  except Exception as e:
    print(e)
  return size

def parse_histogram_equalization(request):
  auto = request.args.get("auto", "")
  if auto == '' or auto == 'no' or auto == '0':
    return False
  return True

@app.route("/", methods=["GET"])
def convert():
  image_url = request.args.get("url", "")
  if not validators.url(image_url):
    return 'Invalid URL: %s\n' % image_url, 400
  size = parse_thumbnail_size(request)
  auto = parse_histogram_equalization(request)

  # 画像をダウンロード
  input_file_name = ''
  try:
    input_file_name = download_image(image_url)
  except Exception as e:
    return 'Invalid request: %s\n' % e, 400

  if not input_file_name:
    return 'Error: input_file_name is empty.\n' % e, 500

  # 画像を点描画に変換
  output_file_path = ''
  try:
    print(size, auto)
    output_file_path = main(input_file_name, thumbnail_size=size, histogram_equalization=auto)
  except Exception as e:
    print(e)
    return 'Error: %s' % e, 500

  return send_file(output_file_path, as_attachment=False, mimetype='image/png')

if __name__ == '__main__':
  create_dirs()
  app.run(host="localhost", port=8080, debug=True)
