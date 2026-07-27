# Reflected XSS in canonical link tag

**Lab Url**: [https://portswigger.net/web-security/cross-site-scripting/contexts/lab-canonical-link-tag](https://portswigger.net/web-security/cross-site-scripting/contexts/lab-canonical-link-tag)

## Objective

This lab reflects user input in a canonical link tag and escapes angle brackets.

To solve the lab, perform a cross-site scripting attack on the home page that injects an attribute that calls the `alert` function.

To assist with your exploit, you can assume that the simulated user will press the following key combinations:

```text
ALT+SHIFT+X
CTRL+ALT+X
Alt+X
```

*Please note that the intended solution to this lab is only possible in Chrome.*

## Solution

The canonical link tag reflects the current URL. Chrome supports the `accesskey` and `onclick` attributes on `<link>` elements, allowing keyboard-triggered XSS.

### Step 1: Craft the payload

Inject the `accesskey` and `onclick` attributes into the `<link>` tag via the URL:

```text
https://YOUR-LAB-ID.web-security-academy.net/?'accesskey='x'onclick='alert(1)
```

The URL-encoded version:

```text
/?%27accesskey=%27x%27onclick=%27alert(1)
```

### Step 2: Trigger the payload

Press the keyboard shortcut (`Alt+Shift+X` on Chrome) to trigger the `onclick` event, executing the `alert` function and solving the lab.
