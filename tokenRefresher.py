import json, requests
from datetime import datetime

def recordRefreshedTime(token_type):
    with open("./data/lastTokenRefreshDate.txt", mode='r') as f:
        refresh, access = f.readline().rstrip(), f.readline().rstrip()

    with open("./data/lastTokenRefreshDate.txt", mode='w') as f:
        current_time = str(datetime.today())
        updated_text = '\n'.join([refresh, current_time]) if token_type == 'access' else '\n'.join([current_time, access])
        f.write(updated_text)
        print("%s_token 발급일을 갱신했습니다." % token_type)
        print("------------------------------")

def isRefreshRequired(token_type):
    with open("./data/lastTokenRefreshDate.txt", mode='r') as f:
        refresh, access = f.readline().rstrip(), f.readline().rstrip()
        target_token = refresh if token_type == 'refresh' else access
        
        old_datetime = datetime.strptime(target_token, "%Y-%m-%d %H:%M:%S.%f")
        current_datetime = datetime.today()
    
    passed_hours = (current_datetime - old_datetime).total_seconds() / 3600

    if token_type == 'refresh': need_refresh = passed_hours / 24 >= 45    
    elif token_type == 'access': need_refresh = passed_hours >= 4
    
    if need_refresh: print("%s_token이 만료되었습니다." % token_type)
    else: print("%s_token은 유효합니다." % token_type)
    
    return need_refresh

def refreshToken(token_type):
    url = 'https://kauth.kakao.com/oauth/token'
    rest_api_key = 'ae0853e0034b1459fa968e890540c744'
    redirect_uri = 'https://example.com/oauth'
    authorize_code = "YSkYyocg2PwernbLIUSPHNY323qvI05miHp9NVeO33Txv4xTNAVeIVmevB9Ucn17cUg26Ao9dGgAAAGEOBFpwg"
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
            json.dump(requests.post(url, data=data).json(), fp)

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
            result_dict = json.loads(result)
            if 'error' in result_dict: print("갱신 에러", result_dict)
            else: print("%s_token 갱신을 성공했습니다!" % token_type)
    recordRefreshedTime(token_type)