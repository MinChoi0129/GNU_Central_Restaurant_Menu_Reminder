FROM python:3
ENV TZ=Asia/Seoul
WORKDIR /usr/src

RUN apt-get update
RUN apt-get -y install unzip
RUN apt-get -y install wget
RUN apt-get -y install fonts-liberation
RUN apt-get -y install libasound2
RUN apt-get -y install libatk-bridge2.0-0
RUN apt-get -y install libatk1.0-0
RUN apt-get -y install libatspi2.0-0
RUN apt-get -y install libcups2
RUN apt-get -y install libdbus-1-3
RUN apt-get -y install libdrm2
RUN apt-get -y install libgbm1
RUN apt-get -y install libgtk-3-0
RUN apt-get -y install libnspr4
RUN apt-get -y install libnss3
RUN apt-get -y install libwayland-client0
RUN apt-get -y install libxcomposite1
RUN apt-get -y install libxdamage1
RUN apt-get -y install libxfixes3
RUN apt-get -y install libxkbcommon0
RUN apt-get -y install libxrandr2
RUN apt-get -y install xdg-utils
RUN apt-get -y install libu2f-udev

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