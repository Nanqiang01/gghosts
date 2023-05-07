import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 800))  
display.start()

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

chrome_options = webdriver.ChromeOptions()    
# Add your options as needed    
options = [
  # Define window size here
   "--window-size=1200,1200",
    "--ignore-certificate-errors"
 
    #"--headless",
    #"--disable-gpu",
    #"--window-size=1920,1200",
    #"--ignore-certificate-errors",
    #"--disable-extensions",
    #"--no-sandbox",
    #"--disable-dev-shm-usage",
    #'--remote-debugging-port=9222'
]

for option in options:
    chrome_options.add_argument(option)

    
driver = webdriver.Chrome(options = chrome_options)

# Get IP address list
ip_url = "https://github.com/Ponderfly/GoogleTranslateIpCheck/raw/master/src/GoogleTranslateIpCheck/GoogleTranslateIpCheck/ip.txt"
response = requests.get(ip_url)
ips = response.text.splitlines()

# Ping IP addresses
avg_latency = {}
for ip in ips:
    driver.get("https://ipw.cn/ping/")
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, "form-input").clear()
    driver.find_element(By.CLASS_NAME, "form-input").send_keys(ip)
    driver.find_element(By.CLASS_NAME, "button").click()
    time.sleep(2)

    before_XPath = "//*[@id='tfhover']/tbody/tr["
    aftertd_XPath_1 = "]/td[1]"
    aftertd_XPath_8 = "]/td[8]"

    rows = len(driver.find_elements(By.XPATH, "//*[@id='tfhover']/tbody/tr"))
    for t_row in range(2, (rows + 1)):
        AreaXPath = before_XPath + str(t_row) + aftertd_XPath_1
        PingXPath = before_XPath + str(t_row) + aftertd_XPath_8
        area = driver.find_element(By.XPATH, AreaXPath).text
        if area == "北京":
            ping = driver.find_element(By.XPATH, PingXPath).text
            if ping == "":
                avg_latency[ip] = 999
                break
            else:
                avg_latency[ip] = float(ping)
                break

# Sort IP addresses by latency and save top 10 to file
sorted_ips = sorted(avg_latency.items(), key=lambda x: x[1])
best_ip = list(dict(sorted_ips[:5]))

driver.quit()
googlehosts = [
    "google.com",
    "googleapis.com",
    "google.com.hk",
    "google.com.jp",
    "googleusercontent.com",
    "ytimg.com",
    "youtube.com",
    "youtube-nocookie.com",
    "youtu.be",
    "ggpht.com",
    "gstatic.com",
    "translate.goog",
    "blogspot.com",
    "blogger.com",
    "blogblog.com",
    "about.google",
    "safety.google",
    "gmail.com",
    "recaptcha.com",
    "recaptcha.net",
    "gvt0.com",
]

with open("gg_hosts.txt", "w") as f:
    for ip in best_ip:
        for hosts in googlehosts:
            f.write("||" + hosts + "^$dnsrewrite=" + ip + "\n")
