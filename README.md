
# Proxy Ninja
Python script to get https or socks(4) proxies by scraping the web using StealthChromiumDriver.
## Installation
Before installing the python3 requirements , please install the ChromiumDriver as following debian/kali
```bash
    sudo apt-get update && sudo apt-get full-upgrade -y
    sudo apt-get install chromium-driver
```
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.
if not installed, install it using the following command.
```bash
sudo apt-get install python3-pip
```

> It is advised to install the python requirements in a virtual environment, for that install the venv package.

```bash
    python3 -m pip install venv
    cd proxy-ninja
    python3 -m venv env
    source env/bin/activate
```
After that run the following commands:
```bash
  python3 -m pip install -r requirements.txt
```
    
## Usage/Examples

```bash
python3 main.py -t PROXY_TYPE -o OUTPUT_FILENAME -f OUTPUT_FORMAT
```
- PROXY_TYPE: https/socks
- OUTPUT_FILENAME: Enter the filename
- OUTPUT_FORMAT: txt/json
OR
```bash
python3 main.py -h/--help
``` 
#### Example:
```bash
python3 main.py -t socks -o proxies -f json
```
## Features

- ChromeDriver to scrape the site.
- Stealth Profle implmented.
- save output in txt or json format.
- User Friendly. :D


## License

[MIT](https://choosealicense.com/licenses/mit/)


## Feedback

If you have any feedback, please reach out to us at akalucifr@protonmail.ch

