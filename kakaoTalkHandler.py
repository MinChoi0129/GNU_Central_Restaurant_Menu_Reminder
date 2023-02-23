from logger import log
import json, requests

def sendKakaoTalkMessage(menu_text) -> None:
    with open("./tokens/access_token.json","r") as fp:
        token = json.load(fp)

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {"Authorization": "Bearer " + token["access_token"]}
    data = {"template_object": json.dumps({
        "object_type": "text",
        "text": menu_text,
        "link": {}
    })}

    response = requests.post(url, headers=headers, data=data)

    if response.json().get('result_code') == 0: log.info(f'전송 성공({response.status_code})')
    else: log.critical(f'전송 실패({str(response.json())})')