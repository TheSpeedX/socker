import contextlib
import time
import requests
import os
import concurrent.futures

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


def test_ip_addresses(ip_file, output_file, domain=DEFAULT_DOMAIN, num_threads=10):
    with open(ip_file, "r") as file:
        ip_addresses = file.read().splitlines()

    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_ip = {executor.submit(test_proxy, ip, domain): ip for ip in ip_addresses}
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
    try:
        num_threads = int(num_threads)
        if num_threads <= 0:
            print("Invalid number of threads. Using the default value.")
            num_threads = 10
    except ValueError:
        print("Invalid input. Using the default number of threads.")
        num_threads = 10
    return num_threads


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

    num_threads = get_num_threads()
    print(f"Using {num_threads} threads for testing.")

    test_ip_addresses(input_file, output_file, domain=domain, num_threads=num_threads)

    print("Testing complete. Results saved to", output_file)


if __name__ == "__main__":
    main()
