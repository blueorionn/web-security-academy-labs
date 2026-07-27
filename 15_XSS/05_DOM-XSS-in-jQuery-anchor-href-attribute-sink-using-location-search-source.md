# DOM XSS in jQuery anchor href attribute sink using location.search source

**Lab Url**: [https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-jquery-href-attribute-sink](https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-jquery-href-attribute-sink)

## Objective

This lab contains a DOM-based cross-site scripting vulnerability in the submit feedback page. It uses the jQuery library's `$` selector function to find an anchor element, and changes its `href` attribute using data from `location.search`.

To solve this lab, make the "back" link alert `document.cookie`.

## Solution

The page reads a `returnPath` parameter from the URL and sets it as the `href` of a back link without validation. Inject a `javascript:` URL to execute code when the link is clicked.

### Step 1: Inject the payload

```text
/feedback?returnPath=javascript:alert(document.cookie)
```

### Step 2: Trigger the payload

Click the **Back** link on the feedback page. The `javascript:` URL executes, solving the lab.
