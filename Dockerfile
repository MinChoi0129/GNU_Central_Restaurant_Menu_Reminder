FROM python:3
ENV TZ=Asia/Seoul
WORKDIR /usr/src

RUN apt-get update && apt-get install -y -r requirements.txt

RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb
RUN apt -f install -y

RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/` curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN mkdir chrome
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/src/chrome

RUN pip install selenium beautifulsoup4 schedule requests

COPY chromeHandler.py constants.py kakaoTalkHandler.py logger.py main.py stringHandler.py tokenHandler.py /usr/src/
COPY data /usr/src/data
COPY tokens /usr/src/tokens

CMD [ "python", "main.py" ]