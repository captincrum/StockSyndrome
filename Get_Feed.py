# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Created By      : Shawn McCrum                                                                  #
# Last Update     : 8.23.2016                                                                     #
# Project Version : 0.1.0.5                                                                       #
# Python Version  : 3.5                                                                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Description: Creates folder for each news source.                                               #
#              Scrape each RSS feed for news articles                                             #
#              Analyze each account for any duplicates.                                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from parse_feed_info import *
from parse_article_xml import *
import feedparser as fp
import re

error_array  = []
already_read = []

class Parse_Feed:

  article_url  = ''
  root_folder  = ''
  current_date = ''

  # Uses variables from work() to start each instance of
  def __init__(self, article_url, root_folder, current_date):
    Parse_Feed.article_url  = article_url
    Parse_Feed.root_folder  = root_folder
    Parse_Feed.current_date = current_date
    self.read_feed(Parse_Feed.article_url)

  @staticmethod
  def read_feed(rss_feed):
    parse_feed = fp.parse(rss_feed)
    for post in parse_feed.entries:
      article_date    = post.updated
      recent_article  = re.search(Parse_Feed.current_date, article_date)
      # Only continue if the article was published this year
      if bool(recent_article):
        article_url     = post.link
        if article_url in already_read:
#          print('Repeat Link:', article_url, '\nFrom Feed  :' + rss_feed)
          pass
        else:
          article_title   = post.title   # Send to analyzer # Eventually: save / compare titles against the pre-existing list
          article_summary = post.summary # Check if summary is repeated word-for-word
#          print('\nArticle Url      :', article_url, '\nArticle Title    :', article_title, '\nArticle Date     :', recent_article.string, '\nArticle Summary  :', article_summary)
  #            full_article(article_title)
  #            full_article(article_summary)
          next_url(article_title, article_summary, article_url)
          already_read.append(article_url)
      else:
        error_array.append('Out of date link:' + rss_feed)
      print(len(error_array), 'articles older then today.')
