# WebSecurity Academy Labs

This repo contains the solutions for the PortSwigger Labs available in the Academy section of their website: [https://portswigger.net/web-security/all-labs](https://portswigger.net/web-security/all-labs)

## Status

| ID | Topic | Apprentice | Practitioner | Expert |
| --- | --- | --- | --- | --- |
| --- | **Server-side topics** | --- | --- | --- |
| 01 | SQL injection | :white_check_mark: 2/2 | 14/16 | - |
| 02 | Authentication | :white_check_mark: 3/3 | 0/9 | 0/2 |
| 03 | Path traversal | :white_check_mark: 1/1 | :white_check_mark: 5/5 | - |
| 04 | Command injection | :white_check_mark: 1/1 | 2/4 | - |
| 05 | Business logic vulnerabilities | 0/4 | 0/7 | - |
| 06 | Information disclosure | :white_check_mark: 4/4 | :white_check_mark: 1/1 | - |
| 07 | Access control | :white_check_mark: 9/9 | :white_check_mark: 4/4 | - |
| 08 | File upload vulnerabilities | :white_check_mark: 2/2 | :white_check_mark: 4/4 | :white_check_mark: 1/1 |
| 09 | Race conditions | 0/1 | 0/4 | 0/1 |
| 10 | Server-side request forgery (SSRF) | 0/2 | 0/3 | 0/2 |
| 11 | XXE injection | :white_check_mark: 2/2 | 0/6 | 0/1 |
| 12 | NoSQL injection | :white_check_mark: 2/2 | :white_check_mark: 2/2 | - |
| 13 | API testing | 0/1 | 0/3 | 0/1 |
| 14 | Web cache deception | 0/1 | 0/3 | 0/1 |
| -- | **Client-side topics** | -- | -- | -- |
| 15 | Cross-site scripting (XSS) | :white_check_mark: 9/9 | 0/15 | 0/6 |
| 16 | Cross-site request forgery (CSRF) | 0/1 | 0/11 | - |
| 17 | Cross-origin resource sharing (CORS) | 0/2 | 0/1 | - |
| 18 | Clickjacking | 0/3 | 0/2 | - |
| 19 | DOM-based vulnerabilities | - | 0/5 | 0/2 |
| 20 | WebSockets | 0/1 | 0/2 | - |
| -- | **Advanced topics** | -- | -- | -- |
| 21 | Insecure deserialization | 0/1 | 0/6 | 0/3 |
| 22 | Web LLM attacks | 0/1 | 0/2 | 0/1 |
| 23 | GraphQL API vulnerabilities | 0/1 | 0/4 | - |
| 24 | Server-side template injection | - | 0/5 | 0/2 |
| 25 | Web cache poisoning | - | 0/9 | 0/4 |
| 26 | HTTP Host header attacks | 0/2 | 0/4 | 0/1 |
| 27 | HTTP request smuggling | - | 0/15 | 0/6 |
| 28 | OAuth authentication | 0/1 | 0/4 | 0/1 |
| 29 | JWT attacks | :white_check_mark: 2/2 | :white_check_mark: 4/4 | :white_check_mark: 2/2 |
| 30 | Prototype pollution | - | 0/9 | 0/1 |
| 31 | Essential skills | - | 0/1 | - |

## Install

### Zip

```bash
wget -c https://github.com/blueorionn/web-security-academy-labs/archive/refs/heads/main.zip -O web-security-academy-labs.zip && unzip web-security-academy-labs.zip && rm -f web-security-academy-labs.zip
```

### Git: No commit history (faster)**

```bash
git clone --depth 1 https://github.com/blueorionn/web-security-academy-labs.git
```

### Git: Complete

```bash
git clone https://github.com/blueorionn/web-security-academy-labs.git
```

## Contributing

Contributions to improve the content and quality of the solutions are highly encouraged! If you’d like to add new labs, refine existing solutions, or correct any errors, please fork the repository and submit a pull request. Be sure to follow any established guidelines in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## Disclaimer

**Educational Use Only:** The information provided in this repository is intended solely for educational purposes. All techniques and tools discussed should only be used in legal and authorized environments. I am not liable for any misuse or legal issues arising from the application of this material.
