FROM python:3.8

RUN mkdir /app
COPY . /app

WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-u", "run.py"]
