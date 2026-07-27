# DOM XSS in innerHTML sink using source location.search

**Lab Url**: [https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-innerhtml-sink](https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-innerhtml-sink)

## Objective

This lab contains a DOM-based cross-site scripting vulnerability in the search blog functionality. It uses an `innerHTML` assignment, which changes the HTML contents of a `div` element, using data from `location.search`.

To solve this lab, perform a cross-site scripting attack that calls the `alert` function.

## Solution

The search query is inserted into the page via `innerHTML` without sanitisation. Use an `img` tag with an `onerror` event to execute JavaScript.

### Step 1: Inject the payload

```text
/?search=<img src=x onerror="alert(document.domain)">
```

The browser attempts to load the image, fails, and triggers the `onerror` event, solving the lab.
