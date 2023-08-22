from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import sys
import webbrowser
import pyautogui
import os.path
import time

cookies = None
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
service = Service(executable_path=ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)
def notion():
    file = "notion.pkl"
    
    notionUrl = input("notion URL: ")
    
    if os.path.exists(file):
        cookies = pickle.load(open("notion.pkl", "rb"))
        driver.get("https://www.notion.so")
        driver.delete_all_cookies()
        
        for cookie in cookies:
            # cookie.pop("domain")
            driver.add_cookie(cookie)
    # https://www.notion.so/ryudomain/c4828705de9e41e2b35bae5691cb7a81?pvs=4 
    # https://www.notion.so/mirimdxlab/Sentry-73f05aa15fdb454a9290f4b5fc6e6f47?pvs=4
    driver.get(notionUrl)
    
    driver.implicitly_wait(20)

    contents = driver.find_elements(By.CLASS_NAME, 'notion-page-content')

    if not os.path.exists(file):
        pickle.dump(driver.get_cookies(), open("notion.pkl", "wb"))

    for c in contents:
        for c2 in c.find_elements(By.CLASS_NAME, "notion-selectable"):
            c2.send_keys(Keys.CONTROL + 'a')
            c2.send_keys(Keys.CONTROL + 'c')
    
    driver.close()
    
    # pyperclip.copy(content2)
    

def velog():
    url = "https://velog.io/write"
    webbrowser.open(url)
    time.sleep(1)
    pyautogui.click(x= 200, y= 400)
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'v')

notion()
velog()

