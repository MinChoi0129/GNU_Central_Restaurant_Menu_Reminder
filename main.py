from tokenHandler import checkTokens
from chromeHandler import getMenuTableFromGNUHomePage
from kakaoTalkHandler import sendKakaoTalkMessage
from stringHandler import generateMenuMesseage
from logger import log
import schedule

def routine() -> None:
    checkTokens(['refresh', 'access'])
    menu_table: list = getMenuTableFromGNUHomePage()
    sendKakaoTalkMessage(generateMenuMesseage(menu_table))

def scheduler() -> None:
    log.info("중앙식당알리미를 시작합니다.")
    schedule.every().day.at("10:30").do(routine)
    # schedule.every(5).seconds.do(routine)
    while True:
        schedule.run_pending()


scheduler()