#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 12:11:53 2022

@author: zeynep
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 31 14:58:51 2022

@author: zeynep
"""

import pandas as pd
from urllib.parse import urlparse,urlencode
import ipaddress
import re
import re
from bs4 import BeautifulSoup
import urllib
import urllib.request
from datetime import datetime
import whois
import re
import requests
from bs4 import BeautifulSoup

dataBenign = pd.read_csv("benign.csv")
#print(data.shape)

dataBenign.columns = ['URLs']
dataBenign.head()

#print(phishurl.shape)

benignUrl = dataBenign.sample(n = 500, random_state = 12).copy()
benignUrl = benignUrl.reset_index(drop=True)
benignUrl.head()

def parseDomain(url):  
  domain = urlparse(url).netloc
  if re.match(r"^www.",domain):
	       domain = domain.replace("www.","")
  return domain


def hasIP(url):
  url = parseDomain(url)
  try:
    ipaddress.ip_address(url)
    label = 1
  except:
    label = 0
  return label


def longURL(url):
  if len(url) < 54:
    label = 0            
  else:
    label = 1            
  return label

shorteningServices = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"
                      

def tinyURL(url):
    match=re.search(shorteningServices,url)
    if match:
      label = 1
    else:
      label = 0
    return label


def hasAtSign(url):
  if "@" in url:
    label = 1    
  else:
    label = 0    
  return label


def redirection(url):
  pos = url.rfind('//')
  if pos > 5:
    if pos > 6:
      return 1
    else:
      return 0
  else:
    return 0        


def prefixSuffix(url):
    if '-' in parseDomain(url):
      return 1            
    else:
      return 0         


def domainAge(domain_name):
  creation_date = domain_name.creation_date
  expiration_date = domain_name.expiration_date
  if (isinstance(creation_date,str) or isinstance(expiration_date,str)):
    try:
      creation_date = datetime.strptime(creation_date,'%Y-%m-%d')
      expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
    except:
      return 1
  if ((expiration_date is None) or (creation_date is None)):
      return 1
  elif ((type(expiration_date) is list) or (type(creation_date) is list)):
      return 1
  else:
    ageofdomain = abs((expiration_date - creation_date).days)
    if ((ageofdomain/30) < 6):
      age = 1
    else:
      age = 0
  return age           


def webTraffic(url):
  try:
    #Filling the whitespaces in the URL if any
    url = urllib.parse.quote(url)
    rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find(
        "REACH")['RANK']
    rank = int(rank)
  except TypeError:
        return 1
  if rank <100000:
    return 1
  else:
    return 0 


def googleIndex(url):

  google = "https://www.google.com/search?q=site:" + url + "&hl=en"
  response = requests.get(google, cookies={"CONSENT": "YES+1"})
  soup = BeautifulSoup(response.content, "html.parser")
  not_indexed = re.compile("did not match any documents")

  if soup(text=not_indexed):
    return 1
  else:
    return 0


def multiSubDomain(url):
  domain = parseDomain(url)

  dotCount = domain.count('.')

  if dotCount >= 3:
    return 1
  else:
    return 0


def issuerVerify(url):
  try:
    #response = requests.get(url)
    return 0
  except:
    return 1


def domainEnd(domain_name):
  expiration_date = domain_name.expiration_date
  if isinstance(expiration_date,str):
    try:
      expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
    except:
      return 1
  if (expiration_date is None):
      return 1
  elif (type(expiration_date) is list):
      return 1
  else:
    today = datetime.now()
    end = abs((expiration_date - today).days)
    if ((end/30) < 6):
      end = 0
    else:
      end = 1
  return end


def httpInDomain(url):
  domain = parseDomain(url)
  if 'http' in domain or 'https' in domain:
    return 1
  else:
    return 0


def iframe(response):
  if response == "":
      return 1
  else:
      if re.findall(r"[<iframe>|<frameBorder>]", response.text):
          return 0
      else:
          return 1
      
        
def mouseOver(response): 
  if response == "" :
    return 1
  else:
    if re.findall("<script>.+onmouseover.+</script>", response.text):
      return 1
    else:
      return 0
  
    
    
def rightClick(response):
  if response == "":
    return 1
  else:
    if re.findall(r"event.button ?== ?2", response.text):
      return 0
    else:
      return 1
  
    
def forwarding(response):
  if response == "":
    return 1
  else:
    if len(response.history) <= 2:
      return 0
    else:
      return 1
  
    
def featureExtraction(url, label):

  features = []
   
  #URL based features = 11
  features.append(parseDomain(url))
  features.append(hasIP(url))
  features.append(longURL(url))
  features.append(tinyURL(url))
  features.append(hasAtSign(url))
  features.append(redirection(url))
  features.append(prefixSuffix(url))
  features.append(googleIndex(url))
  features.append(multiSubDomain(url))
  features.append(issuerVerify(url))
  features.append(httpInDomain(url))

  #Domain based features = 4
  dns = 0
  try:
    domain_name = whois.whois(urlparse(url).netloc)
  except:
    dns = 1

  features.append(dns) #DNS record
  features.append(webTraffic(url))
  features.append(1 if dns == 1 else domainAge(domain_name))
  features.append(1 if dns == 1 else domainEnd(domain_name))
  
  # HTML & Javascript based features = 4
  try:
    response = requests.get(url)
  except:
    response = ""
  features.append(iframe(response))
  features.append(mouseOver(response))
  features.append(rightClick(response))
  features.append(forwarding(response))

  #Label function = 1
  features.append(label)
  
  return features


benignFeatures = []
label = 0

for i in range(0, 500):
  url = dataBenign['URLs'][i]
  benignFeatures.append(featureExtraction(url,label))
  
featureNames = ['domain', 'hasIP', 'longURL', 'tinyURL', 'hasAtSign', 'redirection', 
                      'prefix/suffix', 'googleIndex', 'multiSubDomain', 'issuerVerified', 'httpInDomain', 'DNSRecord', 'webTraffic', 'domainAge',
                        'domainEnd', 'iFrame', 'mouseOver', 'rightClick', 'webForwards', 'class']
benign_dataset = pd.DataFrame(benignFeatures, columns= featureNames)
benign_dataset.head()

benign_dataset.to_csv('b500.csv', index= False)