# Basic SSRF against another back-end system

**Lab Url**: [https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-backend-system](https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-backend-system)

## Objective

This lab has a stock check feature which fetches data from an internal system.

To solve the lab, use the stock check functionality to scan the internal `192.168.0.X` range for an admin interface on port `8080`, then use it to delete the user `carlos`.

## Solution

The stock check feature sends a request to a URL supplied in the `stockApi` parameter. The internal network hosts an admin interface on port `8080`, but we need to find its IP in the `192.168.0.X` range.

### Step 1: Intercept the stock check request

Click **Check stock** on any product and capture the POST request. The request body contains a `stockApi` parameter pointing to an internal URL.

### Step 2: Scan the internal range

Fuzz the `stockApi` parameter across the `192.168.0.1` – `192.168.0.255` range on port `8080`:

```text
stockApi=http://192.168.0.1:8080/admin
stockApi=http://192.168.0.2:8080/admin
...
```

The response that returns an admin panel (instead of a 404/error) reveals the correct internal IP.

### Step 3: Delete carlos

Use the discovered IP to delete the user:

```text
stockApi=http://192.168.0.X:8080/admin/delete?username=carlos
```

The server deletes the user and solves the lab.
