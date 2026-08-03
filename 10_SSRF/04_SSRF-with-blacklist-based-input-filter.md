# SSRF with blacklist-based input filter

**Lab Url**: [https://portswigger.net/web-security/ssrf/lab-ssrf-with-blacklist-filter](https://portswigger.net/web-security/ssrf/lab-ssrf-with-blacklist-filter)

## Objective

This lab has a stock check feature which fetches data from an internal system.

To solve the lab, change the stock check URL to access the admin interface at `http://localhost/admin` and delete the user `carlos`.

The developer has deployed two weak anti-SSRF defenses that you will need to bypass.

## Solution

The stock check feature fetches a URL supplied in the `stockApi` parameter. Two blacklist filters need to be bypassed: one blocks the `localhost` hostname, the other blocks the `admin` path.

### Step 1: Bypass the localhost block

`localhost` is blacklisted, but alternative representations of the loopback address are not. Use `127.0.0.1` instead:

```text
stockApi=http://127.0.0.1/admin
```

### Step 2: Bypass the admin path block

The path `admin` is also blacklisted. URL-encode a character to bypass the string filter — the server decodes it before use:

```text
stockApi=http://127.0.0.1/%61dmin
```

`%61` decodes to `a`, so the path becomes `/admin` on the server side.

### Step 3: Delete carlos

Apply the same encoding to the delete URL:

```text
stockApi=http://127.0.0.1/%61dmin/delete?username=carlos
```

The server deletes the user and solves the lab.
