#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import threading
import time
import sys

# from random import *
import struct
import argparse
import re
from urllib.request import Request, urlopen  # Python 3
import queue as Queue


__author__ = "TheSpeedX"
__version__ = "2.0"

banner = """
███████╗ ██████╗  ██████╗██╗  ██╗███████╗██████╗
██╔════╝██╔═══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
███████╗██║   ██║██║     █████╔╝ █████╗  ██████╔╝
╚════██║██║   ██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
███████║╚██████╔╝╚██████╗██║  ██╗███████╗██║  ██║
╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
    Check Valid Working SOCKS Proxy
"""
socksProxies = Queue.Queue()
checkQueue = Queue.Queue()


class ThreadChecker(threading.Thread):
    def __init__(self, queue, timeout):
        self.timeout = timeout
        self.q = queue
        threading.Thread.__init__(self)

    def isSocks4(self, host, port, soc):

        ipaddr = socket.inet_aton(host)
        port_pack = struct.pack(">H", port)
        packet4 = b"\x04\x01" + port_pack + ipaddr + b"\x00"
        soc.sendall(packet4)
        data = soc.recv(8)
        if len(data) < 2:
            # Null response
            return False
        if data[0] != int("0x00", 16):
            # Bad data
            return False
        if data[1] != int("0x5A", 16):
            # Server returned an error
            return False
        return True

    def isSocks5(self, host, port, soc):
        soc.sendall(b"\x05\x01\x00")
        data = soc.recv(2)
        if len(data) < 2:
            # Null response
            return False
        if data[0] != int("0x05", 16):
            # Not socks5
            return False
        if data[1] != int("0x00", 16):
            # Requires authentication
            return False
        return True

    def getSocksVersion(self, proxy):
        host, port = proxy.split(":")
        try:
            port = int(port)
            if port < 0 or port > 65536:
                print(f"Invalid: {proxy}")
                return 0
        except Exception:
            print(f"Invalid: {proxy}")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.timeout)
        try:
            s.connect((host, port))
            if self.isSocks4(host, port, s):
                s.close()
                return 4
            elif self.isSocks5(host, port, s):
                s.close()
                return 5
            else:
                print(f"Not a SOCKS: {proxy}")
                s.close()
                return 0
        except socket.timeout:
            print(f"Timeout: {proxy}")
            s.close()
            return 0
        except socket.error:
            print(f"Connection refused: {proxy}")
            s.close()
            return 0

    def run(self):
        while True:
            proxy = self.q.get()
            version = self.getSocksVersion(proxy)
            if version in [5, 4]:
                print(f"Working: {proxy}")
                socksProxies.put(proxy)
            self.q.task_done()


class ThreadWriter(threading.Thread):
    def __init__(self, queue, outputPath):
        self.q = queue
        self.outputPath = outputPath
        threading.Thread.__init__(self)

    def run(self):
        while True:
            toWrite = self.q.qsize()
            with open(self.outputPath, "a+") as outputFile:
                for _ in range(toWrite):
                    proxy = self.q.get()
                    outputFile.write(proxy + "\n")
                    self.q.task_done()
            time.sleep(10)


def info():
    print(banner)
    print(f"Author: {__author__} \t\t Version: {__version__}")


def Exit():
    print(banner)
    print("\tThanks For using socker !!!")
    sys.exit()


def get_timestamp():
    return time.strftime("%Y%m%d_%H%M%S")


def get_proxies(sources, is_url=False):
    pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}"
    data = ""
    for source in sources:
        try:
            if is_url:
                req = Request(
                    source,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
                    },
                )
                response = urlopen(req)
                data += response.read().decode("utf-8") + "\n"
            else:
                with open(source) as file:
                    data += file.read() + "\n"
            print(f"Processed: {source}")
        except Exception:
            print(f"Skipping, Error Occured: {source}")
    return re.findall(pattern, data)


def start_socker(proxies, outputPath, threads, timeout):
    print(f"Loaded {len(proxies)} proxies !!!")
    for proxy in proxies:
        checkQueue.put(proxy)
    for _ in range(threads):
        thread = ThreadChecker(checkQueue, timeout)
        thread.setDaemon(True)
        thread.start()
        time.sleep(0.25)
    wT = ThreadWriter(socksProxies, outputPath)
    wT.setDaemon(True)
    wT.start()
    checkQueue.join()
    socksProxies.join()
    Exit()


description = """socker - Check For Valid SOCKS Proxy

socker can utilize multiple sources like file, inbuilt apis, custom urls.
File Mode:
python3 socker.py -i proxys_to_be_checked.txt
URL Mode:
python3 socker.py -u proxlylist1.site -u proxlylist2.site
Auto Mode:
python3 socker.py -auto

These modes can also be used simultaneously to gather more proxies.
python3 socker.py -i proxys_to_be_checked.txt -auto

socker is not intented for malicious uses.
"""

parser = argparse.ArgumentParser(
    description=description,
    epilog="Coded by SpeedX !!!",
    formatter_class=argparse.RawTextHelpFormatter,
)
parser.add_argument(
    "-o",
    "--output",
    default=f"live_proxies_{get_timestamp()}.txt",
    help="Write Proxies to this file",
)
parser.add_argument(
    "-th", "--thread", type=int, default=30, help="Number of concurrent threads to run"
)
parser.add_argument(
    "-t",
    "--timeout",
    type=float,
    default=5.0,
    help="Maximum time to wait for response(seconds)",
)
parser.add_argument(
    "-i", "--input", action="append", help="Input File containing proxy"
)
parser.add_argument(
    "-auto", "--auto", action="store_true", help="Fetches proxy from Proxyscrape"
)
parser.add_argument("-u", "--url", action="append", help="Fetch proxy from custom URL")
parser.add_argument(
    "-v", "--version", action="store_true", help="show current TBomb version"
)

if __name__ == "__main__":
    args = parser.parse_args()
    info()
    if args.version:
        print("Author: ", __author__)
        print("Version: ", __version__)
    else:
        proxies = []
        proxy_api = [
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
        ]
        if args.input:
            proxies.extend(get_proxies(args.input))
        if args.auto:
            proxies.extend(get_proxies(proxy_api, is_url=True))
        if args.url:
            proxies.extend(get_proxies(args.url, is_url=True))
        if proxies:
            start_socker(proxies, args.output, args.thread, args.timeout)
        else:
            print("No proxies found !!!")
            Exit()
