# Web shell upload via race condition

**Lab Url**: [https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-race-condition](https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-race-condition)

## Objective

This lab contains a vulnerable image upload function. Although it performs robust validation on any files that are uploaded, it is possible to bypass this validation entirely by exploiting a race condition in the way it processes them.

To solve the lab, upload a basic PHP web shell, then use it to exfiltrate the contents of the file `/home/carlos/secret`. Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: `wiener:peter`

## Solution

The server temporarily stores uploaded files in a staging directory while performing validation. If validation fails, the file is deleted — but there is a brief window where the file exists on the filesystem before being removed. By sending concurrent requests during this window, we can execute the file before it is deleted.

### Step 1: Upload the web shell

Upload a PHP shell via the avatar upload form:

```php
<?php echo file_get_contents('/home/carlos/secret'); ?>
```

The file will fail validation (it is not a valid image) and be queued for deletion, but it is briefly present in a staging area on the server.

### Step 2: Race the deletion

While the upload is in progress, send a large number of concurrent requests to the staging path (typically `/files/avatars/`) to access the uploaded file before it is removed. One of the concurrent requests will likely land inside the time window where the file still exists, and the PHP code will execute.

A script can automate this race:

```bash
python3 lab_07-script.py -u https://LAB-ID.web-security-academy.net/ -s YOUR-SESSION-COOKIE # your session cookie should be logged in
```

Run this script to obtain the contents of `/home/carlos/secret`. Submit this secret to solve the lab.
