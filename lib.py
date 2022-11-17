import os, sys
from dotenv import load_dotenv
load_dotenv()

base_dir = os.environ.get('BASE_DIR_NAME', './')
if base_dir.startswith('/') and not base_dir.startswith('/tmp/'):
  print('Invalid base_dir:', base_dir)
  sys.exit(1)
# base_dir = '/tmp/'

def remove_tmp_files(image_name, thresholds):
  if not image_name:
    raise Exception('image_name is required.')

  tmp_file_paths = []
  thresholds.append('base')
  for t in thresholds:
    tmp_file_paths.append(base_dir + 'tmp/' + image_name + '.' + str(t) + '.masked.png')

  for tmp_file_path in tmp_file_paths:
    if os.path.exists(tmp_file_path):
      os.remove(tmp_file_path)

def remove_raw_file(image_name):
  if not image_name:
    raise Exception('image_name is required.')
  raw_file_path = base_dir + 'raw/' + image_name
  if os.path.exists(raw_file_path):
    os.remove(raw_file_path)

def create_dirs():
  print('base_dir:', base_dir)
  dir_names = ['tmp', 'raw', 'out']
  for dir_name in dir_names:
    dir_path = base_dir + dir_name
    if not os.path.exists(dir_path):
      os.makedirs(dir_path)

def is_debug():
  debug = os.environ.get('DEBUG', False)
  if debug == 'yes':
    return True
  return False
