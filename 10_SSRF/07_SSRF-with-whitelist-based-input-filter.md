# SSRF with whitelist-based input filter

**Lab Url**: [https://portswigger.net/web-security/ssrf/lab-ssrf-with-whitelist-filter](https://portswigger.net/web-security/ssrf/lab-ssrf-with-whitelist-filter)

## Objective

This lab has a stock check feature which fetches data from an internal system.

To solve the lab, change the stock check URL to access the admin interface at `http://localhost/admin` and delete the user `carlos`.

The developer has deployed an anti-SSRF defense you will need to bypass.

## Solution

The stock check filter whitelists URLs that start with `http://` and contain the hostname `stock.weliketoshop.net`. We can bypass it by exploiting a parsing differential: the filter sees the whitelisted hostname, but the backend request resolves `localhost` instead.

### Step 1: Bypass the whitelist

The filter decodes the URL once when validating. Use a double-encoded character to trick the filter while the backend resolves `localhost`:

```
stockApi=http://localhost:80%2523@stock.weliketoshop.net/admin
```

- The filter decodes `%2523` once to `%23` and sees `stock.weliketoshop.net` as the hostname — the URL passes the whitelist.
- The backend request ultimately resolves `localhost:80`, reaching the admin interface.

### Step 2: Delete carlos

Append the delete path:

```
stockApi=http://localhost:80%2523@stock.weliketoshop.net/admin/delete?username=carlos
```

The server deletes the user and solves the lab.
