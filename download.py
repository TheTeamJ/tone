import requests, urllib, hashlib, secrets
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

def get_ext_from_data_uri(data_uri):
  """Return extension of data URI image"""
  if data_uri.startswith('data:image/jpeg;base64,'):
    return '.jpg'
  elif data_uri.startswith('data:image/jpg;base64,'):
    return '.jpg'
  elif data_uri.startswith('data:image/png;base64,'):
    return '.png'
  raise Exception('Unsupported image: %s' % data_uri)

def download_image(url, is_data_uri = False):
  sec = secrets.token_hex(16)
  md5 = hashlib.md5(url.encode('utf-8')).hexdigest()

  if is_data_uri:
    res = urllib.request.urlopen(url)
    file_name = '%s_%s%s' % (md5, sec, get_ext_from_data_uri(url))
    file_path = base_dir + 'raw/%s' % file_name
    with open(file_path, 'wb') as fp:
      fp.write(res.file.read())
    return file_name

  url = url.split('?')[0]
  res = requests.get(url, stream=True)
  res.raise_for_status()
  raise_for_content_type(res)
  file_name = '%s_%s%s' % (md5, sec, get_ext(res))
  file_path = base_dir + 'raw/%s' % file_name
  with open(file_path, 'wb') as fp:
    fp.write(res.content)
  return file_name
