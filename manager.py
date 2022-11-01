"""Import Libraries"""
# External Libraries
from selenium import webdriver
from bs4 import BeautifulSoup
import schedule, requests
# Internal Libraries
from datetime import datetime
import json
# User Libraries
from tokenGenerator import generateToken

"""MAIN PROGRAM"""

class Type:
    day = ['월요일', '화요일', '수요일', '목요일', '금요일']
    food = ['비빔밥/뚝배기', '양식메뉴', '세트메뉴']

def GNUFoodMessagingService():
    menu: list[str] = [str(bs4_element)[12:-4].split('<br/>')[1:-1] for bs4_element in getSeleniumHTMLFromGNUWebPage()]
    sendKakaoTalkMessage(menu)
    
def getSeleniumHTMLFromGNUWebPage() -> list:
    browser = webdriver.Chrome()
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

def sendKakaoTalkMessage(menu):
    message = generateMenuMesseage(menu)
    
    with open("kakao_code.json","r") as fp:
        tokens = json.load(fp)

    url="https://kapi.kakao.com/v2/api/talk/memo/default/send"

    headers={"Authorization" : "Bearer " + tokens["access_token"]}

    data={
        "template_object": json.dumps({
            "object_type":"text",
            "text":message,
            "link":{}
        })
    }

    response = requests.post(url, headers=headers, data=data)
    print(response.status_code, end = " ")
    if response.json().get('result_code') == 0: print('메시지를 성공적으로 보냈습니다.')
    else: print('메시지를 성공적으로 보내지 못했습니다.' + str(response.json()))
    
def generateMenuMesseage(menu) -> str:
    txt = ""
    today = datetime.today().weekday()
    txt += "[ 오늘은 " + Type.day[today] + "입니다 ]" + '\n'
    txt += Type.food[0] + ' : ' + menu[today][0] + '\n'
    txt += Type.food[1] + ' : ' + menu[today][1] + '\n'
    txt += Type.food[2] + ' : ' + ''.join(menu[today][3:]) + '\n'
    return txt

def run():
    generateToken()
    schedule.every(5).seconds.do(GNUFoodMessagingService)
    print("Running system...")
    while True:
        schedule.run_pending()

run()