# DOM XSS in document.write sink using source location.search inside a select element

**Lab Url**: [https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-document-write-sink-inside-select-element](https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-document-write-sink-inside-select-element)

## Objective

This lab contains a DOM-based cross-site scripting vulnerability in the stock checker functionality. It uses the JavaScript `document.write` function, which writes data out to the page. The `document.write` function is called with data from `location.search` which you can control using the website URL. The data is enclosed within a select element.

To solve this lab, perform a cross-site scripting attack that breaks out of the select element and calls the `alert` function.

## Solution

The `storeId` parameter is written inside a `<select>` element. Inject a payload that closes the `<option>` and `<select>` tags, then injects a `<script>` tag.

### Step 1: Craft the payload

```text
/product?productId=1&storeId=</option><script>alert(document.domain)</script><option>
```

The injected script executes when the page loads, solving the lab.
