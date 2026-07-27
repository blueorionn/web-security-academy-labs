# DOM XSS in document.write sink using source location.search

**Lab Url**: [https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-document-write-sink](https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-document-write-sink)

## Objective

This lab contains a DOM-based cross-site scripting vulnerability in the search query tracking functionality. It uses the JavaScript `document.write` function, which writes data out to the page. The `document.write` function is called with data from `location.search`, which you can control using the website URL.

To solve this lab, perform a cross-site scripting attack that calls the `alert` function.

## Solution

The search query is written into the page via `document.write()` without sanitisation. Break out of the attribute context to inject a script.

### Step 1: Craft the payload

The vulnerable code writes the query into an `img` tag's `src` attribute:

```javascript
document.write('<img src="/resources/images/tracker.gif?searchTerms='+query+'">');
```

Inject a payload that closes the attribute and tag, then adds a script:

```text
/?search="><script>alert('XSS')</script>
```

The script executes, solving the lab.
