#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from rich.console import Console
from json import load, dumps
from json import loads as ld
import urllib.request
from random import choice
from sys import argv
from time import sleep


# Rich Lib Object Intialization--->
console = Console()


# Variables
json_file = "src/chrome.json"
ua_list = []
proxies = []
proxy_type = ""
output_filename = ""
output_format = ""



# Banner
def banner():
    banr = r"""
██████╗ ██████╗  ██████╗ ██╗  ██╗██╗   ██╗    ███╗   ██╗██╗███╗   ██╗     ██╗ █████╗ 
██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝╚██╗ ██╔╝    ████╗  ██║██║████╗  ██║     ██║██╔══██╗
██████╔╝██████╔╝██║   ██║ ╚███╔╝  ╚████╔╝     ██╔██╗ ██║██║██╔██╗ ██║     ██║███████║
██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗   ╚██╔╝      ██║╚██╗██║██║██║╚██╗██║██   ██║██╔══██║
██║     ██║  ██║╚██████╔╝██╔╝ ██╗   ██║       ██║ ╚████║██║██║ ╚████║╚█████╔╝██║  ██║
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝       ╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝ ╚════╝ ╚═╝  ╚═╝                                                                                         
"""
    console.print(f"[cyan bold]{banr}[/cyan bold]")
    console.print("\t\t  [cyan bold]Fetch Latest [magenta bold]Https/Socks4[/magenta bold] Proxies[/cyan bold]")
    console.print("[yellow bold]_[/yellow bold]" * 80 + "\n")


# Check the Internet Connection.
def check_internet_conn():
    try:
        console.print("\n[" + "[blue bold]Info[/blue bold]" + "]" + "[red bold] Checking for Internet Connection...[/red bold]")
        host = "https://www.google.com"
        urllib.request.urlopen(host)
        console.print("[" + "[blue bold]Info[/blue bold]" + "]" + " Connection:[green bold] Connected...[/green bold]")
    except:
        console.print("[" + "[red bold]Error[/red bold]" + "]" + " Connection:[bold] No Internet Connection...[/bold]")
        exit(1)


# Help
def help():
    console.print("\n\t\t\t[green_yellow bold]<<< Help for Proxy Ninja >>>[/green_yellow bold]")
    console.print("""[red bold]Options:[/red bold]
        [yellow bold]Primary:-[/yellow bold] 
            -t      Proxy Type              (Proxy Type https or socks)
            -o      Filename                (Output Filename)
            -f      Format                  (Output File Fprmat [txt,json])
        [yellow bold]Optional:-[/yellow bold]
            -l      load                    (loads json proxy file) [red blink][!Not Implemented yet][/red blink]
    """)
    exit(0)


# Loads User Agent from Json File
def load_ua(json_file, ua_list):
    with open(json_file, "r") as file:
        json_data = load(file)
        for _ in json_data:
            if _['ua'] not in ua_list:
                ua_list.append(_['ua'])    
    return ua_list


# Saving Proxies
def iO_func(json_prox, proxy_type, output_filename, output_format):
    txt_prox = []
    try:
        _filename = f"{output_filename}_{proxy_type}.{output_format}"
        if output_format == "json":
            with open(_filename, "w+") as handle:
                handle.write(proxies)
        else:
            json_data = ld(json_prox)
            for _ in json_data:
                proxy = f"{_['IP Address']}:{_['Port']}"
                if proxy not in txt_prox:
                    txt_prox.append(proxy)
            with open(_filename, "w+") as handle:
                for _ in txt_prox:
                    handle.write(str(_) + "\n")
    except Exception as err:
        console.print("[" + "[red bold]Error[/red bold]" + "]" + f"[bold blink] {err}...![/bold blink]")
        exit(1)



# Get Proxies by Scraping the site
def get_proxies(driver, proxy_type, output_filename, output_format):
    try:
        console.print("[" + "[blue bold]Info[/blue bold]" + "]" + " Setting the URL..")
        sleep(1)
        if proxy_type == "https":
            url = "https://sslproxies.org"
        else:
            url = "https://www.socks-proxy.net"
        console.print("[" + "[blue bold]Info[/blue bold]" + "]" + " Scraping Proxies..")
        console.print("[" + "[yellow bold]Warning[/yellow bold]" + "]" + " This may take some time..")
        console.print("[" + "[blue bold]Info[/blue bold]" + "]" + " Please wait..")
        driver.get(url)
        table = driver.find_element(By.TAG_NAME, 'table')
        thead = table.find_element(By.TAG_NAME, 'thead').find_elements(By.TAG_NAME, 'th')
        tbody = table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')

        headers = []
        for th in thead:
            headers.append(th.text.strip())
        for tr in tbody:
            proxy_data = {}
            tds = tr.find_elements(By.TAG_NAME, 'td')
            for i in range(len(headers)):
                proxy_data[headers[i]] = tds[i].text.strip()
            proxies.append(proxy_data)
        json_prox = dumps(proxies)
        console.print("[" + "[blue bold]Info[/blue bold]" + "]" + " Proxies are Successfully Scraped..")
        console.print("[" + "[blue bold]Info[/blue bold]" + "]" + f" Saving Proxies in [green bold]{output_filename}_{proxy_type}.{output_format}[/green bold] file..")
        iO_func(json_prox, proxy_type, output_filename, output_format)
        sleep(2)
        console.print("[" + "[blue bold]Info[/blue bold]" + "]" + " Proxies Saved Sucessfully..")
        console.print("[magenta bold]=+=[/magenta bold]" * 30)
        console.print("[" + "[blue bold]Info[/blue bold]" + "]" + f" [cyan bold]File Saved: [/cyan bold]{output_filename}_{proxy_type}.{output_format}..")
        console.print("[magenta bold]=+=[/magenta bold]" * 30)
    except Exception as err:
        console.print("[" + "[red bold]Error[/red bold]" + "]" + f"[bold blink] {err}...![/bold blink]")
        exit(1)


# Start the Chrome Driver.
def chrome_driver(ua_list, proxy_type, output_filename, output_format):
    try:
        # Random User Agent
        agent = choice(ua_list)
        console.print("[" + "[blue bold]Info[/blue bold]" + "]" + " Setting up Chrome Driver Options..")

        # Chrome Driver Options
        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1280x1696')
        chrome_options.add_argument('--user-data-dir=/tmp/user-data')
        chrome_options.add_argument('--hide-scrollbars')
        chrome_options.add_argument('--enable-logging')
        chrome_options.add_argument('--log-level=0')
        chrome_options.add_argument('--v=99')
        chrome_options.add_argument('--single-process')
        chrome_options.add_argument('--data-path=/tmp/data-path')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--homedir=/tmp')
        chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
        chrome_options.add_argument(f"user-agent={agent}")

        sleep(2)
        console.print("[" + "[blue bold]Info[/blue bold]" + "]" + " Initializing the Chrome Driver..")
        # Initializing Chromium Driver 
        driver = webdriver.Chrome(options=chrome_options)

        console.print("[" + "[blue bold]Info[/blue bold]" + "]" + " Setting up Chrome Driver Stealth..")
        # Stealth Selenium Options
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        try:
            get_proxies(driver, proxy_type, output_filename, output_format)
            driver.quit()
        except Exception as err:
            driver.quit()
            console.print("[" + "[red bold]Error[/red bold]" + "]" + f"[bold blink] {err}...![/bold blink]")
            exit(1)
    except Exception as err:
        console.print("[" + "[red bold]Error[/red bold]" + "]" + f"[bold blink] {err}...![/bold blink]")
        exit(1)





if __name__ == '__main__':
    args = argv
    banner()
    if len(args) == 2:
            if argv[1] == "-h" or argv[1] == "--help":
                help()
    elif len(args) == 7:
        if (str(argv[2])).lower() == "https" or (str(argv[2])).lower() == "socks":
            proxy_type = str(argv[2])
            output_filename = str(argv[4])
            if (str(argv[6])).lower() == "txt" or (str(argv[6])).lower() == "json":
                output_format = str(argv[6])
                console.print(f"""
                Arguments:-
                    [green bold]Proxy Type:\t\t\t[/green bold][cyan]{proxy_type}[/cyan]
                    [green bold]Output Filename:\t\t[/green bold][cyan]{output_filename}[/cyan]
                    [green bold]Output Format:\t\t[/green bold][cyan]{output_format}[/cyan]
                """)
                console.print("=+=" * 30)
                check_internet_conn()
                console.print("[" + "[blue bold]Info[/blue bold]" + "]" + " Fetching User-Agent List..")
                sleep(2)
                console.print("[" + "[blue bold]Info[/blue bold]" + "]" + " Randomizing User-Agents")
                load_ua(json_file, ua_list)
                chrome_driver(ua_list, proxy_type, output_filename, output_format)
            else:
                console.print("[" + "[red bold]Error[/red bold]" + "]" + "[bold blink] Wrong Argument Value, [yellow]Format[/yellow] should only be (txt) or (json)...![/bold blink]")
                help()
        else:
            console.print("[" + "[red bold]Error[/red bold]" + "]" + "[bold blink]Wrong Argument Value, [yellow]Proxy Type[/yellow] should only be (https) or (socks)...![/bold blink]")
            help()
    else:
        console.print("[" + "[red bold]Error[/red bold]" + "]" + "[bold blink] Argument Missing...![/bold blink]")
        help()
    