# Notion2Velog

# 💱 Notion 2 Velog

처음 이 매크로를 개발하기로 마음 먹은 것은 DX 위키에 자료를 올리고 보니 velog에도 따로 올려서 자료를 정리하는 것이 좋다는 생각이 들었을 때입니다.

두 개의 위키를 작성하고 velog에 옮기려고 하니 물론 복사 붙여넣기가 끝이지만 그 과정 역시 귀찮게 느껴졌습니다. python 으로 매크로 및 웹 스크랩이 가능하니 만들어 볼 수 있겠다 라는 생각과 함께 바로 작업을 시작 했습니다.

## 🐱 프로젝트 링크

### - [🐱 Github](https://github.com/dbwpghks56/notion2velog)

## 🎨 설계

python 으로 가능하다는 건 알았지만 python 을 사용해본 건 알고리즘 풀 때 뿐이라 구글을 많이 찾아봤습니다. 그중에 눈에 들어온 것은 어디서 들어본 적이 있는 selenium 입니다.

selenium을 이용해 notion을 열어서 내용을 긁어오고 다시 velog를 열어 내용을 붙여넣는 방식을 생각했습니다.

하지만 selenium의 경우 가상의 웹을 실행하기 때문에 로그인부터 다시해야된다는 것을 알았고,

로직의 순서로는 

- notion 및 velog 로그인을 진행한다. 이 과정에서 완료시 *.pkl 이라는 파일이 생성 되는데 이 파일에는 로그인 성공 직후의 cookie 값이 들어있기 때문에 토큰 정보를 가지고 있습니다.
( 때문에 .exe 파일과 *.pkl 파일은 같은 경로(폴더) 에 있어야 합니다.)
- 후에는 GUI에 나온데로 notin url 입력 후 버튼 클릭시 notion 데이터 복제가 이루어집니다.
- 완료가 되면 .exe 프로그램에서 로그인한 계정의 velog에 접속해 임시저장 탭을 확인하면 됩니다.

## 🌿 Selenium

selenium을 이용해 입력된 notion url 에 접속해 본문의 div에 접근하고 해당 div 를 전체 복사를 진행합니다.  그 전에 title 값을 읽어와 따로 변수에 저장해줍니다.

본문의 내용을 긁어와서 진행하려 했지만 그럴 경우 markdown의 문법이 적용되지 않아. 많은 어려움이 있었습니다. 

하여 본문을 복사한뒤

[velog.io/write](http://velog.io/write) 에 접속하여 title 변수의 내용을 제목으로 입력하고,

selenium 의 함수를 이용해 본문의 div 를 click() 후에 actions 의 chain을 초기화해주고 붙여넣기 작업을 진행해줍니다. 

그 뒤 selenium을 이용해 가져온 임시저장 버튼을 click() 을 이용해 눌러준 뒤 창을 닫습니다.

selenium의 웹 스크랩핑 능력이 매우 강력하다는 것을 알게된 작업이었습니다.

이게 가능한가 하고 상상으로 생각한 기능이 대부분 가능하다는 것이 놀라웠습니다. 

## 🚧 한계점

- ~~selenium을 이용해 복사한 데이터를 붙여넣기하는 간단한 기능이기 때문에 이미지까지 가능하지는 않아 보입니다.

물론 이미지 url 을 제대로 가져오지만 notion의 보안 정책인지 notion의 s3 에 제대로 접근을 못하여 이미지가 안 나온다고 생각됩니다.~~
- 이미지를 가져오지만 정확한 위치에 삽입은 어렵습니다. 물론 고치려 노력은 해보겠습니다.
- Velog의 경우에는 git 만 notion 의 경우에는 직접 이메일을 입력한 경우에만 로그인이 가능합니다. selenium의 한계점으로 보입니다만 자료를 더 찾아보아야겠습니다.

## 👩🏻‍💻 Code

```python
notionCookies = None
velogCookies = None
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
service = Service(executable_path=ChromeDriverManager().install())
file_paths = []
notionMainLink = "https://www.notion.so/"

def notion():
    global file_paths
    if entryNotionURL.get() != "" and notionMainLink in entryNotionURL.get():
        urlCautionContent.set("")
        driver = webdriver.Chrome(service=service, options=options)
        
        file = "notion.pkl"
        fileVelog = "velogGitLogin.pkl"
        
        if os.path.exists(file):
            notionCookies = pickle.load(open(file, "rb"))
            driver.get(notionMainLink)
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
                
        for c in contents:
            for c2 in c.find_elements(By.TAG_NAME, "img"):
                if "notion.so" in c2.get_attribute("src"):
                    file_paths.append(c2.get_attribute("src"))
        
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
        
        velogTag = driver.find_element(By.CSS_SELECTOR, '[placeholder="태그를 입력하세요"]')
        velogTag.send_keys("Notion2Velog")
        velogTag.send_keys(Keys.ENTER)
        
        velogContent = driver.find_elements(By.CLASS_NAME, "CodeMirror")

        for v in velogContent:
            v.click()
            actions = ActionChains(driver)
            actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL)
            actions.key_down(Keys.ENTER).key_up(Keys.ENTER)
            actions.perform()
            
        for f in file_paths:
            driver2 = webdriver.Chrome(service=service, options=options)
            if os.path.exists(file):
                notionCookies = pickle.load(open(file, "rb"))
                driver2.get(notionMainLink)
                driver2.delete_all_cookies()
                
                for cookie in notionCookies:
                    # cookie.pop("domain")
                    driver2.add_cookie(cookie)
            
            driver2.get(f)
            c = driver2.find_element(By.TAG_NAME, "body")
            c.send_keys(Keys.CONTROL + 'c')
            actions.click()
            actions.perform()
            actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL)
            actions.perform()
            
            driver2.close()
            
        
        velogContent2 = driver.find_element(By.CLASS_NAME, "CodeMirror")
        wait = WebDriverWait(driver, 10)  # 최대 10초 동안 기다림 (필요에 따라 조절)
        def check_url(driver):
            return "업로드중.." not in velogContent2.text
        # 조건 함수를 사용하여 기다리기
        wait.until(check_url)
        
        testSave = driver.find_elements(By.CLASS_NAME, "icODNG")
        for btn in testSave:
            btn.click()
            
        time.sleep(0.5)
        
        driver.close()
        driver.quit()
        driver2.quit()
        file_paths = []
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
```

## 🖊️ To Do

- 명확한 한계점이 있으니 개선해 나갈 생각입니다. 이미지는 물론 로그인 기능의 한계점까지 개선해볼 생각입니다.
- 지금 생각하는 추가 기능은
    - ~~제목 입력받아 velog 임시저장 때 사용하기 ( 빈 문자열의 경우 notion의 데이터 사용)~~
    - 브라우저 실제로 띄우지 않고 실행할 수 있는 법 알아보고( chrome add argument 실패 )
    - 속도 개선
    - 깃 readme 에도 옮기기..?
    - etc…

가 있습니다.

## 🖼️ 결과
![image](https://github.com/dbwpghks56/notion2velog/assets/43091440/a0e34afd-67c2-46fd-8565-1a3c77cb03cd)
