__author__ = 'wim'
import simplejson
import urllib
import urllib2
url = "https://www.virustotal.com/vtapi/v2/file/rescan"
parameters = {"resource": "99017f6eebbac24f351415dd410d522d, 7896b9b34bdbedbe7bdc6d446ecb09d5",
              "apikey": "1fe0ef5feca2f84eb450bc3617f839e317b2a686af4d651a9bada77a522201b0"}
data = urllib.urlencode(parameters)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
json = response.read()
print json
[
 {"response_code": 1,
  "resource": "52d3df0ed60c46f336c131bf2ca454f73bafdc4b04dfa2aea80746f5ba9e6d1c",
  "scan_id": "52d3df0ed60c46f336c131bf2ca454f73bafdc4b04dfa2aea80746f5ba9e6d1c-1333539103",
  "verbose_msg": "Scan request successfully queued, come back later for the report",
  "permalink": "https:\/\/www.virustotal.com\/file\/52d3df0ed60c46f336c131bf2ca454f73bafdc4b04dfa2aea80746f5ba9e6d1c\/analysis\/1333539103\/",
  "sha256": "52d3df0ed60c46f336c131bf2ca454f73bafdc4b04dfa2aea80746f5ba9e6d1c"
 },
 {"response_code": 1,
  "verbose_msg": "Scan request successfully queued, come back later for the report",
  "resource": "dfcbeed0a07f24cded6deda71b07de9c30126c4155c2c20b90ac7c74bbf577f6",
  "scan_id": "dfcbeed0a07f24cded6deda71b07de9c30126c4155c2c20b90ac7c74bbf577f6-1333539103",
  "permalink": "https:\/\/www.virustotal.com\/file\/dfcbeed0a07f24cded6deda71b07de9c30126c4155c2c20b90ac7c74bbf577f6\/analysis\/1333539103\/",
  "sha256": "dfcbeed0a07f24cded6deda71b07de9c30126c4155c2c20b90ac7c74bbf577f6"
 }
]