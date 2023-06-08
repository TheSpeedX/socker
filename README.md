# Proxy Tester

Proxy Tester is a Python script that tests the validity and performance of a list of proxies by sending HTTP requests to specified domains.

## Features

- Validates proxies by sending HTTP requests to specified domains.
- Supports both HTTP and HTTPS proxies.
- Multi-threaded for faster testing.
- Configurable number of threads.
- Customizable timeout for request.
- Generates a report with the results.

## Requirements

- Python 3.6+
- Packages listed in the `requirements.txt` file.

## Usage

1. Clone the repository:

   ```shell
   git clone https://github.com/your-username/proxy-tester.git
   ```

2. Install the required packages:

   ```shell
   pip install -r requirements.txt
   ```

3. Prepare your proxy list in the `input.txt` file, with each proxy URL on a new line.

4. Run the script:

   ```shell
   python proxy_tester_menu.py input.txt output.txt
   ```

   - `input.txt` is the path to your input file containing the list of proxies.
   - `output.txt` is the path to the output file where the test results will be saved.

## Configuration

You can modify the following settings in the `proxy_tester_menu.py` script:

- `THREADS`: The number of threads to use for testing proxies.
- `TIMEOUT`: The timeout for each request.



# SOCKER

Checks for valid SOCKS4 & SOCKS5 proxies.
This code is Python3 port of [SOCKS-Proxy-Checker](https://github.com/BeastsMC/SOCKS-Proxy-Checker/) which was written in Python2
This code runs on python3.

## HOW To RUN

For Help Type

```python3 socker.py -h```

Command Line Usage:

```python3 socker.py -i <proxy_file_list> -o <file_to_write> -th <threads> -t <timeout>```

You can use the auto mode for fetching proxies from default APIs.

```python3 socker.py -auto -o <file_to_write> -th <threads> -t <timeout>```

You can use the URL mode to add new urls to fetch proxies.

```python3 socker.py -u proxlylist1.site -u proxlylist2.site -o <file_to_write> -th <threads> -t <timeout>```

All the parameters are optional.  
File, Auto, URL modes can be used simulaenously to gather more proxies.  
The default thread count is 30 and timeout is 5 seconds.  

### SOME TERMS

Proxy list - An absolute path to the file containing a list of proxies in the of IP:Port  

Output file - An absolute path to the file that the live SOCKS4/5 proxies will be written to.  

Threads - The number of threads that will be used to check proxies. More threads = quicker 
scanning. If the thread count is too high, your internet connection may be interrupted and 
false timeouts/connection refused errors will be printed.  

Timeout - The amount of time to give a potential proxy to repond before giving up and trying 
the next.  

This script attempts to verify if a given IP:Port listing is a SOCKS4/5 proxy by completeing a 
SOCKS4/5 handshake with it. In order to maintain the highest level of compatibility I could, I 
did not use third party libraries and stuck with the default Python libraries.

## SOCKSLIST

You can Also Use My PROXY List to get New SOCKS Proxy. It Gets Updated Every 24 hours.

PROXY-List Link : [https://github.com/TheSpeedX/PROXY-List](https://github.com/TheSpeedX/PROXY-List)

## Test http & https proxy using proxy_tester_menu.py

To use this script, follow these steps:

1. Ensure you have the `requests` library installed. You can install it using `pip install requests` if needed.
2. Create two files named `http.txt` and `https.txt` in the same directory as the script. Each file should contain a list of IP addresses to test, with one IP per line.
3. Run the script using the command: `python proxy_tester_menu.py`.
4. The menu will be displayed, prompting you to select a file to test. Enter your choice by typing `1` or `2`.
5. If the chosen file is not found or empty, an error message will be displayed. Make sure the file contains valid IP addresses.
6. The script will start testing the IP addresses using the selected file. An animation will be displayed to indicate the progress of testing.
7. Once the testing is completed, the results will be saved in a file named `results.txt` in the same directory.
8. The message "Testing complete. Results are saved to results.txt" will be displayed.
Make sure to have the required `http.txt` and `https.txt` files in the same directory as the script and ensure they contain valid IP addresses.

Sample domains you can set:

```
www.google.com
www.example.com
www.yahoo.com
www.microsoft.com
www.facebook.com
www.instagram.com
www.twitter.com
www.amazon.com
www.netflix.com
www.reddit.com
www.wikipedia.org
www.apple.com
www.linkedin.com
www.github.com
www.stackoverflow.com
www.spotify.com
www.dropbox.com
www.pinterest.com
www.tumblr.com
www.airbnb.com
```

## CONTACT

 For Any Queries:  
        Ping Me : [Telegram](http://t.me/the_space_bar)
