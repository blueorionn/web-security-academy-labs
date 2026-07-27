# Stored XSS into HTML context with nothing encoded

**Lab Url**: [https://portswigger.net/web-security/cross-site-scripting/stored/lab-html-context-nothing-encoded](https://portswigger.net/web-security/cross-site-scripting/stored/lab-html-context-nothing-encoded)

## Objective

This lab contains a stored cross-site scripting vulnerability in the comment functionality.

To solve this lab, submit a comment that calls the `alert` function when the blog post is viewed.

## Solution

The comment field is rendered directly in the page HTML without sanitisation.

### Step 1: Submit a malicious comment

Post a comment containing the following payload in the comment body:

```html
<script>alert('XSS')</script>
```

### Step 2: Trigger the payload

Any user viewing the post will trigger the script, solving the lab.
