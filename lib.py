import os

# base_dir = './'
base_dir = './tmproot/'

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

def create_dirs():
  dir_names = ['tmp', 'raw', 'out']
  for dir_name in dir_names:
    dir_path = base_dir + dir_name
    if not os.path.exists(dir_path):
      os.makedirs(dir_path)
