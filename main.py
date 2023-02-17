from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
from tokenRefresher import *
import schedule, requests, json

class Type:
    day = ['월요일', '화요일', '수요일', '목요일', '금요일']
    food = ['비빔밥/뚝배기', '양식메뉴', '세트메뉴']

def GNUFoodMessagingService() -> None:
    for token_type in ['refresh', 'access']:
        if isRefreshRequired(token_type): refreshToken(token_type)

    menu_table = [str(bs4_element)[12:-4].split('<br/>') for bs4_element in getSeleniumHTMLFromGNUWebPage()]
    sendKakaoTalkMessage(menu_table)
    
def getSeleniumHTMLFromGNUWebPage() -> list:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    browser = webdriver.Chrome(options=options)
    browser.get("https://www.gnu.ac.kr/main/ad/fm/foodmenu/selectFoodMenuView.do?mi=1341")  
    browser.execute_script("\
        frm = document.getElementById('detailForm'); \
        frm.restSeq.value = '5';\
        frm.action = '/' + \
        document.getElementById('sysId').value + \
        '/ad/fm/foodmenu/selectFoodMenuView.do?mi=' + \
        document.getElementById('mi').value;\
        frm.submit();")
    
    innerhtml: str = browser.execute_script("return document.body.innerHTML;")
    browser.close()
    
    return BeautifulSoup(innerhtml, 'html.parser').find("div", "BD_table scroll_gr main").select("tbody > tr")[1].select("div p")[:5]

def sendKakaoTalkMessage(menu_table) -> None:
    with open("./tokens/access_token.json","r") as fp:
        token = json.load(fp)

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {"Authorization": "Bearer " + token["access_token"]}
    data = {"template_object": json.dumps({
        "object_type": "text",
        "text": generateMenuMesseage(menu_table),
        "link": {}
    })}

    response = requests.post(url, headers=headers, data=data)
    
    print(datetime.today().strftime("%Y-%m-%d %H:%M:%S"), end = " ")
    print('(', response.status_code, ')', end = " ")
    if response.json().get('result_code') == 0: print('전송 성공.\n')
    else: print('전송 실패.', str(response.json()))
    
def generateMenuMesseage(menu_table) -> str:
    txt, today = "", datetime.today().weekday()
    try:
        txt += "[ 오늘은 " + Type.day[today] + "입니다 ]" + '\n'
        txt += Type.food[0] + ' : ' + menu_table[today][0] + '\n'
        txt += Type.food[1] + ' : ' + menu_table[today][1] + '\n'
        txt += Type.food[2] + ' : ' + ''.join(menu_table[today][3:]) + '\n'
    except: txt += "[ 오늘은 중앙식당을 운영하지 않습니다 ]" + '\n'
    return txt

def run() -> None:
    print("==============================")
    print("중앙식당알리미를 시작합니다.")
    print("==============================")
    # schedule.every().day.at("10:30").do(GNUFoodMessagingService)
    schedule.every(5).seconds.do(GNUFoodMessagingService)
    while True:
        schedule.run_pending()

run()