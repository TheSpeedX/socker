import contextlib
import time
import requests
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

DEFAULT_DOMAIN = "www.google.com"


def test_proxy(ip, domain=DEFAULT_DOMAIN):
    proxies = {
        "http": f"http://{ip}",
        "https": f"http://{ip}",
    }
    with contextlib.suppress(requests.RequestException):
        response = requests.get(f"http://{domain}", proxies=proxies, timeout=5)
        if response.status_code >= 200 and response.status_code < 300:
            return True
    return False


def test_ip_addresses_concurrent(ip_file, output_file, domain=DEFAULT_DOMAIN):
    with open(ip_file, "r") as file:
        ip_addresses = file.read().splitlines()

    results = []

    # Using ThreadPoolExecutor to test multiple proxies concurrently for better performance
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Submit each proxy test to the executor and store the future object along with the IP
        future_to_ip = {executor.submit(test_proxy, ip, domain): ip for ip in ip_addresses}
        for future in as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                # Get the result of the future and determine if the proxy is active or inactive
                is_working = future.result()
                status = "Active" if is_working else "Inactive"
                results.append((ip, status))
            except Exception as e:
                # Handle any exceptions that occur during the proxy test
                print(f"Error testing proxy {ip}: {e}")

    # Write the results to the output file
    with open(output_file, "w") as file:
        for ip, status in results:
            file.write(f"{ip}\t{status}\n")

    print("Testing complete.")


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
    if not os.path.isfile(http_file):
        print(f"Error: '{http_file}' file is missing or not found.")
        return False
    if not os.path.isfile(https_file):
        print(f"Error: '{https_file}' file is missing or not found.")
        return False
    return True


def get_domain_choice():
    domain_choice = input(
        "Enter the domain on which you want to test the proxies (default: www.google.com): "
    )
    return domain_choice.strip() or DEFAULT_DOMAIN


def main():
    if not check_input_files():
        return

    display_menu()
    choice = get_user_choice()
    input_file = get_input_filename(choice)
    output_file = "results.txt"

    print("Testing in progress...")
    time.sleep(1)  # Simulate a delay before starting the testing

    domain = get_domain_choice()
    print(f"Using domain: {domain}")

    test_ip_addresses_concurrent(input_file, output_file, domain=domain)

    print("Testing complete. Results saved to", output_file)


if __name__ == "__main__":
    main()
