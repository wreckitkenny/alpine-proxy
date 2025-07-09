FROM python:3.12.9-alpine
LABEL authors="wiky"
WORKDIR /app
COPY . .
RUN pip install fastapi[standard]
RUN pip install -r requirements.txt
ENTRYPOINT ["fastapi", "run"]