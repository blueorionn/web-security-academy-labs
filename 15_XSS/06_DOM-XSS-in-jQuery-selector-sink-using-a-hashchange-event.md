# DOM XSS in jQuery selector sink using a hashchange event

**Lab Url**: [https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-jquery-selector-hash-change-event](https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-jquery-selector-hash-change-event)

## Objective

This lab contains a DOM-based cross-site scripting vulnerability on the home page. It uses jQuery's `$()` selector function to auto-scroll to a given post, whose title is passed via the `location.hash` property.

To solve the lab, deliver an exploit to the victim that calls the `print()` function in their browser.

## Solution

The application uses jQuery's `$()` selector with the hash value. In vulnerable jQuery versions, if the input looks like HTML, jQuery creates DOM elements from it. Since the code only triggers on hashchange events, deliver the payload via an `<iframe>` from the exploit server.

### Step 1: Craft the exploit

Create an iframe that sets the hash to an `<img>` tag with an `onerror` event:

```html
<iframe src="https://YOUR-LAB-ID.web-security-academy.net/#" onload="this.src+='<img src=1 onerror=print()>'"></iframe>
```

### Step 2: Host and deliver

Host this HTML on the exploit server. When a victim visits the page, the iframe changes the hash, triggering the jQuery selector and executing the `print()` function, solving the lab.
