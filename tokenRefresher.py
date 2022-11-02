import json, requests
from datetime import datetime

def recordRefreshTime(token_type):
    f = open("lastTokenRefreshDate.txt", mode='r')
    access = f.readline()
    refresh = f.readline()            
    f.close()
    
    f = open("lastTokenRefreshDate.txt", mode='w')        
    
    
    current_time = str(datetime.today())
    if token_type == 'access':
        f.write(current_time + '\n' + refresh)
    elif token_type == 'refresh':
        f.write(access + current_time)
    else: raise ValueError
    
    f.close()
    
    

def isRequiredToRefresh_refreshToken(): # 45일마다 갱신시 최적
    f = open("lastTokenRefreshDate.txt", mode='r')
    access = f.readline().rstrip()
    refresh = f.readline().rstrip()    
    f.close()
    old_time = datetime.strptime(refresh, "%Y-%m-%d %H:%M:%S.%f")
    current_time = datetime.today()
    
    passed_days = ((current_time - old_time).total_seconds() / 60 / 60 / 24)
    print(passed_days >= 45)
    return passed_days >= 45

def isRequiredToRefresh_accessToken(): # 4시간마다 갱신시 최적
    f = open("lastTokenRefreshDate.txt", mode='r')
    access = f.readline().rstrip()
    refresh = f.readline().rstrip()    
    f.close()
    old_time = datetime.strptime(access, "%Y-%m-%d %H:%M:%S.%f")
    current_time = datetime.today()
    
    passed_hours = ((current_time - old_time).total_seconds() / 60 / 60)
    print(passed_hours >= 4)
    return passed_hours >= 4

def refreshAccessToken():
    print("access token을 갱신합니다.")
    url = "https://kauth.kakao.com/oauth/token"

    with open("normal_token_including_refresh_token.json","r") as fp:
        tokens = json.load(fp)
    
    data = {
        "grant_type": "refresh_token",
        "client_id": "ae0853e0034b1459fa968e890540c744",
        "refresh_token": tokens["refresh_token"]
    }
    response = requests.post(url, data=data)
    tokens = response.json()

    with open("access_token.json", "w") as fp:
        json.dump(tokens, fp)
    print(tokens)
    recordRefreshTime('access')
    return

def refreshRefreshToken():
    print("refresh token을 갱신합니다.")
    # https://kauth.kakao.com/oauth/authorize?client_id=ae0853e0034b1459fa968e890540c744&redirect_uri=https://example.com/oauth&response_type=code
    url = 'https://kauth.kakao.com/oauth/token'
    rest_api_key = 'ae0853e0034b1459fa968e890540c744'
    redirect_uri = 'https://example.com/oauth'
    authorize_code = "HJTBNubXXgDQcqlWMJIdsW52gd2FVqbE2K31QE82JBaxmaF6GYpgt76cvLokWjreJuBeoAo9dVoAAAGENivjxA"

    data = {
        'grant_type':'authorization_code',
        'client_id':rest_api_key,
        'redirect_uri':redirect_uri,
        'code': authorize_code,
        }

    response = requests.post(url, data=data)
    tokens = response.json()
    print(tokens)


    with open("normal_token_including_refresh_token.json","w") as fp:
        json.dump(tokens, fp)
        
    recordRefreshTime('refresh')