FROM python:3.8-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y build-essential python3-dev libpq-dev libgl1 libglib2.0-dev

RUN pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/

RUN chmod a+x ./manage.py

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:1234"]

EXPOSE 1234/tcp