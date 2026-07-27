# Reflected DOM XSS

**Lab Url**: [https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-dom-xss-reflected](https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-dom-xss-reflected)

## Objective

This lab demonstrates a reflected DOM vulnerability. Reflected DOM vulnerabilities occur when the server-side application processes data from a request and echoes the data in the response. A script on the page then processes the reflected data in an unsafe way, ultimately writing it to a dangerous sink.

To solve this lab, create an injection that calls the `alert()` function.

## Solution

The search results page uses `eval()` on a JSON response that includes the user-controlled search term. The application escapes double quotes with backslashes, but we can break out using a backslash-escaped quote.

### Step 1: Craft the payload

The vulnerable code:

```javascript
eval('var searchResultsObj = ' + this.responseText);
```

Inject a payload that breaks out of the JSON string and executes arbitrary code:

```text
/?search=\"};alert(0)//
```

- `\"` — the backslash escapes the quote that the application adds, leaving an unescaped quote
- `};` — closes the object and the `var` statement
- `alert(0)` — executes the alert
- `//` — comments out the rest

The script executes, solving the lab.
