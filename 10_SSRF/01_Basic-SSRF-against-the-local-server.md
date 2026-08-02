# Basic SSRF against the local server

**Lab Url**: [https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-localhost](https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-localhost)

## Objective

This lab has a stock check feature which fetches data from an internal system.

To solve the lab, change the stock check URL to access the admin interface at `http://localhost/admin` and delete the user `carlos`.

## Solution

The stock check feature sends a request to a URL supplied in the `stockApi` parameter. This URL points to an internal stock system, but we can change it to access internal services instead.

### Step 1: Intercept the stock check request

Click **Check stock** on any product and capture the POST request. The request body contains a `stockApi` parameter pointing to an internal URL:

```bash
stockApi=/product/stock/check?productId=1&storeId=1
```

### Step 2: Access the admin interface

Change the `stockApi` parameter to point to the local admin interface:

```bash
stockApi=http://localhost/admin
```

The server fetches this URL and returns the admin panel HTML in the response.

### Step 3: Delete carlos

From the admin panel response, identify the URL to delete a user. Change the `stockApi` parameter to that URL:

```bash
stockApi=http://localhost/admin/delete?username=carlos
```

The server deletes the user and solves the lab.
