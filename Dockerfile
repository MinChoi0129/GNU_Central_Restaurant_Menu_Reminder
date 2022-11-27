FROM python:3
ENV TZ=Asia/Seoul
WORKDIR /usr/src
RUN apt-get -y update
RUN apt install wget
RUN apt install unzip
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt -y install ./google-chrome-stable_current_amd64.deb
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/` curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN mkdir chrome
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/src/chrome
RUN pip install selenium
RUN pip install beautifulsoup4
RUN pip install schedule
RUN pip install requests
COPY main.py /usr/src/
COPY data /usr/src/data
COPY tokens /usr/src/tokens
COPY tokenRefresher.py /usr/src/
CMD [ "python", "main.py" ]