import json, requests
from logger import log
from datetime import datetime

def checkTokens(token_names: list[str]):
    for token_type in token_names:
        if isRefreshRequired(token_type): refreshToken(token_type)

def recordRefreshedTime(token_type):
    with open("./data/lastTokenRefreshDate.txt", mode='r') as f:
        refresh, access = f.readline().rstrip(), f.readline().rstrip()

    with open("./data/lastTokenRefreshDate.txt", mode='w') as f:
        current_time = str(datetime.today())
        updated_text = '\n'.join([refresh, current_time]) if token_type == 'access' else '\n'.join([current_time, access])
        f.write(updated_text)
        log.info(f'{token_type}_token 발급일을 갱신했습니다.')

def isRefreshRequired(token_type):
    with open("./data/lastTokenRefreshDate.txt", mode='r') as f:
        refresh, access = f.readline().rstrip(), f.readline().rstrip()
        target_token = refresh if token_type == 'refresh' else access
        
        old_datetime = datetime.strptime(target_token, "%Y-%m-%d %H:%M:%S.%f")
        current_datetime = datetime.today()
    
    passed_hours = (current_datetime - old_datetime).total_seconds() / 3600

    if token_type == 'refresh': need_refresh = passed_hours / 24 >= 45    
    elif token_type == 'access': need_refresh = passed_hours >= 4
    
    if need_refresh: log.warning(f'{token_type}_token이 만료되었습니다.')
    else: log.info(f'{token_type}_token은 유효합니다.')
    
    return need_refresh

def refreshToken(token_type):
    url = 'https://kauth.kakao.com/oauth/token'
    rest_api_key = 'ae0853e0034b1459fa968e890540c744'
    redirect_uri = 'https://example.com/oauth'
    authorize_code = "KdaFoIh3Xbc_g_-JEIHUW3UckeWmtReOJ2jXkMamA_nL5fczpdTPawjVjZOAAjv2cF3dpgorDKYAAAGGfqJtFg"
    # https://kauth.kakao.com/oauth/authorize?client_id=ae0853e0034b1459fa968e890540c744&redirect_uri=https://example.com/oauth&response_type=code
        
    if token_type == 'access':
        with open("./tokens/normal_token_including_refresh_token.json","r") as fp:
            token = json.load(fp)
        
        data = {
            "grant_type": "refresh_token",
            "client_id": rest_api_key,
            "refresh_token": token["refresh_token"]
        }

        with open("./tokens/access_token.json", "w") as fp:
            result = requests.post(url, data=data).json()
            json.dump(result, fp)
            if 'error' in result: log.error(f"{token_type}_token 갱신 실패")
            else: log.info(f'{token_type}_token 갱신 성공')

    elif token_type == 'refresh':
        data = {
            'grant_type':'authorization_code',
            'client_id':rest_api_key,
            'redirect_uri':redirect_uri,
            'code': authorize_code,
        }

        with open("./tokens/normal_token_including_refresh_token.json","w") as fp:
            result = requests.post(url, data=data).json()
            json.dump(result, fp)
            if 'error' in result: log.error(f"{token_type}_token 갱신 실패")
            else: log.info(f'{token_type}_token 갱신 성공')

    recordRefreshedTime(token_type)