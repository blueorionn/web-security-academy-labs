# Reflected XSS into HTML context with most tags and attributes blocked

**Lab Url**: [https://portswigger.net/web-security/cross-site-scripting/contexts/lab-html-context-with-most-tags-and-attributes-blocked](https://portswigger.net/web-security/cross-site-scripting/contexts/lab-html-context-with-most-tags-and-attributes-blocked)

## Objective

This lab contains a reflected XSS vulnerability in the search functionality but uses a web application firewall (WAF) to protect against common XSS vectors.

To solve the lab, perform a cross-site scripting attack that bypasses the WAF and calls the `print()` function.

## Solution

The WAF blocks common XSS vectors but allows the `<body>` tag with the `onresize` attribute. Since `onresize` only fires when the window is resized, deliver the payload via an `<iframe>`.

### Step 1: Fuzz allowed tags and attributes

Through testing, the `<body>` tag and the `onresize` attribute are found to be allowed.

### Step 2: Craft the exploit

Host the following HTML on the exploit server:

```html
<iframe src="https://YOUR-LAB-ID.web-security-academy.net/?search=%3Cbody%20onresize=%27print()%27%3E" onload="this.style.width='100px'"></iframe>
```

The iframe loads the lab page with the XSS payload. The `onload` event changes the iframe's width, triggering the `onresize` event inside the iframe, which executes `print()`, solving the lab.
