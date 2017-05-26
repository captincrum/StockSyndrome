# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Contributors    : Shawn McCrum                                                            #
# Date            : 08/22/16                                                                #
# Project Version : 0.2.1.5                                                                 #
# Python Version  : 3.5                                                                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Description: Gathers history for all companies that trade on the nasdaq market.           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from parse_url import *
from queue import Queue
from Get_Feed import *
from parse_url import *
import threading
import datetime
import time

# Required initialization
start_time     = time.time() # Mark start time
print_lock     = threading.Lock()
queue          = Queue()
NUM_OF_WORKERS = 64          # Number of threads

# Date / Time
YYYY_MM_DD   = datetime.date.today()                                  # YYYY-MM-DD
TODAY        = datetime.datetime.strftime(YYYY_MM_DD, '%a, %d %b %Y') # Day, DD Month YYYY
# Project Folders to create
HISTORY_ROOT = 'Nasdaq Company Histories'
RSS_ROOT     = 'RSS News Feeds'
# Website Url
WWW_NASDAQ   = 'http://www.nasdaq.com'
WWW_NPR      = 'http://www.npr.org'
WWW_RUT      = 'http://feeds.reuters.com'
WWW_BBC      = 'http://feeds.bbci.co.uk'
# Query String
HIS_SECTOR   = ['Basic+Industries', 'Finance', 'Capital+Goods', 'Health+Care', 'Consumer+Durables', 'Miscellaneous', 'Consumer+Non-Durables', 'Public+Utilities', 'Consumer+Services', 'Technology', 'Energy', 'Transportation']
NPR_FEED     = ['1006', '1019', '1007', '1026', '1004', '1013', '1025', '1018', '1027', '1070', '1024']
RUT_FEED     = ['business', 'financials', 'technology', 'technologysector', 'science', 'company', 'usmediadiversified', 'usenergy', 'industrials', 'basicmaterials', 'utilities', 'noncyclicalconsumergoods', 'environment', 'health', 'ushealthcare']
BBC_FEED     = ['business', 'technology', 'health', 'education', 'world/us_and_canada', 'world/europe', 'england', 'uk', 'world/asia']
#OTHER_FEED     = ['http://www.investopedia.com/news/', 'https://www.sec.gov/news/pressreleases.rss', 'https://www.sec.gov/rss/investor/alerts']

# Number of workers permitted on project
def create_workers():
  for _ in range(NUM_OF_WORKERS):
    t        = threading.Thread(target=work)
    t.daemon = True
    t.start()

# Instructions for each job
def work():
  while True:
    worker = queue.get()

    # The first job is to focus on the history of all NASDAQ companies
    while WWW_NASDAQ in worker:
      print('Starting', threading.current_thread().name, 'for sector url:', worker)
      Parse_File(worker, HISTORY_ROOT, str(YYYY_MM_DD))
    else:
    # The second job focuses on scraping each RSS feed for news articles to parse
      if WWW_NPR or WWW_RUT or WWW_BBC in worker:
        print('Starting', threading.current_thread().name, 'for RRS Feed:', worker)
        Parse_Feed(worker, RSS_ROOT, TODAY)
    # After each job is complete
    with print_lock: # Lock current job from re-adding to the queue
      print('Finished', threading.current_thread().name, worker, '\nTime Taken:', time.time() - start_time)
      pass
#    worker.remove() # Removing the worker will re-added to the queue
  queue.task_done()
  print(time.time() - start_time) # Marks the time taken to complete each job

# First Priority # Create project folders
def start_project():
  create_project_dir(HISTORY_ROOT)
  create_project_dir(RSS_ROOT + '/Npr')
  create_project_dir(RSS_ROOT + '/Reuter')
  create_project_dir(RSS_ROOT + '/Bbc')
  create_workers()
  create_jobs(HIS_SECTOR, NPR_FEED, RUT_FEED, BBC_FEED)

# Create queue for each worker to complete
def create_jobs(HIS_SECTOR, NPR_FEED, RUT_FEED, BBC_FEED):

  # Nasdaq History
  for sector in HIS_SECTOR:
    folder_name = sector.replace('+', ' ')
    URL_NASDAQ  = WWW_NASDAQ + '/screening/companies-by-industry.aspx?industry=' + sector + '&render=download'
    create_project_dir(HISTORY_ROOT + '/' + folder_name)
    queue.put(URL_NASDAQ)

  # RSS Feeds: Npr
  for npr_category in NPR_FEED:
    RSS_NPR = WWW_NPR + '/rss/rss.php?id=' + npr_category
    queue.put(RSS_NPR)
  # RSS Feeds: Reuters
  for rut_category in RUT_FEED:
    RSS_RUT = WWW_RUT + '/reuters/' + rut_category + 'news?format=xml'
    queue.put(RSS_RUT)
  # RSS Feeds: Bbc
  for bbc_category in BBC_FEED:
    RSS_BBC = WWW_BBC + '/news/' + bbc_category + '/rss.xml'
    queue.put(RSS_BBC)

  queue.join()
start_project()