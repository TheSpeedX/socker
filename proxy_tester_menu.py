import contextlib
import time
import os
import argparse
import concurrent.futures
import urllib.request
from urllib.error import URLError, HTTPError
import ftreq

DEFAULT_DOMAIN = "www.google.com"


def test_proxy(ip, domain=DEFAULT_DOMAIN, use_ftreq=False):
    url = f"http://{domain}"
    proxy_url = f"http://{ip}"
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({'http': proxy_url, 'https': proxy_url}))

    try:
        if use_ftreq:
            ftreq.get(url, opener=opener)
        else:
            urllib.request.urlopen(url, timeout=5, opener=opener)
        return True
    except (URLError, HTTPError):
        return False


def test_ip_addresses(ip_file, output_file, domain=DEFAULT_DOMAIN, num_threads=10, use_ftreq=False):
    with open(ip_file, "r") as file:
        ip_addresses = file.read().splitlines()

    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_ip = {executor.submit(test_proxy, ip, domain, use_ftreq): ip for ip in ip_addresses}
        for future in concurrent.futures.as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                is_working = future.result()
                status = "Active" if is_working else "Inactive"
                results.append((ip, status))
            except Exception as e:
                print(f"An error occurred while testing {ip}: {e}")

    with open(output_file, "w") as file:
        for ip, status in results:
            file.write(f"{ip}\t{status}\n")

    print("\rTesting complete.                  ")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Proxy Tester")
    parser.add_argument("input_file", type=str, help="Path to the input file containing IP addresses")
    parser.add_argument("output_file", type=str, help="Path to the output file to save the results")
    parser.add_argument("--domain", type=str, default=DEFAULT_DOMAIN,
                        help="Domain to test the proxies on (default: www.google.com)")
    parser.add_argument("--threads", type=int, default=10,
                        help="Number of threads to use for testing (default: 10)")
    parser.add_argument("--ftreq", action="store_true",
                        help="Use faster-than-requests library for making requests (optional)")

    return parser.parse_args()


def check_input_file(input_file):
    if not os.path.exists(input_file) or not os.path.isfile(input_file):
        print(f"Error: '{input_file}' file is missing or not found.")
        return False
    return True


def main():
    args = parse_arguments()

    if not check_input_file(args.input_file):
        return

    print("Testing in progress...")
    time.sleep(1)  # Simulate a delay before starting the testing

    test_ip_addresses(args.input_file, args.output_file, domain=args.domain,
                      num_threads=args.threads, use_ftreq=args.ftreq)

    print("Testing complete. Results saved to", args.output_file)


if __name__ == "__main__":
    main()
