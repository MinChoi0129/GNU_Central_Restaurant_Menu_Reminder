from selenium import webdriver
from stringHandler import handleInnerHTMLIntoList

def getOptionizedChromeDriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    return webdriver.Chrome(options=options)

def getMenuTableFromGNUHomePage() -> list:
    with open("./data/browserCommands.txt", 'r') as f:
        url, script1, script2 = f.readlines()
        browser = getOptionizedChromeDriver()
        browser.get(url)
        browser.execute_script(script1)
        innerHTML = browser.execute_script(script2)
        browser.close()
    return handleInnerHTMLIntoList(innerHTML)
