FROM python:3
ENV TZ=Asia/Seoul
WORKDIR /usr/src
RUN apt-get update && apt-get install wget unzip
RUN apt-get update && apt-get -y install \
libxss1 \
fonts-liberation \
libasound2 \
libatk1.0-0 \
libatspi2.0-0 \
libcups2 \
libdbus-1-3 \
libdrm2 \
libgbm1 \
libgtk-3-0 \
libnspr4 \
libnss3 \
libu2f-udev \
libvulkan1 \
libxcomposite1 \
libxdamage1 \
libxfixes3 \
libxkbcommon0 \
libxrandr2 \
xdg-utils

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb 
RUN dpkg -i google-chrome-stable_current_amd64.deb

RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/` curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN mkdir chrome
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/src/chrome

RUN pip install selenium beautifulsoup4 schedule requests
COPY main.py /usr/src/
COPY data /usr/src/data
COPY tokens /usr/src/tokens
COPY tokenRefresher.py /usr/src/
CMD [ "python", "main.py" ]