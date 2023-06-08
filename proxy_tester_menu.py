import contextlib
import time
import os
import argparse
import concurrent.futures
import subprocess

DEFAULT_DOMAIN = "www.google.com"


def test_proxy(ip, domain=DEFAULT_DOMAIN):
    url = f"http://{domain}"
    proxy_url = f"http://{ip}"
    proxies = {'http': proxy_url, 'https': proxy_url}

    try:
        # Use subprocess to make requests using cURL
        command = f"curl --connect-timeout 5 --max-time 5 --proxy {proxy_url} {url}"
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
        )

        # Check if the request was successful
        return result.returncode == 0
    except subprocess.SubprocessError:
        return False


def test_ip_addresses(ip_file, output_file, domain=DEFAULT_DOMAIN, num_threads=10):
    with open(ip_file, "r") as file:
        ip_addresses = file.read().splitlines()

    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for ip in ip_addresses:
            future = executor.submit(test_proxy, ip, domain)
            futures.append(future)

        for i, future in enumerate(concurrent.futures.as_completed(futures), start=1):
            ip = ip_addresses[i - 1]
            is_working = future.result()
            status = "Active" if is_working else "Inactive"
            results.append((ip, status))

            progress = i / len(ip_addresses) * 100
            print(
                f'\rTesting - Progress: {progress:.1f}% | {"." * (i % 4)}    ',
                end="",
                flush=True,
            )
            time.sleep(0.1)  # Add a slight delay to simulate animation

    with open(output_file, "w") as file:
        for ip, status in results:
            file.write(f"{ip}\t{status}\n")

    print("\rTesting complete.                  ")


def display_menu():
    print("Select a file to test:")
    print("1. http.txt")
    print("2. https.txt")


def get_user_choice():
    while True:
        choice = input("Enter your choice (1 or 2): ")
        if choice in ["1", "2"]:
            return choice
        print("Invalid choice. Please try again.")


def get_input_filename(choice):
    if choice == "1":
        return "http.txt"
    elif choice == "2":
        return "https.txt"


def check_input_files():
    http_file = "http.txt"
    https_file = "https.txt"
    if not os.path.exists(http_file) or not os.path.isfile(http_file):
        print(f"Error: '{http_file}' file is missing or not found.")
        return False
    if not os.path.exists(https_file) or not os.path.isfile(https_file):
        print(f"Error: '{https_file}' file is missing or not found.")
        return False
    return True


def get_domain_choice():
    domain_choice = input(
        "Enter the domain on which you want to test the proxies (default: www.google.com): "
    )
    return domain_choice.strip() or DEFAULT_DOMAIN


def get_num_threads():
    num_threads = input("Enter the number of threads to use for testing (default: 10): ")
    return int(num_threads.strip() or "10")


def main():
    if not check_input_files():
        return

    display_menu()
    choice = get_user_choice()
    input_file = get_input_filename(choice)
    output_file = "output.txt"
    domain = get_domain_choice()
    num_threads = get_num_threads()

    test_ip_addresses(input_file, output_file, domain, num_threads)


if __name__ == "__main__":
    main()
