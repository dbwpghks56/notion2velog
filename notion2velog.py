from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import pickle
import os.path
import time
import pyperclip
import base64
import PIL.Image
from tkinter import *
from tkinter import filedialog

notionCookies = None
velogCookies = None
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
service = Service(executable_path=ChromeDriverManager().install())
file_paths = []

def notion():
    if entryNotionURL.get() != "" and "https://www.notion.so/" in entryNotionURL.get():
        urlCautionContent.set("")
        driver = webdriver.Chrome(service=service, options=options)
        
        file = "notion.pkl"
        fileVelog = "velogGitLogin.pkl"
        
        if os.path.exists(file):
            notionCookies = pickle.load(open(file, "rb"))
            driver.get("https://www.notion.so")
            driver.delete_all_cookies()
            
            for cookie in notionCookies:
                # cookie.pop("domain")
                driver.add_cookie(cookie)
        # https://www.notion.so/ryudomain/c4828705de9e41e2b35bae5691cb7a81?pvs=4 
        # https://www.notion.so/mirimdxlab/Sentry-73f05aa15fdb454a9290f4b5fc6e6f47?pvs=4
        driver.get(entryNotionURL.get())
        
        driver.implicitly_wait(120)
        
        if velogTitleEntry.get() == "":
            title = driver.find_element(By.CSS_SELECTOR, '[placeholder="제목 없음"]').text
        
        else:
            title = velogTitleEntry.get()
        
        contents = driver.find_elements(By.CLASS_NAME, 'notion-page-content')

        for c in contents:
            for c2 in c.find_elements(By.CLASS_NAME, "notion-selectable"):
                c2.send_keys(Keys.CONTROL + 'a')
                c2.send_keys(Keys.CONTROL + 'c')
        
        driver.close()
        
        driver = webdriver.Chrome(service=service, options=options)
        
        if os.path.exists(fileVelog):
            velogCookies = pickle.load(open(fileVelog, "rb"))
            driver.get("https://velog.io")
            driver.delete_all_cookies()
            
            for cookie in velogCookies:
                driver.add_cookie(cookie)
        
        driver.get("https://velog.io/write")
        
        driver.implicitly_wait(120)
        
        velogTitle = driver.find_element(By.CSS_SELECTOR, '[placeholder="제목을 입력하세요"]')
        velogTitle.send_keys(title)
        
        velogContent = driver.find_elements(By.CLASS_NAME, "CodeMirror")

        for v in velogContent:
            v.click()
            actions = ActionChains(driver)
            actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL)
            # time.sleep(1)
            # if file_paths:
            #     for f in file_paths:
            #         ff = PIL.Image.open(f)
                
            #         print(ff.format)
            #         print(ff.size)
            #         print(ff.mode)
            #         actions.send_keys(ff)
            #         actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL)
            #         ff.close()
            #         time.sleep(1)
            actions.perform()
        
        testSave = driver.find_elements(By.CLASS_NAME, "icODNG")
        
        for btn in testSave:
            btn.click()
        time.sleep(0.5)
        
        driver.close()
        driver.quit()
        
        successCheck.set(" 임시저장 성공했습니다.")
        
    elif entryNotionURL.get() == "" or "https://www.notion.so/" not in entryNotionURL.get():
        successCheck.set("")
        urlCautionContent.set("notion url 을 입력하세요.")
    # pyperclip.copy(content2)
    

def velogGitHubLogin():
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get("https://v2.velog.io/api/v2/auth/social/redirect/github?next=/&isIntegrate=0")
        
        # 로그인 후 리디렉트될 예상 URL
        redirected_url = "https://velog.io/"
        wait = WebDriverWait(driver, 120)
        
        # 리디렉트되는 동안 기다리기
        wait.until(EC.url_to_be(redirected_url))
        
        if driver.current_url == redirected_url:
            pickle.dump(driver.get_cookies(), open("velogGitLogin.pkl", "wb"))
            checkVelogLogin.set("True")

    finally:
        # 작업 완료 후 드라이버 종료
        driver.quit()
    
def notionLogin():
    print(entryNotionURL.get() == "")
    driver = webdriver.Chrome(service=service, options=options)
    notionLoginUrl = "https://www.notion.so/login"
    try:
        driver.get(notionLoginUrl)
        
        # 로그인 후 리디렉트될 예상 URL
        redirected_url = "https://www.notion.so/"
        wait = WebDriverWait(driver, 120)
        def check_url(driver):
            return redirected_url in driver.current_url and notionLoginUrl not in driver.current_url
        
        # 조건 함수를 사용하여 기다리기
        wait.until(check_url)
        
        if redirected_url in driver.current_url and driver.current_url != notionLoginUrl :
            pickle.dump(driver.get_cookies(), open("notion.pkl", "wb"))
            checkNotionLogin.set("True")
            
    finally:
        # 작업 완료 후 드라이버 종료
        driver.quit()

def imageUpload():
    global file_paths
    file_paths = filedialog.askopenfilenames(filetypes=[("image files", "*.jpg, *.png")])
    if file_paths:
        print("Selected files:")
        for path in file_paths:
            print(path)

# GUI 작업
root = Tk()
root.title("Notion2Velog")

checkNotionLogin = StringVar(value= "False")
checkVelogLogin = StringVar(value= "False")
urlCautionContent = StringVar(value="")
successCheck = StringVar(value="")

if os.path.exists("notion.pkl"):
    checkNotionLogin.set("True")
    
if os.path.exists("velogGitLogin.pkl"):
    checkVelogLogin.set("True")

exeCaution = Label(root, text=".exe 파일과 .pkl이 같은 경로(폴더)에 존재하지 않을 경우 로그인을 진행해야합니다."
                             , fg="red").grid(column=1, row=0)
Label(root, text="notion Login : ").grid(column=0,row=0)
labelNotionLoginCheck = Label(root, text="notion Login : ", textvariable=checkNotionLogin).grid(column=0, row=1)
Label(root, text="velog Login : ").grid(column=0,row=2)
labelVelogLoginCheck = Label(root, text="velog Login : ", textvariable= checkVelogLogin).grid(column=0, row=3)

loginCaution = Label(root, text="Velog 및 Notion 로그인이 진행되어 있지 않을 경우 기능이 정상동작하지 않을 수 있습니다."
                             , fg="red").grid(column=1, row=1)
urlCaution = Label(root, textvariable=urlCautionContent
                             , fg="red").grid(column=1, row=2)
successCheckLabel = Label(root, textvariable=successCheck
                             , fg="blue").grid(column=1, row=3)

velogTitlelabel = Label(root, text="velog title").grid(column=0,row=4)
labelNotionURL = Label(root, text="notion URL").grid(column=0,row=6)

velogTitleEntry = Entry(root,width=50)
velogTitleEntry.grid(column=1, row=4)
imageUploadBtn = Button(root, text="이미지 업로드", command=imageUpload, width=15, height=3).grid(column=2, row=4)
velogTitlecaution = Label(root, text="제목을 입력하지 않으면 노션의 제목이 들어갑니다.", fg="green").grid(column=1,row=5)

entryNotionURL = Entry(root, width=70)
entryNotionURL.grid(column=1, row=6)

btnNotionToVelog = Button(root, text="Notion2Velog", command=notion, width=10, height=3).grid(column=0, row=7)
btnVelogGitLogin = Button(root, text="Velog Git Login", command=velogGitHubLogin, width=15, height=3).grid(column=1, row=7)
btnNotionLogin = Button(root, text="Notion Login", command=notionLogin, width=15, height=3).grid(column=2, row=7)

root.mainloop()