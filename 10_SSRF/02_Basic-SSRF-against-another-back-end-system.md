# Basic SSRF against another back-end system

**Lab Url**: [https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-backend-system](https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-backend-system)

## Objective

This lab has a stock check feature which fetches data from an internal system.

To solve the lab, use the stock check functionality to scan the internal `192.168.0.X` range for an admin interface on port `8080`, then use it to delete the user `carlos`.

## Solution
