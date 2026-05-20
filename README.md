# Magento 2 RCE Exploit - Unauthenticated File Upload to RCE

**⚠️ This tool is for educational and authorized security testing only. Unauthorized use against systems you do not own is illegal.**

This exploit targets a critical unauthenticated remote code execution (RCE) vulnerability in **Magento 2** (Adobe Commerce). By chaining the GraphQL product lookup, guest cart creation, and a malicious file upload via custom product options, an attacker can upload a PHP webshell and gain arbitrary code execution on the target server.

The vulnerability allows a remote attacker to write a PHP file to the server's filesystem, then access it to execute system commands, read/write files, and fully compromise the Magento installation.

## Features

- **Multi-threaded** scanning and exploitation (up to 10 concurrent threads)
- Automatic detection of product SKU via GraphQL
- Creates guest cart and uploads a PHP webshell as a custom option file
- Verifies shell deployment by checking for a unique marker (`Shinday`)
- Saves successful shell URLs to `up.txt`
- Handles large target lists with queue-based workload distribution

## How It Works

1. **GraphQL Product Query** – Retrieves a valid product SKU from `/graphql`.
2. **Guest Cart Creation** – Calls `/rest/default/V1/guest-carts` to obtain a cart ID.
3. **Malicious File Upload** – Sends a POST request to `/rest/default/V1/guest-carts/{cart_id}/items` with a base64-encoded PHP webshell as a custom option file.
4. **Shell Deployment** – The server stores the file under `/pub/media/custom_options/quote/...` or `/media/custom_options/quote/...`.
5. **Verification** – The script attempts to fetch the uploaded PHP file and checks for the string `Shinday` in the response.
6. **Output** – Successful shell URLs are appended to `up.txt`.

## Requirements

- Python **2.7** (the script uses `Queue`, `unicode`, and other Python 2‑specific modules)
- `requests`, `urllib3` libraries

Install dependencies:
```bash
pip install requests urllib3
```

## Usage

```bash
python exploit.py <list.txt>
```

- `<list.txt>` – file containing target base URLs (one per line), with or without `http://`/`https://`.  
  Example:
  ```
  https://example.com
  http://shop.test
  magento2.target.net
  ```

### Output

- Console logs show progress, SKU, cart ID, upload status, and final shell URL if successful.
- Successful shell URLs are saved to `up.txt` in the current directory.

### Example Run

```bash
python exploit.py targets.txt
[*] Total targets: 5
[*] Start time: 2025-03-15 12:00:00
[*] Starting 5 threads...

[Thread 1] Processing: https://example.com
[+] SKU  : 24-WG080
[+] CART : 8f7c3e9a-1b2f-4d5e-9a8b-7c6d5e4f3a2b
[+] Upload Status : 200
[+] Webshell terpasang: https://example.com/pub/media/custom_options/quote/a1/b2/shell_xyz.php
[✓] Saved to up.txt: https://example.com/pub/media/custom_options/quote/a1/b2/shell_xyz.php
```

## Webshell Details

The uploaded PHP file is a simple file manager (named like `xxxxx_shin.php`) that responds to requests with a web‑based file explorer. It contains the unique marker `Shinday` which the script uses to verify successful upload.

**Do not leave this shell on a system after testing – clean up immediately.**

## Mitigation

- Apply Adobe/Magento security patches immediately.
- Disable unused GraphQL endpoints if not required.
- Restrict file uploads to authenticated users only.
- Use a Web Application Firewall (WAF) to block malicious POST patterns.
- Regularly audit `/media/custom_options/` for unexpected PHP files.

## Disclaimer

This software is provided **for educational and authorized penetration testing purposes only**. The authors are not responsible for any misuse or damage caused by this tool. You must obtain explicit written permission from the system owner before running this exploit against any target. Unauthorized access to computer systems is a criminal offense in most jurisdictions.

