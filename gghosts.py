import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

# Set headless option for Chrome driver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Open Chrome driver
driver_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
driver = webdriver.Chrome(driver_path, options=chrome_options)

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

driver.quit()
googlehosts = [
    "google.com",
    "googleapis.com",
    "google.com.hk",
    "googleusercontent.com",
    "ytimg.com",
    "youtube.com",
    "youtube-nocookie.com",
    "youtu.be",
    "ggpht.com",
    "youtu.be",
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

with open("google_hosts.txt", "w") as f:
    for ip in sorted_ips[:10]:
        for hosts in googlehosts:
            f.write("||" + hosts + "^$dnsrewrite=" + ip + "\n")
