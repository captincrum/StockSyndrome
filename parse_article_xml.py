# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Created By      : Shawn McCrum                                                                  #
# Last Update     : 8.23.2016                                                                     #
# Project Version : 0.1.0.5                                                                       #
# Python Version  : 3.5                                                                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Description: Parse information of each RSS news feed                                            #
#            : Use the information to determine the possible impact of each article.              #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from lxml.html import parse
from general import *

def next_url(article_title, article_summary, article_url):

# # # # # # # # # # For NPR (Working) # # # # # # # # # #
  if 'http://www.npr.org' in article_url:
    print('NPR:', article_url)
    root        = parse(article_url)
    pic_caption = root.xpath('//div[@class="caption"]/p/text()')
    tag_words   = root.xpath('//div[@class="tags"]/ul/li/a/text()') # Send to analyzer
    article_des = root.xpath('//meta[@name="description"]/@content')
    story_body  = root.xpath('//div[@id="storytext"]/p/text()')
    author_one  = root.xpath('//*[@class="byline__name byline__name--block"]/text()')
    author      = root.xpath('//*[@class="byline__name byline__name--block"]/a/text()')
    story_body  = root.xpath('//div[@id="storytext"]/p/text()')
#    clean_line(article_des)
#    clean_line(author)
#    clean_line(story_body)
#    clean_line(pic_caption)
    print('Article Tag Words:', tag_words)

# # # # # # # # # # For Reuters (Working) # # # # # # # # # #
  if 'http://feeds.reuters.com' in article_url:
    print('Reuters:', article_url)
    root           = parse(article_url)
    news_category  = root.xpath('//span[@class="article-section"]/a/text()')
#    news_category  = str(root.xpath('//meta[@name="DCSext.DartZone"]/@content')).replace("/", "', '") # Sub categories of each article # Set up to help generalizing what dictionary to use for analyzing each article
    article_des    = root.xpath('//meta[@property="og:description"]/@content') # Article description  # First paragraph
    word_bank      = root.xpath('//meta[@name="keywords"]/@content')           # Lists keywords related to each article # These words can be used to generalise the main idea of each article
    article_author = root.xpath('//meta[@name="Author"]/@content')             # Lists each main author to each article
    body_content   = root.xpath('//*[@id="article-text"]/p/text()')            # Full article content excluding the description paragraph: article_des
    full_article   = (article_des + body_content)
    print('Article Author   :', article_author, '\nSub Categories   :', news_category, '\nKeywords         :', word_bank, '\nFull Article     :', full_article)

# # # # # # # # # # BBC (Working) # # # # # # # # # #
  if 'http://www.bbc' in article_url:
    root           = parse(article_url)
    news_category  = root.xpath('//*[@class="mini-info-list__section"]/text()')            # News category which can be used to define which dictionary to use while analyzing
    article_des    = root.xpath('//meta[@property="og:description"]/@content')             # Description for each article
    author_origin  = root.xpath('//div[@class="byline"]/span/text()')                      # Returns both the author and the area of coverage (U.S, U.K, etc)
    image_caption  = root.xpath('//span[@class="media-caption__text"]/text()')             # Image caption text
    img_alt_tag    = root.xpath('//span[@class="image-and-copyright-container"]/img/@alt') # Alt tag for images without captions
    body_content   = root.xpath('//div[@class="story-body__inner"]/p/text()')              # Full article story
    referenced_art = root.xpath('//li[@class="story-body__list-item"]/a/@href')            # Related article link # After everything is parsed determine if the related links should be parsed too
    related_title  = root.xpath('//li[@class="story-body__list-item"]/a/text()')           # Title for related articles
    tag_words      = root.xpath('//li[@class="tags-list__tags"]/a/text()')                 # Words tagged by author to categorize article

    # Only print if true
    if bool(body_content):
      print('BBC:', article_url)#], '\nArticle Description:', article_des)
#      clean_line(image_caption)
#      clean_line(img_alt_tag)
#      clean_line(body_content)
      print('Article Category   :', news_category, '\nArticle Tag Words  :', tag_words, '\nArticle Author     :', author_origin, '\nArticle List       :', related_title, '\nRelated Links      :', referenced_art)
    # Action to take when body_content is not found
    else:
      pass
      print(article_url)