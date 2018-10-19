import subprocess
import csv

def get_processing_date_from_product_id(product_id):
  """
    Ex: LC08_L1TP_149039_20180703_20180717_01_T1
  """
  fields = product_id.split('_')
  return fields[4]

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


if __name__ == '__main__':
  d = Downloader()
  print(d.search(216, 66, "20170801", "20170930"))