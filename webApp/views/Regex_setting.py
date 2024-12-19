import re
import html
# as per recommendation from @freylis, compile once only
CLEANR = re.compile('<.*?>') 
def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  cleantext = html.unescape(cleantext) 
  if cleantext.endswith("\r\n"): 
    cleantext = cleantext[:-2] 
  
  if cleantext.startswith("\r\n"): 
    cleantext = cleantext[2:] 
  return cleantext