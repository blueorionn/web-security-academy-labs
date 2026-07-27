# Reflected XSS into attribute with angle brackets HTML-encoded

**Lab Url**: [https://portswigger.net/web-security/cross-site-scripting/contexts/lab-attribute-angle-brackets-html-encoded](https://portswigger.net/web-security/cross-site-scripting/contexts/lab-attribute-angle-brackets-html-encoded)

## Objective

This lab contains a reflected cross-site scripting vulnerability in the search blog functionality where angle brackets are HTML-encoded. To solve this lab, perform a cross-site scripting attack that injects an attribute and calls the `alert` function.

## Solution

The search term is reflected into an `<input>` tag's `value` attribute. Since angle brackets are encoded, inject an event handler that executes when the input is focused.

### Step 1: Craft the payload

Break out of the `value` attribute and add an event handler:

```text
/?search=" onfocus="javascript:alert(0)" autofocus="true
```

When the page loads, the `autofocus` attribute focuses the input, triggering the `onfocus` event and executing the alert, solving the lab.
