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


class Downloader():
  def setup(self):
    subprocess.call(['curl', 'https://landsat-pds.s3.amazonaws.com/c1/L8/scene_list.gz', '--output', 'scene_list.gz'])
    subprocess.call(['gunzip', 'scene_list.gz'])

  def search(self, path, row, start_date = None, end_date = None):
    products = []
    with open('scene_list') as csvfile:
      csv_reader = csv.reader(csvfile, delimiter = ',')
      
      header = csv_reader.next()
      
      path_index = header.index('path')
      row_index = header.index('row')
      product_id_index = header.index('productId')
      download_url_index = header.index('download_url')

      for product in csv_reader:
        if(int(product[path_index]) == path and int(product[row_index]) == row):
          is_valid = True
          product_id = product[product_id_index]
          processing_date = get_processing_date_from_product_id(product_id)
          if(start_date and processing_date < start_date):
            is_valid = False
          if(end_date and processing_date > end_date):
            is_valid = False
          # only T1 images
          if(product_id[-1] != '1'):
            is_valid = False
          if(is_valid):

            product_obj = {}
            product_obj['product_id'] = product_id
            product_obj['path'] = path
            product_obj['row'] = row
            product_obj['download_url'] = product[download_url_index]
            product_obj['processed_at'] = processing_date

            products.append(product_obj)
    return products

  """
    query = {
      path {
        row {
          start_date,
          end_date
        }
      }
    }
  """
  def batch_search(self, query):
    result = {}
    paths = query.keys()
    for path in paths:
      result[path] = {}
      rows = query[path].keys()
      for row in rows:
        result[path][row] = []
    
    with open('scene_list') as csvfile:
      csv_reader = csv.reader(csvfile, delimiter = ',')
      
      header = csv_reader.next()
      
      path_index = header.index('path')
      row_index = header.index('row')
      product_id_index = header.index('productId')
      download_url_index = header.index('download_url')

      for product in csv_reader:
        path = int(product[path_index])
        row = int(product[row_index])
        if query.has_key(path) and query[path].has_key(row):
          start_date = query[path][row]['start_date']
          end_date = query[path][row]['end_date']

          is_valid = True
          product_id = product[product_id_index]
          processing_date = get_processing_date_from_product_id(product_id)
          if(start_date and processing_date < start_date):
            is_valid = False
          if(end_date and processing_date > end_date):
            is_valid = False
          # only T1 images
          if(product_id[-1] != '1'):
            is_valid = False
          if(is_valid):

            product_obj = {}
            product_obj['product_id'] = product_id
            product_obj['path'] = path
            product_obj['row'] = row
            product_obj['download_url'] = product[download_url_index]
            product_obj['processed_at'] = processing_date

            result[path][row].append(product_obj)
    
    return result



  def download_scene(self, scenes, output_directory):
    subprocesses = []
    for scene in scenes:
      url_sp = scene['download_url'].split('/')
      url_sp = url_sp[0:len(url_sp) - 1]
      bands = ['B4', 'B5', 'BQA']
      for band in bands:
        product_band_id = scene['product_id'] + '_' + band + '.TIF'
        new_url = '/'.join(url_sp) + '/' + product_band_id
        FNULL = open(os.devnull, 'w')
        subprocesses.append((subprocess.Popen(' '.join(['curl', new_url, '--output', output_directory + product_band_id]), 
            shell=True, stdout=FNULL, stderr=FNULL), scene['product_id'] + '_' + band))
    for (process, product_id) in subprocesses:
      process.wait()
      print(product_id + ' downloaded')

      

  def download(self, path_and_rows_file, time_periods, output_directory):
    ids = path_and_rows_file.keys()
    subprocess.call(['mkdir', '-p', output_directory])
    for id in ids:
      subprocess.call(['mkdir', '-p', output_directory + id])
    for id in ids:
      start_date = time_periods[id]['start_date']
      end_date = time_periods[id]['end_date']
      for pr_obj in path_and_rows[id]:
        scenes = self.search(pr_obj['path'], pr_obj['row'], start_date, end_date)
        self.download_scene(scenes, output_directory + id + '/')


if __name__ == '__main__':
  # if(len(sys.argv) != 4):
  #   print('Incorrect number of arguments')
  #   exit()
  print(sys.argv)
  command = sys.argv[1]
  downloader = Downloader()
  # downloader.setup()
  if command == 'search':
    path = int(sys.argv[2])
    row = int(sys.argv[3])
    start_date = sys.argv[4]
    end_date = sys.argv[5]
    pprint(downloader.search(path, row, start_date, end_date))
    pprint(downloader.batch_search({
      path: {
        row: {
          "start_date": start_date,
          "end_date": end_date
        }
      }
    }))
  elif command == 'download':
    path_and_rows = parse_path_and_rows(sys.argv[2])
    time_periods = parse_time_periods(sys.argv[3])
    output_directory = sys.argv[4 ]
    downloader.download(path_and_rows, time_periods, output_directory)
  