# Stored XSS into anchor href attribute with double quotes HTML-encoded

**Lab Url**: [https://portswigger.net/web-security/cross-site-scripting/contexts/lab-href-attribute-double-quotes-html-encoded](https://portswigger.net/web-security/cross-site-scripting/contexts/lab-href-attribute-double-quotes-html-encoded)

## Objective

This lab contains a stored cross-site scripting vulnerability in the comment functionality. To solve this lab, submit a comment that calls the `alert` function when the comment author name is clicked.

## Solution

The website field is used directly as the `href` of an anchor tag. Inject a `javascript:` URL to execute code when the author name is clicked.

### Step 1: Submit a malicious comment

Post a comment with the following values:

- **Website:** `javascript:alert(0)`
- **Name:** (any name)
- **Comment:** (any text)

### Step 2: Trigger the payload

Click the comment author's name. The `javascript:` URL executes, solving the lab.
