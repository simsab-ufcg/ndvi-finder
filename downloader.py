import subprocess
import csv
import sys
import os
from pprint import pprint

def get_processing_date_from_product_id(product_id):
  """
    Ex: LC08_L1TP_149039_20180703_20180717_01_T1
  """
  fields = product_id.split('_')
  return fields[3]

def get_path_from_product_id(product_id):
  fields = product_id.split('_')
  return fields[2][0:3]

def get_row_from_product_id(product_id):
  fields = product_id.split('_')
  return fields[2][3:6]

def parse_path_and_rows(filename):
  parsed_data = {}
  with open(filename) as open_file:
    for line in open_file:

      line_sp = line.split(' ')
      id = line_sp[0]
      parsed_data[id] = []
      
      for i in range(1, (len(line_sp) - 1)/2 + 1):
        scene_obj = {}
        scene_obj['path'] = int(line_sp[2 * i - 1])
        scene_obj['row'] = int(line_sp[2 * i])
        parsed_data[id].append(scene_obj)
  
  return parsed_data

def parse_time_periods(filename):
  parsed_data = {}
  with open(filename) as csvfile:
    csv_reader = csv.reader(csvfile, delimiter = ',')
    
    header = csv_reader.next()

    region_name_index = header.index('REGION_NAME')
    start_date_index = header.index('START_DATE')
    end_date_index = header.index('END_DATE')

    for line in csv_reader:
      
      id = line[region_name_index]
      parsed_data[id] = {}
      parsed_data[id]['start_date'] = ''.join(line[start_date_index].split(' '))
      parsed_data[id]['end_date'] = ''.join(line[end_date_index].split(' '))

  return parsed_data 

def is_valid_product(product_id, start_date, end_date):
  is_valid = True
  processing_date = get_processing_date_from_product_id(product_id)
  if(start_date and processing_date < start_date):
    is_valid = False
  if(end_date and processing_date > end_date):
    is_valid = False
  # only T1 images
  if(product_id[-1] != '1'):
    is_valid = False
  return is_valid

def build_product_obj(product_id, start_date, end_date, download_url, cloud_cover):
  if(is_valid_product(product_id, start_date, end_date)):
    product_obj = {}
    product_obj['product_id'] = product_id
    product_obj['path'] = get_path_from_product_id(product_id)
    product_obj['row'] = get_row_from_product_id(product_id)
    product_obj['download_url'] = download_url
    product_obj['processed_at'] = get_processing_date_from_product_id(product_id)
    product_obj['cloud_cover'] = cloud_cover
    return product_obj
  else:
    return None

def setup():
  subprocess.call(['curl', 'https://landsat-pds.s3.amazonaws.com/c1/L8/scene_list.gz', '--output', 'scene_list.gz'])
  subprocess.call(['gunzip', 'scene_list.gz'])

def search(path, row, start_date = None, end_date = None):
  products = []
  with open('scene_list') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter = ',')
    
    header = csv_reader.next()
    
    path_index = header.index('path')
    row_index = header.index('row')
    product_id_index = header.index('productId')
    download_url_index = header.index('download_url')
    cloud_cover_index = header.index('cloudCover')

    for product in csv_reader:
      if(int(product[path_index]) == path and int(product[row_index]) == row):
        product_id = product[product_id_index]
        download_url = product[download_url_index]
        cloud_cover = float(product[cloud_cover_index])
        product_obj = build_product_obj(product_id, start_date, end_date, download_url, cloud_cover)

        if(product_obj): 
          products.append(product_obj)

  return products

"""
  query = {
    path {
      Set(row)
    }
  }
"""
def batch_search(query, start_date=None, end_date=None):
  result = {}
  paths = query.keys()
  for path in paths:
    result[path] = {}
    rows = query[path]
    for row in rows:
      result[path][row] = []
  
  with open('scene_list') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter = ',')
    
    header = csv_reader.next()
    
    path_index = header.index('path')
    row_index = header.index('row')
    product_id_index = header.index('productId')
    download_url_index = header.index('download_url')
    cloud_cover_index = header.index('cloudCover')

    for product in csv_reader:
      path = int(product[path_index])
      row = int(product[row_index])
      if query.has_key(path) and row in query[path]:

        product_id = product[product_id_index]
        download_url = product[download_url_index]
        cloud_cover = float(product[cloud_cover_index])

        product_obj = build_product_obj(product_id, start_date, end_date, download_url, cloud_cover)

        if(product_obj):
          result[path][row].append(product_obj)
  
  return result



def download_scene(scenes, output_directory):
  subprocesses = []
  for scene in scenes:
    url_sp = scene['download_url'].split('/')
    url_sp = url_sp[0:len(url_sp) - 1]
    bands = ['B4', 'B5', 'BQA']
    scene_directory = output_directory + scene['product_id'] + '/'
    subprocess.call(['mkdir', '-p', scene_directory])
    for band in bands:
      print 'started download of ' + scene['product_id'] + '_' + band
      product_band_id = scene['product_id'] + '_' + band + '.TIF'
      new_url = '/'.join(url_sp) + '/' + product_band_id
      FNULL = open(os.devnull, 'w')
      subprocesses.append((subprocess.Popen(' '.join(['curl', new_url, '--output', scene_directory + product_band_id]), 
          shell=True, stdout=FNULL, stderr=FNULL), scene['product_id'] + '_' + band))
  for (process, product_id) in subprocesses:
    process.wait()
    print product_id + ' downloaded'

def get_scenes(path_and_rows, start_date, end_date):
  path_and_rows_obj = {}
  for pr_obj in path_and_rows:
    if(path_and_rows_obj.has_key(pr_obj['path'])):
      path_and_rows_obj[pr_obj['path']].add(pr_obj['row'])
    else:
      path_and_rows_obj[pr_obj['path']] = set([pr_obj['row']])

  return batch_search(path_and_rows_obj, start_date, end_date)

def info(path_and_rows_file, time_periods):
  ids = path_and_rows_file.keys()
  num_semi = 0
  num_plac = 0
  for id in ids:
    start_date = time_periods[id]['start_date']
    end_date = time_periods[id]['end_date']

    scenes = get_scenes(path_and_rows[id], start_date, end_date)

    num_scenes = 0
    num_places = 0
    paths = scenes.keys()
    for path in paths:
      rows = scenes[path].keys()
      for row in rows:
        print 'posistion', 'path='+str(path), 'row='+str(row), 'nscenes='+str(len(scenes[path][row]))
        cloud_cover_loc = []
        for scene in scenes[path][row]:
          cloud_cover_loc.append(scene['cloud_cover'])
        cloud_cover_loc.sort()
        print '\033[94m' + 'cloud cover: ' + ' '.join(map(str, cloud_cover_loc)) + '\033[0m'
        num_scenes += min(len(scenes[path][row]), 3)
        num_places += 1
    print '\033[92m' + 'region', 'id='+id, 'nscenes=' + str(num_scenes), 'nplaces=' + str(num_places) + '\033[0m'
    num_semi += num_scenes
    num_plac += num_places
  print '\033[91m' + 'semi-arid', 'nscenes=' + str(num_semi), 'nplaces='+str(num_plac) + '\033[0m'

def download(path_and_rows_file, time_periods, output_directory):
  ids = path_and_rows_file.keys()
  for id in ids:
    start_date = time_periods[id]['start_date']
    end_date = time_periods[id]['end_date']

    scenes = get_scenes(path_and_rows[id], start_date, end_date)

    num_scenes = 0
    num_places = 0
    paths = scenes.keys()
    for path in paths:
      rows = scenes[path].keys()
      for row in rows:
        num_scenes += min(len(scenes[path][row]), 3)
        num_places += 1
        download_scene(scenes[path][row], output_directory + id + '/')
  

if __name__ == '__main__':
  # if(len(sys.argv) != 4):
  #   print('Incorrect number of arguments')
  #   exit()
  print(sys.argv)
  command = sys.argv[1]
  if command == 'setup':
    setup()
  elif command == 'search':
    path = int(sys.argv[2])
    row = int(sys.argv[3])
    start_date = sys.argv[4]
    end_date = sys.argv[5]
    # pprint(search(path, row, start_date, end_date))
    pprint(batch_search({
      path: set([row])
    }, start_date, end_date))
  elif command == 'download':
    path_and_rows = parse_path_and_rows(sys.argv[2])
    time_periods = parse_time_periods(sys.argv[3])
    output_directory = sys.argv[4 ]
    download(path_and_rows, time_periods, output_directory)
  elif command == 'info':
    path_and_rows = parse_path_and_rows(sys.argv[2])
    time_periods = parse_time_periods(sys.argv[3])
    info(path_and_rows, time_periods)
  