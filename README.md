# SOCKER
This is a SOCKS Proxy Checker
Checks an IP:Port list of SOCKS4/5 and outputs working proxies to a file.

For Contact Go To End...

### HOW To RUN
To Run type 
```
python2 socker.py
```
For Help Type
```
python2 socker.py help
```
Command Line Usage:
```
python2 socker.py <socks_file_list> <file_to_write> <threads> <timeout>
```

### SOME TERMS:

Proxy list - An absolute path to the file containing a list of proxies in the of IP:Port

Output file - An absolute path to the file that the live SOCKS4/5 proxies will be written to.

Threads - The number of threads that will be used to check proxies. More threads = quicker 
scanning. If the thread count is too high, your internet connection may be interrupted and 
false timeouts/connection refused errors will be printed.

Timeout - The amount of time to give a potential proxy to repond before giving up and trying 
the next.


This script attempts to verify if a given IP:Port listing is a SOCKS4/5 proxy by completeing a 
SOCKS4/5 handshake with it. In order to maintain the highest level of compatibility I could, I 
did not use third part libraries and stuck with the default Python libraries. Also, I skipped 
adding some 'fancy' features, such as a GUI.



# SOCKSLIST

You can Also Use My SOCKS List to get New SOCKS Proxy ...

It Gets Updated Every 24 hours

SOCKS-List Link : https://github.com/TheSpeedX/SOCKS-List

<a href="https://github.com/TheSpeedX/SOCKS-List">Click Here To Go To SOCK List Page</a>

You Can Also Directly Type this to get SOCKS-List (Make Sure You Have curl installed)
```
curl -LO https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks.txt
```

# NOTES

 NOTE: It is Only For Educational Purposes. Neither I Say Nor I Promote To Do Anything Illegal.

 For Any Queries Join Me On WhatsApp!!!
          Group Link: http://bit.do/thespeedxgit
  <a href="http://bit.do/thespeedxgit">Join My Group</a>

           YouTube Channel: https://www.youtube.com/c/GyanaTech
  <a href="https://www.youtube.com/c/GyanaTech">Check My Channel</a>
  
  To Support Me By Either Helping In Project Or Donating Small Amount To Me For That Contact Me By
          
          Mail: ggspeedx29@gmail.com
          
 That's All !!!

# CONTACT

 For Any Queries Join Me On WhatsApp!!!
          Group Link: http://bit.do/thespeedxgit
  <a href="http://bit.do/thespeedxgit">Join My Group</a>

           Mail: ggspeedx29@gmail.com

           YouTube Channel: https://www.youtube.com/c/GyanaTech
  <a href="https://www.youtube.com/c/GyanaTech">Check My Channel</a>
