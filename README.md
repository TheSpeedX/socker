SOCKS-Proxy-Checker
===================

Checks an IP:Port list of SOCKS4/5 and outputs working proxies to a file.


Inputs:

Proxy list - An absolute path to the file containing a list of proxies in the of IP:Port

Output file - An absolute path to the file that the live SOCKS4/5 proxies will be written to.

Threads - The number of threads that will be used to check proxies. More threads = quicker scanning. If the thread count is too high, your internet connection may be interrupted and false timeouts/connection refused errors will be printed.

Timeout - The amount of time to give a potential proxy to repond before giving up and trying the next.


This script attempts to verify if a given IP:Port listing is a SOCKS4/5 proxy by completeing a SOCKS4/5 handshake with it. In order to maintain the highest level of compatibility I could, I did not use third part libraries and stuck with the default Python libraries. Also, I skipped adding some 'fancy' features, such as a GUI.