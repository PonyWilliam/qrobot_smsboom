FROM python:3.10

WORKDIR /src

COPY . /src/

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install -r requirements.txt
ENTRYPOINT [ "gunicorn","-w","4","-b","0.0.0.0:80","smsboom_web:app" ]

EXPOSE 80
