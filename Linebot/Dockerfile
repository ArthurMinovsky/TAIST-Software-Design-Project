FROM python:3.9-bullseye

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8888
CMD ["uvicorn", "src.linenotify:app", "--host", "0.0.0.0"]
