# Reflected XSS into HTML context with nothing encoded

**Lab Url**: [https://portswigger.net/web-security/cross-site-scripting/reflected/lab-html-context-nothing-encoded](https://portswigger.net/web-security/cross-site-scripting/reflected/lab-html-context-nothing-encoded)

## Objective

This lab contains a simple reflected cross-site scripting vulnerability in the search functionality.

To solve the lab, perform a cross-site scripting attack that calls the `alert` function.

## Solution

The search term is displayed directly in the page HTML without sanitisation. Inject a `<script>` tag with the `alert` function.

### Step 1: Inject the payload

```text
/?search=<script>alert('XSS')</script>
```

The script executes and an alert box pops up, solving the lab.
