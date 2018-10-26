# -*- coding: utf-8 -*-

import subprocess
import csv
import sys
import os
from pprint import pprint

def get_processing_date_from_scene_id(scene_id):
  """
    Ex: LC8 214 063 2013241 LGN02
  """
  return scene_id[9:16]

def get_path_from_scene_id(scene_id):
  return int(scene_id[3:6])

def get_row_from_scene_id(scene_id):
  return int(scene_id[6:9])

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

def is_valid_product(scene_id, start_date, end_date):
  is_valid = True
  processing_date = get_processing_date_from_scene_id(scene_id)
  if(start_date and processing_date < start_date):
    is_valid = False
  if(end_date and processing_date > end_date):
    is_valid = False
  if(scene_id[2] != '8' and scene_id[2] != '7' and scene_id[2] != '5' and scene_id[2] != '4'):
    is_valid = False
  # # only T1 images
  # if(scene_id[-1] != '1'):
  #   is_valid = False
  return is_valid

def build_product_obj(scene_id, start_date, end_date, download_url, cloud_cover):
  if(is_valid_product(scene_id, start_date, end_date)):
    product_obj = {}
    product_obj['scene_id'] = scene_id
    product_obj['path'] = get_path_from_scene_id(scene_id)
    product_obj['row'] = get_row_from_scene_id(scene_id)
    product_obj['download_url'] = download_url
    product_obj['processed_at'] = get_processing_date_from_scene_id(scene_id)
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
    
    path_index = header.index('PATH')
    row_index = header.index('ROW')
    scene_id_index = header.index('SCENE_ID')
    download_url_index = header.index('DOWNLOAD_URL')
    cloud_cover_index = header.index('CLOUD_COVER')

    for product in csv_reader:
      if(int(product[path_index]) == path and int(product[row_index]) == row):
        scene_id = product[scene_id_index]
        download_url = product[download_url_index]
        cloud_cover = float(product[cloud_cover_index])
        product_obj = build_product_obj(scene_id, start_date, end_date, download_url, cloud_cover)

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
    
    path_index = header.index('PATH')
    row_index = header.index('ROW')
    scene_id_index = header.index('SCENE_ID')
    download_url_index = header.index('DOWNLOAD_URL')
    cloud_cover_index = header.index('CLOUD_COVER')

    for product in csv_reader:
      path = int(product[path_index])
      row = int(product[row_index])
      if query.has_key(path) and row in query[path]:
        scene_id = product[scene_id_index]
        download_url = product[download_url_index]
        cloud_cover = float(product[cloud_cover_index])

        product_obj = build_product_obj(scene_id, start_date, end_date, download_url, cloud_cover)

        if(product_obj):
          result[path][row].append(product_obj)
  
  return result



def download_scene(scenes, output_directory):
  subprocesses = []
  paths = []
  for scene in scenes:
    url_sp = scene['download_url'].split('/')
    url_sp.append(url_sp[-1])
    bands = ['B4', 'B5', 'BQA', 'MTL']
    scene_id = scene['scene_id']
    pathrow = str(get_path_from_scene_id(scene_id)) + str(get_row_from_scene_id(scene_id))
    scene_directory = output_directory + pathrow + '/' + scene['scene_id'] + '/'
    subprocess.call(['mkdir', '-p', scene_directory])
    for band in bands:
      print 'started download of ' + scene['scene_id'] + '_' + band
      product_band_id = url_sp[-1] + '_' + band + '.TIF'
      new_url = '/'.join(url_sp) + '_' + band + '.TIF'
      FNULL = open(os.devnull, 'w')
      subprocesses.append((subprocess.Popen(' '.join(['curl', new_url, '--output', scene_directory + product_band_id]), 
          shell=True, stdout=FNULL, stderr=FNULL), scene['scene_id'] + '_' + band))
      paths.append(scene_directory + product_band_id)
  for (process, scene_id) in subprocesses:
    process.wait()
    print scene_id + ' downloaded'
  return paths

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

    print 'region=' + id
    num_scenes = 0
    num_places = 0
    paths = scenes.keys()
    for path in paths:
      rows = scenes[path].keys()
      for row in rows:
        real_scenes_obj = {}
        for scene in scenes[path][row]:
          real_scenes_obj[get_processing_date_from_scene_id(scene['scene_id'])] = scene
        real_scenes = real_scenes_obj.values()
        print 'path='+str(path), 'row='+str(row), 'nscenes='+str(len(real_scenes))
        cloud_cover_loc = []
        for scene in real_scenes:
          cloud_cover_loc.append(scene['cloud_cover'])
        cloud_cover_loc.sort()
        # print '\033[94m' + 'product ids: ' + str(len(real_scenes)) + '\033[0m'
        for scene in real_scenes:
          print 'SCENE_ID=' + scene['scene_id'], 'CLOUD_COVER=' + str(scene['cloud_cover'])
        print
        # print '\033[94m' + 'cloud cover: ' + ' '.join(map(str, cloud_cover_loc)) + '\033[0m'
        num_scenes += min(len(real_scenes), 100)
        num_places += 1
    # print '\033[92m' + 'region', 'id='+id, 'nscenes=' + str(num_scenes), 'nplaces=' + str(num_places) + '\033[0m'
    num_semi += num_scenes
    num_plac += num_places
  # print '\033[91m' + 'semi-arid', 'nscenes=' + str(num_semi), 'nplaces='+str(num_plac) + '\033[0m'

def get_shape_files(path_and_rows, directory_sample):
  ids = path_and_rows.keys()
  shps = {}
  for id in ids:
    shp = directory_sample + id + '.shp'
    shps[id] = shp
  return shps


def download(path_and_rows, time_periods, output_directory):
  ids = path_and_rows.keys()
  for id in ids:
    start_date = time_periods[id]['start_date']
    end_date = time_periods[id]['end_date']

    scenes = get_scenes(path_and_rows[id], start_date, end_date)

    paths = scenes.keys()
    for path in paths:
      rows = scenes[path].keys()
      for row in rows:
        download_scene(scenes[path][row], output_directory + id + '/')
  

if __name__ == '__main__':
  # if(len(sys.argv) != 4):
  #   print('Incorrect number of arguments')
  #   exit()
  command = sys.argv[1]
  if command == 'setup':
    setup()
  elif command == 'search':
    path = int(sys.argv[2])
    row = int(sys.argv[3])
    start_date = sys.argv[4]
    end_date = sys.argv[5]
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

  