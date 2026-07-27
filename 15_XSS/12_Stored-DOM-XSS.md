# Stored DOM XSS

**Lab Url**: [https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-dom-xss-stored](https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-dom-xss-stored)

## Objective

This lab demonstrates a stored DOM vulnerability in the blog comment functionality. To solve this lab, exploit this vulnerability to call the `alert()` function.

## Solution

The `escapeHTML` function uses JavaScript's `string.replace()` which only replaces the first occurrence. We can bypass this by using a payload where the remaining unmatched bracket survives to form a valid tag.

### Step 1: Craft the bypass payload

The vulnerable function:

```javascript
function escapeHTML(html) {
    return html.replace('<', '&lt;').replace('>', '&gt;');
}
```

Submit a comment with the following payload in the comment body:

```html
<><img src=x onerror="alert(document.domain)">
```

- The first `<` and `>` are replaced, becoming `&lt;>` — the `>` remains unencoded
- The remaining `>` closes a tag, and the second `<img ...>` is left unencoded
- The browser parses the unencoded `<img>` tag, triggering the `onerror` event

The script executes when the page is viewed, solving the lab.
