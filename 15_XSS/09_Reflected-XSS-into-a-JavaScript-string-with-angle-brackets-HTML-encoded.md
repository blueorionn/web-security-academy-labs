# Reflected XSS into a JavaScript string with angle brackets HTML encoded

**Lab Url**: [https://portswigger.net/web-security/cross-site-scripting/contexts/lab-javascript-string-angle-brackets-html-encoded](https://portswigger.net/web-security/cross-site-scripting/contexts/lab-javascript-string-angle-brackets-html-encoded)

## Objective

This lab contains a reflected cross-site scripting vulnerability in the search query tracking functionality where angle brackets are encoded. The reflection occurs inside a JavaScript string. To solve this lab, perform a cross-site scripting attack that breaks out of the JavaScript string and calls the `alert` function.

## Solution

The search term is assigned to a JavaScript variable inside a `<script>` block. Angle brackets are encoded, but we can break out of the string context.

### Step 1: Break out of the JavaScript string

The vulnerable code assigns the search term to a variable:

```javascript
var searchTerms = 'USER-INPUT';
```

Inject a payload that closes the string and executes arbitrary code:

```text
/?search=';alert(document.domain)//
```

- `';` — closes the string and the assignment statement
- `alert(document.domain)` — executes the alert
- `//` — comments out the rest of the line

The script executes, solving the lab.
