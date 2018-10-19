import subprocess
import csv
import sys
from pprint import pprint

def get_processing_date_from_product_id(product_id):
  """
    Ex: LC08_L1TP_149039_20180703_20180717_01_T1
  """
  fields = product_id.split('_')
  return fields[4]

def parse_path_and_rows(filename):
  parsed_data = []
  with open(filename) as open_file:
    for line in open_file:

      line_sp = line.split(' ')
      line_obj = {}
      line_obj['id'] = line_sp[0]
      line_obj['scenes'] = []
      
      for i in xrange(1, (len(line_sp) - 1)/2 + 1):
        scene_obj = {}
        scene_obj['path'] = line_sp[2 * i - 1]
        scene_obj['row'] = line_sp[2 * i]
        line_obj['scenes'].append(scene_obj)
      
      parsed_data.append(line_obj)
  
  return parsed_data

def parse_time_periods(filename):
  parsed_data = []
  with open(filename) as csvfile:
    csv_reader = csv.reader(csvfile, delimiter = ',')
    
    header = csv_reader.next()

    region_name_index = header.index('REGION_NAME')
    start_date_index = header.index('START_DATE')
    end_date_index = header.index('END_DATE')

    for line in csv_reader:
      
      line_obj = {}
      line_obj['id'] = line[region_name_index]
      line_obj['start_date'] = line[start_date_index]
      line_obj['end_date'] = line[end_date_index]

      parsed_data.append(line_obj)
  return parsed_data      


class Downloader():
  def setup(self):
    subprocess.call('./downloader.sh')

  def search(self, path, row, start_date = None, end_date = None):
    products = []
    with open('scene_list') as csvfile:
      csv_reader = csv.reader(csvfile, delimiter = ',')
      
      header = csv_reader.next()
      
      path_index = header.index('path')
      row_index = header.index('row')
      product_id_index = header.index('productId')
      dowload_url_index = header.index('download_url')

      for product in csv_reader:
        if(int(product[path_index]) == path and int(product[row_index]) == row):
          is_valid = True
          product_id = product[product_id_index]
          processing_date = get_processing_date_from_product_id(product_id)
          if(start_date and processing_date < start_date):
            is_valid = False
          if(end_date and processing_date > end_date):
            is_valid = False
          if(is_valid):

            product_obj = {}
            product_obj['product_id'] = product_id
            product_obj['path'] = path
            product_obj['row'] = row
            product_obj['dowload_url'] = product[dowload_url_index]

            products.append(product_obj)
    return products

  def download(self, path_and_rows_file, time_periods, output_directory):

    pass


if __name__ == '__main__':
  if(len(sys.argv) != 4):
    print('Incorrect number of arguments')
    exit()
  print(sys.argv)
  path_and_rows = parse_path_and_rows(sys.argv[1])
  time_periods = parse_time_periods(sys.argv[2])
  output_directory = sys.argv[3]
  downloader = Downloader()
  pprint(path_and_rows)
  pprint(time_periods)
  downloader.download(path_and_rows, time_periods, output_directory)
  