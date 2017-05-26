# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Contributors    : Shawn McCrum                                                            #
# Date            : 08/22/16                                                                #
# Project Version : 0.2.1.5                                                                 #
# Python Version  : 3.5                                                                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Description: Use Pandas to open and manipulate saved company history                      #
#            : Create folders for each sector / industry                                    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from collections import Counter
from general import *
import pandas as pd

# From: Main.py -> def work():
class Parse_File:

  # Empty variables
  url_nasdaq    = ''
  root_folder   = ''
  sub_folder    = ''
  last_date_run = ''

  # Uses variables from work() to start each instance of Parse_File
  def __init__(self, url_nasdaq, root_folder, last_date_run):
    Parse_File.url_nasdaq    = url_nasdaq
    Parse_File.root_folder   = root_folder
    Parse_File.last_date_run = last_date_run
    self.nasdaq_folders()

  @staticmethod
  def nasdaq_folders():

    symbol_array    = []
    folder_array    = []
    # Open url_nasdaq
    open_nasdaq     = pd.read_csv(Parse_File.url_nasdaq)
    column_name     = pd.DataFrame.sort_values(open_nasdaq, by='Industry', ascending=True)
    # Columns in file
    sector_column   = column_name['Sector'][0] # The files are already categorized by sector
    industry_column = column_name['Industry']
    symbol_column   = column_name['Symbol']
    save_columns    = (sector_column + ', ' + industry_column + ', ' + symbol_column)
    industry_sorted = sorted(list(Counter([industry_column][0]))) # Sort each industry folder in alphabetical order
    # File locations
    sector_root     = Parse_File.root_folder + '/' + sector_column
    file_location   = sector_root + '/' + Parse_File.last_date_run
    # Make directory / Save file
    save_project(file_location, save_columns) # Add try statement to see if today's file has already been downloaded

    # Clean each symbol
    for row_s in symbol_column:
      clean_dot    = row_s.replace    ('.', '')
      clean_symbol = clean_dot.replace('^', '')
      symbol_array.append(clean_symbol)

    # Clean each industry
    for row_i in industry_sorted:
      clean_name       = row_i.replace      ('/', '--')
      clean_industry   = clean_name.replace (':', '--')
      industry_sector  = sector_root + '/' + clean_industry
      create_project_dir(industry_sector)
      folder_array.append(industry_sector)
    get_history(industry_column, sector_column, industry_sorted, symbol_array, folder_array)

def get_history(industry, sector, industry_sorted, symbol_array, folder_location):

  count_one     = 0
  count_two     = 0
  count_three   = 0
  array_two     = []
  industry_len  = len(industry)
  column_len    = len(industry_sorted)

  while count_one != column_len:
    while count_two != industry_len:
      if not industry_sorted[count_one] == industry[count_two]:
        pass
      else:
        www_yahoo = 'http://real-chart.finance.yahoo.com/table.csv?s='
        url_yahoo = (www_yahoo + symbol_array[count_two])
        try:
          open_yahoo   = pd.read_csv(url_yahoo)
          save_history = pd.DataFrame(open_yahoo, columns=['Date','Low','High','Open','Close','Volume'])
          company_file = folder_location[count_one] + '/' + symbol_array[count_two]
          save_project(company_file, save_history)
        except:
          array_two.append(folder_location[count_one] + '/' + symbol_array[count_two])
          pass
        count_three += 1
      count_two += 1

    completed_histories = count_three - len(array_two)
    print('\nCompany Sector     :', sector, '\nCompleted Industry :', industry_sorted[count_one], '(', count_one + 1, 'of', column_len, ')\nCompleted History  : (', completed_histories, 'of', count_three, ')')
    count_one += 1

    for skipped in array_two:
      print(skipped)
    count_three *= 0
    count_two   *= 0
    array_two.clear()