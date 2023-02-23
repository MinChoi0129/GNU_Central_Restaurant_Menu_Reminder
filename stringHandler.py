from bs4 import BeautifulSoup
from datetime import datetime
from constants import Type

def handleInnerHTMLIntoList(innerHTML):
    parsed = BeautifulSoup(innerHTML, 'html.parser').find("div", "BD_table scroll_gr main")
    selected = parsed.select("tbody > tr")[1].select("div p")[:5]
    return [str(bs4_element)[12:-4].split('<br/>') for bs4_element in selected]

def generateMenuMesseage(menu_table: list) -> str:
    txt, today = "", datetime.today().weekday()
    try:
        txt += "[ 오늘은 " + Type.day[today] + "입니다 ]" + '\n'
        txt += Type.food[0] + ' : ' + menu_table[today][0] + '\n'
        txt += Type.food[1] + ' : ' + menu_table[today][1] + '\n'
        txt += Type.food[2] + ' : ' + ''.join(menu_table[today][3:]) + '\n'
    except: txt += "[ 오늘은 중앙식당을 운영하지 않습니다 ]" + '\n'
    return txt
