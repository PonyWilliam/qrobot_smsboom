FROM python:3.10

WORKDIR /src

COPY . /src/

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install -r requirements.txt
ENTRYPOINT [ "gunicorn","-w","4","-b","0.0.0.0:80","smsboom_web:app" ]

EXPOSE 80

yum install docker
alias python='/var/lang/python3/bin/python3'
alias pip='/var/lang/python3/bin/pip3
pip install -r requirements.txt
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:9000 smsboom_web:app