# TechViper - Web Security Scanner 🔎

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Malwareman007/TechViper/blob/main/LICENSE)

## Description

TechViper is a powerful web security scanner that helps identify and detect vulnerabilities in web applications. It utilizes advanced techniques to comprehensively analyze web assets, providing users with detailed security assessments and enabling them to enhance the overall security posture of their web applications.

![image](https://github.com/Malwareman007/TechViper/assets/86009160/595f25fb-c1cd-4a84-a91b-4e8294533215)


## Key Vulnerabilities Detected

- Remote Code Execution (Linux)
- Reflected XSS (Cross-Site Scripting)
- Template Injection (Jinja2, ERB, Java, Twig, Freemarker)
- SQL Injection

## OS Support

- Kali Linux
- Android (Termux)
- Windows

## Installation

### Prerequisites

- Python 3.x

### Clone the Repository

```shell
$ git clone https://github.com/Malwareman007/TechViper.git
```
### Navigate to the TechViper Directory
```shell
$ cd TechViper
```
### Install Dependencies
```shell
$ python3 -m pip install -r requirements.txt
```
### Android (Termux) Installation
* Download and Install the Termux App from the Google Play Store.
* Open the Termux app.
* Run the following commands:
```shell
$ pkg install python -y
$ pkg install git -y
$ git clone https://github.com/Malwareman007/TechViper.git
$ cd TechViper
$ python3 -m pip install -r requirements.txt
```
### Windows Installation
* Download and Install Python 3.x.
* Open the Command Prompt.
* Navigate to the TechViper directory.
```shell
$ cd TechViper
```
### Install the required dependencies.
```shell
$ python3 -m pip install -r requirements.txt
```
## Usage
TechViper provides a range of options to customize and fine-tune the scanning process. Here are the available options:
```shell
Options:
  -h, --help          |    Show the help message and exit.
  --version           |    Show the program's version number and exit.
  -u URL, --url=URL   |    Specify the target URL (e.g., "http://www.target.com/vuln.php?id=1").
  --data=DATA         |    Provide data string to be sent through POST (e.g., "id=1").
  --list=FILE         |    Load URLs from a file.
  --threads           |    Set the maximum number of concurrent HTTP(s) requests (default: 10).
  --timeout           |    Set the number of seconds to wait before timeout connection.
  --proxy             |    Start the connection with an HTTP(s) proxy.
  --cookies           |    Set the HTTP Cookie header value (e.g., "PHPSESSID=a8d127e..").
  --encode            |    Specify the number of payload encodings to use (default: 1).
  --allow-redirect    |    Allow the main redirect.
  ```

## Examples
### Scan a single target URL:

```shell
$ python3 TechViper.py -u 'http://www.example.com/vuln.php?id=1'
```

![Viper](https://github.com/Malwareman007/TechViper/assets/86009160/ffadc7e2-785c-44db-8aed-85a181688f3e)


### Scan multiple URLs from a file:
```shell
$ python3 TechViper.py --list=targets.txt
```
## Contribution
Contributions to TechViper are welcome! If you have suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## Support
If you encounter any issues or need assistance, feel free to reach out to the project maintainers by creating an issue in the repository.
