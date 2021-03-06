import requests, hashlib, secrets
from lib import base_dir

def raise_for_content_type(res):
  """Raises Exception, if one occurred."""
  content_type = res.headers['Content-Type']

  error_msg = ''
  if not content_type:
    error_msg = 'Content-Type is empty'
  elif content_type not in ['image/jpg', 'image/jpeg', 'image/png']:
    error_msg = 'Unsupported image: %s' % content_type

  if error_msg:
    raise Exception(error_msg)

def get_ext(res):
  """Return file extension"""
  content_type = res.headers['Content-Type']
  if content_type == 'image/png':
    return '.png'
  elif content_type in ['image/jpg', 'image/jpeg']:
    return '.jpg'

def download_image(url):
  url = url.split('?')[0]
  res = requests.get(url, stream=True)
  res.raise_for_status()
  raise_for_content_type(res)
  md5 = hashlib.md5(url.encode('utf-8')).hexdigest()
  sec = secrets.token_hex(16)
  file_name = '%s_%s%s' % (md5, sec, get_ext(res))
  file_path = base_dir + 'raw/%s' % file_name
  with open(file_path, 'wb') as fp:
    fp.write(res.content)
  return file_name
