import validators
from flask import Flask, request
from download import download_image

app = Flask(__name__)

@app.route("/", methods=["GET"])
def convert():
  image_url = request.args.get("url", "")
  if not validators.url(image_url):
    return 'Invalid URL: %s' % image_url, 400
  try:
    download_image(image_url)
  except Exception as e:
    return 'Invalid request: %s' % e, 400
  return f"OK\n"

if __name__ == '__main__':
  app.run(host="localhost", port=8080, debug=True)
